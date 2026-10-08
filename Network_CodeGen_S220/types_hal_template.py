header='''package android.hardware.automotive.vehicle@2.3;
import android.hardware.automotive.vehicle@2.0;
import android.hardware.automotive.vehicle@2.1;
import android.hardware.automotive.vehicle@2.2;
/**
* Extension of VehiclePropertyType enum declared in Vehicle HAL 2.0
*/
enum VehiclePropertyType: @2.0::VehiclePropertyType {
};
/**
* Extension of VehicleProperty enum declared in Vehicle HAL 2.0
*/
enum VehicleProperty: @2.2::VehicleProperty{'''
body = '''/*** {0} 
* @change_mode VehiclePropertyChangeMode: ON_CHANGE
* @access VehiclePropertyAccess: {1} 
{2}
*/
{3}= (  
    {4}
    |VehiclePropertyGroup:VENDOR 
    |VehiclePropertyType:INT32 
    |VehicleArea:GLOBAL),'''
bodyclose='''};'''
enumbody='''enum {0} : int32_t {{'''
enumblock ='''      {0} = {1}, '''
enumend='''     };'''