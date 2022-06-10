import shelve
from time import strftime
import flask
import argparse
import json
import numpy as np
import yaml
import cv2
import logging
from collections import defaultdict
from tilsdk.cv.types import BoundingBox, DetectedObject
from tilsdk.localization.types import *
from datetime import datetime
import os
from werkzeug.serving import WSGIRequestHandler
from .types import *

app = flask.Flask(__name__) 

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000) # use different from localization system
aruco_params = cv2.aruco.DetectorParameters_create()

valid_history = []
last_submitted = defaultdict(int) # maps image_id to tuple(last submitted class, report)
config = {}
start_time = None
run_id = 0
image_cnt = 0
out_dir = ''
out_file:shelve.Shelf = None

##### Flask server #####

# Flask defaults to HTTP 1.0. Use HTTP 1.1 to keep connections alive for high freqeuncy requests.
WSGIRequestHandler.protocol_version = 'HTTP/1.1'

@app.route('/start_run', methods=['GET'])
def get_start_run():
    global start_time, valid_history, last_submitted, run_id, image_cnt, out_file, out_dir
    start_time = datetime.now()
    valid_history = []
    last_submitted = defaultdict(int)
    run_id = start_time.strftime('%H%M%S')
    image_cnt = 0

    if out_file:
        out_file.close()
    
    out_file = shelve.open(os.path.join(out_dir, 'run_{}.shelve'.format(run_id)), protocol=4)

    logging.getLogger('Scoring').info('========== Run started, ID: {} =========='.format(run_id))

    return 'OK', 200

@app.route('/report', methods=['POST'])
def post_report():
    global valid_history, last_submitted, start_time, image_cnt, out_file

    recv_time = datetime.now()

    # rejection conditions
    if not start_time:
        logging.getLogger('Scoring').error('Report received but run not started.')
        return 'Run not started', 400

    if (recv_time - start_time).total_seconds() > config['max_time_per_run_s']:
        logging.getLogger('Scoring').error('Report received outside max run time.')
        return 'Outside max run time', 400

    # parse JSON data
    report = Report.from_json(flask.request.data, id=recv_time.timestamp(), timestamp=recv_time)

    logging.getLogger('Scoring').info('Report received: {}'.format(report.id))

    # detect markers in image
    corners, image_ids, _ = cv2.aruco.detectMarkers(report.image, aruco_dict, parameters=aruco_params)

    if not corners:
        # no markers seen
        logging.getLogger('Scoring').warning('No image marker detected!')
        report.marker_detected = False
    else:
        image_ids = set(image_ids.flatten())
        
        if len(image_ids) > 1:
            logging.getLogger('Scoring').warning('More than 1 target image reported!')
        else:
            report.marker_detected = True

            (image_id,) = image_ids
            report.image_id = image_id

            actual_target = config['targets'][image_id] # TODO
            

            if actual_target:
                report.image_in_config = True

                if check_valid(report, actual_target):
                    logging.getLogger('Scoring').info('Report is valid.')

                    for target in report.targets:
                        valid_history.append((recv_time, target))
                        last_submitted[image_id] = (target.cls, report.id) ####### TODO

                    curr_score = calculate_score()
                    tie_score = len(last_submitted.keys())/(recv_time - start_time).total_seconds() # TODO: verify

                    logging.getLogger('Scoring').info('Current Score: {}'.format(curr_score))
                    logging.getLogger('Scoring').info('Tie-breaker Score: {}'.format(tie_score))
                else:
                    logging.getLogger('Scoring').warning('Report is not valid.')
            else:
                logging.getLogger('Scoring').warning('Reported image not in config.')
                report.image_in_config = False

    # dump report to pickle file
    out_file[str(report.id)] = report


    # TODO: send result to API to be broadcasted 
    # send to PICO

    return {'response': True}

def check_valid(report:Report, actual_target) -> bool:
    '''Check if report is valid.'''

    global valid_history, config

    report.range_valid = True
    report.time_valid = True

    actual_target_pose = RealPose(**actual_target['pose'])

    # check for distance from target 
    # data structure for currpose is in list form
    if euclidean_distance(report.pose, actual_target_pose) > config['valid_range_m']:
        logging.getLogger('Scoring').debug('Out of physical range.')
        report.range_valid = False

    # last known attempt was within the valid_time 
    if len(valid_history) != 0:
        prev_time = valid_history[-1][0]
        if (report.timestamp - prev_time).total_seconds() < config['valid_time_s']:
            logging.getLogger('Scoring').debug('Within time range.')
            report.time_valid = False

    return report.range_valid and report.time_valid

def calculate_score():
    global config, last_submitted, out_file

    score = 0

    score_entry = dict() # maps image id to the report used and score for report.

    for actual_target_id in config['targets']:
        actual_target = config['targets'][actual_target_id]
        if actual_target['id'] in last_submitted:
            reported_cls, report_id = last_submitted[actual_target_id]

            if actual_target['cls'] == reported_cls:
                dscore = config['correct_score']
            else:
                dscore = config['wrong_score']

            logging.getLogger('Scoring.calculate_score').info(
                'Target {}: actual: {}, reported: {}, report_id: {}, score: {}'.format(
                    actual_target['id'],
                    actual_target['cls'],
                    reported_cls,
                    report_id,
                    dscore
                ))

            # record image score
            score_entry[actual_target['id']] = {
                'report_id': report_id,
                'dscore': dscore
            }

            score += dscore
        else:
            score += config['missed_score']
    
    # write scores to file
    if not 'latest_scores' in out_file.keys():
        out_file['latest_scores'] = dict()
    out_file['latest_scores'] = score_entry

    logging.getLogger('Scoring.calculate_score').info('Total score: {}'.format(score))        

    return score

def main():
    global config, out_dir

    parser = argparse.ArgumentParser(description='TIL Scoring Server.')
    parser.add_argument('config', type=str, help='Scoring configuration YAML file.')
    parser.add_argument('-i', '--host', metavar='host', type=str, required=False, default='0.0.0.0', help='Server hostname or IP address. (Default: "0.0.0.0")')
    parser.add_argument('-p', '--port', metavar='port', type=int, required=False, default=5501, help='Server port number. (Default: 5501)')
    parser.add_argument('-o', '--out_dir', dest='out_dir', type=str, required=False, default='./scoring', help='Scoring output directory.')
    parser.add_argument('-ll', '--log', dest='log_level', metavar='level', type=str, required=False, default='info', help='Logging level. (Default: "info")')
    args = parser.parse_args()

    out_dir = args.out_dir

    os.makedirs(out_dir, exist_ok=True)

    ##### Setup logging #####
    map_log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    logging.basicConfig(level=map_log_level[args.log_level],
                    format='[%(levelname)5s][%(asctime)s][%(name)s]: %(message)s',
                    datefmt='%H:%M:%S',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(os.path.join(out_dir, 'scoring_log.txt'))
                    ])

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    app.run(args.host, args.port)

if __name__ == '__main__':
    main()