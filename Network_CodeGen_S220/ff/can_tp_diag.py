import os,sys,json

dbc=None
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgIlSupport'

code_gen_dir='./code_gen/'
tp_diag_html_dir='./html/'
tp_diag_js_dir='./tp_diag_js_dir/'
tp_diag_data_dir='./data/'

service_count = 0
rcrrp_enable =0
function_response = 0
min_length = 0
physical_pid = -1
functional_pid = -1
resp_pid = -1
time_str = ''
dbc_file_name=''
footer=''
    
def diag_code_init(time_st):
    global service_count,rcrrp_enable,function_response,min_length
    global time_str,dbc_file_name,footer
    time_str=time_st
    service_count = 0
    rcrrp_enable =0
    function_response = 0
    min_length = 0
    time_str=time_st
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

def tp_code_init(time_st):
    global time_str
    global physical_pid,functional_pid,resp_pid
    time_str=time_st
    physical_pid = -1
    functional_pid = -1
    resp_pid = -1
    

def set_file_node_tp_nm(file_name,node):
    global dbc,dbc_file_name
    from Dbc_Parser import dbc_parser
    dbc=dbc_parser(file_name,node)
    dbc_file_name=file_name.split('/')[len(file_name.split('/'))-1]
    
def tp_par_cfg_h():
    debug = 0
    global dbc,tp_generic_config,nm_generic_config,il_generic_config,footer
    global code_gen_dir,tp_diag_data_dir,physical_pid,functional_pid,resp_pid
    handle_count_tx=0
    handle_count_rx=0
    
    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    f=open(code_gen_dir+'/CanTp_Par_Cfg.h','w')
    
    sys.stdout=f

    include_marker='''#if !defined( CAN_TP_APP_CFG_H )
#define CAN_TP_APP_CFG_H'''
    
    print include_marker
    
    header='''
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
**  Name:           CanTp_Par_Cfg.h
**
**  Description:    CAN TP configuration parameters for configured 
**                    database
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''
    print header
    
    includes='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
# include "CanTp_Cfg.h"
'''
    print includes
    
    global_macro='''/* ===========================================================================
** G L O B A L  M A C R O  D E F I N I T I O N S
** =========================================================================*/
'''
    print global_macro
    
        

    if dbc.get_msg_type(il_generic_config,'tx') !=[]:
        handle_count_tx+=len(dbc.get_msg_type(il_generic_config,'tx'))
    if dbc.get_msg_type(nm_generic_config,'tx') !=[]:
        handle_count_tx+=len(dbc.get_msg_type(nm_generic_config,'tx'))

    if dbc.get_msg_type(il_generic_config,'rx') !=[]:
        handle_count_rx+=len(dbc.get_msg_type(il_generic_config,'rx'))
    if dbc.get_msg_type(nm_generic_config,'rx') !=[]:
        handle_count_rx+=1
    temp_count = -1
    print '\n/*   TP TX MESSAGE PDU MACRO  DEFINITIONS */ \n'
    if  handle_count_tx >= 0:
        tp_tx_mes=dbc.get_msg_type(tp_generic_config,'tx')
        if  tp_tx_mes !=[]:
            tp_sorted_mes_tx = sorted(tp_tx_mes,key = lambda x: int(x['id']))
            temp_count=handle_count_tx
            for mes in tp_sorted_mes_tx:
                print '#define'+' Can_Channel0_Tp_TxMessage_'+mes['Msg_name']+'_TMH '+' '*(40-len(mes['Msg_name']))+str(temp_count)+'u'
                temp_count+=1
                
    if  temp_count >= 0:
        print '#define CanTp_Start_RespID_Handle          '+str(temp_count-1)+'u'
    else:
        print '#define CanTp_Start_RespID_Handle          0xFFu'
    
    resp_pid=temp_count-1
    print '\n/*   TP RX MESSAGE PDU MACRO  DEFINITIONS */ \n'

    diag_cfg_file = open(tp_diag_data_dir+"CanDbcMsgConfiguration.data",'r')
    diag_mes_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    physical_id=[]
    functional_id=[]
    app_id=[]
    
    if  handle_count_rx >= 0:
        tp_rx_mes=dbc.get_msg_type(tp_generic_config,'rx')
        if  tp_rx_mes !=[]:
            tp_sorted_mes_rx = sorted(tp_rx_mes,key = lambda x: int(x['id']))
            
            for mes in tp_sorted_mes_rx:
                if mes['Msg_name']+'_tp_type_no_of_events' in diag_mes_data:
                        if diag_mes_data[mes['Msg_name']+'_tp_type_no_of_events'] == 'Functional_Request':
                            functional_id.append((mes,mes['Msg_name']))
                        elif diag_mes_data[mes['Msg_name']+'_tp_type_no_of_events'] == 'Physical_Request':
                            physical_id.append((mes,mes['Msg_name']))
                        else:
                            app_id.append((mes,mes['Msg_name']))
    temp_count = -1
    if physical_id!=[]:
        temp_count=handle_count_rx
        physical_pid=handle_count_rx
        for mes in physical_id:
                print '#define'+' Can_Channel0_Tp_RxMessage_'+mes[1]+' '+' '*(40-len(mes[1]))+str(temp_count)+'u'
                temp_count+=1
        
    if functional_id!=[]:
        if temp_count == -1 :
            temp_count=handle_count_rx
        functional_pid = temp_count
        for mes in functional_id:
                print '#define'+' Can_Channel0_Tp_RxMessage_'+mes[1]+' '+' '*(40-len(mes[1]))+str(temp_count)+'u'
                temp_count+=1

    if app_id!=[]:
        if temp_count == -1 :
            temp_count=handle_count_rx
        for mes in app_id:
                print '#define'+' Can_Channel0_Tp_RxMessage_'+mes[1]+' '+' '*(40-len(mes[1]))+str(temp_count)+'u'
                temp_count+=1

    print '#define CanTp_Start_ReqID_Handle '+' '*8+str(handle_count_rx)+'u'
    if temp_count >= 0:
        print '#define CanTp_Stop_ReqID_Handle  '+' '*8+str(temp_count-1)+'u'
    else:
        print '#define CanTp_Stop_ReqID_Handle  '+' '*8+'0xFFu'

    
    print '''#define CanTp_Num_Of_RxCB_Func          VTP_NUM_CHANNEL_COUNT
#define CanTp_Num_Of_TxCB_Func          VTP_NUM_CHANNEL_COUNT
'''

    global_const='''/* ===========================================================================
** G L O B A L  C O N S T A N T  D E C L A R A T I O N S
** =========================================================================*/

extern const sTP_Parameter_Config_Type CanTp_Parameter_Config[VTP_NUM_CHANNEL_COUNT];

extern const sTP_RxTiming_Config_Type  CanTp_Receive_Timing_Config[VTP_NUM_CHANNEL_COUNT];

extern const sTP_TxTiming_Config_Type  CanTp_Transmit_Timing_Config[VTP_NUM_CHANNEL_COUNT];

extern const sTP_RxCB_Config_Type   CanTp_Appl_ReceiveCB_FuncPtr[CanTp_Num_Of_RxCB_Func];

extern const sTP_TxCB_Config_Type   CanTp_Appl_TransmitCB_FuncPtr[CanTp_Num_Of_TxCB_Func];

'''
    print global_const
    
    print '''#endif  /* CAN_TP_APP_CFG_H */'''

    
    if debug == 0:
        print '\n\n',footer

        
    f.close()

def can_tp_par_cfg_c():
    debug = 0
    global code_gen_dir,tp_diag_data_dir,footer

    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    f=open(code_gen_dir+'/CanTp_Par_Cfg.c','w')
    
    sys.stdout=f

    tp_cfg_file = open(tp_diag_data_dir+"CanTPConfiguration.data",'r')
    tp_cfg_data = json.loads(tp_cfg_file.read())
    tp_cfg_file.close()
    
    
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
**  Name:           CanTp_Par_Cfg.c
**
**  Description:    CAN TP configuration parameters for configured 
**                    database
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''
    print header,'\n'

    includes='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/

# include "CanTp_Par_Cfg.h"
# include "CanDiag_Uds.h"

/* ===========================================================================
** C O N F I G U R A T I O N S  D E F I N I T I O N S
** =========================================================================*/
'''
    print includes,'\n'
    
    print '''const sTP_Parameter_Config_Type CanTp_Parameter_Config[VTP_NUM_CHANNEL_COUNT] =
{'''
    print '{ 0,'+' CanTp_Start_ReqID_Handle ,'+' CanTp_Stop_ReqID_Handle ,'+' CanTp_Start_RespID_Handle ,'+' CANTP_DIAG_MESSAGE ,',
    if tp_cfg_data['VTP_FC_SUPPORT'] == 'VTP_YES':
        print 'VTP_YES ,',
    else:
        print 'VTP_NO ,',
    print '0, 0 ',
    print '}'
    print '};\n\n'

    

    print '''const sTP_RxTiming_Config_Type  CanTp_Receive_Timing_Config[VTP_NUM_CHANNEL_COUNT] =
{
    {''',
    if tp_cfg_data['VTP_FC_SUPPORT'] == 'VTP_YES':
        print tp_cfg_data['N_Cr_Rx_CF_Timeout']+',',
    print tp_cfg_data['N_WFTmax_No_OF_WAIT_FRAMES'],

    print '}\n};\n\n'

    print '''const sTP_TxTiming_Config_Type  CanTp_Transmit_Timing_Config[VTP_NUM_CHANNEL_COUNT] =
{
    {''',
    print tp_cfg_data['N_As_Tx_CONFIRMATION_TIMEOUT']+',',
    if tp_cfg_data['VTP_FC_SUPPORT'] == 'VTP_YES':
        print tp_cfg_data['N_Bs_FLOW_CONTROL_TIMEOUT']+',',
        print '{'+tp_cfg_data['Stmin']+' , '+tp_cfg_data['Blocksize']+' },',
    print tp_cfg_data['N_WFTmax_No_OF_WAIT_FRAMES']+',',
    print tp_cfg_data['N_Cs_TX_CF_Timeout'],
    print '}'
    print '};\n\n'

    #Below will change when application tp is included,1st element is for diag
    print '''const sTP_RxCB_Config_Type   CanTp_Appl_ReceiveCB_FuncPtr[CanTp_Num_Of_RxCB_Func] =
{
    { CanDiag_UdsStartOfReception , CanDiag_UdsCopyRxData , CanDiag_UdsTpRxIndication }
};


const sTP_TxCB_Config_Type   CanTp_Appl_TransmitCB_FuncPtr[CanTp_Num_Of_TxCB_Func] =
{
    { CanDiag_UdsCopyTxData , CanDiag_UdsTpTxConfirmation , CanDiag_UdsTxConfirmation }
};
'''


    if debug == 0:
        print '\n\n',footer
        

    f.close()

    
def tp_cfg_h():
    debug = 0
    global dbc,footer
    global code_gen_dir,tp_diag_data_dir 
    tp_cfg_file = open(tp_diag_data_dir+"CanTPConfiguration.data",'r')
    tp_cfg_data = json.loads(tp_cfg_file.read())
    tp_cfg_file.close()

    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    f=open(code_gen_dir+'/CanTp_Cfg.h','w')
    
    sys.stdout=f
    
    header='''#if !defined( CAN_TP_CFG_H )
#define CAN_TP_CFG_H

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
**  Name:           CanTp_Cfg.h
**
**  Description:    CAN TP specific configuration parameters
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''
    print header,'\n'

    includes='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/

# include "CanTp_Defines.h"

/* ===========================================================================
** M A C R O   D E F I N I T I O N S
** =========================================================================*/
'''
    print includes,'\n'
    
    print '#define VTP_CAN_CHANNEL      0'
    str_len=[len(x) for x in tp_cfg_data]
    max_len=max(str_len)+2
    
    for keys in tp_cfg_data:
        print '#define '+keys+' '*(max_len-len(keys))+tp_cfg_data[keys]

    print '\n\n#endif /* CAN_TP_CFG_H */'

    if debug == 0:
        print '\n\n',footer

        
    f.close()    




    
def diag_par_cfg_c():
    debug= 0

    global code_gen_dir,tp_diag_data_dir,footer
    global service_count,rcrrp_enable,function_response,min_length
    global physical_pid,functional_pid,resp_pid
    
    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    f=open(code_gen_dir+'/CanDiag_Uds_Par_Cfg.c','w')

    if debug == 0:
        sys.stdout=f

    diag_cfg_file = open(tp_diag_data_dir+"CanDiagServiceConfiguration.data",'r')
    diag_service_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    diag_cfg_file = open(tp_diag_data_dir+"CanDiagSessionConfiguration.data",'r')
    diag_session_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    session=[]
    if 'no_of_session' in diag_session_data:
        for val in range(1,int(diag_session_data['no_of_session'])+1):
            session.append(diag_session_data['session_'+str(val)])
    else:
        session=['DEFAULT','EXTENTED']


    header='''/*****************************************************************************
*
*                            CONFIDENTIAL - Visteon
*
*   This is unpublished work, which is a trade secret, created in 2012.
*   Visteon owns all rights to this work and intends to maintain it in
*   confidence to preserve its trade secret status. Visteon reserves
*   the right to protect this work as an unpublished copyrighted work
*   in the event of an inadvertent or deliberate unauthorized publication.
*   Visteon also reserves its right under the copyright laws to protect
*   this work as a published work. Those having access to this work may
*   not copy it, use it, or disclose the information contained in it
*   without the written authorization of Visteon.
*
*                            Copyright 2013, Visteon
*
*****************************************************************************/

/* ===========================================================================

  Name:           CanDiag_Uds_Par_Cfg.c

  Description:    CAN UDS Parameter project specific configuration parameters

  Organization:   Multiplex Core Technology

 =========================================================================*/

/***************************************************************************
                     P R O J E C T   I N C L U D E S                        
***************************************************************************/
'''

    includes='''#include "CanDiag_Uds_Defines.h"
#include "CanDiag_Uds_Par_Cfg.h"
#include "CanDiag_Uds.h"
#include "CanVnim_DiagnosticInterface.h"
'''

    generic='''/*****************************************************************************
                     C O N S T A N T   D E F I N I T I O N S                  
*****************************************************************************/

CanDiag_UdsBufferSizeType const CanDiag_UdsMaxBufferSize[CANDIAG_NUMOFDIAGREQUEST_TYPES] =
{
    CANDIAG_MAXPRIMARYBUFFLEN,
    CANDIAG_MAXSECONDARYBUFFLEN
};

CanDiag_UdsSrvcType const CanDiag_UdsNumSrv = CANDIAG_NUM_SERVICES;

'''

    if debug== 0:
        print header,'\n'
        print includes,'\n'
        print generic,'\n'

    
    print '''CanDiag_UdsServiceInfoType const CanDiag_UdsSrvcInfoTable[CANDIAG_NUM_SERVICES] =
{
'''
    

    '''for serv in diag_service_data:
        temp_serv = serv.split('_enable')
        print temp_serv
        if len(temp_serv) == 2 :
            if temp_serv[1] =="":
                services.append(temp_serv[0])'''
    
    services=['StartDiagnosticSession','EcuReset','SecurityAccess','CommunicationControl','TesterPresent',\
              'SecuredDataTransmission','ControlDTCSetting','ResponseOnEvent','ReadDataByIdentifier','ReadMemoryByAddress',\
              'WriteDataByIdentifier','WriteMemoryByAddress','ReadDataByPeriodicIdentifier','DynamicallyDefineIdentifier',\
              'ClearDiagnosticInformation','ReadDTCInformation','InputOutputControlByIdentifier','RoutineControl','AccessTimingParameter','LinkControl','ReadScalingDataByIdentifier']
    
    #print services
    
    temp_str=''
    service_count=0
    rcrrp_enable=0
    function_response = 0
    min_length = 0
    for idx in services:
        if idx+'_enable' in diag_service_data:
            if diag_service_data[idx+'_enable'] == 'on':
                service_count+=1
                temp_str+= '    {  '
                if diag_service_data[idx+'_request_id'] != '':
                    temp_str+= '0x'+diag_service_data[idx+'_request_id']
                else:
                    temp_str+= '0x'+'00'
                
                if diag_service_data[idx+'_response_id'] != '':
                    temp_str+= '   ,0x'+diag_service_data[idx+'_response_id']
                else:
                    temp_str+= '   ,0x'+'00'
                no_session_check = 0
                ses_str = ''
                temp_i=0
                for ses in session:
                    #print idx+'_'+ses.lower()
                    if diag_service_data[idx+'_SNO_'+str(temp_i)] == 'on':
                       ses_str+='|'+ses.upper()+'SESSION'
                       no_session_check+=1
                       temp_i+=1
                       
                if len(session) == no_session_check:
                    temp_str+= '   ,'+'NOSESSIONCHECK'
                else:
                    #print ses_str
                    if ses_str != '|' and ses_str !='':
                        temp_str+= '   ,'+'('+ses_str.lstrip('|')+')'
                    else:
                        temp_str+= '   ,'+'DEFAULTSESSION'
                    
                if diag_service_data[idx+'_data_length_check'] == 'on':
                    min_length+=1
                    if diag_service_data[idx+'_data_length_val'] !='':
                        temp_str+= '   ,'+diag_service_data[idx+'_data_length_val']

                    if diag_service_data[idx+'_data_length_option'] !='':
                        temp_str+= '   ,'+diag_service_data[idx+'_data_length_option']

                if diag_service_data[idx+'_func_response'] == 'on':
                    temp_str+= '   ,'+'CANDIAG_ENABLE'
                    function_response+=1
                else:
                    temp_str+= '   ,'+'CANDIAG_DISABLE'

                if diag_service_data[idx+'_rcrrp'] == 'on':
                    rcrrp_enable+=1
                    temp_str+= '   ,'+'CANDIAG_ENABLE'
                else:
                    temp_str+= '   ,'+'CANDIAG_DISABLE'

                temp_str+= '},   /*'+idx+'*/\n'

    temp_str.rstrip(',')
    print temp_str
    print '};'

    print '''CanDiag_UdsRequestInfoType const CanDiag_UdsRequestInfoTable[CANDIAG_NUMOFDIAGREQUEST_TYPES] =
{'''
    if physical_pid > 0:
        print '     {CANDIAG_PHY_ADDR_FRAME_PDUID, CANDIAG_PHY_ADDR_FRAME_PDUID},\n',
    if functional_pid > 0:
        print '     {CANDIAG_FUNC_ADDR_FRAME_PDUID, CANDIAG_FUNC_ADDR_FRAME_PDUID}'

    print '''};'''


    generic_chunk='''CanDiag_UdsNrcType const CanDiag_UdsSupportedNrcSuppression[CANDIAG_NUM_SUPPRESS_NRC] =
{
    0x00, 0x11, 0x12, 0x31
};'''

    if debug== 0:
        print '\n',generic_chunk,'\n'
        
    diag_cfg_file = open(tp_diag_data_dir+"CanDIAGConfiguration.data",'r')
    diag_cfg_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    #pre condition check callback function		
    print 'CanDiag_UdsPreConditionsChkFuncType const CanDiag_UdsPreCondCheckFuncPtr = ',
    if diag_cfg_data['CANDIAG_PRECONDITIONS_CHECK_SUPPORT'] != 'CANDIAG_ENABLE':
        print 'CanVnim_DiagPreCondCheck',
    else:
        print 'NULL',
    print ';'

    #session timeout callback function													
    print 'CanDiag_SessionTOApplCBType const CanDiag_SessionTimeOutApplCB = CanVnim_DiagSessionTOApplCB;\n'

    #service timeout callback function		
    print 'CanDiag_ServiceTOApplCBType const CanDiag_ServiceTimeOutApplCB = CanVnim_DiagServiceTOCB;\n'


    if debug == 0:
        print '\n\n',footer

    f.close()



def diag_par_cfg_h():
    debug=0
    global code_gen_dir,tp_diag_data_dir,footer
    global service_count,rcrrp_enable,function_response
    global physical_pid,functional_pid,resp_pid
    
    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
      
    f=open(code_gen_dir+'/CanDiag_Uds_Par_Cfg.h','w')
    if debug == 0:
        sys.stdout=f

    header='''#ifndef CANDIAG_UDS_APP_CFG_H
#define CANDIAG_UDS_APP_CFG_H
/*****************************************************************************
*
*                            CONFIDENTIAL - Visteon
*
*   This is unpublished work, which is a trade secret, created in 2012.
*   Visteon owns all rights to this work and intends to maintain it in
*   confidence to preserve its trade secret status. Visteon reserves
*   the right to protect this work as an unpublished copyrighted work
*   in the event of an inadvertent or deliberate unauthorized publication.
*   Visteon also reserves its right under the copyright laws to protect
*   this work as a published work. Those having access to this work may
*   not copy it, use it, or disclose the information contained in it
*   without the written authorization of Visteon.
*
*                            Copyright 2013, Visteon
*
*****************************************************************************/
'''

    includes='''
/***************************************************************************
                    P R O J E C T   I N C L U D E S
***************************************************************************/

#include "Can_defs.h"
#include "CanDiag_Uds_Cfg.h"
'''

    macro='''/***************************************************************************
                    M A C R O   D E C L A R A T I O N S
***************************************************************************/

'''

    if debug == 0:
        print header,'\n'
        print includes,'\n'
        print macro,'\n'

    diag_cfg_file = open(tp_diag_data_dir+"CanDIAGConfiguration.data",'r')
    diag_cfg_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    max_data = 0
    max_data_type=''
    if 'CANDIAG_MAXPRIMARYBUFFLEN' in diag_cfg_data:
        max_data=int(diag_cfg_data['CANDIAG_MAXPRIMARYBUFFLEN'])
        print '#define CANDIAG_MAXPRIMARYBUFFLEN  '+diag_cfg_data['CANDIAG_MAXPRIMARYBUFFLEN']
        max_data_type='CANDIAG_MAXPRIMARYBUFFLEN'

    if 'CANDIAG_MAXSECONDARYBUFFLEN' in diag_cfg_data:
        if int(diag_cfg_data['CANDIAG_MAXSECONDARYBUFFLEN']) >= int(diag_cfg_data['CANDIAG_MAXPRIMARYBUFFLEN']):
            max_data=int(diag_cfg_data['CANDIAG_MAXSECONDARYBUFFLEN'])
            max_data_type='CANDIAG_MAXSECONDARYBUFFLEN'
        print '#define CANDIAG_MAXSECONDARYBUFFLEN  '+diag_cfg_data['CANDIAG_MAXSECONDARYBUFFLEN']

    if 'CANDIAG_UDS_P2RESPTIME_IN_MSEC' in diag_cfg_data:
        print '#define CANDIAG_UDS_P2RESPTIME_IN_MSEC  '+diag_cfg_data['CANDIAG_UDS_P2RESPTIME_IN_MSEC']

    if 'CANDIAG_UDS_S3TIME_INMSEC' in diag_cfg_data:
        print '#define CANDIAG_UDS_S3TIME_INMSEC  '+diag_cfg_data['CANDIAG_UDS_S3TIME_INMSEC']

    if 'CANDIAG_UDS_RCRRPTIME_INMSEC' in diag_cfg_data:
        print '#define CANDIAG_UDS_RCRRPTIME_INMSEC  '+diag_cfg_data['CANDIAG_UDS_RCRRPTIME_INMSEC']

    if 'CANDIAG_UDS_RCRRPMAXCOUNT' in diag_cfg_data:
        print '#define CANDIAG_UDS_RCRRPMAXCOUNT  '+diag_cfg_data['CANDIAG_UDS_RCRRPMAXCOUNT']

    
    print '#define CANDIAG_NUM_SUPPRESS_NRC  4'
    print '#define CANDIAG_NUM_SERVICES  '+str(service_count)


    print '#define CANDIAG_MAX_DATA_SIZE  '+max_data_type
    
    print '''#define MainHandler                            (CanVnim_DiagSrvcMainHandler)
#define PostHandler                            (CanVnim_DiagSrvcPostHandler)
'''

    #getting input from user for physical and functinal request.
    

    
    
    if physical_pid >= 0:
        print '#define CANDIAG_PHY_ADDR_FRAME_PDUID   '+str(physical_pid)
    else:
        print '#define CANDIAG_PHY_ADDR_FRAME_PDUID   0xFF'
        
    if functional_pid>= 0:
        print '#define CANDIAG_FUNC_ADDR_FRAME_PDUID    '+str(functional_pid)
    else:
        print '#define CANDIAG_PHY_ADDR_FRAME_PDUID   0xFF'

    if physical_pid >= 0: 
        print '#define CANDIAG_FIRST_PDUID    '+str(physical_pid)
    else:
        print '#define CANDIAG_FIRST_PDUID    0xFF'
        
    if functional_pid>= 0:  
        print '#define CANDIAG_LAST_PDUID     '+str(functional_pid)
    else:
        print '#define CANDIAG_LAST_PDUID     0xFF'


    if resp_pid>= 0:  
        print '#define CANDIAG_RESPONSE_FRAME_PDUID     '+str(resp_pid)
    else:
        print '#define CANDIAG_RESPONSE_FRAME_PDUID     0xFF'

    print '''#include "CanDiag_Uds_Defines.h"

/***************************************************************************
 *                        GLOBAL CONSTANT DECLARATIONS
***************************************************************************/

extern const CanDiag_UdsSrvcType CanDiag_UdsNumSrv;

extern const CanDiag_UdsBufferSizeType CanDiag_UdsMaxBufferSize[CANDIAG_NUMOFDIAGREQUEST_TYPES];

extern const CanDiag_UdsServiceInfoType CanDiag_UdsSrvcInfoTable[CANDIAG_NUM_SERVICES];

extern const CanDiag_UdsRequestInfoType CanDiag_UdsRequestInfoTable[CANDIAG_NUMOFDIAGREQUEST_TYPES];

extern const CanDiag_UdsNrcType CanDiag_UdsSupportedNrcSuppression[CANDIAG_NUM_SUPPRESS_NRC];

extern const CanDiag_UdsPreConditionsChkFuncType CanDiag_UdsPreCondCheckFuncPtr;

extern const CanDiag_SessionTOApplCBType CanDiag_SessionTimeOutApplCB;

extern const CanDiag_ServiceTOApplCBType CanDiag_ServiceTimeOutApplCB;'''


    

    print '\n\n#endif /* CANDIAG_UDS_APP_CFG_H */'
    
    if debug == 0:
        print '\n\n',footer
        
        
    f.close() 


def diag_cfg_h():
    global code_gen_dir,tp_diag_data_dir,footer
    global service_count,rcrrp_enable,function_response,min_length
    debug = 0
    
    if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    f=open(code_gen_dir+'/CanDiag_Uds_Cfg.h','w')

    if debug == 0:
        sys.stdout=f

    diag_cfg_file = open(tp_diag_data_dir+"CanDIAGConfiguration.data",'r')
    diag_cfg_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()
    

    header='''#ifndef CANDIAG_UDS_CFG_H
#define CANDIAG_UDS_CFG_H
/*****************************************************************************
*
*                            CONFIDENTIAL - Visteon
*
*   This is unpublished work, which is a trade secret, created in 2012.
*   Visteon owns all rights to this work and intends to maintain it in
*   confidence to preserve its trade secret status. Visteon reserves
*   the right to protect this work as an unpublished copyrighted work
*   in the event of an inadvertent or deliberate unauthorized publication.
*   Visteon also reserves its right under the copyright laws to protect
*   this work as a published work. Those having access to this work may
*   not copy it, use it, or disclose the information contained in it
*   without the written authorization of Visteon.
*
*                            Copyright 2013, Visteon
*
*****************************************************************************/'''

    includes='''/***************************************************************************
                    P R O J E C T   I N C L U D E S
***************************************************************************/
'''

    macro='''
/***************************************************************************
                    M A C R O   D E C L A R A T I O N S
***************************************************************************/

'''

    if debug == 0:
        print header,'\n'
        print includes,'\n'
        print macro,'\n'


    print '#define CANDIAG_TPCHANNEL '+' '*(40-len('CANDIAG_TPCHANNEL'))+'0'
    if 'CANDIAG_NUMOFCHANNELS' in diag_cfg_data:
        if diag_cfg_data['CANDIAG_NUMOFCHANNELS']!=' ':
            print '#define CANDIAG_NUMOFCHANNELS '+' '*(40-len('CANDIAG_NUMOFCHANNELS'))+diag_cfg_data['CANDIAG_NUMOFCHANNELS']
        else:
            print '#define CANDIAG_NUMOFCHANNELS '+' '*(40-len('CANDIAG_NUMOFCHANNELS'))+'1'

    print '\n'
    #session 
    diag_cfg_file = open(tp_diag_data_dir+"CanDiagSessionConfiguration.data",'r')
    diag_session_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()

    session=[]
    if 'no_of_session' in diag_session_data:
        for val in range(1,int(diag_session_data['no_of_session'])+1):
            session.append(diag_session_data['session_'+str(val)])
    else:
        session=['DEFAULT','EXTENTED']
        
    
    ses_val=['0x00','0x01','0x02','0x04','0x8','0x10','0x20','0x40','0x80']
    temp_count = 0
    for val in session:
        print '#define '+val+'SESSION'+' '*(40-len(val+'SESSION'))+ses_val[temp_count]
        temp_count+=1       
        
     
    
    print #define CANDIAG_CALLCYCLE_INMSEC                  10
    if 'CANDIAG_CALLCYCLE_INMSEC' in diag_cfg_data:
        if diag_cfg_data['CANDIAG_CALLCYCLE_INMSEC']!=' ':
            print '#define CANDIAG_CALLCYCLE_INMSEC '+' '*(40-len('CANDIAG_CALLCYCLE_INMSEC'))+diag_cfg_data['CANDIAG_CALLCYCLE_INMSEC']
        else:
            print '#define CANDIAG_CALLCYCLE_INMSEC '+' '*(40-len('CANDIAG_CALLCYCLE_INMSEC'))+'10'

    if 'CANDIAG_PRECONDITIONS_CHECK_SUPPORT' in diag_cfg_data:
        print '#define CANDIAG_PRECONDITIONS_CHECK_SUPPORT '+' '*(40-len('CANDIAG_PRECONDITIONS_CHECK_SUPPORT'))+diag_cfg_data['CANDIAG_PRECONDITIONS_CHECK_SUPPORT']
        if diag_cfg_data['CANDIAG_PRECONDITIONS_CHECK_SUPPORT'] == 'CANDIAG_ENABLE':
            if 'CANDIAG_PRECOND_CHECK_AT_START' in diag_cfg_data:
                print '#define CANDIAG_PRECOND_CHECK_AT_START '+' '*(40-len('CANDIAG_PRECOND_CHECK_AT_START'))+diag_cfg_data['CANDIAG_PRECOND_CHECK_AT_START']
            else:
                print '#define CANDIAG_PRECOND_CHECK_AT_START '+' '*(40-len('CANDIAG_PRECOND_CHECK_AT_START'))+'CANDIAG_DISABLE'
        else:
            print '#define CANDIAG_PRECOND_CHECK_AT_START '+' '*(40-len('CANDIAG_PRECOND_CHECK_AT_START'))+'CANDIAG_DISABLE'

    else:
        print '#define CANDIAG_PRECONDITIONS_CHECK_SUPPORT '+' '*(40-len('CANDIAG_PRECONDITIONS_CHECK_SUPPORT'))+'CANDIAG_DISABLE'

    print '#define CANDIAG_ASR_SUPPORT '+' '*(40-len('CANDIAG_ASR_SUPPORT'))+'CANDIAG_ENABLE'

    if 'CANDIAG_SECONDARY_RCRRP_SUPPORT' in diag_cfg_data:
        print '#define CANDIAG_SECONDARY_RCRRP_SUPPORT '+' '*(40-len('CANDIAG_SECONDARY_RCRRP_SUPPORT'))+diag_cfg_data['CANDIAG_SECONDARY_RCRRP_SUPPORT']
    else:
        print '#define CANDIAG_SECONDARY_RCRRP_SUPPORT '+' '*(40-len('CANDIAG_SECONDARY_RCRRP_SUPPORT'))+'CANDIAG_DISABLE'

    if 'CANDIAG_FUNC_NRC_SUPPRESS' in diag_cfg_data:
        print '#define CANDIAG_FUNC_NRC_SUPPRESS '+' '*(40-len('CANDIAG_FUNC_NRC_SUPPRESS'))+diag_cfg_data['CANDIAG_FUNC_NRC_SUPPRESS']
    else:
        print '#define CANDIAG_FUNC_NRC_SUPPRESS '+' '*(40-len('CANDIAG_FUNC_NRC_SUPPRESS'))+'CANDIAG_DISABLE'
    #define CANDIAG_FUNC_NRC_SUPPRESS				  CANDIAG_ENABLE

   

    if rcrrp_enable >=1:#define CANDIAG_RCRRP_SUPPORT                     CANDIAG_ENABLE
        print '#define CANDIAG_RCRRP_SUPPORT '+' '*(40-len('CANDIAG_RCRRP_SUPPORT'))+'CANDIAG_ENABLE'
    else:
        print '#define CANDIAG_RCRRP_SUPPORT '+' '*(40-len('CANDIAG_RCRRP_SUPPORT'))+'CANDIAG_DISABLE'

    if function_response >=1:
        print '#define CANDIAG_RESPONSE_ON_FUNC_REQ '+' '*(40-len('CANDIAG_RESPONSE_ON_FUNC_REQ'))+'CANDIAG_ENABLE'
    else:
        print '#define CANDIAG_RESPONSE_ON_FUNC_REQ '+' '*(40-len('CANDIAG_RESPONSE_ON_FUNC_REQ'))+'CANDIAG_DISABLE'

    if function_response == service_count:
        print '#define CANDIAG_RESPONSE_ALL_ON_FUNC_REQ '+' '*(40-len('CANDIAG_RESPONSE_ALL_ON_FUNC_REQ'))+'CANDIAG_ENABLE'
    else:
        print '#define CANDIAG_RESPONSE_ALL_ON_FUNC_REQ '+' '*(40-len('CANDIAG_RESPONSE_ALL_ON_FUNC_REQ'))+'CANDIAG_DISABLE'

    #CANDIAG_REQUEST_MIN_LENGTH_CHECK
    if min_length >=1:
        print '#define CANDIAG_REQUEST_MIN_LENGTH_CHECK '+' '*(40-len('CANDIAG_REQUEST_MIN_LENGTH_CHECK'))+'CANDIAG_ENABLE'
    else: 
        print '#define CANDIAG_REQUEST_MIN_LENGTH_CHECK '+' '*(40-len('CANDIAG_REQUEST_MIN_LENGTH_CHECK'))+'CANDIAG_DISABLE'


    

    print '\n\n#endif /* CANDIAG_UDS_CFG_H */'

    if debug == 0:
        print '\n\n',footer
        
    f.close()



if __name__ == '__main__':
    pass
    '''file_name="FF_Door.dbc"
    node="DDP"
    set_file_node_tp_nm(file_name,node)

    diag_code_init()
    tp_code_init()
    
    tp_par_cfg_h()
    can_tp_par_cfg_c()
    tp_cfg_h()

    diag_cfg_h()
    diag_par_cfg_h()
    diag_par_cfg_c()'''

    
