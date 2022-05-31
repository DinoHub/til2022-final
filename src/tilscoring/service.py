import flask
import argparse
import json
import numpy as np
import base64
import cv2
import logging
from collections import defaultdict
from tilsdk.localization.types import euclidean_distance
import datetime

app = flask.Flask(__name__) 

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000) # use different from localization system
aruco_params = cv2.aruco.DetectorParameters_create()

all_history = []
valid_history = []
last_submitted = defaultdict(int)
lut={}


##### Flask server #####

@app.route('/route', methods=['POST'])
def post_report():
    global all_history, valid_history, last_submitted

    # parse JSON data
    data = json.loads(flask.request.data)
    bin_data = base64.b64decode(data['image'])
    np_img = np.asarray(bytearray(bin_data), dtype=np.uint8)
    final_img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # detect markers in image
    corners, ids, _ = cv2.aruco.detectMarkers(final_img, aruco_dict, parameters=aruco_params)

    if corners:
        ids = set(ids.flatten())
        if len(ids) > 1:
            logging.getLogger('Scoring').warning('More than 1 target image reported!')
        else:
            # if valid submission, proceed, else, return:
            # fast way to unpack the set
            (item_id,) = ids
            item_id = str(item_id)

            if lut['targets'][item_id] and check_valid(data['pose'], lut['targets'][item_id]):
                logging.getLogger('Scoring').info('isValid')
                for t in data['targets']:
                    valid_history.append((datetime.now().timestamp(),t))
                    last_submitted[item_id]=t['cls']
                curr_score = calculate_score()
                logging.getLogger('Scoring').info('Current Score:' + str(curr_score))


                # real_num_targets = lut[item]
                # d = real_num_targets - num_targets
                # if d > 0:
                # 	logging.getLogger('Scoring').info('{} targets missed.'.format(d))
                # elif d < 0:
                # 	logging.getLogger('Scoring').info('{} false positives.'.format(-d))
                # else:
                # 	logging.getLogger('Scoring').info('All targets identified')
                    #        TODO: modify score

    # send result to API to be broadcasted 
    # send to PICO

    # log all target submission
    if data['targets']:
        for t in data['targets']:
            all_history.append((datetime.now().timestamp(),t))

    return {'response': True}

def check_valid(currpose, targetpose):
    global valid_history, lut

    # check for distance from target 
    # data structure for currpose is in list form
    if euclidean_distance((currpose[0],currpose[1],currpose[2]),(targetpose['x'],targetpose['y'],targetpose['z'])) > lut['valid_range']:
        logging.getLogger('Scoring').info('Out of physical range')
        return False

    # last known attempt was within the valid_time 
    if len(valid_history) != 0:
        prevtime = valid_history[-1][0]
        if datetime.now().timestamp() - prevtime < lut['valid_time_s']:
            logging.getLogger('Scoring').info('within time range')
            return False

    return True 

def check_penalty(target):
    return 0.0

def calculate_score():
    global lut, last_submitted

    score = 0
    for t in lut['targets']:
        if t in last_submitted and lut['targets'][t]['cls'] == last_submitted[t]:
            if lut['targets'][t]['priority']=='h':
                score += lut['score_per_target'] * lut['priority_wt']
            else:
                score += lut['score_per_target']
    return score 

def main():
    global lut

    parser = argparse.ArgumentParser(description='TIL Scoring Server.')
    parser.add_argument('config', type=str, help='Target configuration JSON file.')
    parser.add_argument('-i', '--host', metavar='host', type=str, required=False, default='0.0.0.0', help='Server hostname or IP address. (Default: "0.0.0.0")')
    parser.add_argument('-p', '--port', metavar='port', type=int, required=False, default=5501, help='Server port number. (Default: 5501)')
    parser.add_argument('-ll', '--log', dest='log_level', metavar='level', type=str, required=False, default='info', help='Logging level. (Default: "info")')
    args = parser.parse_args()


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
                    datefmt='%H:%M:%S')

    with open(args.config, 'r') as f:
        lut = json.load(f)
    
    app.run(args.host, args.port)