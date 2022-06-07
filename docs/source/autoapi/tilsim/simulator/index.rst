:py:mod:`tilsim.simulator`
==========================

.. py:module:: tilsim.simulator


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsim.simulator.ActualRobot
   tilsim.simulator.SimRobot



Functions
~~~~~~~~~

.. autoapisummary::

   tilsim.simulator.draw_clues
   tilsim.simulator.draw_robot
   tilsim.simulator.draw_targets
   tilsim.simulator.get_camera
   tilsim.simulator.get_map
   tilsim.simulator.get_pose
   tilsim.simulator.main
   tilsim.simulator.post_cmd_vel
   tilsim.simulator.post_report
   tilsim.simulator.start_server



Attributes
~~~~~~~~~~

.. autoapisummary::

   tilsim.simulator.Rot
   tilsim.simulator.app
   tilsim.simulator.map_log_level
   tilsim.simulator.protocol_version


.. py:class:: ActualRobot(host = 'localhost', port = 5567)

   Passthrough for actual robot.

   Uses pose information from a localization service
   instance and does not perform simulation.

   :param host: Localization service host.
   :type host: str
   :param port: Localization service port.
   :type port: int

   .. py:method:: pose(self)
      :property:


   .. py:method:: step(self, dt)

      Step the simulation.

      For ActualRobot this gets latest pose from localization service.

      :param dt: Time since last simulation step.
      :type dt: float



.. py:data:: Rot
   

   

.. py:class:: SimRobot(pose=(0, 0, 0), vel=(0, 0, 0), timeout = 0.5)

   Simulated robot.

   :param pose: Initial pose.
   :param vel: Initial velocity.

   .. py:method:: last_changed(self)
      :property:


   .. py:method:: noisy_pose(self)
      :property:


   .. py:method:: pose(self)
      :property:


   .. py:method:: step(self, dt)

      Step the simulation.

      :param dt: Time since last simulation step.
      :type dt: float


   .. py:method:: vel(self)
      :property:



.. py:data:: app
   

   

.. py:function:: draw_clues(ax)


.. py:function:: draw_robot(ax, refs=None, draw_noisy=False)

   Draw robot on given axes.

   :param refs: Matplotlib refs to previously draw robot.
   :param draw_noisy: Draw robot with simulated noise.
   :type draw_noisy: bool

   :returns: Matplotlib refs to drawn robot.
   :rtype: new_refs


.. py:function:: draw_targets(ax)


.. py:function:: get_camera()


.. py:function:: get_map()


.. py:function:: get_pose()


.. py:function:: main()


.. py:data:: map_log_level
   

   

.. py:function:: post_cmd_vel()


.. py:function:: post_report()


.. py:data:: protocol_version
   :annotation: = HTTP/1.1

   

.. py:function:: start_server()


