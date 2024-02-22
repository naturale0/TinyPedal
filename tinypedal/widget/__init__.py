#  TinyPedal is an open-source overlay application for racing simulation.
#  Copyright (C) 2022-2023 TinyPedal developers, see contributors.md file
#
#  This file is part of TinyPedal.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Widget modules

Add new widget to import list below in ascending order,
file name must match corresponding key name
in template/setting_widget.py dictionary.
"""

from . import (
    battery,
    brake_bias,
    brake_pressure,
    brake_temperature,
    cruise,
    damage,
    deltabest,
    deltabest_extended,
    drs,
    electric_motor,
    engine,
    flag,
    force,
    friction_circle,
    fuel,
    gear,
    heading,
    instrument,
    lap_time_history,
    navigation,
    p2p,
    pedal,
    radar,
    rake_angle,
    relative,
    ride_height,
    sectors,
    session,
    speedometer,
    standings,
    steering,
    stint_history,
    suspension_position,
    timing,
    track_map,
    trailing,
    tyre_carcass,
    tyre_load,
    tyre_pressure,
    tyre_temperature,
    tyre_wear,
    weather,
    wheel_alignment,
)
