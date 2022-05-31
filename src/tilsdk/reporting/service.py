import urllib3
import json
import base64
import logging 
import cv2
from typing import List, Any
from tilsdk.cv.types import DetectedObject
from tilsdk.localization.types import RealPose

class ReportingService:
    '''Communicates with reporting server to submit target reports.'''

    def __init__(self, host:str='localhost', port:int=5000):
        '''
        Parameters
        ----------
        host
            Hostname or IP address of reporting server.
        port
            Port number of reporting server.
        '''

        self.url = 'http://{}:{}'.format(host, port)
        self.manager = urllib3.PoolManager()

    def report(self, pose:RealPose, img:Any, targets:List[DetectedObject]):
        '''Report targets.

        Parameters
        ----------
        pose
            Robot pose where targets were seen.
        img
            OpenCV image from which targets were detected.
        targets
            Detected targets.
        '''

        # throttle the submission to an acceptable rate (1?2? per s)
        # # pipe the results
        _, encoded_img = cv2.imencode('.png',img)
        base64_img = base64.b64encode(encoded_img).decode("utf-8")

        # logging.getLogger('Reporting').info([t._asdict() for t in targets])

        response = self.manager.request(method='POST',
                                        url=self.url+'/report',
                                        headers={'Content-Type': 'application/json'},
                                        body=json.dumps({
                                            'pose': pose,
                                            'image':base64_img,
                                            'targets': [t._asdict() for t in targets]
                                        }))
        

        # return json.loads(response.data.decode('utf-8'))
        # print(response)
        return response