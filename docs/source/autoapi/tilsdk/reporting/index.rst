:py:mod:`tilsdk.reporting`
==========================

.. py:module:: tilsdk.reporting


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   service/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.reporting.RealPose
   tilsdk.reporting.ReportingService




Attributes
~~~~~~~~~~

.. autoapisummary::

   tilsdk.reporting.DetectedObject


.. py:data:: DetectedObject
   

   Detected target object.

   .. py:attribute:: id

       Unique target id.

   .. py:attribute:: cls

       Target classification.

   .. py:attribute:: bbox
       :type: BoundingBox

       Bounding box of target.

.. py:class:: RealPose

   Bases: :py:obj:`NamedTuple`

   Real coordinates (x, y, z) where z is angle from x-axis in deg.

   .. py:attribute:: x
      :annotation: :float

      X-coordinate.

   .. py:attribute:: y
      :annotation: :float

      Y-coordinate.

   .. py:attribute:: z
      :annotation: :float

      Heading angle (rel. x-axis) in degrees.


.. py:class:: ReportingService(host = 'localhost', port = 5000)

   Communicates with reporting server to submit target reports.

   :param host: Hostname or IP address of reporting server.
   :param port: Port number of reporting server.

   .. py:method:: report(self, pose, img, targets)

      Report targets.

      :param pose: Robot pose where targets were seen.
      :param img: OpenCV image from which targets were detected.
      :param targets: Detected targets.



