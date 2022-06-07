:py:mod:`tilsdk.utilities.controllers`
======================================

.. py:module:: tilsdk.utilities.controllers


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.utilities.controllers.PIDController




.. py:class:: PIDController(Kp, Kd, Ki, state = None, t = time.perf_counter())

   PID Controller Implementation

   :param Kp: P-gain values. Same dimension as state.
   :type Kp: ArrayLike
   :param Kd: D-gain values. Same dimension as state.
   :type Kd: ArrayLike
   :param Ki: I-gain values. Same dimension as state.
   :type Ki: ArrayLike
   :param state: Initial state.
   :type state: ArrayLike
   :param t: Initial time.
   :type t: float

   .. py:method:: reset(self)

      Reset the controller.

      Control gains are preserved.


   .. py:method:: update(self, state, t = time.perf_counter())

      Update the controller with new state.

      :param state: State update.
      :type state: ArrayLike
      :param t: Time associated with state update.
      :type t: float

      :returns: **output** -- Controller output.
      :rtype: ArrayLike



