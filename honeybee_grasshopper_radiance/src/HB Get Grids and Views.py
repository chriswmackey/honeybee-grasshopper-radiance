# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2025, Ladybug Tools.
# You should have received a copy of the GNU Affero General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license AGPL-3.0-or-later <https://spdx.org/licenses/AGPL-3.0-or-later>

"""
Get Radiance Sensor Grids and/or Views from a Honeybee Model and visualize them
in the Rhino scene.
-

    Args:
        _model: A Honeybee Model for which grids and views will be output.
        view_filter_: Text for a view identifer or a pattern to filter the views of the
            model that are output. For instance, `first_floor_*` will simulate
            only the views that have an identifier that starts with `first_floor_`.
            By default, all views in the model will be output.
        grid_filter_: Text for a grid identifer or a pattern to filter the sensor grids of
            the model that are output. For instance, first_floor_* will simulate
            only the sensor grids that have an identifier that starts with
            first_floor_. By default, all grids in the model will be output.

    Returns:
        views: A list of Honeybee-Radiance Views that are assigned to the
            input _model.
        grids: A list of Honeybee-Radiance SensorGrids that are assigned to
            the input _model.
        points: The points that are at the center of each grid cell.
        meshes: Mesh for each sensor grid, which can be passed to the "LB Spatial
            Heatmap" component.
"""

ghenv.Component.Name = 'HB Get Grids and Views'
ghenv.Component.NickName = 'GetGridsViews'
ghenv.Component.Message = '1.9.0'
ghenv.Component.Category = 'HB-Radiance'
ghenv.Component.SubCategory = '0 :: Basic Properties'
ghenv.Component.AdditionalHelpFromDocStrings = '5'

try:  # import core ladybug_geometry dependencies
    from ladybug_geometry.geometry3d.pointvector import Point3D
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_geometry:\n\t{}'.format(e))

try:  # import core honeybee dependencies
    from honeybee.model import Model
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import honeybee_radiance dependencies
    from honeybee_radiance.writer import _filter_by_pattern
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_radiance:\n\t{}'.format(e))

try:  # import ladybug_rhino dependencies
    from ladybug_rhino.fromgeometry import from_point3d, from_mesh3d
    from ladybug_rhino.grasshopper import all_required_inputs, list_to_data_tree
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    assert isinstance(_model, Model), \
        'Expected Honeybee Model. Got {}.'.format(type(_model))
    # get the honeybee-radiance objects
    views = _model.properties.radiance.views
    if view_filter_ is not None:
        views = _filter_by_pattern(views, view_filter_)
    grids = _model.properties.radiance.sensor_grids
    if grid_filter_ is not None:
        grids = _filter_by_pattern(grids, grid_filter_)

    # get the visualizable attributes
    points = [[from_point3d(Point3D.from_array(s.pos)) for s in sg] for sg in grids]
    points = list_to_data_tree(points)
    meshes = []
    for grid in grids:
        if grid.mesh is not None:
            meshes.append(from_mesh3d(grid.mesh))
