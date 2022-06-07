:py:mod:`tilsdk.mock_robomaster.camera`
=======================================

.. py:module:: tilsdk.mock_robomaster.camera


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.mock_robomaster.camera.Camera




.. py:class:: Camera(robot)

   Mock robomaster camera.

   .. py:method:: read_cv2_image(self, timeout = 3, strategy = 'pipeline')

      Read image from robot camera.

      For mock, gets image from simulator.

      :param timeout: Timeout value.
      :param strategy: Image acquisition strategy. For challenge, 'newest' should be used.

      :returns: **img** -- cv2 image.
      :rtype: ndarray


   .. py:method:: start_video_stream(self, display = True, resolution='720p')



