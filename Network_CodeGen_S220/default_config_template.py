header = '''/*
 * Copyright (C) 2016 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef android_hardware_automotive_vehicle_V2_3_impl_DefaultConfig_H_
#define android_hardware_automotive_vehicle_V2_3_impl_DefaultConfig_H_

//#include <android/hardware/automotive/vehicle/2.0/IVehicle.h>
#include "HalVersion.h"
#include <vhal_v2_0/VehicleUtils.h>

namespace android {
namespace hardware {
namespace automotive {
namespace vehicle {
namespace V2_3 {

namespace impl {
//
// Some handy constants to avoid conversions from enum to int.
constexpr int ABS_ACTIVE = (int)VehicleProperty::ABS_ACTIVE;
constexpr int AP_POWER_STATE_REQ = (int)VehicleProperty::AP_POWER_STATE_REQ;
constexpr int AP_POWER_STATE_REPORT = (int)VehicleProperty::AP_POWER_STATE_REPORT;
constexpr int DOOR_1_LEFT = (int)VehicleAreaDoor::ROW_1_LEFT;
constexpr int DOOR_1_RIGHT = (int)VehicleAreaDoor::ROW_1_RIGHT;
constexpr int OBD2_LIVE_FRAME = (int)VehicleProperty::OBD2_LIVE_FRAME;
constexpr int OBD2_FREEZE_FRAME = (int)VehicleProperty::OBD2_FREEZE_FRAME;
constexpr int OBD2_FREEZE_FRAME_INFO = (int)VehicleProperty::OBD2_FREEZE_FRAME_INFO;
constexpr int OBD2_FREEZE_FRAME_CLEAR = (int)VehicleProperty::OBD2_FREEZE_FRAME_CLEAR;
constexpr int TRACTION_CONTROL_ACTIVE = (int)VehicleProperty::TRACTION_CONTROL_ACTIVE;
constexpr int VEHICLE_MAP_SERVICE = (int)VehicleProperty::VEHICLE_MAP_SERVICE;
constexpr int WHEEL_TICK = (int)VehicleProperty::WHEEL_TICK;
constexpr int ALL_WHEELS =
    (int)(VehicleAreaWheel::LEFT_FRONT | VehicleAreaWheel::RIGHT_FRONT |
          VehicleAreaWheel::LEFT_REAR | VehicleAreaWheel::RIGHT_REAR);
constexpr int HVAC_LEFT = (int)(VehicleAreaSeat::ROW_1_LEFT | VehicleAreaSeat::ROW_2_LEFT |
                                VehicleAreaSeat::ROW_2_CENTER);
constexpr int HVAC_RIGHT = (int)(VehicleAreaSeat::ROW_1_RIGHT | VehicleAreaSeat::ROW_2_RIGHT);
constexpr int HVAC_ALL = HVAC_LEFT | HVAC_RIGHT;

constexpr int CLOCK_VALUE_TIME = (int)V2_2::VehicleProperty::CLOCK_VALUE_TIME;
constexpr int SET_ALERT_ACTIVE = (int)V2_2::VehicleProperty::SET_ALERT_ACTIVE;
/*CAN Message Signal*/ //--- Nethaji

//constexpr int CAN_ACC_PED_MSG			= (int)V2_0::VehicleProperty::ACC_PED_MSG;
//constexpr int CAN_ENG_SPD_MSG			= (int)V2_0::VehicleProperty::ENG_SPD_MSG;
//constexpr int CAN_INJ_QTY_MSG			= (int)V2_0::VehicleProperty::INJ_QTY_MSG;
//constexpr int CAN_CURRENT_GEAR_MT_MSG	= (int)V2_0::VehicleProperty::CURRENT_GEAR_MT_MSG;
//constexpr int CAN_BRK_PEDAL_MSG			= (int)V2_0::VehicleProperty::BRK_PEDAL_MSG;
//constexpr int CAN_STS_AC_COMPRESSOR_MSG = (int)V2_0::VehicleProperty::STS_AC_COMPRESSOR_MSG;
//constexpr int CAN_STS_ENG_MSG			= (int)V2_0::VehicleProperty::STS_ENG_MSG;
//constexpr int CAN_ENG_TEMP_MSG			= (int)V2_0::VehicleProperty::ENG_TEMP_MSG;

///////////////////////////////// - End Nethaji



/**
 * This property is used for test purpose to generate fake events. Here is the test package that
 * is referencing this property definition: packages/services/Car/tests/vehiclehal_test
 */
const int32_t kGenerateFakeDataControllingProperty =
    0x0666 | VehiclePropertyGroup::VENDOR | VehicleArea::GLOBAL | VehiclePropertyType::MIXED;

/**
 * FakeDataCommand enum defines the supported command type for kGenerateFakeDataControllingProperty.
 * All those commands can be send independently with each other. And each will override the one sent
 * previously.
 *
 * The controlling property has the following format:
 *
 *     int32Values[0] - command enum defined in FakeDataCommand
 *
 * The format of the arguments is defined for each command type as below:
 */
enum class FakeDataCommand : int32_t {
    /**
     * Starts linear fake data generation. Caller must provide additional data:
     *     int32Values[1] - VehicleProperty to which command applies
     *     int64Values[0] - periodic interval in nanoseconds
     *     floatValues[0] - initial value
     *     floatValues[1] - dispersion defines the min/max value relative to initial value, where
     *                      max = initial_value + dispersion, min = initial_value - dispersion.
     *                      Dispersion should be non-negative, otherwise the behavior is undefined.
     *     floatValues[2] - increment, with every timer tick the value will be incremented by this
     *                      amount. When reaching to max value, the current value will be set to min.
     *                      It should be non-negative, otherwise the behavior is undefined.
     */
    StartLinear = 0,

    /** Stops generating of fake data that was triggered by Start commands.
     *     int32Values[1] - VehicleProperty to which command applies. VHAL will stop the
     *                      corresponding linear generation for that property.
     */
    StopLinear = 1,

    /**
     * Starts JSON-based fake data generation. Caller must provide a string value specifying
     * the path to fake value JSON file:
     *     stringValue    - path to the fake values JSON file
     */
    StartJson = 2,

    /**
     * Stops JSON-based fake data generation. No additional arguments needed.
     */
    StopJson = 3,

    /**
     * Injects key press event (HAL incorporates UP/DOWN acction and triggers 2 HAL events for every
     * key-press). We set the enum with high number to leave space for future start/stop commands.
     * Caller must provide the following data:
     *     int32Values[2] - Android key code
     *     int32Values[3] - target display (0 - for main display, 1 - for instrument cluster, see
     *                      VehicleDisplay)
     */
    KeyPress = 100,
};

const int32_t kHvacPowerProperties[] = {
    toInt(VehicleProperty::HVAC_FAN_SPEED),
    toInt(VehicleProperty::HVAC_FAN_DIRECTION),
};

struct ConfigDeclaration {
    VehiclePropConfig config;

    /* This value will be used as an initial value for the property. If this field is specified for
     * property that supports multiple areas then it will be used for all areas unless particular
     * area is overridden in initialAreaValue field. */
    VehiclePropValue::RawValue initialValue;
    /* Use initialAreaValues if it is necessary to specify different values per each area. */
    std::map<int32_t, VehiclePropValue::RawValue> initialAreaValues;
};
const ConfigDeclaration kVehicleProperties[]{
'''

#{0} = signal name
#{1} = proper (read,read_write)
#{2] = signal.minimum
#{3} = signal.maximum
#{4} = signal.initial

body = '''    	{{.config =
		{{
			.prop = toInt(VehicleProperty::{0}),
			.access = VehiclePropertyAccess::{1},
			.changeMode = VehiclePropertyChangeMode::ON_CHANGE,
			.minSampleRate = {2},
			.maxSampleRate = {3},
		}},
	.initialValue = {{.int32Values = {{{4}}}}}}},    
'''

footer = '''};

}  // impl

}  // namespace V2_0
}  // namespace vehicle
}  // namespace automotive
}  // namespace hardware
}  // namespace android

#endif // android_hardware_automotive_vehicle_V2_0_impl_DefaultConfig_H_
'''
