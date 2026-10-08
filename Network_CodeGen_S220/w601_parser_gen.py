import cantools
import sys
import json
import datetime
import string
import sys, json
import os
import re
import collections

import can_msg_parser_template as parser
import default_config_template as defaultparser
import types_hal_template as typeshal
dbc = None
dbc_file_name = None
il_code_gen_dir = './CODE_GEN'
il_data_dir = './data/'
tp_generic_config = 'TpMessage'
nm_generic_config = 'NmMessage'
il_generic_config = 'GenMsgILSupport'
full_msg = "ALL"
time_str = ''
footer = ''
header = ''
dbc_info = ''
datatype_8 = 'CAN_UINT8'
datatype_16 = 'CAN_UINT16'
datatype_32 = 'CAN_UINT32'
db = ''

def set_file_node_il(file_name, node):
    global dbc, dbc_file_name,db
    from Dbc_Parser import dbc_parser
    dbc = dbc_parser(file_name, node)
    dbc_file_name = file_name.split('/')[len(file_name.split('/')) - 1]
    db = cantools.database.load_file(file_name)

def set_init_global(time_st):
    global time_str,header,usr_name
    time_str = time_st
    usr_name='Tool'
    try:
      import getpass
      usr_name=getpass.getuser()
    except:
      usr_name='Tool'
    header = parser.header.format(time_str,usr_name)

def precopy():
    with open("CODE_GEN/nw_il_par.c") as par:
        parfp = par.readlines()
        parfpprecopy = []
        for line in parfp:
            if "PreCopy" in line:
                parfpprecopy.append(line.strip("\n").split()[1])
        return parfpprecopy

def removePrecopy():
    ''' It is call to precopy function it is return the
    ['EMS12_200_PreCopy', 'EMS1_10_PreCopy', 'EMS29_100_PreCopy', 'EMS36_10_PreCopy', 'EMS3_10_PreCopy
    return ['EMS12_200,EMS1_10'''
    value = map(lambda x:x.replace('_PreCopy',''),precopy())
    return natural_sort(value)

def getCaseName():
    startingstring = "Interaction Layer Receive Message Enumerations"
    endstring = "P U B L I C   M E M O R Y"
    parserStart=False
    with open("CODE_GEN/nw_il_par.h") as case:
        casefp = case.readlines()
        caseName=[]
        for line in casefp:
            if startingstring in line:
                parserStart = True
            elif endstring in line:
                return caseName
            if parserStart:
                if "#define" in line:
                    line = line.replace("# define VNIM_","")
                    line = line.replace("_MESSAGE     .*","")
                    caseName.append(line)

def can_parser():
    usr_name = 'Tool'
    try:
        import getpass
        usr_name = getpass.getuser()
    except:
        usr_name = 'Tool'
    f = open('./CODE_GEN/CanMsgParser.cpp', 'w')
    sys.stdout = f
    print parser.header.format(time_str, usr_name)
    datachangedsignal = getSignalList()
    for messagaName in removePrecopy():
        if datachangedsignal[messagaName]:
            print parser.caseblock.format(messagaName)
            for signalname in datachangedsignal[messagaName]:
                name = signalname
                print parser.ifblock.format(name, name.upper())
            print parser.caseblockend.format(messagaName.lower(),messagaName.upper())
            print parser.ifblockend
    print parser.default
    print parser.footer


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def getMessageList():
    messageList=[]
    with open("CODE_GEN/nw_il_par.h") as case:
        pattern = "#define VNIM_(.*)_MESSAGE.*[0-9]$"
        for line in case.readlines():
            match = re.match(pattern,line)
            if match:
                messageList.append(match.group(1))
    return natural_sort(messageList)

def getSignalList():
    msgList = getMessageList()
    sigaldict = {}
    for msgName in msgList:
        pattern = ".*%s\.%s\.(.*)= data" % (msgName, msgName.lower())
        sigaldict[msgName]=[]
        with open("CODE_GEN/nw_il_par.h") as case:
            for line in case.readlines():
                match = re.match(pattern,line)
                if match:
                    sigaldict[msgName].append(match.group(1))
        sigaldict[msgName].sort()
    return sigaldict

def dbc_obj_update():
    # global  db
    with open("./data/dbc_details.data",'r')  as data_file:
        dbc_details = json.loads(data_file.read())
        data_file.close()
        dbc_name = dbc_details["ch0_file"]
        node_name = dbc_details["ch0_node_name"]
    db = cantools.database.load_file(dbc_name)
    return db

def get_dbc_parser(db,messageName):
    for message in db.messages:
        if messageName == message.name:
            return message


def default_parser():
    global db
    f = open("./CODE_GEN/DefaultConfig.hpp", "w+")
    sys.stdout = f
    # il_msg_tx, il_msg_rx, nm_msg_rx, diag_msg_rx = buffer_obj()
    print defaultparser.header
    # il_sorted_mes_rx = sorted(il_msg_rx, key=lambda x: x['Msg_name'])
    db = dbc_obj_update()
    defaultsignal = []
    creatsignal = getSignalList()

    for key, value in creatsignal.iteritems():
        defaultsignal.extend(value)

    # for signal in natural_sort(defaultsignal):
    for signal in ['HVAC_FAN_SPEED', 'HVAC_FAN_DIRECTION', 'ENG_OIL_PRESSURE_SENSOR', 'BATT_CHARGE_LAMP_INDC', 'ENG_OIL_TEMP', 'STS_WATER_IN_FUEL', 'ENG_SPD', 'INDC_GLOW_PLUG', 'CURRENT_GEAR_MT', 'ENG_TEMP', 'STS_AC_COMPRESSOR', 'STS_ENG', 'INDC_CRUISE', 'DIST_DEF_EMPTY', 'STS_DEF', 'DEF_DOSING_MALFUNC', 'INDC_REGEN', 'DEF_LEVEL', 'INCORRECT_DEF', 'EMS36_MSG_CNT', 'ENG_TRQ_AFTR_RED1', 'ENG_SPD1', 'EMS36_CRC', 'CLUTCH_STS', 'STS_DPF_REGENERATION', 'ODO_ERROR_FLAG_EMS', 'STS_ESS_INDC', 'ENG_OIL_PRESSURE', 'INDC_MIL', 'CRUISE_SET_SPD', 'FUEL_CONSMP_RATE', 'INDC_DPF_REGEN', 'INDC_CRUISE_ON_OFF', 'STS_EMS_DRV_ADV_MODE', 'INDC_SYS_LAMP', 'EMS_DRIVE_ALERT', 'ENGINE_DRIVE_MODE', 'VIN_DATA_1', 'VIN_DATA_0', 'VIN_DATA_2', 'VIN_INDEX', 'VALET_MODE_STATUS', 'DISP_AMBT_TEMP_EMS', 'HYBRID_LAMP_INDC', 'GEAR_UP_FLG', 'GEAR_DOWN_FLG', 'TARGET_GEAR_GSI', 'STS_ESS', 'RESERVED_EMS', 'EPS1_CRC', 'EPS_DRV_ADV_MODE', 'EPS_FLEX_DISP', 'EPS1_MSG_COUNT', 'INDC_EPS', 'RESERVED_EPS', 'STS_SAS_TRIM', 'STS_SAS_INTERNAL', 'ABOLUTE_ANGLE', 'SAS_MSG_CNT', 'ANGLE_SPD', 'STS_SAS_CALIB', 'STS_SAS_FAILURE', 'SAS_CRC', 'ESC12_CRC', 'ODO_DISTANCE_ESC12', 'VEHICLE_SPEED_ESC12', 'ESC12_MSG_CNT', 'STS_DDD', 'STS_ESC_DRV_ADV_MODE', 'DROWSINESS_INDEX', 'ESC_ADV_MOD_REQ', 'INDC_ROLL', 'INDC_PITCH', 'ADV_MODE_ALERT', 'AVH_FUNCTION_STS', 'PARK_BRK_ACTIVE_STS', 'EPB_ALERT', 'AVH_ACTIVE_STS', 'HDC_ACTIVE', 'STS_HHC', 'HHC_ACTIVE', 'STS_EBD', 'VEHICLE_SPEED_ESC', 'STS_EMERGENCY_BRAKING', 'STS_HDC', 'ODO_DISTANCE_ESC', 'STS_ABS', 'STS_ESC', 'ESC_ACTIVE', 'ESC5_CRC', 'STS_TVB', 'ESC5_MSG_CNT', 'EBD_ACTIVE', 'ABS_ACTIVE', 'ESC7_MSG_CNT', 'LATTERAL_ACCEL', 'LONG_ACCEL', 'ESC7_CRC', 'ESCL_NOT_LOCK_WRN', 'ESCL_WRN_FUNC', 'ESCL_WRN_SFTY', 'ESCL1_MSG_CNT', 'ESCL_STEER_WHL_JAM_WRN', 'ESCL1_CRC', 'ESCL_NOT_LEARNED_WRN', 'RESERVED_ESCL', 'RESERVED_ESC', 'STS_REAR_DEFOG_LOAD', 'INDC_REAR_FOG', 'PARK_LAMP_ON_REMINDER', 'STS_BRAKE_FLUID_LVL', 'SECURITY_LED_MBFM', 'STS_HIGH_BEAM', 'STS_TRAILER', 'STS_PARKLAMP', 'INDC_TURN_FLSHR', 'ENG_OFF_TIME', 'STS_RKE_BATT', 'INDC_FRNT_FOG', 'STS_IGN', 'KEY_IN_REMINDER', 'STS_DOOR', 'TPMS_SIGNAL_MISSING', 'HIGH_TYRE_PRESSURE', 'TPMS_PROGRAM_MODE', 'SPARE_TYRE_SWAP', 'TPMS_SYSTEM_FAULT', 'TPMS_LEAKAGE_ALERT', 'STS_RKE', 'STS_TPMS_LED', 'HIGH_TYRE_TEMPERATURE', 'TPMS_ID_NOT_LEARNT', 'LOW_TYRE_PRESSURE', 'FR_TYRE_PRESSURE', 'RL_TYRE_TEMP', 'FL_TYRE_TEMP', 'RR_TYRE_PRESSURE', 'FR_TYRE_TEMP', 'RR_TYRE_TEMP', 'FL_TYRE_PRESSURE', 'RL_TYRE_PRESSURE', 'AUTO_RAIN', 'SPARE_TYRE_TEMP', 'AUTO_LIGHT', 'BATT_VOLT', 'SPARE_TYRE_PRESSURE', 'CONFIRM_PWRDWIND_CLS_AC_MBFM', 'CONFRIM_PWRDWIND_CLS_RAIN_MBFM', 'STS_EHORN_FAIL', 'STS_LAMP_FAILURE_2', 'INDC_BRK_LAMP', 'PSGR_REAR_SEAT_BELT', 'STS_LAMP_FAILURE_1', 'CONFIRM_SUNROOF_CLS_RAIN_MBFM', 'STS_SRF_AC_ALERT', 'CONFIRM_SUNROOF_CLS_AC_MBFM', 'STS_VACATION_MODE', 'STS_SUNROOF', 'HEAD_LAMP_SW_STS', 'STS_SRF_RAIN_ALERT', 'STS_AJAR_LMP_FAILURE', 'RESERVED_MBFM', 'FPAS_DISP_DIST', 'BAR_ZONE_RRC', 'BAR_ZONE_RR', 'BAR_ZONE_FL', 'BAR_ZONE_FLC', 'FPAS_ACTIVE_STS', 'RPAS_ACTIVE_STS', 'BAR_ZONE_FR', 'RPAS_ERROR', 'BAR_ZONE_FRC', 'FPAS_ERROR', 'FPAS_SWT_STS', 'BAR_ZONE_RL', 'BAR_ZONE_RLC', 'FPAS_ALERT_DISABLE_SWT', 'RPAS_DISP_DIST', 'FOB_AUTH_FAIL_WRN', 'PKE_SHIFT_TO_PARK', 'KEY_NOT_VEH_WRN', 'TERMINAL_NOT_OFF_WRN_CMD', 'PKE_PN_OFF_WARNING', 'SSB_FAIL_WRN', 'EMRGNCY_CRANK_WRN', 'KEY_FOB_INSD_WRN', 'FOB_BATT_DISCHG_WRN', 'DOOR_LOCK_WRN', 'PKE_ICU2_MSG_CNT', 'REMOTE_ENGINE_STATE', 'P_IMMTRG_STATE', 'PKE_ICU2_CRC', 'STS_SECURITY_KEY', 'RESERVED_PKE', 'POWER_SEAT_MEMORY_STORE', 'POWER_SEAT_MEMORY_RECALL', 'DOOR_UNLOCK', 'INDC_SRS', 'INDC_PADL', 'SRS_CRC', 'STS_SEAT_BLT_PSGR', 'SRS_MSG_CNT', 'SRS_RESERVE1', 'STS_CRASH', 'STS_SEAT_BLT_DRV', 'EVEN_PARITY_BIT', 'RESERVED_SRS', 'RESERVED_EMS_SP', 'TC1_CRC', 'INDC_TC_ALERT', 'REQ_TRQ_RED_TC', 'TC1_MSG_CNT', 'INDC_TC_MALF', 'TRANSFER_MODE_TC', 'GEAR_TARGET', 'SHIFTING', 'GEAR_ACTUAL', 'INDC_AT_MALFUNC', 'TGS_MODE', 'TGS_LEVER', 'RESERVED_TCU', 'RESERVED_TC', 'TIME_TO_CHARGE']:
        for key, value in creatsignal.iteritems():
            if signal in value:
                message_obj = get_dbc_parser(db,key)
                sig_obj = filter(lambda sign: sign.name == signal,message_obj.signals).pop()
                print defaultparser.body.format(sig_obj.name+"_V",
                                                "READ_WRITE" if message_obj.senders == "SMART_CORE" else "READ" ,
                                                0 if sig_obj.maximum == None else sig_obj.maximum,
                                                0 if sig_obj.minimum == None else sig_obj.minimum,
                                                0 if sig_obj.initial == None else sig_obj.initial)
    print defaultparser.footer


def findDuplicatSignal(signals):
    '''list duplicate in list if duplicate found send True'''
    if ([item for item, count in collections.Counter(signals).items() if count > 1]):
        return True
    return False



def types_hal_parser():
    f = open("./CODE_GEN/types.hal", "w+")
    sys.stdout = f

    print typeshal.header
    # {0} = comments
    # {1} = Read/ Read or Write
    # {2} = unit or enum
    # {3} = Signal Name
    # {4} = Address
    address = 32768

    db = dbc_obj_update()
    defaultsignal = []
    creatsignal = getSignalList()

    for key, value in creatsignal.iteritems():
        defaultsignal.extend(value)

    for signal in natural_sort(defaultsignal):
        for key, value in creatsignal.iteritems():
            if signal in value:
                message_obj = get_dbc_parser(db,key)
                sig_obj = filter(lambda sign: sign.name == signal,message_obj.signals).pop()
                sig_obj.comment = "" if sig_obj.comment == None else sig_obj.comment.lstrip().rstrip()
                if "\n" in sig_obj.comment:
                    sig_obj.comment = sig_obj.comment.replace("\n", "")

                # {0} = comments
                # {1} = Read/ Read or Write
                # {2} = unit or enum
                # {3} = Signal Name
                # {4} = Address
                unit = sig_obj.unit
                if unit == None:
                    if sig_obj.choices:
                        unit = "* @data_enum " + re.sub("_", "", sig_obj.name)
                    else:
                        unit = "*"
                else:
                    unit = "* @unit VehicleUnit:" + ''.join(e for e in unit if e.isalnum())

                print typeshal.body.format(sig_obj.comment,
                                                "READ_WRITE" if message_obj.senders == "SMART_CORE" else "READ" ,
                                                unit,
                                                sig_obj.name+"_V",
                                                hex(address))
                address = address + 1
    print typeshal.bodyclose

        #enum operation

    for signal in natural_sort(defaultsignal):
        for key, value in creatsignal.iteritems():
            if signal in value:
                message_obj = get_dbc_parser(db,key)
                sig_obj = filter(lambda sign: sign.name == signal, message_obj.signals).pop()
                if sig_obj.choices and not sig_obj.unit:
                    name = re.sub("_", "", sig_obj.name)
                    print typeshal.enumbody.format(name)
                    items = filter(lambda x: "Reserved" not in x, sig_obj.choices.items())
                    items = filter(lambda x: "reserved" not in x, items)
                    items = filter(lambda x: "RESERVED" not in x, items)
                    for key, value in items:
                        value = ''.join(e for e in value if e.isalnum())
                        if value[0].isdigit():
                            result = re.match("\d+", value)
                            value = value[len(result.group(0)):] + value[:len(result.group(0))]
                        print typeshal.enumblock.format(value, key)
                    print typeshal.enumend




def releaseNotes():
    f = open("./CODE_GEN/ReleaseNotes.txt", "w+")
    sys.stdout =f
    availablesignals = getSignalList()
    db = dbc_obj_update()
    for key in natural_sort(availablesignals):
        message_obj = get_dbc_parser(db, key)
        if availablesignals[key]:
            print key+" :-"
            for signal in natural_sort(availablesignals[key]):
                sig_obj = filter(lambda sign: sign.name == signal, message_obj.signals).pop()
                sig_obj.comment = "" if sig_obj.comment == None else sig_obj.comment.lstrip().rstrip()
                print "\t"+signal+"_V"
                if sig_obj.comment:
                    for line in filter(lambda item:item,sig_obj.comment.split("\n")):
                        print "\t\t"+line

            print " "





if __name__ == "__main__":
    # can_parser()f
    default_parser()
    # types_hal_parser()
    # releaseNotes()

    # print getSignalList()
    # signallist = []
    # with open("C:\Users\mreegan\CoGent Tool Base\U321_TOOL_2_1\CODE_GEN\DefaultConfig.hpp") as fp:
    #     for line in fp.readlines():
    #         if "(VehicleProperty::" in line:
    #             signallist.append(line.split(":")[2].rstrip().replace("_V),",""))
    # print signallist
    # dbc_obj_update()
    #
    # defaultsignal = []
    #
    #
    #
    # print creatsignal.iteritems()



    # for key,value in creatsignal.iteritems():
    #     defaultsignal.extend(value)
    # print defaultsignal
    #
    # # if not findDuplicatSignal(natural_sort(defaultsignal)):
    # for signal in natural_sort(defaultsignal):
    #     for key,value in creatsignal.iteritems():
    #         if signal in value:
    #             print get_dbc_parser(db,key)