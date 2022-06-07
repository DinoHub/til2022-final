:py:mod:`tilsdk.reporting.service`
==================================

.. py:module:: tilsdk.reporting.service


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.reporting.service.ReportingService




.. py:class:: ReportingService(host = 'localhost', port = 5000)

   Communicates with reporting server to submit target reports.

   :param host: Hostname or IP address of reporting server.
   :param port: Port number of reporting server.

   .. py:method:: report(self, pose, img, targets)

      Report targets.

      :param pose: Robot pose where targets were seen.
      :param img: OpenCV image from which targets were detected.
      :param targets: Detected targets.



