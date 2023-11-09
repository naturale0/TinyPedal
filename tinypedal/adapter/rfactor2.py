#  TinyPedal is an open-source overlay application for racing simulation.
#  Copyright (C) 2022-2023  Xiang
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
Data set for rFactor 2
"""

from . import DataAdapter, calc, chknm, cs2py, fmt


class State(DataAdapter):
    """State check"""
    def version(self) -> str:
        """Identify API version"""
        return cs2py(self.info.rf2Ext.mVersion)

    def combo(self) -> str:
        """Identify track & vehicle combo"""
        track_name = cs2py(self.info.rf2Scor.mScoringInfo.mTrackName)
        class_name = cs2py(self.info.rf2ScorVeh().mVehicleClass)
        return fmt.strip_invalid_char(f"{track_name} - {class_name}")

    def vehicle(self) -> str:
        """Identify vehicle & class"""
        class_name = cs2py(self.info.rf2ScorVeh().mVehicleClass)
        veh_name = cs2py(self.info.rf2ScorVeh().mVehicleName)
        return fmt.strip_invalid_char(f"{class_name} - {veh_name}")

    def track(self) -> str:
        """Identify track name"""
        return fmt.strip_invalid_char(cs2py(self.info.rf2Scor.mScoringInfo.mTrackName))

    def session(self):
        """Identify session"""
        session_length = chknm(self.info.rf2Scor.mScoringInfo.mEndET)
        session_type = chknm(self.info.rf2Scor.mScoringInfo.mSession)
        session_stamp = int(session_length * 100 + session_type)
        session_etime = int(chknm(self.info.rf2Scor.mScoringInfo.mCurrentET))
        session_tlaps = chknm(self.info.rf2ScorVeh().mTotalLaps)
        return session_stamp, session_etime, session_tlaps

    def is_driving(self) -> bool:
        """Is local player driving or in monitor"""
        return self.info.rf2TeleVeh().mIgnitionStarter

    def lap_finish(self) -> bool:
        """Is lap finish type race, false for time finish type"""
        return chknm(self.info.rf2Scor.mScoringInfo.mMaxLaps) < 2147483647

    def in_countdown(self) -> bool:
        """Is in countdown phase before race"""
        return chknm(self.info.rf2Scor.mScoringInfo.mGamePhase) == 4

    def in_race(self) -> bool:
        """Is in race session"""
        return chknm(self.info.rf2Scor.mScoringInfo.mSession) > 9

    def in_pits(self, index: int=None) -> bool:
        """Is in pits"""
        return chknm(self.info.rf2ScorVeh(index).mInPits)

    def in_garage(self, index: int=None) -> bool:
        """Is in garage"""
        return chknm(self.info.rf2ScorVeh(index).mInGarageStall)

    def pit_open(self) -> bool:
        """Is pit lane open"""
        return chknm(self.info.rf2Scor.mScoringInfo.mGamePhase) > 0

    def same_vehicle_class(self, index: int=None) -> bool:
        """Is same vehicle class"""
        class_opt = cs2py(self.info.rf2ScorVeh(index).mVehicleClass)
        class_plr = cs2py(self.info.rf2ScorVeh().mVehicleClass)
        return class_opt == class_plr

    def blue_flag(self, index: int=None) -> int:
        """Blue flag"""
        return chknm(self.info.rf2ScorVeh(index).mFlag) == 6

    def yellow_flag(self) -> bool:
        """Yellow flag in any sectors"""
        return 1 in (chknm(self.info.rf2Scor.mScoringInfo.mSectorFlag[0]),
                     chknm(self.info.rf2Scor.mScoringInfo.mSectorFlag[1]),
                     chknm(self.info.rf2Scor.mScoringInfo.mSectorFlag[2]))

    def start_lights(self) -> int:
        """Start lights countdown sequence"""
        lights_frame = chknm(self.info.rf2Scor.mScoringInfo.mStartLight)
        lights_number = chknm(self.info.rf2Scor.mScoringInfo.mNumRedLights) + 1
        return lights_number - lights_frame


class Brake(DataAdapter):
    """Brake"""
    def bias(self, index: int=None) -> float:
        """Brake bias"""
        return chknm(self.info.rf2TeleVeh(index).mRearBrakeBias)

    def pressure(self, index: int=None):
        """Brake pressure"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mBrakePressure)
                for data in range(4)]

    def temperature(self, index: int=None):
        """Brake temperature"""
        return [calc.kelvin2celsius(
                chknm(self.info.rf2TeleVeh(index).mWheels[data].mBrakeTemp))
                for data in range(4)]


class ElectricMotor(DataAdapter):
    """Electric motor"""
    def rpm(self, index: int=None) -> float:
        """Motor RPM"""
        return chknm(self.info.rf2TeleVeh(index).mElectricBoostMotorRPM)

    def torque(self, index: int=None) -> float:
        """Motor torque"""
        return chknm(self.info.rf2TeleVeh(index).mElectricBoostMotorTorque)

    def state(self, index: int=None) -> int:
        """Motor state"""
        return chknm(self.info.rf2TeleVeh(index).mElectricBoostMotorState)

    def battery_charge(self, index: int=None) -> float:
        """Battery charge percentage"""
        return chknm(self.info.rf2TeleVeh(index).mBatteryChargeFraction)

    def motor_temperature(self, index: int=None) -> float:
        """Motor temperature"""
        return chknm(self.info.rf2TeleVeh(index).mElectricBoostMotorTemperature)

    def water_temperature(self, index: int=None) -> float:
        """Motor water temperature"""
        return chknm(self.info.rf2TeleVeh(index).mElectricBoostWaterTemperature)


class Engine(DataAdapter):
    """Engine"""
    def gear(self, index: int=None) -> int:
        """Gear"""
        return chknm(self.info.rf2TeleVeh(index).mGear)

    def gear_max(self, index: int=None) -> int:
        """Max gear"""
        return chknm(self.info.rf2TeleVeh(index).mMaxGears)

    def rpm(self, index: int=None) -> float:
        """RPM"""
        return chknm(self.info.rf2TeleVeh(index).mEngineRPM)

    def rpm_max(self, index: int=None) -> float:
        """Max RPM"""
        return chknm(self.info.rf2TeleVeh(index).mEngineMaxRPM)

    def turbo(self, index: int=None) -> float:
        """Turbo"""
        return chknm(self.info.rf2TeleVeh(index).mTurboBoostPressure)

    def oil_temperature(self, index: int=None) -> float:
        """Oil temperature"""
        return chknm(self.info.rf2TeleVeh(index).mEngineOilTemp)

    def water_temperature(self, index: int=None) -> float:
        """Water temperature"""
        return chknm(self.info.rf2TeleVeh(index).mEngineWaterTemp)


class Input(DataAdapter):
    """Input"""
    def throttle(self, index: int=None) -> float:
        """Throttle filtered"""
        return chknm(self.info.rf2TeleVeh(index).mFilteredThrottle)

    def throttle_raw(self, index: int=None) -> float:
        """Throttle raw"""
        return chknm(self.info.rf2TeleVeh(index).mUnfilteredThrottle)

    def brake(self, index: int=None) -> float:
        """Brake filtered"""
        return chknm(self.info.rf2TeleVeh(index).mFilteredBrake)

    def brake_raw(self, index: int=None) -> float:
        """Brake raw"""
        return chknm(self.info.rf2TeleVeh(index).mUnfilteredBrake)

    def clutch(self, index: int=None) -> float:
        """Clutch filtered"""
        return chknm(self.info.rf2TeleVeh(index).mFilteredClutch)

    def clutch_raw(self, index: int=None) -> float:
        """Clutch raw"""
        return chknm(self.info.rf2TeleVeh(index).mUnfilteredClutch)

    def steering(self, index: int=None) -> float:
        """Steering filtered"""
        return chknm(self.info.rf2TeleVeh(index).mFilteredSteering)

    def steering_raw(self, index: int=None) -> float:
        """Steering raw"""
        return chknm(self.info.rf2TeleVeh(index).mUnfilteredSteering)

    def steering_shaft_torque(self, index: int=None) -> float:
        """Steering shaft torque"""
        return chknm(self.info.rf2TeleVeh(index).mSteeringShaftTorque)

    def steering_range_physical(self, index: int=None) -> float:
        """Steering physical rotation range"""
        return chknm(self.info.rf2TeleVeh(index).mPhysicalSteeringWheelRange)

    def steering_range_visual(self, index: int=None) -> float:
        """Steering physical rotation range"""
        return chknm(self.info.rf2TeleVeh(index).mVisualSteeringWheelRange)

    def force_feedback(self) -> float:
        """Steering force feedback"""
        return chknm(self.info.rf2Ffb.mForceValue)


class Lap(DataAdapter):
    """Lap"""
    def number(self, index: int=None) -> int:
        """Current lap number"""
        return chknm(self.info.rf2TeleVeh(index).mLapNumber)

    def total(self, index: int=None) -> int:
        """Total completed laps"""
        return chknm(self.info.rf2ScorVeh(index).mTotalLaps)

    def track_length(self) -> float:
        """Full lap or track length"""
        return chknm(self.info.rf2Scor.mScoringInfo.mLapDist)

    def distance(self, index: int=None) -> float:
        """Distance into lap"""
        return chknm(self.info.rf2ScorVeh(index).mLapDist)

    def percent(self, index: int=None) -> float:
        """Lap percentage completion"""
        return calc.percentage_distance(
            self.distance(index),
            self.track_length(),
            0.99999)

    def maximum(self) -> int:
        """Maximum lap"""
        return chknm(self.info.rf2Scor.mScoringInfo.mMaxLaps)

    def sector_index(self, index: int=None) -> int:
        """Sector index - convert to 0,1,2 order"""
        return (2,0,1)[min(max(chknm(self.info.rf2ScorVeh(index).mSector), 0), 2)]

    def behind_leader(self, index: int=None) -> int:
        """Laps behind leader"""
        return chknm(self.info.rf2ScorVeh(index).mLapsBehindLeader)

    def behind_next(self, index: int=None) -> int:
        """Laps behind next place"""
        return chknm(self.info.rf2ScorVeh(index).mLapsBehindNext)


class Session(DataAdapter):
    """Session"""
    def elapsed(self) -> float:
        """Session elapsed time"""
        return chknm(self.info.rf2Scor.mScoringInfo.mCurrentET)

    def start(self) -> float:
        """Session start time"""
        return chknm(self.info.rf2Scor.mScoringInfo.mStartET)

    def end(self) -> float:
        """Session end time"""
        return chknm(self.info.rf2Scor.mScoringInfo.mEndET)

    def remaining(self) -> float:
        """Session time remaining"""
        return self.end() - self.elapsed()


class Suspension(DataAdapter):
    """Suspension"""
    def ride_height(self, index: int=None):
        """Ride height"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mRideHeight)
                for data in range(4)]

    def deflection(self, index: int=None):
        """Suspension deflection (meters)"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mSuspensionDeflection)
                for data in range(4)]

    def force(self, index: int=None):
        """Suspension force (Newtons)"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mSuspForce)
                for data in range(4)]


class Switch(DataAdapter):
    """Switch"""
    def headlights(self, index: int=None) -> int:
        """Headlights"""
        return chknm(self.info.rf2TeleVeh(index).mHeadlights)

    def ignition_starter(self, index: int=None) -> int:
        """Ignition"""
        return chknm(self.info.rf2TeleVeh(index).mIgnitionStarter)

    def speed_limiter(self, index: int=None) -> int:
        """Speed limiter"""
        return chknm(self.info.rf2TeleVeh(index).mSpeedLimiter)

    def drs(self, index: int=None) -> int:
        """DRS"""
        return chknm(self.info.rf2TeleVeh(index).mRearFlapActivated)

    def drs_status(self, index: int=None) -> int:
        """DRS status"""
        return chknm(self.info.rf2TeleVeh(index).mRearFlapLegalStatus)

    def auto_clutch(self) -> int:
        """Auto clutch"""
        return chknm(self.info.rf2Ext.mPhysics.mAutoClutch)


class Timing(DataAdapter):
    """Timing"""
    def start(self, index: int=None) -> float:
        """Current lap start time"""
        return chknm(self.info.rf2TeleVeh(index).mLapStartET)

    def elapsed(self, index: int=None) -> float:
        """Current lap elapsed time"""
        return chknm(self.info.rf2TeleVeh(index).mElapsedTime)

    def current_laptime(self, index: int=None) -> float:
        """Current lap time"""
        return self.elapsed(index) - self.start(index)

    def last_laptime(self, index: int=None) -> float:
        """Last lap time"""
        return chknm(self.info.rf2ScorVeh(index).mLastLapTime)

    def best_laptime(self, index: int=None) -> float:
        """Best lap time"""
        return chknm(self.info.rf2ScorVeh(index).mBestLapTime)

    def curr_sector1(self, index: int=None) -> float:
        """Current lap sector 1 time"""
        return chknm(self.info.rf2ScorVeh(index).mCurSector1)

    def curr_sector2(self, index: int=None) -> float:
        """Current lap sector 1+2 time"""
        return chknm(self.info.rf2ScorVeh(index).mCurSector2)

    def last_sector1(self, index: int=None) -> float:
        """Last lap sector 1 time"""
        return chknm(self.info.rf2ScorVeh(index).mLastSector1)

    def last_sector2(self, index: int=None) -> float:
        """Last lap sector 1+2 time"""
        return chknm(self.info.rf2ScorVeh(index).mLastSector2)

    def best_sector1(self, index: int=None) -> float:
        """Best lap sector 1 time"""
        return chknm(self.info.rf2ScorVeh(index).mBestSector1)

    def best_sector2(self, index: int=None) -> float:
        """Best lap sector 1+2 time"""
        return chknm(self.info.rf2ScorVeh(index).mBestSector2)

    def behind_leader(self, index: int=None) -> float:
        """Time behind leader"""
        return chknm(self.info.rf2ScorVeh(index).mTimeBehindLeader)

    def behind_next(self, index: int=None) -> float:
        """Time behind next place"""
        return chknm(self.info.rf2ScorVeh(index).mTimeBehindNext)


class Tyre(DataAdapter):
    """Tyre"""
    def compound(self, index: int=None):
        """Tyre compound"""
        return (chknm(self.info.rf2TeleVeh(index).mFrontTireCompoundIndex),
                chknm(self.info.rf2TeleVeh(index).mRearTireCompoundIndex))

    def surface_temperature(self, index: int=None):
        """Tyre surface temperature"""
        return [[calc.kelvin2celsius(
                chknm(self.info.rf2TeleVeh(index).mWheels[tyre].mTemperature[data])
                ) for data in range(3)] for tyre in range(4)]

    def inner_temperature(self, index: int=None):
        """Tyre inner layer temperature"""
        return [[calc.kelvin2celsius(
                chknm(self.info.rf2TeleVeh(index).mWheels[tyre].mTireInnerLayerTemperature[data])
                ) for data in range(3)] for tyre in range(4)]

    def pressure(self, index: int=None):
        """Tyre pressure"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mPressure)
                for data in range(4)]

    def load(self, index: int=None):
        """Tyre load"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mTireLoad)
                for data in range(4)]

    def wear(self, index: int=None):
        """Tyre wear"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mWear)
                for data in range(4)]


class Vehicle(DataAdapter):
    """Vehicle"""
    def driver_list(self):
        """Create player name list based on player index order"""
        return [cs2py(self.info.rf2ScorVeh(index).mDriverName)
                for index in range(max(chknm(self.info.rf2Tele.mNumVehicles), 1))]

    def is_player(self, index: int=0) -> bool:
        """Is local player"""
        return self.info.isPlayer(index)

    def player_index(self) -> int:
        """Get Local player index"""
        return self.info.playerScorIndex

    def sync_index(self, index: int=0) -> int:
        """Get synchronized target player index"""
        return self.info.find_player_index_tele(index)

    def slot_id(self, index: int=None) -> int:
        """Vehicle slot id"""
        return chknm(self.info.rf2ScorVeh(index).mID)

    def driver_name(self, index: int=None) -> str:
        """Driver name"""
        return cs2py(self.info.rf2ScorVeh(index).mDriverName)

    def vehicle_name(self, index: int=None) -> str:
        """Vehicle name"""
        return cs2py(self.info.rf2ScorVeh(index).mVehicleName)

    def class_name(self, index: int=None) -> str:
        """Vehicle class name"""
        return cs2py(self.info.rf2ScorVeh(index).mVehicleClass)

    def total(self) -> int:
        """Total vehicles"""
        return chknm(self.info.rf2Tele.mNumVehicles)

    def place(self, index: int=None) -> int:
        """Vehicle overall place"""
        return chknm(self.info.rf2ScorVeh(index).mPlace)

    def number_pitstops(self, index: int=None) -> int:
        """Number of pit stops"""
        return chknm(self.info.rf2ScorVeh(index).mNumPitstops)

    def pit_state(self, index: int=None) -> int:
        """Pit state"""
        return chknm(self.info.rf2ScorVeh(index).mPitState)

    def fuel(self, index: int=None) -> float:
        """Remaining fuel"""
        return chknm(self.info.rf2TeleVeh(index).mFuel)

    def tank_capacity(self, index: int=None) -> float:
        """Fuel tank capacity"""
        return chknm(self.info.rf2TeleVeh(index).mFuelCapacity)

    def orientation_yaw(self, index: int=None):
        """Orientation yaw"""
        return (chknm(self.info.rf2TeleVeh(index).mOri[2].x),
                chknm(self.info.rf2TeleVeh(index).mOri[2].z))

    def pos_x(self, index: int=None) -> float:
        """Raw X position"""
        return chknm(self.info.rf2TeleVeh(index).mPos.x)

    def pos_y(self, index: int=None) -> float:
        """Raw Y position"""
        return chknm(self.info.rf2TeleVeh(index).mPos.y)

    def pos_z(self, index: int=None) -> float:
        """Raw Z position"""
        return chknm(self.info.rf2TeleVeh(index).mPos.z)

    def pos_xyz(self, index: int=None):
        """Raw XYZ position"""
        return self.pos_x(index), self.pos_y(index), self.pos_z(index)

    def pos_longitudinal(self, index: int=None) -> float:
        """Longitudinal axis position related to world plane"""
        return self.pos_x(index)  # in RF2 coord system

    def pos_lateral(self, index: int=None) -> float:
        """Lateral axis position related to world plane"""
        return -self.pos_z(index)  # in RF2 coord system

    def pos_vertical(self, index: int=None) -> float:
        """Vertical axis position related to world plane"""
        return self.pos_y(index)  # in RF2 coord system

    def accel_lateral(self, index: int=None) -> float:
        """Lateral acceleration"""
        return chknm(self.info.rf2TeleVeh(index).mLocalAccel.x)  # in RF2 coord system

    def accel_longitudinal(self, index: int=None) -> float:
        """Longitudinal acceleration"""
        return chknm(self.info.rf2TeleVeh(index).mLocalAccel.z)  # in RF2 coord system

    def accel_vertical(self, index: int=None) -> float:
        """Vertical acceleration"""
        return chknm(self.info.rf2TeleVeh(index).mLocalAccel.y)  # in RF2 coord system

    def speed(self, index: int=None) -> float:
        """Speed"""
        return calc.vel2speed(
            chknm(self.info.rf2TeleVeh(index).mLocalVel.x),
            chknm(self.info.rf2TeleVeh(index).mLocalVel.y),
            chknm(self.info.rf2TeleVeh(index).mLocalVel.z))

    def downforce_front(self, index: int=None) -> float:
        """Downforce front"""
        return chknm(self.info.rf2TeleVeh(index).mFrontDownforce)

    def downforce_rear(self, index: int=None) -> float:
        """Downforce rear"""
        return chknm(self.info.rf2TeleVeh(index).mRearDownforce)


class Wheel(DataAdapter):
    """Wheel"""
    def camber(self, index: int=None):
        """Wheel camber"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mCamber)
                for data in range(4)]

    def toe(self, index: int=None):
        """Wheel toe"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mToe)
                for data in range(4)]

    def rotation(self, index: int=None):
        """Wheel rotation"""
        return [chknm(self.info.rf2TeleVeh(index).mWheels[data].mRotation)
                for data in range(4)]


class Weather(DataAdapter):
    """Weather"""
    def track_temp(self) -> float:
        """Track temperature"""
        return chknm(self.info.rf2Scor.mScoringInfo.mTrackTemp)

    def ambient_temp(self) -> float:
        """Ambient temperature"""
        return chknm(self.info.rf2Scor.mScoringInfo.mAmbientTemp)

    def raininess(self) -> float:
        """Rain percentage"""
        return chknm(self.info.rf2Scor.mScoringInfo.mRaining)

    def wetness(self):
        """Road wetness"""
        return (chknm(self.info.rf2Scor.mScoringInfo.mMinPathWetness),
                chknm(self.info.rf2Scor.mScoringInfo.mMaxPathWetness),
                chknm(self.info.rf2Scor.mScoringInfo.mAvgPathWetness))


class DataSet:
    """Data set"""

    def __init__(self, info):
        self.state = State(info)
        self.brake = Brake(info)
        self.emotor = ElectricMotor(info)
        self.engine = Engine(info)
        self.input = Input(info)
        self.lap = Lap(info)
        self.session = Session(info)
        self.suspension = Suspension(info)
        self.switch = Switch(info)
        self.timing = Timing(info)
        self.tyre = Tyre(info)
        self.vehicle = Vehicle(info)
        self.weather = Weather(info)
        self.wheel = Wheel(info)
