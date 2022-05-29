from typing import List
from tilsdk.cv.types import *
import onnxruntime as ort
import cv2
import numpy as np

class CVService:
    def __init__(self, model_dir):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''

        self.session = ort.InferenceSession(model_dir, providers=["CUDAExecutionProvider"])

    def targets_from_image(self, img) -> List[DetectedObject]:
        '''Process image and return targets.
        
        Parameters
        ----------
        img : Any
            Input image.
        
        Returns
        -------
        results  : List[DetectedObject]
            Detected targets.
        '''
        
        # preprocess img
        img_ = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_ = img_.astype(np.float32) / 255.0
        img_ = np.transpose(img_, axes=(2, 0, 1))

        # do inference
        labels, scores, boxes = self.session.run(['label', 'score', 'box'], {'image': img_})

        targets = []

        for i, res in enumerate(zip(labels, scores, boxes)):
            label, score, box = res
            
            # box is in (x, y, w, h) format
            obj = DetectedObject(
                id = i,
                cls = label,
                bbox = BoundingBox(*box)
            )

            targets.append(obj)

        return targets

class MockCVService:
    '''Mock CV Service.
    
    This is provided for testing purposes and should be replaced by your actual service implementation.
    '''

    def __init__(self, model_dir:str):
        '''
        Parameters
        ----------
        model_dir : str
            Path of model file to load.
        '''
        # Does nothing.
        pass

    def targets_from_image(self, img:Any) -> List[DetectedObject]:
        '''Process image and return targets.
        
        Parameters
        ----------
        img : Any
            Input image.
        
        Returns
        -------
        results  : List[DetectedObject]
            Detected targets.
        '''
        # dummy data
        bbox = BoundingBox(100,100,300,50)
        obj = DetectedObject("1", "1", bbox)
        return [obj]