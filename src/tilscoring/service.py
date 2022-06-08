import flask
import argparse
import json
import numpy as np
import base64
import cv2
import logging
from collections import defaultdict
from tilsdk.cv.types import BoundingBox, DetectedObject
from tilsdk.localization.types import *
from datetime import datetime
import os

app = flask.Flask(__name__) 

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000) # use different from localization system
aruco_params = cv2.aruco.DetectorParameters_create()

valid_history = []
last_submitted = defaultdict(int) # maps image_id to last submitted class
config = {}
start_time = None
run_id = 0
image_cnt = 0
out_dir = ''

##### Flask server #####

@app.route('/start_run', methods=['GET'])
def get_start_run():
    global start_time, valid_history, last_submitted, run_id, image_cnt
    start_time = datetime.now().timestamp()
    valid_history = []
    last_submitted = defaultdict(int)
    run_id = np.random.randint(10000)
    image_cnt = 0

    logging.getLogger('Scoring').info('========== Run started, ID: {} =========='.format(run_id))

    return 'OK', 200

@app.route('/report', methods=['POST'])
def post_report():
    global valid_history, last_submitted, start_time, image_cnt

    recv_time = datetime.now().timestamp()

    if not start_time:
        logging.getLogger('Scoring').error('Report received but run not started.')
        return 'Run not started', 400

    if recv_time - start_time > config['max_time_per_run_s']:
        logging.getLogger('Scoring').error('Report received outside max run time.')
        return 'Outside max run time', 400

    logging.getLogger('Scoring').info('Report received: {}'.format(recv_time))

    # parse JSON data
    data = json.loads(flask.request.data)
    
    img_data = base64.b64decode(data['image'])
    np_img = np.asarray(bytearray(img_data), dtype=np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    image_fn = os.path.join(out_dir, '{}_{:05d}.png'.format(run_id, image_cnt))
    logging.getLogger('Scoring').info('Image file: {}'.format(image_fn))
    cv2.imwrite(image_fn, image)
    image_cnt += 1

    reported_pose = RealPose(**data['pose'])

    reported_targets = [DetectedObject(
        id = t['id'],
        cls = t['cls'],
        bbox = BoundingBox(**t['bbox'])
    ) for t in data['targets']]

    # detect markers in image
    corners, image_ids, _ = cv2.aruco.detectMarkers(image, aruco_dict, parameters=aruco_params)

    if not corners:
        # no markers seen
        logging.getLogger('Scoring').warning('No image marker detected!')
    else:
        image_ids = set(image_ids.flatten())
        
        if len(image_ids) > 1:
            logging.getLogger('Scoring').warning('More than 1 target image reported!')
        else:
            (image_id,) = image_ids
            image_id = str(image_id)
            actual_target = config['targets'][image_id]

            if actual_target:
                actual_target_pose = RealPose(**actual_target['pose'])

                if check_valid(reported_pose, actual_target_pose):
                    logging.getLogger('Scoring').info('Report is valid.')

                    for target in reported_targets:
                        valid_history.append((recv_time, target))
                        last_submitted[image_id] = target.cls

                    curr_score = calculate_score()
                    tie_score = len(last_submitted.keys())/(recv_time - start_time)

                    logging.getLogger('Scoring').info('Current Score: {}'.format(curr_score))
                    logging.getLogger('Scoring').info('Tie-breaker Score: {}'.format(tie_score))
                else:
                    logging.getLogger('Scoring').warning('Report is not valid.')
            else:
                logging.getLogger('Scoring').warning('Reported image not in config.')



    # TODO: send result to API to be broadcasted 
    # send to PICO

    return {'response': True}

def check_valid(curr_pose:RealPose, target_pose):
    global valid_history, config

    # check for distance from target 
    # data structure for currpose is in list form
    if euclidean_distance(curr_pose, target_pose) > config['valid_range_m']:
        logging.getLogger('Scoring').debug('Out of physical range.')
        return False

    # last known attempt was within the valid_time 
    if len(valid_history) != 0:
        prev_time = valid_history[-1][0]
        if datetime.now().timestamp() - prev_time < config['valid_time_s']:
            logging.getLogger('Scoring').debug('Within time range.')
            return False

    return True 

def calculate_score():
    global config, last_submitted

    score = 0

    for actual_target in config['targets']:
        if actual_target in last_submitted:
            logging.getLogger('Scoring').debug('Classes:  actual: {}, reported: {}'.format(config['targets'][actual_target]['cls'], last_submitted[actual_target]))

            if config['targets'][actual_target]['cls'] == str(last_submitted[actual_target]):
                score += config['correct_score']
            else:
                score += config['wrong_score']
        else:
            score += config['missed_score']

    return score

def main():
    global config, out_dir

    parser = argparse.ArgumentParser(description='TIL Scoring Server.')
    parser.add_argument('config', type=str, help='Target configuration JSON file.')
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
        config = json.load(f)

    app.run(args.host, args.port)

if __name__ == '__main__':
    main()