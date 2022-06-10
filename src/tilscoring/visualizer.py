import argparse
import shelve
import cv2
from termcolor import colored
from tilscoring.types import Report
from tilsdk.localization.types import euclidean_distance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='Pickle filename')

    args = parser.parse_args()

    shelf = shelve.open(args.filename, 'r', protocol=4)

    latest_score_record:dict = shelf['latest_scores']

    scored_image_ids = sorted(latest_score_record.keys())
    num_images = len(scored_image_ids)
    ind = 0

    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)

    print('===== Analyzing latest score =====')

    while True:
        image_id = scored_image_ids[ind]
        report_id = latest_score_record[image_id]['report_id']
        dscore = latest_score_record[image_id]['dscore']
        report:Report = shelf[str(report_id)]


        print(
            '[{:4d}/{:4d}]\t'.format(ind+1, num_images),
            'id: ' + str(report.id) + '\t',
            't: '+ report.timestamp.isoformat() + '\t',
            'img_id: {:2d}'.format(report.image_id) + '\t',
            'd: {:5.2f}'.format(euclidean_distance(report.pose, report.actual_pose)) + '\t',
            colored('image_in_config', 'green' if report.image_in_config else 'red') + '\t',
            colored('time_valid', 'green' if report.time_valid else 'red') + '\t',
            colored('range_valid', 'green' if report.range_valid else 'red') + '\t',
            'dscore: {:4.1f}'.format(dscore)
        )

        cv2.imshow('Preview', report.get_annotated(3))
        k = cv2.waitKey(0) & 0xFF
        
        if k == 81:
            ind -= 1
            ind = max(ind, 0)
        elif k == 83:
            ind += 1
            ind = min(ind, num_images-1)
        elif k == ord('q'):
            break


if __name__ == '__main__':
    main()