import argparse
import shelve
import cv2
from termcolor import colored
from tilsdk.localization.types import euclidean_distance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Pickle filename')

    args = parser.parse_args()

    shelf = shelve.open(args.filename, 'r', protocol=4)

    keys = sorted(shelf.keys())
    ind = 0

    while True:
        report = shelf[keys[ind]]

        print(
            'id: ' + str(report.id) + '\t',
            't: '+ report.timestamp.isoformat() + '\t',
            'img_id: {:3d}'.format(report.image_id) + '\t',
            'd: {:6.2f}'.format(euclidean_distance(report.pose, report.actual_pose)) + '\t',
            colored('image_in_config', 'green' if report.image_in_config else 'red') + '\t',
            colored('time_valid', 'green' if report.time_valid else 'red') + '\t',
            colored('range_valid', 'green' if report.range_valid else 'red') + '\t',
        )

        cv2.imshow('Preview', report.get_annotated())
        k = cv2.waitKey(0)
        
        if k == 81:
            ind -= 1
            ind = max(ind, 0)
        elif k == 83:
            ind += 1
            ind = min(ind, len(keys)-1)
        elif k == ord('q'):
            break


if __name__ == '__main__':
    main()