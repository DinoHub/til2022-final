:py:mod:`tilsdk.utilities`
==========================

.. py:module:: tilsdk.utilities

.. autoapi-nested-parse::

   Utility functions that may be useful in autonomy code.



Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   controllers/index.rst
   filters/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.utilities.PIDController
   tilsdk.utilities.SimpleMovingAverage




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



.. py:class:: SimpleMovingAverage(n, elements = [])

   Bases: :py:obj:`Generic`\ [\ :py:obj:`_T`\ ]

   Simple Moving Average filter.

   :param n: Size of averaging window.
   :type n: int
   :param elements: Initial sequence of elements.
   :type elements: Sequence[_T]

   .. py:method:: clear(self)

      Clear filter.


   .. py:method:: get_value(self)

      Get filtered value.

      :returns: **value** -- Filtered value.
      :rtype: _T


   .. py:method:: is_full(self)

      Check if filter is fully populated.

      :returns: **is_full** -- True if full, False otherwise.
      :rtype: bool


   .. py:method:: update(self, p)

      Update filter with new reading.

      :param p: New value.
      :type p: _T

      :returns: **value** -- Filtered value.
      :rtype: _T



