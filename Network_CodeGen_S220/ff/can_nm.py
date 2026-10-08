import os,sys,json


dbc=None
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgIlSupport'
nm_code_gen_dir='./code_gen/'
nm_html_dir='./html/'
nm_js_dir='./js/'
nm_data_dir='./data/'
time_str=''
footer=''
dbc_file_name=''

def set_file_node_nm(file_name,node):
    global dbc,dbc_file_name
    from Dbc_Parser import dbc_parser
    dbc=dbc_parser(file_name,node)
    dbc_file_name=file_name.split('/')[len(file_name.split('/'))-1]
    
def set_init_nm(time_st):
    global time_str,dbc_file_name,footer
    time_str = time_st
    usr_name='Tool'
    try:
        import getpass
        usr_name=getpass.getuser()
    except:
        usr_name='Tool'
    footer= '''/*****************************************************************************
    R E V I S I O N     N O T E S
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -
For each change to this file, be sure to record:
1.   Who made the change and when the change was made.
2.   Why the change was made and the intended result.

Date       By         Reason For Change
------------------------------------------------------------------------------

******************************************************************************/
/*****************************************************************************
Date			    : '''+time_str+'''
By			        : '''+usr_name+'''
Traceability		: '''+dbc_file_name+'''
Change Description	: Tool Generated code
*****************************************************************************/'''
    
def CanNm_cfg_h():
    global nm_code_gen_dir,nm_data_dir,footer
    debug = 0
    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/CanNm_Cfg.h','w')
    
    sys.stdout=f
    
    nm_cfg_file = open(nm_data_dir+"CanNMConfiguration.data",'r')
    nm_cfg_data = json.loads(nm_cfg_file.read())
    nm_cfg_file.close()

    
    include_marker = '''#ifndef CAN_NM_CFG_H
#define CAN_NM_CFG_H'''
    header='''/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           CanNm_Cfg.h
**
**  Description:    CAN NM generic configuration file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/'''

    if debug == 0:
        print include_marker,'\n',header,'\n'
        
    print '#define CANNM_NUMBER_OF_CHANNELS'+' '*10+nm_cfg_data['NM_CHANNELS']+'u'
    print '#define CANNM_MAX_DATA_LENGTH'+' '*10+nm_cfg_data['CANNM_MAX_DATA_LENGTH']+'u'



    if debug == 0:
        
        print '\n\n#endif /* CAN_NM_CFG_H */'
        print '\n\n',footer
        
    f.close()


def CanNm_par_cfg_h():
    debug=0
    global dbc,tp_generic_config,nm_generic_config,il_generic_config,footer
    global nm_code_gen_dir,nm_data_dir 
    handle_count_tx=0
    handle_count_rx=0
    
    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/CanNm_Par_Cfg.h','w')
    
    sys.stdout=f

    include_marker='''#ifndef CAN_NM_APP_CFG_H
#define CAN_NM_APP_CFG_H
'''
    if debug == 0:
        print include_marker
    
    header='''/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           CanNm_Par_Cfg.h
**
**  Description:    CAN NM project specific configurations declaration file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''
    if debug == 0:
        print header
    
    includes='''/*===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
#include "CanNm_Cfg.h"
#include "CanNm_Defines.h"

'''
    if debug == 0:
        print includes
    
    global_macro='''/* ===========================================================================
** G L O B A L  M A C R O  D E F I N I T I O N S
** =========================================================================*/
'''
    if debug == 0:
        print global_macro
    
    if dbc.get_msg_type(il_generic_config,'tx') !=[]:
        handle_count_tx+=len(dbc.get_msg_type(il_generic_config,'tx'))

    if dbc.get_msg_type(il_generic_config,'rx') !=[]:
        handle_count_rx+=len(dbc.get_msg_type(il_generic_config,'rx'))
        
    if dbc.get_msg_type(nm_generic_config,'rx') !=[]:
        handle_count_rx+=1

    print '\n/*   TP TX MESSAGE PDU MACRO  DEFINITIONS */ \n'
    if  handle_count_tx != 0:
        nm_tx_mes=dbc.get_msg_type(nm_generic_config,'tx')
        if  nm_tx_mes !=[]:
            nm_sorted_mes_tx = sorted(nm_tx_mes,key = lambda x: int(x['id']))
            temp_count=handle_count_tx
            for mes in nm_sorted_mes_tx:
                print '#define'+'    Can_Channel0_Nm_TxMessage_'+mes['Msg_name']+'_TMH '+' '*(40-len(mes['Msg_name']))+str(temp_count)+'u'
                temp_count+=1

    print '\n/*   TP RX MESSAGE PDU MACRO  DEFINITIONS */ \n'                
    if  handle_count_rx != 0:
        nm_rx_mes=dbc.get_msg_type(nm_generic_config,'rx')
        if  nm_rx_mes !=[]:
            print '#define Can_Channel0_Nm_RxMessage_NmRangeMask                '+str(handle_count_rx)+'u'

            
               

    global_const='''\n/* ===========================================================================
** G L O B A L   C O N F I G U R A T I O N   C O N S T A N T S
** =========================================================================*/

extern const NmConfigType CanNm_ReceiveFrameConfig[CANNM_NUMBER_OF_CHANNELS];

extern const NmConfigType CanNm_TransmitFrameConfig[CANNM_NUMBER_OF_CHANNELS];

'''
    if debug ==0:
        print global_const
    
        print '''\n\n#endif /* CAN_NM_APP_CFG_H */'''
        
    if debug == 0:
        print '\n\n',footer
        
    f.close()
    
def CanNm_par_cfg_c():
    debug= 0
    global dbc,tp_generic_config,nm_generic_config,il_generic_config,footer
    global nm_code_gen_dir,nm_data_dir

    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/CanNm_Par_Cfg.c','w')
    
    sys.stdout=f

    
    header='''/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           CanNm_Par_Cfg.c
**
**  Description:    CAN NM project specific configurations definition file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/'''

    includes = '''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
#include "CanNm_Par_Cfg.h"
'''
    if debug == 0:
        print header,'\n',includes,'\n'

    default_nm_rx='''/* ===========================================================================
** G L O B A L   C O N F I G U R A T I O N   C O N S T A N T S
** =========================================================================*/

const NmConfigType CanNm_ReceiveFrameConfig[CANNM_NUMBER_OF_CHANNELS] =
{
    { Can_Channel0_Nm_RxMessage_NmRangeMask,  0 }
};
'''
    if debug == 0:
        print default_nm_rx,'\n'

    print '''const NmConfigType CanNm_TransmitFrameConfig[CANNM_NUMBER_OF_CHANNELS] =
{'''
    #clarification needed to generate NM tx message
    if dbc.get_msg_type(nm_generic_config,'tx') !=[]:
        nm_msg = dbc.get_msg_type(nm_generic_config,'tx')
        for mes in nm_msg:
            print '    { Can_Channel0_Nm_TxMessage_'+mes['Msg_name']+'_TMH,  0 },'

    print '};'

    if debug == 0:
        print '\n\n',footer

    f.close()
    
def nm_cfg_h():
    
    global nm_code_gen_dir,nm_data_dir,footer
    debug = 0
    
    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/nm_cfg.h','w')
    
    sys.stdout=f
    
    nm_cfg_file = open(nm_data_dir+"CanNMConfiguration.data",'r')
    nm_cfg_data = json.loads(nm_cfg_file.read())
    nm_cfg_file.close()
    
    header='''#ifndef NM_CFG_H
#define NM_CFG_H
/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           nm_cfg.h
**
**  Description:    CAN NM specific configurations file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/

/* ===========================================================================
** G L O B A L   M A C R O   D E F I N I T I O N S
** =========================================================================*/
'''
    if debug == 0:
        print header,'\n'
    print '#define ECU_ID_BITS_6 '
    print '#define NM_CHANNELS                            ('+nm_cfg_data['NM_CHANNELS']+'u)'

    
    
    str_len=[len(x) for x in nm_cfg_data]
    max_len=max(str_len)+2
    
    for keys in nm_cfg_data:
        if keys != 'CANNM_MAX_DATA_LENGTH':
            print '#define '+keys+' '*(max_len-len(keys))+nm_cfg_data[keys]
        

    print '#endif /* NM_CFG_H */'

    if debug == 0:
        print '\n\n',footer

    f.close()
    
def nm_par_cfg_h():
    
    global nm_code_gen_dir,nm_data_dir,footer
    debug = 0
    
    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/nm_par_cfg.h','w')
    
    sys.stdout=f
    
    header = '''#ifndef NM_PAR_CFG_H
#define NM_PAR_CFG_H
/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           nm_par_cfg.h
**
**  Description:    CAN NM specific configurations file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''
    includes='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
#include "nm_types.h"
'''

    chunk='''/* Channel specific configurations */

extern const Nm_configStruct NmConfigInfo[NM_CHANNELS];

extern const Nm_FeatureStruct NmFeatureConfig[NM_CHANNELS];

extern const Nm_ChannelConfigStruct Nm_ChannelConfig[NM_CHANNELS];'''

    if debug == 0:
        print header
        print includes
        print chunk
        
    print '#endif /* NM_PAR_CFG_H */'

    if debug == 0:
        print '\n\n',footer

    f.close()
    
def nm_par_cfg_c():
    global dbc
    global nm_code_gen_dir,nm_data_dir,footer
    debug = 0
    nm_cfg_file = open(nm_data_dir+"CanNMConfiguration.data",'r')
    nm_cfg_data = json.loads(nm_cfg_file.read())
    nm_cfg_file.close()

    if not os.path.exists(nm_code_gen_dir):
      os.mkdir(nm_code_gen_dir)
    f=open(nm_code_gen_dir+'/nm_par_cfg.c','w')
    
    sys.stdout=f

    
    
    header='''/* ===========================================================================
**
**                     CONFIDENTIAL VISTEON CORPORATION
**
**  This is an unpublished work of authorship, which contains trade secrets,
**  created in 2007.  Visteon Corporation owns all rights to this work and
**  intends to maintain it in confidence to preserve its trade secret status.
**  Visteon Corporation reserves the right, under the copyright laws of the
**  United States or those of any other country that may have jurisdiction, to
**  protect this work as an unpublished work, in the event of an inadvertent
**  or deliberate unauthorized publication.  Visteon Corporation also reserves
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           nm_cfg.c
**
**  Description:    CAN NM Channel specific Configuration definitions file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''

    includes='''
/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
#include "nm_par_cfg.h"
'''
    
    if debug == 0:
        print header
        print includes

    print '''const Nm_configStruct NmConfigInfo[NM_CHANNELS] =
{'''
    print'       /* channelConf         NodeId            WakeBitMap   */ '
    print '     {'+nm_cfg_data['NM_TYPE']+', CANNM_NODEID,  CANNM_CH0_WAKE_MASK    }'
    print '};'

    temp_str=''
    temp_data=' '
    print '''const Nm_FeatureStruct NmFeatureConfig[NM_CHANNELS] =
{'''
    temp_str+= '''   /*   Passive Mode   User Data     ImmTxRestart   DiagCommCtrl   BusLoadReduction '''
    temp_data+= '     {     '+nm_cfg_data['CANNM_PASSIVE_MODE_ENABLED']+',   '+nm_cfg_data['CANNM_USER_DATA_ENABLED']+',    '+nm_cfg_data['CANNM_IMMEDIATE_RESTART_ENABLED']+\
          ',    '+ nm_cfg_data['NM_DIAG_COMMCTRL_SUPPORT']+',     '+nm_cfg_data['CANNM_BUS_LOAD_REDUCTION_ENABLED']

    
    if nm_cfg_data['CANNM_NODE_DETECTION_ENABLED'] == 'NM_ENABLE':
        temp_str+='  '+'NodeDetectionSupport'
        temp_data+=',     '+'NM_ENABLE'  

        if nm_cfg_data['CANNM_REMOTE_SLEEP_IND_ENABLED'] == 'NM_ENABLE':
            temp_str+='  '+'RemoteSleepIndSupport'
            temp_data+=',     '+'NM_ENABLE'  
                    
        if nm_cfg_data['CANNM_REPEAT_MSG_IND_ENABLED'] == 'NM_ENABLE':
            temp_str+='  '+'RepeatMessageIndSupport'
            temp_data+=',     '+'NM_ENABLE'  

    if nm_cfg_data['CANNM_BUS_SYNCHRONIZATION_ENABLED'] == 'NM_ENABLE':
        temp_str+='  '+'BusSynchSupport'
        temp_data+=',     '+'NM_ENABLE'  


    if nm_cfg_data['CanNmActiveWakeupBitEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'ActiveWakeupBitSupport'
        temp_data+=',     '+'NM_ENABLE'  


    if nm_cfg_data['CanNmRetryFirstMessageRequest'] == 'NM_ENABLE':
        temp_str+='  '+'RetryFirstMessageSupport'
        temp_data+=',     '+'NM_ENABLE'    


    if nm_cfg_data['CANNM_COORDINATOR_SYNC_SUPPORT'] == 'NM_ENABLE':
        temp_str+='  '+'CoordinatorSyncSupport'
        temp_data+=',     '+'NM_ENABLE'    


    if nm_cfg_data['CANNM_IMMEDIATE_TXCONF_ENABLED'] == 'NM_ENABLE':
        temp_str+='  '+'ImmTxConfirmationSupport'
        temp_data+=',     '+'NM_ENABLE'    


    if nm_cfg_data['CanNmCarWakeUpRxEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'CarWakeupRxSupport'
        temp_str+='  '+'CarWakeupFilterSupport'
        temp_data+=',     '+nm_cfg_data['CanNmCarWakeUpRxEnabled']
        temp_data+=',     '+nm_cfg_data['CanNmCarWakeUpFilterEnabled']


    if nm_cfg_data['CanNmPnEnabled'] == 'NM_ENABLE':
        temp_data+=',     '+nm_cfg_data['CanNmPnEnabled']
        temp_str+='  '+'CANNmPnSupport'
        temp_data+=',     '+nm_cfg_data['CanNmPnHandleMultipleNetworkRequests']
        temp_str+='  '+'CANNmPnHandleMultReqSupport'
        temp_data+=',     '+nm_cfg_data['CanNmAllNmMessagesKeepAwake']
        temp_str+='  '+'CANNmAllMessagesKeepAwakeSupport'


    if nm_cfg_data['CanNmPnEiraCalcEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'CANNmEiraCalcSupport'
        temp_data+=',     '+nm_cfg_data['CanNmPnEiraCalcEnabled']

    if nm_cfg_data['CanNmPnEraCalcEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'CANNmEraCalcSupport'
        temp_data+=',     '+nm_cfg_data['CanNmPnEraCalcEnabled']

    temp_data+='}'
    temp_str+='*/'
    print temp_str
    print temp_data
    print '};'

    temp_str=' '
    temp_data=' '
    print '''const Nm_ChannelConfigStruct Nm_ChannelConfig[NM_CHANNELS] =
{'''
    temp_str+='  '+'/*  NumOfImmMessages   NmMsgCycleOffset   NmMsgCycleTime   NmImmTransmissions   NmReducedTime '
    temp_data+='  '+ '{ '+nm_cfg_data['NM_NUMBER_OF_IMMIDIATE_MESSAGES']+',     '+nm_cfg_data['NM_MSG_CYCLE_OFFSET']+',     '+nm_cfg_data['NM_IMM_CYCLE_TIME']+\
                ',     '+nm_cfg_data['NmImmTransmissions']+',     '+nm_cfg_data['NmReducedTime']
   

    if nm_cfg_data['CANNM_REMOTE_SLEEP_IND_ENABLED'] == 'NM_ENABLE':
        temp_str+='  '+'RemoteSleepIndTime'
        temp_data+=',     '+nm_cfg_data['RemoteSleepIndTime']
        
    if nm_cfg_data['CanNmCarWakeUpRxEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'CarWakeBytePos'
        temp_data+=',     '+nm_cfg_data['CarWakeBytePos']

        temp_str+='  '+'CarWakeBitPos'
        temp_data+=',     '+nm_cfg_data['CarWakeBitPos']

        temp_str+='  '+'CarWakeFltrNodeId'
        temp_data+=',     '+nm_cfg_data['CarWakeFltrNodeId']


    if nm_cfg_data['CanNmPnEnabled'] == 'NM_ENABLE':
        temp_str+='  '+'CBV_PNInfo'
        temp_data+=',     '+nm_cfg_data['NM_CBV_PARTIAL_NETWORK_INFORMATION_BIT']

        temp_str+='  '+'NmPnInfoLength'
        temp_data+=',     '+nm_cfg_data['NmPnInfoLength']

        temp_str+='  '+'NmPnInfoOffset'
        temp_data+=',     '+nm_cfg_data['NmPnInfoOffset']

        temp_str+='  '+'NmPnResetTime'
        temp_data+=',     '+nm_cfg_data['NmPnResetTime']

        
    temp_str+='*/'
    temp_data+='}'
    print temp_str
    print temp_data
    print '};'

    if debug == 0:
        print '\n\n',footer

    f.close()
    


        
if __name__ == '__main__':
    pass
    '''file_name="FF_Door.dbc"
    node="DDP"
    set_file_node_tp_nm(file_name,node)
    #below are represented for NM co-ordinator
    CanNm_par_cfg_h()
    CanNm_par_cfg_c()
    CanNm_cfg_h()
    #below are files represented for can NM since Faraday code is used.
    #below are represented for faraday Autosar NM ,source code is given 

    nm_cfg_h()
    nm_par_cfg_h()
    nm_par_cfg_c()'''
