from tilsdk.reporting import ReportingService
from tilsdk.localization.types import *
from tilsdk.cv.types import *
import cv2

pos_target = DetectedObject(1337, 1, BoundingBox(200,200,200,200))
neg_target = DetectedObject(1338, 0, BoundingBox(200,200,200,200))

good_pose = RealPose(3,7,0)
bad_pose = RealPose(20,20,0)

img = cv2.imread('/home/jehon/Pictures/til2022/test_imgs/fallen_sample.png')

def print_help():
    print('''
    s: start
    1: good pose, good class
    2: good pose, bad  class
    3: bad  pose, good class (invalid)
    4: bad  pose, bad  class (invalid)
    ''')

service = ReportingService(port='5501')

while True:
    print_help()
    key = input('>')

    if key == 's':
        service.start_run()
    elif key == '1':
        service.report(
            pose = good_pose,
            img = img,
            targets = [pos_target]
        )
    elif key == '2':
        service.report(
            pose = good_pose,
            img = img,
            targets = [neg_target]
        )
    elif key == '3':
        service.report(
            pose = bad_pose,
            img = img,
            targets = [pos_target]
        )
    elif key == '4':
        service.report(
            pose = bad_pose,
            img = img,
            targets = [neg_target]
        )
    elif key == 'q':
        break