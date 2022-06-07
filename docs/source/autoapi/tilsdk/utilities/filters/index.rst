:py:mod:`tilsdk.utilities.filters`
==================================

.. py:module:: tilsdk.utilities.filters


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.utilities.filters.SimpleMovingAverage




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



