:py:mod:`tilsdk.localization.types`
===================================

.. py:module:: tilsdk.localization.types


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   tilsdk.localization.types.Clue
   tilsdk.localization.types.GridLocation
   tilsdk.localization.types.GridPose
   tilsdk.localization.types.RealLocation
   tilsdk.localization.types.RealPose
   tilsdk.localization.types.SignedDistanceGrid



Functions
~~~~~~~~~

.. autoapisummary::

   tilsdk.localization.types.euclidean_distance
   tilsdk.localization.types.grid_to_real
   tilsdk.localization.types.real_to_grid
   tilsdk.localization.types.real_to_grid_exact



.. py:class:: Clue

   Bases: :py:obj:`NamedTuple`

   Clue

   .. py:attribute:: audio
      :annotation: :bytes

      Clue audio data.

   .. py:attribute:: clue_id
      :annotation: :int

      Unique clue id.

   .. py:attribute:: location
      :annotation: :RealLocation

      Associated location.


.. py:class:: GridLocation

   Bases: :py:obj:`NamedTuple`

   Pixel coordinates (x, y)

   .. py:attribute:: x
      :annotation: :int

      X-coordinate.

   .. py:attribute:: y
      :annotation: :int

      Y-coordinate.


.. py:class:: GridPose

   Bases: :py:obj:`NamedTuple`

   Pixel coordinates (x, y, z) where z is angle from x-axis in deg.

   .. py:attribute:: x
      :annotation: :int

      X-coordinate.

   .. py:attribute:: y
      :annotation: :int

      Y-coordinate.

   .. py:attribute:: z
      :annotation: :float

      Heading angle (rel. x-axis) in degrees.


.. py:class:: RealLocation

   Bases: :py:obj:`NamedTuple`

   Pixel coordinates (x, y)

   .. py:attribute:: x
      :annotation: :float

      X-coordinate.

   .. py:attribute:: y
      :annotation: :float

      Y-coordinate.


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


.. py:class:: SignedDistanceGrid(width = 0, height = 0, grid = None, scale = 1.0)

   Grid map representation.

   Grid elements are square and represented by a float.
   Value indicates distance from nearest obstacle.
   Value <= 0 indicates occupied, > 0 indicates passable.

   Grid is centered-aligned, i.e. real-world postion
   corresponds to center of grid square.

   :param width: Width of map in number of grid elements, corresponding to real-world x-axis. Ignored if grid parameter is specified.
   :type width: int
   :param height: Height of map in number of grid elements, corresponding to real-world y-axis. Ignored if grid parameter is specified.
   :type height: int
   :param grid: Numpy array of grid data, corresponding to a grid of width m and heigh n.
   :type grid: nxm ArrayLike
   :param scale: Ratio of real-world unit to grid unit.
   :type scale: float

   .. py:method:: dilated(self, distance)

      Dilate obstacles in grid.

      :param distance: Size of dilation.
      :type distance: float

      :returns: Grid with dilated obstacles.
      :rtype: SignedDistanceGrid


   .. py:method:: from_image(img, scale = 1.0)
      :staticmethod:

      Factory method to create map from image.

      Only the first channel is used. Channel value should be 0 where passable.

      :param img: Input image.
      :type img: Any
      :param scale: Ratio of real-world unit to grid unit.
      :type scale: float

      :returns: **map**
      :rtype: SignedDistanceGrid


   .. py:method:: grid_to_real(self, id)

      Convert grid coordinates to real coordinates.

      :param id: Input location.
      :type id: GridLocation

      :returns: Corresponding RealLocation.
      :rtype: RealLocation


   .. py:method:: in_bounds(self, id)

      Check if grid location is in bounds.

      :param id: Input location.
      :type id: GridLocation

      :returns: True if location is in bounds.
      :rtype: bool


   .. py:method:: neighbours(self, id)

      Get valid neighbours and cost of grid location.

      :param id: Input location.
      :type id: GridLocation

      :returns: **neighbours** -- List of tuples of neighbouring locations and the costs to those locations.
      :rtype: List[Tuple[GridLocation, float]]


   .. py:method:: passable(self, id)

      Check if grid location is passable.

      :param id: Input location.
      :type id: GridLocation

      :returns: True if location is in passable.
      :rtype: bool


   .. py:method:: real_to_grid(self, id)

      Convert real coordinates to grid coordinates.

      :param id: Input location.
      :type id: RealLocation

      :returns: Corresponding GridLocation.
      :rtype: GridLocation



.. py:function:: euclidean_distance(a, b)

   Compute the Euclidean distance between points.

   :param a: First point.
   :param b: Second point.

   :returns: Euclidean distance between points.
   :rtype: float


.. py:function:: grid_to_real(id: GridLocation, scale: float) -> RealLocation
              grid_to_real(id: GridPose, scale: float) -> RealPose

   Convert grid coordinates to real coordinates.

   :param id: Input location/pose.

   :returns: Corresponding real location/pose.
   :rtype: output


.. py:function:: real_to_grid(id: RealLocation, scale: float) -> GridLocation
              real_to_grid(id: RealPose, scale: float) -> GridPose

   Convert real coordinates to grid coordinates.

   .. note::
       Grid coordinates are discretized. To get non discretized grid coordinates, see :meth:`real_to_grid_exact`.

   :param id: Input location/pose.

   :returns: Corresponding gird location/pose.
   :rtype: output


.. py:function:: real_to_grid_exact(id, scale)

   Convert real coordinates to grid coordinates without discretization.

   :param id: Input location.
   :param scale: Ratio of real-world unit to grid unit.

   :returns: Grid location without discretization.
   :rtype: Tuple[float, float]


