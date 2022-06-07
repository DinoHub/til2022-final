:py:mod:`tilsdk.cv`
===================

.. py:module:: tilsdk.cv


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   types/index.rst


Package Contents
----------------

.. py:data:: BoundingBox
   

   Bounding box (bbox).

   .. py:attribute:: x
       :type: float

       bbox center x-coordinate.

   .. py:attribute:: y
       :type: float

       bbox center y-coordinate.

   .. py:attribute:: w
       :type: float

       bbox width.

   .. py:attribute:: h
       :type: float

       bbox height.

.. py:data:: DetectedObject
   

   Detected target object.

   .. py:attribute:: id

       Unique target id.

   .. py:attribute:: cls

       Target classification.

   .. py:attribute:: bbox
       :type: BoundingBox

       Bounding box of target.

