
#{0} = time
#{1} = username
header='''/********************************************************************
 *
 *   VISTEON TECHNICAL & SERVICES CENTRE CONFIDENTIAL PROPRIETARY
 *
 *
 *   FILENAME       - CanMsgParser.cpp
 *
 *
 *********************************************************************
 *   CHANGE HISTORY
 *   -----------------------------------------------------------------
 *   DATE           REVISION      AUTHOR             COMMENTS
 *   -----------------------------------------------------------------
 *   {0}           1.0       {1}        Initial version
 *********************************************************************
 *  File Description
 *  ---------------------
 *
 ********************************************************************/
#include <iostream>
#include <cstring>
#include <log/log.h>

#include "CanMsgParser.hpp"
#include <utils/SystemClock.h>

using namespace std;

extern "C" {{
  #include "../CODE_GEN/nw_il_par.h" //a C header, so wrap it in extern "C"
}}

namespace android {{
namespace hardware {{
namespace automotive {{
namespace vehicle {{
namespace V2_3 {{
namespace impl {{

CanMsgParser*  CanMsgParser::canMsgParserInstance = NULL;


CanMsgParser* CanMsgParser::getinstance(const std::shared_ptr<VstCommBase> commBase, const sp<IVehicleCallback>& callback)
{{
	if(NULL == canMsgParserInstance)
	{{
		canMsgParserInstance = new CanMsgParser(commBase, callback);
	}}
	return canMsgParserInstance;
}}

CanMsgParser::CanMsgParser(const std::shared_ptr<VstCommBase> commBase, const sp<IVehicleCallback>& callback) :
		mCommBase(commBase), mVehicleCallback(callback)
{{
	std::cout << "CanMsgParser VstCommBase" << std::endl;
}}
bool CanMsgParser::handleEvent(const uint32_t _iMethodID, const std::vector<uint8_t> _sPayloadData) {{ // TODO :: Change the function name
	//parse the event
	//Send to HMI - onPropertyEvent
	uint32_t method_id = _iMethodID;
	std::vector < uint8_t > payloadData = _sPayloadData;
	VehiclePropValue parameter;
	switch (method_id)
	{{'''

#{0}= message.name
caseblock = '''
      	case VNIM_{0}_MESSAGE :{{
      		memcpy(&{0}, payloadData.data(), sizeof({0}_buf));
      		{0}_PreCopy();
'''

#{0} = message.name + '_'+ signal.name
#{1} = (message.name + '_'+ signal.name).upper()
ifblock = '''
			if (ILGet_{0}_DataChanged() != FALSE)
			{{
			    parameter.prop = (int32_t) VehicleProperty::{0}_V;
			    parameter.value.int32Values = hidl_vec<int32_t> {{ IlRxGet{1}() }};
			    parameter.status = VehiclePropertyStatus::AVAILABLE;
			    parameter.timestamp = elapsedRealtimeNano();
			    hidl_vec < VehiclePropValue > parameters = hidl_vec < VehiclePropValue > ( {{parameter}});
			    onPropertyEvent (parameters);
			    ILClr_{1}_DataChanged();
			}}
			else
			{{
				ALOGD("CanParser::() :: {0} Data Not Changed");
			}}
'''
ifblockend='''
            }
              break;
      '''
default=''' default:
        ALOGD("CanParser::() :: No Siganl Found");
        break;
        }'''

caseblockend = '''            Rx_buffer.{0} = {1}.{0};'''

footer='''
  return false;
}

void CanMsgParser::onPropertyEvent(hidl_vec<android::hardware::automotive::vehicle::V2_0::VehiclePropValue> propValues)
{
	ALOGV("CanParser::%s() - Entering", __func__);

	if (mVehicleCallback != NULL) {
		mVehicleCallback->onPropertyEvent(propValues);
		ALOGD("CanParser::%s() - Property Event callback to VST_Vehicle", __func__);
	} else {
		ALOGE("CanParser VipInterface Callback is NULL !!!");
	}

	ALOGV("CanParser::%s() - Exit", __func__);
}

}  // impl
}  // namespace V2_3
}  // namespace vehicle
}  // namespace automotive
}  // namespace hardware
}  // namespace android
        '''
