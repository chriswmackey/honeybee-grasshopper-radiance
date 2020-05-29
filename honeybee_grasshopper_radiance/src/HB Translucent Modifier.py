# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2019, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

"""
Create a translucent radiance modifier from a reflectances and transmittances.
-

    Args:
        _name: Text to set the name for the modifier and to be incorporated into
            a unique modifier identifier.
        _diff_ref: A number between 0 and 1 for the opaque diffuse reflectance.
            This reflectance will be the same for the red, green and blue channels.
        _diff_trans: A number between 0 and 1 for the transmitted diffuse component.
            This is the fraction of transmitted light that is diffusely scattered.
        _spec_trans: A number between 0 and 1 for the transmitted specular component.
            This is the fraction of transmitted light that is not diffusely
            scattered but passes through like a beam.
        _spec_: A number between 0 and 1 for the fraction of specularity. Specularity
            fractions greater than 0.1 are not common in non-metallic materials (Default: 0).
        _rough_: Roughness is specified as the rms slope of surface facets. A value
            of 0 corresponds to a perfectly smooth surface, and a value of 1 would be
            a very rough surface. Roughness values greater than 0.2 are not very
            realistic. (Default: 0).
    
    Returns:
        modifier: A translucent modifier that can be assigned to a Honeybee geometry
            or Modifier Sets.
"""

ghenv.Component.Name = 'HB Translucent Modifier'
ghenv.Component.NickName = 'TransMod'
ghenv.Component.Message = '0.1.0'
ghenv.Component.Category = 'HB-Radiance'
ghenv.Component.SubCategory = '1 :: Modifiers'
ghenv.Component.AdditionalHelpFromDocStrings = '2'

try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_rad_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the honeybee-radiance dependencies
    from honeybee_radiance.modifier.material import Trans
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_radiance:\n\t{}'.format(e))

try:  # import ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))


if all_required_inputs(ghenv.Component):
    # set the default modifier properties
    _spec_ = 0.0 if _spec_ is None else _spec_
    _rough_ = 0.0 if _rough_ is None else _rough_

    # create the modifier
    modifier = Trans.from_single_reflectance(
        clean_and_id_rad_string(_name), _diff_ref, _spec_, _rough_,
        _diff_trans, _spec_trans)
    modifier.display_name = _name