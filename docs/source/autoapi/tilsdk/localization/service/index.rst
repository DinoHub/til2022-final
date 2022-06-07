:py:mod:`tilsdk.localization.service`
=====================================

.. py:module:: tilsdk.localization.service


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.localization.service.LocalizationService




.. py:class:: LocalizationService(host = 'localhost', port = 5566)

   Communicates with localization server to obtain map, pose and clues.


   :param host: Hostname or IP address of localization server.
   :type host: str
   :param port: Port number of localization server.
   :type port: int

   .. py:method:: get_map(self)

      Get map as occupancy grid.

      :returns: **grid** -- Signed distance grid.
      :rtype: SignedDistanceGrid


   .. py:method:: get_pose(self)

      Get real-world pose of robot.

      :returns: * **pose** (*RealPose*) -- Pose of robot.
                * **clues** (*List[Clue]*) -- Clues available at robot's location.



