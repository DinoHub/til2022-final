import cv2

class Camera:
    '''Mock robomaster camera.'''

    def __init__(self, robot):
        self.url = robot.url
        self.manager = robot.manager
        self._is_initialized = False

    def read_cv2_image(self, timeout:float=3, strategy:str='pipeline'):
        '''Read image from robot camera.
        
        Parameters
        ----------
        timeout
            Timeout value.

        strategy
            Image acquisition strategy. For challenge, 'newest' should be used.

        Returns
        -------
        img : ndarray
            cv2 image.
        '''
        if not self._is_initialized:
            raise Exception('Camera stream not started.')

        im = cv2.imread('fallen_man2.jpg', cv2.IMREAD_COLOR)
        return im

    def start_video_stream(self, display:bool=True, resolution='720p'):
        self._is_initialized = True