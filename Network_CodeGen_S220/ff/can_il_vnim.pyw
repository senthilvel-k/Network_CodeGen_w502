import json,sys,os

dbc=None
vnim_generic_cfg={}
shadow_rx_buffer=[]

CanVnim_Rx_Num_TaskIds=1
CanVnim_Tx_Num_TaskIds=1
CanVnim_Rx_Num_ErrTaskIds=1
CanVnim_Tx_Num_ErrTaskIds=1
CanVnim_Tx_MaxNum_TaskIdsForSignal=1
CanVnim_Rx_MaxNum_TaskIdsForSignal=1
vnim_code_gen_dir = './CODE_GEN'
vnim_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgIlSupport'
time_str=''
footer=''
dbc_file_name=''
max_alive_cnt_tx = 0
max_alive_cnt_rx = 0
    
def set_file_node_il_vnim(file_name,node):
    global dbc,dbc_file_name
    from Dbc_Parser import dbc_parser
    dbc=dbc_parser(file_name,node)
    dbc_file_name=file_name.split('/')[len(file_name.split('/'))-1]
    
def set_init_global(time_st):
    global CanVnim_Rx_Num_TaskIds,CanVnim_Tx_Num_TaskIds,CanVnim_Rx_Num_ErrTaskIds,CanVnim_Tx_Num_ErrTaskIds,CanVnim_Tx_MaxNum_TaskIdsForSignal,CanVnim_Rx_MaxNum_TaskIdsForSignal,shadow_rx_buffer 
    global time_str,dbc_file_name,footer,max_alive_cnt_tx,max_alive_cnt_rx
    CanVnim_Rx_Num_TaskIds=1
    CanVnim_Tx_Num_TaskIds=1
    CanVnim_Rx_Num_ErrTaskIds=1
    CanVnim_Tx_Num_ErrTaskIds=1
    CanVnim_Tx_MaxNum_TaskIdsForSignal=1
    CanVnim_Rx_MaxNum_TaskIdsForSignal=1
    max_alive_cnt_tx = 0
    max_alive_cnt_rx = 0
    shadow_rx_buffer=[]
    vnim_generic_cfg={}
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
    
def Vnim_par_c():

    global CanVnim_Rx_Num_TaskIds,CanVnim_Tx_Num_TaskIds,CanVnim_Rx_Num_ErrTaskIds,CanVnim_Tx_Num_ErrTaskIds,CanVnim_Tx_MaxNum_TaskIdsForSignal,CanVnim_Rx_MaxNum_TaskIdsForSignal,shadow_rx_buffer
    global dbc,il_generic_config,max_alive_cnt_tx,max_alive_cnt_rx
    
    global vnim_code_gen_dir,vnim_data_dir,vnim_generic_cfg
    vnim_generic_cfg={}
    vnim_cfg_data={}
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanVnim_Par_Cfg.c','w')
  
    
    sys.stdout = f

    #vnim_generic=open(vnim_data_dir+"CanVNIMConfiguration.data",'r')
    #vnim_generic_gui = json.loads(vnim_generic.read())
    #vnim_generic.close()
    
    vnim_cfg_file = open(vnim_data_dir+"CanDbcSigConfiguration.data",'r')
    vnim_cfg_data = json.loads(vnim_cfg_file.read())
    vnim_cfg_file.close()
    
    vnim_cfg_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r')
    vnim_mes_cfg_data = json.loads(vnim_cfg_file.read())
    vnim_cfg_file.close()

    header = '''/* ===========================================================================
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
**  its rights under all copyright laws to protect this work as a published
**  work, when appropriate.  Those having access to this work may not copy it,
**  use it, modify it or disclose the information contained in it without the
**  written authorization of Visteon Corporation.
**
** =========================================================================*/

/* ===========================================================================
**
**  Name:           CanVnim_Par_Cfg.c
**
**  Description:    CAN VNIM configuration parameter Configuration file for 
**                  configured database file
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
** =========================================================================*/'''

    print header
    includes = '''/* ===========================================================================
**  I N C L U D E   F I L E S
** =========================================================================*/

/* ===========================================================================
**  I N C L U D E   F I L E S
** =========================================================================*/

# include "CanVnim_Par_Cfg.h"
# include "etsuppt.cfg"
# include "etsuppt.h"
'''
    print'\n',includes
    junk='''/* ===========================================================================
** G L O B A L   C O N S T A N T   D E F I N I T I O N S
** =========================================================================*/
'''
    
    print '\n',junk
    
    il_msg_tx=dbc.get_msg_type(il_generic_config,'tx')
    il_msg_rx=dbc.get_msg_type(il_generic_config,'rx')
    #sorting messages by ascending order of id
    il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: int(x['id']))
    il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: int(x['id']))
    #sorting messages 
    sig_count_tx=0

    tx_conf_id_unique=[]
    tx_conf_id=[]
    tx_err_id=[]
    tx_id_mask=[]
    temp_msg_count = 0;
    tx_ind_msg_count=[]
    tx_error_count=[]
    #tx error id
    tx_conf_id_1=[]
    tx_conf_id_2=[]
    tx_conf_id_3=[]
    tx_err_id_msg=[]
    tx_id_err_mask=[]
    no_of_event_id=[]

    vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXEVENTID_SUPPORT'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXERREVENTID_SUPPORT']='STD_OFF'
    vnim_generic_cfg['CANVNIM_TX_TOUTINDICATION_API']="STD_OFF"
    vnim_generic_cfg['CANVNIM_EVENTID_DIFFERFROM_ERRORID'] = 'STD_ON'
    vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS']= 'STD_OFF'
    vnim_generic_cfg['CANVNIM_EVENT_INACTIVE_SUPPORT'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_SEPARATE_INIT_CONDITIONS']='STD_ON'
    
    vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']="STD_OFF"
    vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT']="STD_OFF"
    
    vnim_generic_cfg['CANVNIM_VALIDATION_CONDITION_CHECK'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_ALIVECNTR_INVALID_ONCONDITION'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_IL_HASHFUNCTION']='NONE'
    vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']='NO_ASSIGN'
    
#define CANVNIM_IL_HASHFUNCTION                       CRC
#define CANVNIM_IL_VALIDATION_SUPPORT                 SIGNAL

    il_hash_macro_cnt=[]
    il_val_sup_macro=[]
    for mes in il_sorted_mes_tx:
        sig_par=[]
        sorted_list=[]
        temp_ind_id_cnt=0
        temp_err_id_cnt=0
        temp_tx_conf_id_1=[]
        temp_tx_conf_id_2=[]
        temp_tx_conf_id_3=[]
        temp_tx_err_id=[]
        temp_tx_id_err_mask=[]
        
        #tx_error_macro=[]
        temp_tx_err_mask=[]
        
         #code for evaluating wheter the support for ack
        if vnim_mes_cfg_data[str(mes['Msg_name'])+'_validation_supp'] == 'on':
            vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']="STD_ON"
         
        if vnim_mes_cfg_data[str(mes['Msg_name'])+'_alive_counter_supp'] == 'on':
            vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT']="STD_ON"   
            vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']="STD_ON"
            
        
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
       
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
        for signals in sig_sorted:
            ind_tx = "CANVNIM_NO"
            timeout_tx = "CANVNIM_NO"
            
            
            
            if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_no_of_events'] !='' and  vnim_cfg_data[str(signals['signal_name'])+'_tx_conf'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_no_of_events'])
                temp_lst=[0]*no_of_events
                #print no_of_events
                no_of_event_id.append(no_of_events)
                #print no_of_event_id

                if  vnim_cfg_data[str(signals['signal_name']+'_tx_timeout')] == 'on':
                    vnim_generic_cfg['CANVNIM_TX_TOUTINDICATION_API']="STD_ON"
                              
                for i in range(1,no_of_events+1):
                    
                    if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)] not in tx_conf_id_unique:
                        tx_conf_id_unique.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                        temp_ind_id_cnt+=1
                        
                    if i==1:
                        if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)] not in temp_tx_conf_id_1:
                            temp_tx_conf_id_1.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                    
                    if i==2:
                    
                        if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)] not in temp_tx_conf_id_2:
                            temp_tx_conf_id_2.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                    if i==3:
                        if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)] not in temp_tx_conf_id_3:
                            temp_tx_conf_id_3.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                            
                    tx_conf_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                    tx_id_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_MASK_'+str(i)])

            #print vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_no_of_events']
            if vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_no_of_events'] !='' and vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_no_of_events'])
                
                    
                for i in range(1,no_of_events+1):
                    if vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_ID_'+str(i)] not in tx_err_id:
                        tx_err_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_ID_'+str(i)])
                        temp_err_id_cnt+=1
                    if vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_ID_'+str(i)] not in temp_tx_err_id:
                        temp_tx_err_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_ID_'+str(i)])
                        temp_tx_id_err_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_MASK_'+str(i)])
                    #tx_conf_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_ID_'+str(i)])
                    temp_tx_err_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_MASK_'+str(i)]) 
                        
            ''' 
            #{ /*     1 */       		 0,		    0x0,   SIG_NOSENDTYPE,           CANVNIM_YES,              CANVNIM_YES }, /* [ApplVers_Minor]   */
            if vnim_cfg_data[str(signals['signal_name']+'_tx_conf'] == 'on':
                             ind_tx = "CANVNIM_YES"

            if  vnim_cfg_data[str(signals['signal_name']+'_tx_timeout'] == 'on':
                              timeout_tx="CANVNIM_YES"
                              
            print '{ /*     '+str(sig_count)+' */      0,      '+hex(int(vnim_cfg_data[str(signals['signal_name'])+'_init_value')))+',   SIG_NOSENDTYPE,           '+CANVNIM_YES,              CANVNIM_YES }, /* [ApplVers_Minor]   */'''
            sig_count_tx+=1
        tx_ind_msg_count.append(temp_ind_id_cnt)
        
        tx_conf_id_1.append(temp_tx_conf_id_1)
        tx_conf_id_2.append(temp_tx_conf_id_2)
        tx_id_err_mask.append(temp_tx_id_err_mask)
        tx_err_id_msg.append(temp_tx_err_id)
        tx_error_count.append(temp_err_id_cnt)
        temp_ind_id_cnt+=temp_err_id_cnt
        
        time_out_mask = 0
        for x in temp_tx_err_mask:
            if temp_tx_err_mask[0] != x:
                time_out_mask=1
                break

        if len(temp_tx_err_id) >1 or time_out_mask ==1:#if the error ids are different from each other in a signal.
            vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXERREVENTID_SUPPORT']='STD_ON'
        
    if no_of_event_id != []:
        CanVnim_Tx_MaxNum_TaskIdsForSignal = max(no_of_event_id)#no of event id for a signal
    else:
        CanVnim_Tx_MaxNum_TaskIdsForSignal = 0


    if CanVnim_Tx_MaxNum_TaskIdsForSignal > 1:
        vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXEVENTID_SUPPORT'] = 'STD_ON'

    #print CanVnim_Tx_MaxNum_TaskIdsForSignal
    
    #print no_of_event_id
    #print CanVnim_Tx_MaxNum_TaskIdsForSignal
    
    if CanVnim_Tx_MaxNum_TaskIdsForSignal >1 :#multiple event id support for a single signal
        vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS']= 'STD_ON'
    
    if vnim_generic_cfg['CANVNIM_TX_TOUTINDICATION_API']== "STD_ON":#Tx timeout id enabled 
        vnim_generic_cfg['CANVNIM_EVENTID_DIFFERFROM_ERRORID'] = 'STD_ON'
     
        
    
    #print tx_ind_msg_count
    #print CanVnim_Tx_MaxNum_TaskIdsForSignal
    
    #print tx_conf_id_unique
    temp_count= 0
    #task id    
    print '''/**********************************************************************************************************************
  CanVnim_TxEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_TxEventTaskIdTable
  brief  Contains all task ids for application notification related to transmit messages 
  details
  Element                      Description
  CanVnim_TxAppNotifyTaskId    Tx Event Task Id
*/
CanVnim_TxEventTaskIdType const CanVnim_TxEventTaskIdTable[CanVnim_Tx_Num_TaskIds] = 
{
  /* Index            TxAppNotifyTaskId   */'''
    if len(tx_conf_id_unique)!=0:
        for idx in tx_conf_id_unique:
            print '/*     '+str(temp_count)+'*/     '+str(idx)+','
            temp_count+=1
    else:
        print '     /*0*/       0xFF'
    print '};'
    CanVnim_Tx_Num_TaskIds = temp_count
    #error ID Tx
    print '''/**********************************************************************************************************************
  CanVnim_TxErrEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_TxErrEventTaskIdTable
  brief  Contains all task ids for application notification related to transmit message errors 
  details
  Element                      Description
  CanVnim_TxAppNotifyTaskId    Tx Event Task Id
*/
CanVnim_TxEventTaskIdType const CanVnim_TxErrEventTaskIdTable[CanVnim_Tx_Num_ErrTaskIds] = 
{
  /* Index            TxAppNotifyTaskId   */'''
    temp_count= 0
    if len(tx_err_id)!=0:
        for idx in tx_err_id:
            print '/*     '+str(temp_count)+' */ '+idx+','
            temp_count+=1
    else:
        print '     /*0*/       0xFF'
        
    print '};'
    print '\n'
    CanVnim_Tx_Num_ErrTaskIds = temp_count

    msg_content_info_tx=''
    frame_val_type=''
    #tx_table
    print '''
/**********************************************************************************************************************
  CanVnim_TxSigInfo
**********************************************************************************************************************/
'''
    print '''CanVnim_TxSigInfoType const CanVnim_TxSigInfo[CanVnim_Tx_Num_Signals] = {'''
    print '''    /* Index      ControllerId    InitValue          SendType   IsRequiredTxAckNotif     IsRequiredTxTOutNotif   */ '''
    sig_count_tx=0
    temp_msg_count=0
    sig_start_index=0
    
    alive_sig_count=0
    max_alive_cnt_tx=0
    for mes in il_sorted_mes_tx:
        sig_par=[]
        sorted_list=[]
        
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
        
        msg_content_info_tx+='      { /*     '+str(temp_msg_count)+ '*/              '+' '+str(sig_start_index)+' ,          '+str(len(mes['Sig_List']))
        
        
        if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
            alive_sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
            val_count=-1
            ver_count = -1
            
            for alive_signals in alive_sig_sorted:
                 
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':  
                    if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp'] == 'on'and vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_hold_no_of_events'] != 'Bit_Position':
                        if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_no_of_events'] == alive_signals['signal_name']:
                            val_count = alive_sig_count
                            
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp'] == 'on' and vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_hold_no_of_events']!= 'Bit_Position':
                    if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_1_no_of_events'] == alive_signals['signal_name']:
                            ver_count = alive_sig_count
                            
                alive_sig_count+=1
                
                
            frame_val_type+='\n     {'
            if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON': 
                
                if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp'] == 'on':
                    max_alive_cnt_tx+=1
                    frame_val_type+=' CANVNIM_YES'
                    if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_hold_no_of_events'] == 'Bit_Position':
                        
                        if 'BYTE' not in il_val_sup_macro:
                            il_val_sup_macro.append('BYTE')
                            
                        frame_val_type+=' ,          BYTE'
                        bit_pos = (vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_bit_Pos'])
                        int_rep = 0
                        try:
                            int(bit_pos)
                            int_rep=1
                        except ValueError:
                            int_rep=0
                        
                        if int_rep == 1:
                            temp_val=0xffff
                            bit_pos=int(bit_pos)
                            bit_pos<<8
                            temp_val=bit_pos&(0xff00)
                            bit_value = int(vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_bit_len_no_of_events'])
                            bit_value = 0x00ff & bit_value
                            
                            temp_val=temp_val|bit_value
                            
                            frame_val_type+=' ,          '+str(temp_val)
                       
                        else:
                            frame_val_type+=' ,          0xFFFFu'
                                     
                    else:
                        frame_val_type+=' ,          SIGNAL'
                        if 'SIGNAL' not in il_val_sup_macro:
                            il_val_sup_macro.append('SIGNAL')
                        if val_count != -1:
                            frame_val_type+=' ,          '+str(val_count)+'u'
                        else:
                            frame_val_type+=' ,          '+'0xFFFFu'
                else:
                    frame_val_type+=' CANVNIM_NO'
                    frame_val_type+=' ,          NO_ASSIGN'
                    frame_val_type+=' ,          0xFFFFu'
                    
            
                
            if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp'] == 'on':
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON': 
                    frame_val_type+=' ,          CANVNIM_YES'
                else:
                    frame_val_type+='          CANVNIM_YES'
                frame_val_type+=' ,          '+vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events']
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events'] not in il_hash_macro_cnt:
                    il_hash_macro_cnt.append(vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events'])
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_hold_no_of_events'] == 'Bit_Position':
                    frame_val_type+=' ,          BYTE'
                    
                    if 'BYTE' not in il_val_sup_macro:
                            il_val_sup_macro.append('BYTE')
                            
                    bit_pos = (vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_bit_Pos'])
                    int_rep = 0
                    try:
                        int(bit_pos)
                        int_rep=1
                    except ValueError:
                        int_rep=0
                    
                    if int_rep == 1:
                        temp_val=0xffff
                        bit_pos=int(bit_pos)
                        bit_pos<<8
                        temp_val=bit_pos&(0xff00)
                        bit_value = int(vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_bit_len_no_of_events'])
                        bit_value = 0x00ff & bit_value
                        
                        temp_val=temp_val|bit_value
                        
                        frame_val_type+=' ,          '+str(temp_val)
                   
                    else:
                        frame_val_type+=' ,          0xFFFFu'
                   
                else:
                    frame_val_type+=' ,          SIGNAL'
                    if 'SIGNAL' not in il_val_sup_macro:
                            il_val_sup_macro.append('SIGNAL')
                    if ver_count != -1:
                        frame_val_type+=' ,          '+str(val_count)+'u'
                    else:
                        frame_val_type+=' ,          '+'0xFFFFu'
                    
               
            else:
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':
                    frame_val_type+=' ,          CANVNIM_NO'
                else:
                    frame_val_type+='          CANVNIM_NO'
                frame_val_type+=' ,          NONE'
                frame_val_type+=' ,          NO_ASSIGN'
                frame_val_type+=' ,          0xFFFFu'
                
            frame_val_type+='},'
            
        
        if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXEVENTID_SUPPORT'] == 'STD_ON':
           
            msg_content_info_tx+=',   '+str(len(tx_conf_id_1[temp_msg_count]))
            
        if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXERREVENTID_SUPPORT'] == 'STD_ON':
            msg_content_info_tx+=',   '+str(len(tx_err_id_msg[temp_msg_count]))
        else:
            
            if tx_err_id_msg[temp_msg_count]!=[]:
                msg_content_info_tx+=',   '+str(tx_err_id.index(tx_err_id_msg[temp_msg_count][0]))
                msg_content_info_tx+=',   '+tx_id_err_mask[temp_msg_count][0]
            else:
                msg_content_info_tx+=',   '+'0xFF'
                msg_content_info_tx+=',   '+'0xFF'
             
            
        
        if vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS'] == 'STD_ON':
            for val in range(2,CanVnim_Tx_MaxNum_TaskIdsForSignal+1):
                #print val
                if val ==2:
                    msg_content_info_tx+=',   '+str(len(tx_conf_id_2[temp_msg_count]))
                elif val == 3:
                    msg_content_info_tx+=',   '+str(len(tx_conf_id_3[temp_msg_count]))
                else:
                    pass
                
        msg_content_info_tx+='},'
       
        
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
        for signals in sig_sorted:
            temp_str=''
            ind_tx = "CANVNIM_NO"
            timeout_tx = "CANVNIM_NO"
            if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf'] == 'on':
                             ind_tx = "CANVNIM_YES"

            if  vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout'] == 'on':
                              timeout_tx="CANVNIM_YES"

            temp_str+='     { /*     '+str(sig_count_tx)+' */      0,      '+vnim_cfg_data[str(signals['signal_name'])+'_init_value']
            
            if vnim_generic_cfg['CANVNIM_EVENT_INACTIVE_SUPPORT'] == "STD_ON ":
                temp_str+=',   '+'0xFF'
            
            if 'GenSigSendType' in signals:
                
                sig_send=['Cyclic','OnWrite','OnWriteWithRepetition','OnChange','OnChangeWithRepetition','IfActive','IfActiveWithRepetition','NoSigSendType']
                try:
                    if int(signals['GenSigSendType']) < len(sig_send):
                        temp_str += ',     '+sig_send[int(signals['GenSigSendType'])]
                    else:
                        temp_str += ',     '+'SIG_NOSENDTYPE'
                except:
                    temp_str += ',     '+'SIG_NOSENDTYPE'
            else:
                temp_str += ',     '+'SIG_NOSENDTYPE'
                
            temp_str+=',          '+ind_tx+',     '+timeout_tx

            if vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_no_of_events'] !='':
                i=1
                if ind_tx == "CANVNIM_YES":
                    temp_str+=',   '+ str(tx_conf_id_unique.index(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)]))
                    temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_MASK_'+str(i)]
                else:
                    temp_str+=',   '+'0xFF'
                    temp_str+=',     0xFF'
            #temp_str+=',    '
            
            if vnim_generic_cfg['CANVNIM_TX_TOUTINDICATION_API'] == 'STD_ON':
                if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_TXERREVENTID_SUPPORT'] == 'STD_ON':
                    if vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_no_of_events'] !='':
                        i=1
                        if timeout_tx == "CANVNIM_YES":
                            #print tx_conf_id_unique
                            temp_str+=',     '+ str(tx_err_id.index(vnim_cfg_data[(str(signals['signal_name'])+'_tx_timeout_ID_'+str(i))]))
                            temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_tx_timeout_MASK_'+str(i)]
                        else:
                            temp_str+=',     '+'0xFF'
                            temp_str+=',     0xFF'
                    else:
                        temp_str+=',     '+'0xFF'
                        temp_str+=',     '+',     0xFF'
                        
            
            if vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS'] == 'STD_ON':
                no_of_events_usr = int(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_no_of_events'])
                no_of_events_tot = CanVnim_Tx_MaxNum_TaskIdsForSignal
                
                #print no_of_events_usr,no_of_events_tot
               
                for i in range(2,no_of_events_tot+1):
                    if ind_tx == "CANVNIM_YES" and (i<=no_of_events_usr):
                        temp_str+= ',     '+str(tx_conf_id_unique.index(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)]))
                        temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_MASK_'+str(i)]
                    else:
                        temp_str+=',     '+'0xFF'
                        temp_str+=',     0xFF'


            temp_str+='},'
            sig_count_tx+=1
            sig_start_index+=1
            print temp_str
        msg_content_info_tx+='\n'
        temp_msg_count+=1
        
    print '};'

    print '\n'

    print '''/**********************************************************************************************************************
  CanVnim_NumOfContainedTxSignals
**********************************************************************************************************************/
CanVnim_TxMessageContentInfo const CanVnim_NumOfContainedTxSignals[CanVnim_Tx_Num_Messages] = 
{
      /* Index      SigStartIndex   SigCount   ErrEventId   ErrNotifyBit   */'''

    print msg_content_info_tx
    print '};\n'
    
    if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
      
        print '''/**********************************************************************************************************************
CanVnim_TxFrameValidationInfo
**********************************************************************************************************************/
/** 
    var    CanVnim_TxFrameValidationInfo
    brief  Structure describing the validation methods used for Tx Frames
*/
CanVnim_FrameValInfoType const CanVnim_TxFrameValidationInfo[CanVnim_Tx_Num_Messages] =
{'''
        print frame_val_type.rstrip(',')
        print '};\n'
    
    #rx Signal notification and error id
    rx_indication_id=[]
    rx_indication_id_unique=[]
    rx_invalid_id_unique=[]
    rx_timeout_id_unique=[]
    rx_error_id=[]
    rx_ind_msg_count=[]
    rx_ind_error_count=[]
    rx_indication_id_unique_1=[]
    rx_indication_bit_mask_1=[]
    rx_indication_id_unique_2=[]
    rx_indication_bit_mask_2=[]
    rx_invalid_id_unique_1=[]
    rx_invalid_bit_mask_1=[]
    rx_timeout_id_unique_1=[]
    rx_timeout_bit_mask_1=[]

    no_of_event_id_rx=[]
    
    vnim_generic_cfg['CANVNIM_RX_INVINDICATION_API'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_EVENTID_DIFFERFROM_ERRORID']= 'STD_ON'
    vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXERREVENTID_SUPPORT'] = 'STD_OFF'
    vnim_generic_cfg['CANVNIM_RX_TOUTINDICATION_API'] = 'STD_ON'

                
    for mes in il_sorted_mes_rx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
        temp_ind_id_cnt=0
        temp_err_id_cnt=0

        temp_rx_indication_id_unique_1=[]
        temp_rx_indication_id_unique_2=[]
        
        temp_rx_invalid_id_unique_1=[]
        temp_rx_timeout_id_unique_1=[]

        temp_rx_indication_bit_mask_1=[]
        temp_rx_indication_bit_mask_2=[]
        temp_rx_invalid_bit_mask_1=[]
        temp_rx_timeout_bit_mask_1=[]
        temp_rx_timeout_mask = []

        rx_ind_msg_count=[]
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
        
        if vnim_mes_cfg_data[str(mes['Msg_name'])+'_validation_supp'] == 'on':
            vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']="STD_ON"
         
        if vnim_mes_cfg_data[str(mes['Msg_name'])+'_alive_counter_supp'] == 'on':
            vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT']="STD_ON"  
            vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']="STD_ON"
        
        for signals in sig_sorted:
            ind_rx = "CANVNIM_NO"
            timeout_rx = "CANVNIM_NO"
            invalid_rx="CANVNIM_NO"
            #indication ID
            
            if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'] !='' and vnim_cfg_data[str(signals['signal_name'])+'_rx_indication'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'])
                no_of_event_id_rx.append(no_of_events)
                
                for i in range(1,no_of_events+1):
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)] not in rx_indication_id_unique:
                        #print str(signals['signal_name'])+'_rx_indication_ID_'+str(i)
                        rx_indication_id_unique.append( vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)])
                        temp_ind_id_cnt+=1
                        
                for i in range(1,2):
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)] not in temp_rx_indication_id_unique_1:
                        temp_rx_indication_id_unique_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)])
                        temp_rx_indication_bit_mask_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_MASK_'+str(i)])
                        
                    #tx_conf_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                    #tx_id_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_MASK_'+str(i)])


            if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'] !='' and vnim_cfg_data[str(signals['signal_name'])+'_rx_indication'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'])
                
                for i in range(2,no_of_events+1):
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)] not in temp_rx_indication_id_unique_2 :
                        temp_rx_indication_id_unique_2.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)])
                        temp_rx_indication_bit_mask_2.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_MASK_'+str(i)])

                        
            if vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_no_of_events'] !='' and vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_no_of_events'])
                
                vnim_generic_cfg['CANVNIM_RX_INVINDICATION_API'] = 'STD_ON'
                vnim_generic_cfg['CANVNIM_EVENTID_DIFFERFROM_ERRORID']= 'STD_ON'
                
                for i in range(1,no_of_events+1):
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)] not in rx_invalid_id_unique:
                        rx_invalid_id_unique.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)])
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)] not in rx_error_id:
                        temp_err_id_cnt+=1
                        rx_error_id.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)])
                        
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)] not in temp_rx_invalid_id_unique_1:
                        temp_rx_invalid_id_unique_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)])
                        temp_rx_invalid_bit_mask_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_MASK_'+str(i)])
                    #tx_conf_id.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_ID_'+str(i)])
                    #tx_id_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_tx_conf_MASK_'+str(i)])

            if vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_no_of_events'] !='' and vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout'] == 'on':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_no_of_events'])
                
                vnim_generic_cfg['CANVNIM_RX_TOUTINDICATION_API'] = 'STD_ON'
                
                for i in range(1,no_of_events+1):
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)] not in rx_timeout_id_unique:
                        rx_timeout_id_unique.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)])
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)] not in rx_error_id:
                        temp_err_id_cnt+=1
                        rx_error_id.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)])
                    if vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)] not in temp_rx_timeout_id_unique_1:
                        temp_rx_timeout_id_unique_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)])
                        temp_rx_timeout_bit_mask_1.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_MASK_'+str(i)])
                    temp_rx_timeout_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_MASK_'+str(i)])
                        

                    
                        #tx_conf_id.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)])
                    #tx_id_mask.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_MASK_'+str(i)])
            rx_ind_msg_count.append(temp_ind_id_cnt)
            
        rx_indication_id_unique_1.append(temp_rx_indication_id_unique_1)
        rx_indication_id_unique_2.append(temp_rx_indication_id_unique_2)
        
        rx_invalid_id_unique_1.append(temp_rx_invalid_id_unique_1)
        rx_timeout_id_unique_1.append(temp_rx_timeout_id_unique_1)
        
        check_mask = 0
        #print temp_rx_timeout_mask
        for x in temp_rx_timeout_mask:
            if x!= temp_rx_timeout_mask[0]:
                check_mask = 1
                break
            
            
        if len(temp_rx_timeout_id_unique_1) >1 or check_mask == 1:
            vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXERREVENTID_SUPPORT'] = 'STD_ON'
            
        rx_indication_bit_mask_1.append(temp_rx_indication_bit_mask_1)
        rx_indication_bit_mask_2.append(temp_rx_indication_bit_mask_2)
        
        rx_invalid_bit_mask_1.append(temp_rx_invalid_bit_mask_1)
        rx_timeout_bit_mask_1.append(temp_rx_timeout_bit_mask_1)
        
        rx_ind_msg_count.append(temp_ind_id_cnt)
        rx_ind_error_count.append(temp_err_id_cnt)

    if no_of_event_id_rx !=[]:
        CanVnim_Rx_MaxNum_TaskIdsForSignal=max(no_of_event_id_rx)
    else:
        CanVnim_Rx_MaxNum_TaskIdsForSignal = 0
    
    
    
    if CanVnim_Rx_MaxNum_TaskIdsForSignal >1:
        vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT'] = 'STD_ON'
     
    
    
    print '''/**********************************************************************************************************************
  CanVnim_RxEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_RxEventTaskIdTable
  brief  Contains all task ids for application notification related to receive messages 
  details
  Element                      Description
  CanVnim_RxAppNotifyTaskId    Rx Event Task Id
*/
CanVnim_RxEventTaskIdType const CanVnim_RxEventTaskIdTable[CanVnim_Rx_Num_TaskIds] = 
{
  /* Index          RxAppNotifyTaskId   */'''
    temp_count = 0
    if len(rx_indication_id_unique)!= 0:
        for idx in rx_indication_id_unique:
            print '/*     '+str(temp_count)+' */ '+idx+','
            temp_count+=1
    else:
        print '     /*0*/       0xFF'
        
    print '};'
    CanVnim_Rx_Num_TaskIds = temp_count
    print '\n'
    print '''/**********************************************************************************************************************
  CanVnim_RxErrEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_RxErrEventTaskIdTable
  brief  Contains all task ids for application notification related to receive message errors 
  details
  Element                      Description
  CanVnim_RxAppNotifyTaskId    Rx Event Task Id
*/
CanVnim_RxEventTaskIdType const CanVnim_RxErrEventTaskIdTable[CanVnim_Rx_Num_ErrTaskIds] = 
{
  /* Index          RxAppNotifyTaskId   */'''
    temp_count = 0
    if len(rx_error_id) != 0:
        for idx in rx_error_id:
            print '/*     '+str(temp_count)+' */ '+idx+','
            temp_count+=1
    else:
        print '     /*0*/       0xFF'
    print '};'
    print '\n'
    CanVnim_Rx_Num_ErrTaskIds=temp_count
    print '''/**********************************************************************************************************************
  CanVnim_RxAccessInfo
**********************************************************************************************************************/
'''
    print '''CanVnim_RxAccessInfoType const CanVnim_RxAccessInfo[CanVnim_Rx_Num_Signals] = {
    /* Index      ControllerId   InitValue   InitCondition   InvalidValue         SendType   IsRequiredRxAckNotif   IsRequiredRxTOutNotif   IsRequiredRxInvNotif   EventId0   NotifyBit                     */'''

    #rx signal table
    temp_sig_count_rx=0
    sig_start_index=0
    temp_msg_count=0
    msg_content_info=''

    #print vnim_generic_cfg['CANVNIM_RX_INVINDICATION_API']
    #print vnim_generic_cfg['CANVNIM_EVENTID_DIFFERFROM_ERRORID']
    #print vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT'] 
    #print vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXERREVENTID_SUPPORT']
    alive_sig_count=0
    frame_val_type = ''
    for mes in il_sorted_mes_rx:
        sig_par=[]
        
        sorted_list=[]
        no_of_even_id1=0
        no_of_even_id2=0
        no_of_error_id=0    
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''


        '''{ /*     0 */              0,	       0x0,           0x08,          0xFF,  SIG_NOSENDTYPE,		      CANVNIM_YES,			 CANVNIM_YES,		    CANVNIM_YES,          0,          2  }  /* [DimmingLvl] */
};'''
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        msg_content_info+='     { /*     '+str(temp_msg_count)+ '*/        '+str(sig_start_index)+',     '+str(len(mes['Sig_List']))
        #print rx_indication_id_unique_2[temp_msg_count]
        
        if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
            alive_sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
            val_count=-1
            ver_count = -1
            
            for alive_signals in alive_sig_sorted:
                 
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':  
                    if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp'] == 'on'and vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_hold_no_of_events'] != 'Bit_Position':
                        if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_no_of_events'] == alive_signals['signal_name']:
                            val_count = alive_sig_count
                            
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp'] == 'on' and vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_hold_no_of_events']!= 'Bit_Position':
                    if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_1_no_of_events'] == alive_signals['signal_name']:
                            ver_count = alive_sig_count
                            
                alive_sig_count+=1
                
                
            frame_val_type+='\n     {'
            if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':          
                if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp'] == 'on':
                    frame_val_type+=' CANVNIM_YES'
                    max_alive_cnt_rx+=1
                    if vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_hold_no_of_events'] == 'Bit_Position':
                        frame_val_type+=' ,          BYTE'
                        if 'BYTE' not in il_val_sup_macro:
                            il_val_sup_macro.append('BYTE')
                        bit_pos = (vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_bit_Pos'])
                        int_rep = 0
                        try:
                            int(bit_pos)
                            int_rep=1
                        except ValueError:
                            int_rep=0
                        
                        if int_rep == 1:
                            temp_val=0xffff
                            bit_pos=int(bit_pos)
                            bit_pos<<8
                            temp_val=bit_pos&(0xff00)
                            bit_value = int(vnim_mes_cfg_data[mes['Msg_name']+'_alive_counter_supp_bit_len_no_of_events'])
                            bit_value = 0x00ff & bit_value
                            
                            temp_val=temp_val|bit_value
                            
                            frame_val_type+=' ,          '+str(temp_val)
                       
                        else:
                            frame_val_type+=' ,          0xFFFFu'
                                     
                    else:
                        frame_val_type+=' ,          SIGNAL'
                        if 'SIGNAL' not in il_val_sup_macro:
                            il_val_sup_macro.append('SIGNAL')
                        if val_count != -1:
                            frame_val_type+=' ,          '+str(val_count)+'u'
                        else:
                            frame_val_type+=' ,          '+'0xFFFFu'
                else:
                    frame_val_type+='CANVNIM_NO'
                    frame_val_type+=' ,          NO_ASSIGN'
                    frame_val_type+=' ,          0xFFFFu'
                    
            
                
            if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp'] == 'on':
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':
                    frame_val_type+=' ,          CANVNIM_YES'
                else:
                    frame_val_type+='CANVNIM_YES'
                    
                frame_val_type+=' ,          '+vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events']
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events'] not in il_hash_macro_cnt:
                    il_hash_macro_cnt.append(vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_0_no_of_events'])
                if vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_hold_no_of_events'] == 'Bit_Position':
                    frame_val_type+=' ,          BYTE'
                    if 'BYTE' not in il_val_sup_macro:
                            il_val_sup_macro.append('BYTE')
                    bit_pos = (vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_bit_Pos'])
                    int_rep = 0
                    try:
                        int(bit_pos)
                        int_rep=1
                    except ValueError:
                        int_rep=0
                    
                    if int_rep == 1:
                        temp_val=0xffff
                        bit_pos=int(bit_pos)
                        bit_pos<<8
                        temp_val=bit_pos&(0xff00)
                        bit_value = int(vnim_mes_cfg_data[mes['Msg_name']+'_validation_supp_bit_len_no_of_events'])
                        bit_value = 0x00ff & bit_value
                        
                        temp_val=temp_val|bit_value
                        
                        frame_val_type+=' ,          '+str(temp_val)
                   
                    else:
                        frame_val_type+=' ,          0xFFFFu'
                   
                else:
                    frame_val_type+=' ,          SIGNAL'
                    if 'SIGNAL' not in il_val_sup_macro:
                            il_val_sup_macro.append('SIGNAL')
                    if ver_count != -1:
                        frame_val_type+=' ,          '+str(val_count)+'u'
                    else:
                        frame_val_type+=' ,          '+'0xFFFFu'
                    
               
            else:
                if vnim_generic_cfg['CANVNIM_ALIVECOUNTER_SUPPORT'] =='STD_ON':
                    frame_val_type+=' ,          CANVNIM_NO'
                else:
                    frame_val_type+=' CANVNIM_NO'
                frame_val_type+=' ,          NONE'
                frame_val_type+=' ,          NO_ASSIGN'
                frame_val_type+=' ,          0xFFFFu'
            frame_val_type+='},'
            
        for signals in sig_sorted:
            #print signals
            temp_str=''
            ind_rx = "CANVNIM_NO"
            timeout_rx = "CANVNIM_NO"
            invalid_rx="CANVNIM_NO" 
            if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication'] == 'on':
                             ind_rx = "CANVNIM_YES"

            if  vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid'] == 'on':
                              invalid_rx="CANVNIM_YES"

            if  vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout'] == 'on':
                              timeout_rx="CANVNIM_YES"
            temp_str += '   { /*     '+str(temp_sig_count_rx)+'  */         0,	       0x0'

            if vnim_generic_cfg['CANVNIM_SEPARATE_INIT_CONDITIONS'] == 'STD_ON': 
                temp_str += ',     '+'0x00'

            if vnim_cfg_data[str(signals['signal_name'])+'_invalid_value']!='':
                temp_str += ',     '+vnim_cfg_data[str(signals['signal_name'])+'_invalid_value']
            else:
                temp_str += ',     '+'0xFFu'
                
            if 'GenSigSendType' in signals:
                
                sig_send=['Cyclic','OnWrite','OnWriteWithRepetition','OnChange','OnChangeWithRepetition','IfActive','IfActiveWithRepetition','NoSigSendType']
                try:            
                    if int(signals['GenSigSendType']) < len(sig_send):
                        temp_str += ',     '+sig_send[int(signals['GenSigSendType'])]
                    else:
                        temp_str += ',     '+'SIG_NOSENDTYPE'
                except:
                    temp_str += ',     '+'SIG_NOSENDTYPE'
                    
            else:
                temp_str += ',     '+'SIG_NOSENDTYPE'
                
            temp_str+=',     '+ind_rx+',         '+timeout_rx+',         '+invalid_rx

            if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'] !='':
                no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'])
                for i in range(1,2):
                            #no_of_even_id1+=1
                            if ind_rx == "CANVNIM_YES":
                                temp_str+= ',     '+str(rx_indication_id_unique.index(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)]))
                                temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_MASK_'+str(i)]
                            else:
                                temp_str+=',     '+'0xFF'
                                temp_str+=',     '+'0xFF'
                            

            if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXERREVENTID_SUPPORT'] == 'STD_ON':
                if vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_no_of_events'] !='':
                    no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_no_of_events'])
                    for i in range(1,no_of_events+1):
                        if timeout_rx == "CANVNIM_YES":
                            temp_str+=',     '+ str(rx_error_id.index(vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_ID_'+str(i)]))
                            temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_rx_timeout_MASK_'+str(i)]
                            
                        else:
                            temp_str+=',     '+'0xFF'
                            temp_str+=',     '+'0xFF'
                        
                            
                            #print temp_rx_timeout_id_unique_1
                            
                                
            if vnim_generic_cfg['CANVNIM_RX_INVINDICATION_API'] == 'STD_ON':
                if vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_no_of_events'] !='':
                    no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_no_of_events'])
                    for i in range(1,no_of_events+1):    
                        if invalid_rx == "CANVNIM_YES":
                            temp_str+= ',     '+str(rx_error_id.index(vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_ID_'+str(i)]))
                            temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_rx_invalid_MASK_'+str(i)]
                        else:
                            temp_str+=',     '+'0xFF'
                            temp_str+=',     '+'0xFF'
                                
                        

            if vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS'] == 'STD_ON':

                if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'] !='':
                    no_of_events = int(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_no_of_events'])
                    
                    for i in range(2,CanVnim_Rx_MaxNum_TaskIdsForSignal+1):
                            #no_of_even_id1+=1
                            if ind_rx == "CANVNIM_YES" and (i<=no_of_events):
                                temp_str+= ',     '+str(rx_indication_id_unique.index(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)]))
                                temp_str+=',     '+vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_MASK_'+str(i)]+','
                            else:
                                temp_str+=',     '+'0xFF'
                                temp_str+=',     '+'0xFF'
                            '''if vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)] not in temp_rx_indication_id_unique_2:
                                temp_rx_indication_id_unique_2.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_ID_'+str(i)])
                                temp_rx_indication_bit_mask_2.append(vnim_cfg_data[str(signals['signal_name'])+'_rx_indication_MASK_'+str(i)])'''
            temp_str+='},'
            print temp_str
            temp_sig_count_rx+=1
            sig_start_index+=1
            
        
        if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT'] == 'STD_ON' :
            msg_content_info+=',     '+str(len(rx_indication_id_unique_1[temp_msg_count]))
        #print vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS']
        
        if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXERREVENTID_SUPPORT'] == 'STD_ON':
            msg_content_info+=',     '+str(len(rx_timeout_id_unique_1[temp_msg_count]))
           
        else:
            #print rx_timeout_bit_mask_1
            if rx_error_id != []:
                if rx_timeout_id_unique_1[temp_msg_count]!=[]:
                    msg_content_info+=',     '+str(rx_error_id.index(str(rx_timeout_id_unique_1[temp_msg_count][0])))
                    msg_content_info+=',     '+str(rx_timeout_bit_mask_1[temp_msg_count][0])
                else:
                    msg_content_info+=',     '+'0xFF'
                    msg_content_info+=',     '+'0xFF'
            else:
                msg_content_info+=',     '+'0xFF'
                msg_content_info+=',     '+'0xFF'

        if vnim_generic_cfg['CANVNIM_RX_INVINDICATION_API'] == 'STD_ON':
            if vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT'] == 'STD_ON':
                msg_content_info+=',     '+str(len(rx_invalid_id_unique_1[temp_msg_count]))
                
        if vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS'] == 'STD_ON':
            #print rx_indication_id_unique_2
            if CanVnim_Rx_MaxNum_TaskIdsForSignal>1:
                for i in range(2,CanVnim_Rx_MaxNum_TaskIdsForSignal+1):
                    if i==2:
                        msg_content_info+=',     '+str(len((rx_indication_id_unique_2[temp_msg_count])))
                    '''if i==3:
                        msg_content_info+=',     '+str(len((rx_indication_id_unique_3)))'''
            
        msg_content_info.rstrip(',')
        msg_content_info+='        },\n'
        #print vnim_generic_cfg['CANVNIM_MESSAGE_MULT_RXEVENTID_SUPPORT']
        #print vnim_generic_cfg['CANVNIM_NEEDTOSUPPORT_MULTEVENTIDS']
        temp_msg_count+=1
    print '};'
    print '\n'

    
    #print msg_content_info
    #print vnim_generic_cfg
    
    print '''/**********************************************************************************************************************
  CanVnim_NumOfContainedRxSignals
**********************************************************************************************************************/
CanVnim_RxMessageContentInfo const CanVnim_NumOfContainedRxSignals[CanVnim_Rx_Num_Messages] =
{
     /* Index      SigStartIndex   SigCount   ErrEventId   ErrNotifyIDCount   */'''
    print msg_content_info
    print '};'
    
    if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
        print '''/**********************************************************************************************************************
  CanVnim_RxFrameVerificationInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_RxFrameVerificationInfo
  brief  Structure describing the validation methods used for Rx Frames
*/
CanVnim_FrameValInfoType const CanVnim_RxFrameVerificationInfo[CanVnim_Rx_Num_Messages] =
{
'''
        print frame_val_type.rstrip(',')
        print '};\n'

    
    if il_hash_macro_cnt!=[]:
        if len(il_hash_macro_cnt) >1:
            vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']='MIXED_TYPE'
        else:
            vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']=il_hash_macro_cnt[0]
    else:
        vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']='NONE'
                            
    if il_val_sup_macro!=[]:
        if len(il_val_sup_macro) >1:
            vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']='MIXED'
        else:
            vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']=il_val_sup_macro[0]
    else:
        vnim_generic_cfg['CANVNIM_IL_VALIDATION_SUPPORT']='NO_ASSIGN'
                            
    print '''
/**********************************************************************************************************************
  CanVnim_Rx_Signals
**********************************************************************************************************************/
'''
    print '''/* Receive messages */
CAN_VNIM_SIGNAL const
CanVnim_Rx_Signals[ CanVnim_Rx_Num_Signals ] =
{ '''
    temp_count = 0
    print '/*  CAN Frame,   Num Bytes,  MS Byte,  MS Bit,  LS Byte,  LS Bit */'
    for i in shadow_rx_buffer:
        print '     { '+str(temp_count)+',    '+i
    print '};\n'
    
    #has to be implemented later
    print '''
#if (CANVNIM_RX_INDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkRxAckFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxAckFuncPtr
  brief  Function pointer table containing configured Rx Indication notifications for signals and signal groups.*/

CanVnimCbkDefRxAckType const CanVnim_CbkRxAckFuncPtr = KernelPostEvent;

/*CanVnimCbkImRxAckType const CanVnim_CbkImCpy_RxAckFuncPtr = KernelSendMessage;*/

#endif


#if (CANVNIM_RX_TOUTINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkRxTOutFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxTOutFuncPtr
  brief  Function pointer table containing configured Rx timeout notifications for signals and signal groups.
*/ 
CanVnimCbkRxTOutType const CanVnim_CbkRxTOutFuncPtr = KernelPostEvent;
#endif


#if (CANVNIM_RX_INVINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkRxInvFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxInvFuncPtr
  brief  Function pointer table containing configured Rx Indication notifications for signals and signal groups.*/

CanVnimCbkInvType const CanVnim_CbkRxInvFuncPtr = KernelPostEvent;

#endif


#if (CANVNIM_TX_ACKINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkTxAckFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkTxAckFuncPtr
  brief  Function pointer table containing configured Tx Confirmation notifications for signals and signal groups.
*/ 
CanVnimCbkTxAckImType const CanVnim_CbkTxAckFuncPtr = KernelPostEvent;
#endif


#if (CANVNIM_TX_TOUTINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkTxTOutFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkTxTOutFuncPtr
  brief  Function pointer table containing configured Tx Timeout notifications for signals and signal groups
*/
CanVnimCbkTxTOutType const CanVnim_CbkTxTOutFuncPtr = KernelPostEvent;
#endif


/
/**********************************************************************************************************************
  CanVnim_CbkCommNotifyPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkCommNotifyPtr
  brief  Function pointer table containing configured Comm related notification function to application
*/
CanVnimCbkCommNotifyType const CanVnim_CbkCommNotifyPtr = KernelPostEvent;

'''

    print '''
/**********************************************************************************************************************
  CanVnim_PduGrpVector
**********************************************************************************************************************/
/** 
  var    CanVnim_PduGrpVector
  brief  Contains an I-PDU-Group vector for each I-PDU, mapping the I-PDU to the corresponding I-PDU-Groups.
  */ 
CanVnim_PduGrpVectorType const CanVnim_PduGrpVector[CanVnim_Num_Of_PduGroups] = {
  /* Index    PduGrpVector   */
  /*     0 */        0x02,
  /*     1 */        0x01
};


/**********************************************************************************************************************
  CanVnim_TxPduGrpInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_TxPduGrpInfo
  brief  Contains all I-PDU-Group relevant information for Tx I-PDUs.
  details
  Element                 Description
  ControllerId            ControllerId of the Pdu group
  PduGrpVectorStartIdx    the start index of the 0:n relation pointing to CanVnim_PduGrpVector
*/ 
CanVnim_TxPduGrpInfoType const CanVnim_TxPduGrpInfo[CanVnim_Tx_Num_Messages] = {
    /* Index    ControllerId    PduGrpVectorStartIdx */
  { /*     0 */           0U,                     0U  }
};

/**********************************************************************************************************************
  CanVnim_RxPduGrpInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_RxPduGrpInfo
  brief  Contains all I-PDU-Group relevant information for Rx I-PDUs.
  details
  Element                 Description
  ControllerId            ControllerId of the Pdu group
  PduGrpVectorStartIdx    the start index of the 0:n relation pointing to CanVnim_PduGrpVector
*/ 
CanVnim_RxPduGrpInfoType const CanVnim_RxPduGrpInfo[CanVnim_Rx_Num_Messages] = {
    /* Index    ControllerId    PduGrpVectorStartIdx */
  { /*     0 */           0U,                     1U  }
};
'''

    print '''/**********************************************************************************************************************
  CanVnim_DiagFuncHandlerTable
**********************************************************************************************************************/
/** 
  var    CanVnim_DiagFuncHandlerTable
  brief  Contains all function handlers for diagnostic reception and for post handling services
*/\n
'''
    print '''CanVnim_DiagFuncHandlerType const CanVnim_DiagFuncHandlerTable[CANVNIM_DIAG_NUM_SERVICES] = {'''
    
    diag_cfg_file = open(vnim_data_dir+"CanDiagServiceConfiguration.data",'r')
    diag_service_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()
    
    
    services=['StartDiagnosticSession','EcuReset','SecurityAccess','CommunicationControl','TesterPresent',\
              'SecuredDataTransmission','ControlDTCSetting','ResponseOnEvent','ReadDataByIdentifier','ReadMemoryByAddress',\
              'WriteDataByIdentifier','WriteMemoryByAddress','ReadDataByPeriodicIdentifier','DynamicallyDefineIdentifier',\
              'ClearDiagnosticInformation','ReadDTCInformation','InputOutputControlByIdentifier','RoutineControl','AccessTimingParameter','LinkControl','ReadScalingDataByIdentifier']
    temp_cnt = 0
    for idx in services:
        if idx+'_enable' in diag_service_data:
            if diag_service_data[idx+'_enable'] == 'on':
                print '     { /* '+str(temp_cnt)+' */    '+diag_service_data[idx+'_main_handler']+',     ',
                temp_cnt+=1
                if diag_service_data[idx+'_post_handler_en'] == 'on':
                    if diag_service_data[idx+'_post_handler'] != " " and diag_service_data[idx+'_post_handler'] != "":
                        print diag_service_data[idx+'_post_handler'],
                    else:
                        print 'NULL',
                else:
                    print 'NULL',
                    
                print '} ,'
    print '};'
                    
    diag_cfg_file = open(vnim_data_dir+"CanDiagSessionConfiguration.data",'r')
    diag_session_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()
    
    diag_cfg_file = open(vnim_data_dir+"CanDIAGConfiguration.data",'r')
    diag_cfg_data = json.loads(diag_cfg_file.read())
    diag_cfg_file.close()
    
    
    print '''/**********************************************************************************************************************
  CanVnim_DiagPreCondCheckFuncPtr
**********************************************************************************************************************/'''
#pre condition check callback function		
    
    if diag_cfg_data['CANDIAG_PRECONDITIONS_CHECK_SUPPORT'] != 'CANDIAG_ENABLE':
        if diag_session_data['diag_precondition']!='' and diag_session_data['diag_precondition']!=' ':
            print 'CanVnim_DiagPreConditionsChkFuncType const CanVnim_DiagPreCondCheckFuncPtr = '+diag_session_data['diag_precondition']+';'
        else:
            print 'CanVnim_DiagPreConditionsChkFuncType const CanVnim_DiagPreCondCheckFuncPtr = NULL;'
    else:
        print 'CanVnim_DiagPreConditionsChkFuncType const CanVnim_DiagPreCondCheckFuncPtr = NULL;'
    
    print '''/**********************************************************************************************************************
  CanVnim_DiagSessionTimeOutApplCB
**********************************************************************************************************************/'''
    if diag_session_data['diag_sessioncallback']!='' and diag_session_data['diag_sessioncallback']!=' ':
        print 'CanVnim_DiagSessionTOApplCBType const CanVnim_DiagSessionTimeOutApplCB = '+diag_session_data['diag_sessioncallback']+';'
    else:
        print 'CanVnim_DiagSessionTOApplCBType const CanVnim_DiagSessionTimeOutApplCB = NULL;'


    print footer

    #f.close()


def Vnim_par_h():
    global vnim_code_gen_dir,vnim_data_dir,il_generic_config,footer,max_alive_cnt_tx,max_alive_cnt_rx
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanVnim_Par_Cfg.h','w')
   
    sys.stdout = f
    global CanVnim_Rx_Num_TaskIds,CanVnim_Tx_Num_TaskIds,CanVnim_Rx_Num_ErrTaskIds,CanVnim_Tx_Num_ErrTaskIdsCanVnim_Tx_MaxNum_TaskIdsForSignal,CanVnim_Rx_MaxNum_TaskIdsForSignal
    global dbc
    il_msg_tx=dbc.get_msg_type(il_generic_config,'tx')
    il_msg_rx=dbc.get_msg_type(il_generic_config,'rx')

    #sorting messages by ascending order of id
    il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: int(x['id']))
    il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: int(x['id']))
    
    header='''#if !defined( CANVNIM_PAR_CFG_H )
#define CANVNIM_PAR_CFG_H

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
**  its rights under all copyright laws to protect this work as a published
**  work, when appropriate.  Those having access to this work may not copy it,
**  use it, modify it or disclose the information contained in it without the
**  written authorization of Visteon Corporation.
**
** =========================================================================*/

/* ===========================================================================
**
**  Name:           CanVnim_Par_Cfg.h
**
**  Description:    CAN VNIM configuration parameters for configured database
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
** =========================================================================*/'''
    print header,'\n'
    includes='''
/* ===========================================================================
**  I N C L U D E   F I L E S
** =========================================================================*/

# include "CanVnim_Cfg.h"
# include "CanVnim_SignalInterface.h"
# include "CanDiag_Uds_Par_Cfg.h"

'''
    print includes,'\n'
    junk='''/* ===========================================================================
**  M A C R O   D E F I N I T I O N S
** =========================================================================*/

/* DBC Tx & Rx CFG */
'''
    print junk,'\n'
   
    print '\n'
    print '#define CanVnim_Tx_MaxNum_TaskIdsForSignal '+str(CanVnim_Tx_MaxNum_TaskIdsForSignal)
    print '#define CanVnim_Rx_MaxNum_TaskIdsForSignal '+str(CanVnim_Rx_MaxNum_TaskIdsForSignal)
    print '\n'
    
    periodic_count=0
    temp_num_signals=0
    for mes in il_msg_tx:
        if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5']:
            periodic_count=periodic_count+1
        temp_num_signals+=len(mes['Sig_List'])
    
    #CanVnim_Tx_Num_Messages
    print '#define CanVnim_Tx_Num_Messages   ('+str(len(il_msg_tx))+')'
    print '\n'
    print '#define CanVnim_Tx_Num_Signals   ('+str(temp_num_signals)+')'
    #assuming no burst message
    print '#define CanVnim_Tx_Num_Burst_Periodic   (0)'
    print '\n'
    print '#define CanVnim_Tx_Num_Periodic         ('+str(periodic_count)+')'
    print '\n'
    

    print '\n'
    
    periodic_count=0
    periodic_sig_count=0
    no_signals=0
    for mes in il_msg_rx:
        if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5']:
            periodic_count=periodic_count+1
            periodic_sig_count+=len(mes['Sig_List'])
        no_signals+=len(mes['Sig_List'])
    #define Can_Channel0_Il_Rx_Num_Periodic         (1)
    print '#define CanVnim_Rx_Num_Messages        ('+str(len(il_msg_rx))+')'
    print '#define CanVnim_Rx_Num_Periodic_Messages        ('+str(periodic_count)+')'
    print '\n'
    print '#define CanVnim_Rx_Num_Signals       ('+str(no_signals)+')\n' 
    print '#define CanVnim_Rx_Num_Periodic_Signals ('+str(periodic_sig_count)+')\n'
    print '#define CanVnim_Rx_Num_Req_Frames       (0)\n'    

    config_not_from_tool=''' #define CanVnim_Tx_Num_Burst_Periodic               		  (0)'''


    print config_not_from_tool,'\n'
    config_not_from_tool='''#define CanVnim_Num_Of_PduGroups							  (2)

#define CANVNIM_MAX_IPDUGROUPVECTOR_BYTES                     (1)'''
    print config_not_from_tool,'\n'
    vnim_generic=open(vnim_data_dir+"CanVNIMConfiguration.data",'r')
    vnim_generic_cfg_1 = json.loads(vnim_generic.read())
    vnim_generic.close()
    
    print '#define CanVnim_AliveCounter_InvalidValue                         '+hex(int(vnim_generic_cfg_1['CanVnim_AliveCounter_InvalidValue']))
    print '#define CanVnim_AliveCounter_MinValue                             '+hex(int(vnim_generic_cfg_1['CanVnim_AliveCounter_MinValue']))
    print '#define CanVnim_AliveCounter_MaxValue                             '+hex(int(vnim_generic_cfg_1['CanVnim_AliveCounter_MaxValue']))

    print '#define CanVnim_RxNumOfAliveCntrMessages       '+str(max_alive_cnt_rx)
    print '#define CanVnim_TxNumOfAliveCntrMessages        '+str(max_alive_cnt_tx)

    print ''' /* Event Definitions */
/* CAN Channel Busoff Event Mapping - can_comm_notify_KSEvtTskID */
#define EVENT_CAN_NOTIFY_EVENTID                              (can_comm_notify_KSEvtTskID)
#define EVENT_CAN_ERROR_BUSOFF                                (BIT2)
#define EVENT_CAN_SLEEP_ENTRY                                 (BIT3)
#define EVENT_CAN_WAKEUP_EVENT                                (BIT4)
#define CAN_BUSOFF_RECOVERY_DELAY                              (100)'''

    print config_not_from_tool,'\n'

    #Group handles
    print '''  /*Handle IDs active in all predefined variants (the application has not to take the active variant into account) */
/*      Symbolic Name                                  Value   Active in predefined variant(s) */
#define CanVnimConf_IPduGroup_DDM_CAN_Rx                       1
#define CanVnimConf_IPduGroup_DDM_CAN_Tx                       0'''
    
    print '\n'
    #Tx message Handles
    print '''/* Handle IDs of handle space CanVnimTxSig [Tx Signals] */
/*      Symbolic Name                                  Value   Active in predefined variant(s) */'''

    temp_sig_count=0
    for mes in il_sorted_mes_tx:
        sig_par=[]
        
        sorted_list=[]
        no_of_even_id1=0
        no_of_even_id2=0
        no_of_error_id=0    
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))

        for signals in sig_sorted:
            ##define CanVnimTxHndlCh0_ApplVers_Major                        0
            print '#define CanVnimTxHndlCh0_'+signals['signal_name']+' '*(60-len('CanVnimTxHndlCh0_'+signals['signal_name']))+str(temp_sig_count)
            temp_sig_count+=1

    print '\n'

    #Rx message handles
    print '''/* Handle IDs of handle space CanVnimRxSig [Rx Signals] */
/*      Symbolic Name                                  Value   Active in predefined variant(s) */'''
    temp_sig_count=0
    for mes in il_sorted_mes_rx:
        sig_par=[]
        
        sorted_list=[]
        no_of_even_id1=0
        no_of_even_id2=0
        no_of_error_id=0    
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])
        '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))

        for signals in sig_sorted:
            ##define CanVnimTxHndlCh0_ApplVers_Major                        0
            print '#define CanVnimRxHndlCh0_'+signals['signal_name']+' '*(60-len('CanVnimRxHndlCh0_'+signals['signal_name']))+str(temp_sig_count)
            temp_sig_count+=1

    print '\n'

    #event IDs
    print '''/* Event Task Id Definitions */'''
    if CanVnim_Rx_Num_TaskIds !=0:
        print '#define CanVnim_Rx_Num_TaskIds                                 '+str(CanVnim_Rx_Num_TaskIds)
    else:
       print '#define CanVnim_Rx_Num_TaskIds                                 1'
    
    if CanVnim_Tx_Num_TaskIds!=0:
        print '#define CanVnim_Tx_Num_TaskIds                                 '+str(CanVnim_Tx_Num_TaskIds)
    else:
        print '#define CanVnim_Tx_Num_TaskIds                                 1'
        
    if CanVnim_Rx_Num_ErrTaskIds!=0:
        print '#define CanVnim_Rx_Num_ErrTaskIds                              '+str(CanVnim_Rx_Num_ErrTaskIds)
    else:
        print '#define CanVnim_Rx_Num_ErrTaskIds                              1'
    
    if CanVnim_Tx_Num_ErrTaskIds !=0:
        print '#define CanVnim_Tx_Num_ErrTaskIds                              '+str(CanVnim_Tx_Num_ErrTaskIds)
    else:
        print '#define CanVnim_Tx_Num_ErrTaskIds                              1'
        

    
    print '''/* State Manager Related Definitions */'''
    print '#define CanVnim_MaxNumOfStateTransitions                            '+'3'
    if vnim_generic_cfg_1['CANVNIM_EVENT_QUEUE_SUPPORT'] == 'STD_ON':
        print '#define CANVNIM_SM_EVENT_QUEUE_SIZE                                 '+vnim_generic_cfg_1['CANVNIM_SM_EVENT_QUEUE_SIZE']
    
    if vnim_generic_cfg_1['CANVNIM_EVENT_DATA_SUPPORT'] == 'STD_ON':
        print '#define CANVNIM_SM_MAXEVENT_DATA_SIZE	                           '+vnim_generic_cfg_1['CANVNIM_EVENT_DATA_SUPPORT']

    print '''#define CANVNIM_DIAG_NUM_SERVICES                                   CANDIAG_NUM_SERVICES
'''
    print '# include "CanVnim_Defines.h"'
    junk='''/* ===========================================================================
** G L O B A L   C O N S T A N T   D E C L A R A T I O N S
** =========================================================================*/

extern CanVnim_TxSigInfoType const CanVnim_TxSigInfo[CanVnim_Tx_Num_Signals];

#if (CANVNIM_TX_ACKINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkTxAckFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkTxAckFuncPtr
  brief  Function pointer table containing configured Tx Confirmation notifications for signals and signal groups.
*/ 
extern CanVnimCbkTxAckImType const CanVnim_CbkTxAckFuncPtr;
#endif


#if (CANVNIM_TX_TOUTINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkTxTOutFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkTxTOutFuncPtr
  brief  Function pointer table containing configured Tx Timeout notifications for signals and signal groups
*/ 
extern CanVnimCbkTxTOutType const CanVnim_CbkTxTOutFuncPtr;
#endif


extern CanVnim_RxAccessInfoType const CanVnim_RxAccessInfo[CanVnim_Rx_Num_Signals];


#if (CANVNIM_RX_INDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkRxAckFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxAckFuncPtr
  brief  Function pointer table containing configured Rx indication notifications for signals and signal groups.
*/
   
extern CanVnimCbkDefRxAckType const CanVnim_CbkRxAckFuncPtr;

#endif


#if (CANVNIM_RX_TOUTINDICATION_API == STD_ON)
/**********************************************************************************************************************
  CanVnim_CbkRxTOutFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxTOutFuncPtr
  brief  Function pointer table containing configured Rx timeout notifications for signals and signal groups.}
*/ 

extern CanVnimCbkRxTOutType const CanVnim_CbkRxTOutFuncPtr;

#endif

/**********************************************************************************************************************
  CanVnim_CbkRxInvFuncPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkRxInvFuncPtr
  brief  Function pointer table containing configured Rx invalid notifications for signals and signal groups.
*/

#if (CANVNIM_RX_INVINDICATION_API == STD_ON)
extern CanVnimCbkInvType const CanVnim_CbkRxInvFuncPtr;
#endif

/**********************************************************************************************************************
  CanVnim_CbkCommNotifyPtr
**********************************************************************************************************************/
/** 
  var    CanVnim_CbkCommNotifyPtr
  brief  Function pointer table containing configured Comm related notification function to application
*/
extern CanVnimCbkCommNotifyType const CanVnim_CbkCommNotifyPtr;



/* Receive messages */
extern CAN_VNIM_SIGNAL const
CanVnim_Rx_Signals[ CanVnim_Rx_Num_Signals ];


/**********************************************************************************************************************
  CanVnim_NumOfContainedRxSignals
**********************************************************************************************************************/
/** 
  var    CanVnim_NumOfContainedRxSignals
  brief  Structure describing the starting signal handle and the number of signals contained in Rx messages
*/

extern CanVnim_RxMessageContentInfo const CanVnim_NumOfContainedRxSignals[CanVnim_Rx_Num_Messages];'''
    print junk
    
    if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
        print '''/**********************************************************************************************************************
  CanVnim_RxFrameVerificationInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_RxFrameVerificationInfo
  brief  Structure describing the validation methods used for Rx Frames
*/
extern CanVnim_FrameValInfoType const CanVnim_RxFrameVerificationInfo[CanVnim_Rx_Num_Messages];'''


    print '''
/**********************************************************************************************************************
  CanVnim_NumOfContainedTxSignals
**********************************************************************************************************************/
/** 
  var    CanVnim_NumOfContainedTxSignals
  brief  Structure describing the starting signal handle and the number of signals contained in Tx messages
*/


extern CanVnim_TxMessageContentInfo const CanVnim_NumOfContainedTxSignals[CanVnim_Tx_Num_Messages];'''
    if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API'] =="STD_ON":
        print '''
/**********************************************************************************************************************
  CanVnim_TxFrameValidationInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_TxFrameValidationInfo
  brief  Structure describing the validation methods used for Tx Frames
*/
extern CanVnim_FrameValInfoType const CanVnim_TxFrameValidationInfo[CanVnim_Tx_Num_Messages];

'''
    print '''
/**********************************************************************************************************************
  CanVnim_PduGrpVector
**********************************************************************************************************************/
/** 
  var    CanVnim_PduGrpVector
  brief  Contains an I-PDU-Group vector for each I-PDU, mapping the I-PDU to the corresponding I-PDU-Groups.
  */ 
extern CanVnim_PduGrpVectorType const CanVnim_PduGrpVector[CanVnim_Num_Of_PduGroups];


/**********************************************************************************************************************
  CanVnim_TxPduGrpInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_TxPduGrpInfo
  brief  Contains all I-PDU-Group relevant information for Tx I-PDUs.
  details
  Element                 Description
  PduGrpVectorStartIdx    the start index of the 0:n relation pointing to CanVnim_PduGrpVector
*/ 
extern CanVnim_TxPduGrpInfoType const CanVnim_TxPduGrpInfo[CanVnim_Tx_Num_Messages];


/**********************************************************************************************************************
  CanVnim_RxPduGrpInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_RxPduGrpInfo
  brief  Contains all I-PDU-Group relevant information for Rx I-PDUs.
  details
  Element                 Description
  PduGrpVectorStartIdx    the start index of the 0:n relation pointing to CanVnim_PduGrpVector
*/ 
extern CanVnim_RxPduGrpInfoType const CanVnim_RxPduGrpInfo[CanVnim_Rx_Num_Messages];


/**********************************************************************************************************************
  CanVnim_DefRxPduInfo
**********************************************************************************************************************/
/** 
  var    CanVnim_DefRxPduInfo
  brief  Contains all relevant information for deferred Rx I-PDUs.
  details
  Element                   Description
  RxDefPduBufferUsed        TRUE, if the 0:n relation has 1 relation pointing to ilRxBuffer
*/
extern CanVnim_DefRxPduInfoType const CanVnim_DefRxPduInfo[CanVnim_Rx_Num_Messages];


/**********************************************************************************************************************
  CanVnim_TxEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_TxEventTaskIdTable
  brief  Contains all task ids for application notification related to transmit messages 
  details
  Element                      Description
  CanVnim_TxAppNotifyTaskId    Tx Event Task Id
*/
extern CanVnim_TxEventTaskIdType const CanVnim_TxEventTaskIdTable[CanVnim_Tx_Num_TaskIds];

/**********************************************************************************************************************
  CanVnim_RxEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_RxEventTaskIdTable
  brief  Contains all task ids for application notification related to receive messages 
  details
  Element                      Description
  CanVnim_RxAppNotifyTaskId    Rx Event Task Id
*/
extern CanVnim_RxEventTaskIdType const CanVnim_RxEventTaskIdTable[CanVnim_Rx_Num_TaskIds];

/**********************************************************************************************************************
  CanVnim_TxErrEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_TxErrEventTaskIdTable
  brief  Contains all task ids for application notification related to transmit message errors 
  details
  Element                      Description
  CanVnim_TxAppNotifyTaskId    Tx Event Task Id
*/
extern CanVnim_TxEventTaskIdType const CanVnim_TxErrEventTaskIdTable[CanVnim_Tx_Num_ErrTaskIds];

/**********************************************************************************************************************
  CanVnim_RxErrEventTaskIdTable
**********************************************************************************************************************/
/** 
  var    CanVnim_RxErrEventTaskIdTable
  brief  Contains all task ids for application notification related to receive message errors 
  details
  Element                      Description
  CanVnim_RxAppNotifyTaskId    Rx Event Task Id
*/
extern CanVnim_RxEventTaskIdType const CanVnim_RxErrEventTaskIdTable[CanVnim_Rx_Num_ErrTaskIds];'''

    print '''
/**********************************************************************************************************************
  CanVnim_DiagFuncHandlerTable
**********************************************************************************************************************/
/** 
  var    CanVnim_DiagFuncHandlerTable
  brief  Contains all function handlers for diagnostic reception and for post handling services
*/
extern CanVnim_DiagFuncHandlerType const CanVnim_DiagFuncHandlerTable[CANVNIM_DIAG_NUM_SERVICES];


/**********************************************************************************************************************
  CanVnim_DiagPreCondCheckFuncPtr
**********************************************************************************************************************/
extern CanVnim_DiagPreConditionsChkFuncType const CanVnim_DiagPreCondCheckFuncPtr;


/**********************************************************************************************************************
  CanVnim_DiagSessionTimeOutApplCB
**********************************************************************************************************************/
extern CanVnim_DiagSessionTOApplCBType const CanVnim_DiagSessionTimeOutApplCB;

'''
    print '#endif /* CANVNIM_PAR_CFG_H */'

    

    print footer   
    
    f.close()
    

def Vnim_cfg_h():
    global dbc,footer
    global vnim_code_gen_dir,vnim_data_dir,vnim_generic_cfg
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanVnim_Cfg.h','w')
    
    
    sys.stdout = f
    vnim_generic=open(vnim_data_dir+"CanVNIMConfiguration.data",'r')
    vnim_generic_cfg_1 = json.loads(vnim_generic.read())
    vnim_generic.close()

    print '''#if !defined( CANVNIM_CFG_H )
#define CANVNIM_CFG_H

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
**  its rights under all copyright laws to protect this work as a published
**  work, when appropriate.  Those having access to this work may not copy it,
**  use it, modify it or disclose the information contained in it without the
**  written authorization of Visteon Corporation.
**
** =========================================================================*/

/* ===========================================================================
**
**  Name:           CanVnim_Cfg.h
**
**  Description:    CAN VNIM specific configuration parameters
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
** =========================================================================*/

/* ===========================================================================
**  I N C L U D E   F I L E S
** =========================================================================*/

/* ===========================================================================
**  M A C R O   D E F I N I T I O N S
** =========================================================================*/'''

    
    str_len=[len(x) for x in vnim_generic_cfg_1]
    max_len=max(str_len)+2
    
    for keys in vnim_generic_cfg_1:
        if keys not in vnim_generic_cfg and keys not in ['CanVnim_AliveCounter_InvalidValue','CanVnim_AliveCounter_MinValue','CanVnim_AliveCounter_MaxValue','CANVNIM_SM_EVENT_QUEUE_SIZE','CANVNIM_SM_MAXEVENT_DATA_SIZE']:
            print '#define '+keys+' '*(max_len-len(keys))+vnim_generic_cfg_1[keys]
        
    if vnim_generic_cfg!={}:
        for keys in vnim_generic_cfg:
            print '#define '+keys+' '*(max_len-len(keys))+vnim_generic_cfg[keys]
    
    print '''#endif /* CANVNIM_CFG_H */'''
    print footer 

    f.close()
    

def CanIL_cfg_h():
    global dbc,footer,CanVnim_Rx_Num_ErrTaskIds,CanVnim_Tx_Num_ErrTaskIds
    global shadow_rx_buffer,vnim_generic_cfg
    global vnim_code_gen_dir,vnim_data_dir
    disp_cfg_file = open(vnim_data_dir+"CanILConfiguration.data",'r')
    disp_cfg_data = json.loads(disp_cfg_file.read())
    disp_cfg_file.close()
    shadow_rx_buffer=[]
    
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanIl_Cfg.h','w')
    sys.stdout=f
    
    print '''#if !defined(CAN_IL_CFG_H)
#define CAN_IL_CFG_H'''
    
   

    header = '''/* ===========================================================================
 
                      CONFIDENTIAL VISTEON CORPORATION
 
   This is an unpublished work of authorship, which contains trade secrets,
   created in 2006.  Visteon Corporation owns all rights to this work and
   intends to maintain it in confidence to preserve its trade secret status.
   Visteon Corporation reserves the right, under the copyright laws of the
   United States or those of any other country that may have jurisdiction, to
   protect this work as an unpublished work, in the event of an inadvertent
   or deliberate unauthorized publication.  Visteon Corporation also reserves
   its rights under all copyright laws to protect this work as a published
   work, when appropriate.  Those having access to this work may not copy it,
   use it, modify it or disclose the information contained in it without the
   written authorization of Visteon Corporation.
 
  =========================================================================*/
/* ===========================================================================
 
   Name:           CanIl_Cfg.h
 
   Description:    CAN Interaction Layer Configuration Parameters Header File
 
   Organization:   Multiplex Core Technology
 
  =========================================================================*/'''
    print header,'\n'
    print '''/* ===========================================================================
   P U B L I C   M A C R O S
  =========================================================================*/'''

    print '\n\n'
    
    str_len=[len(x) for x in disp_cfg_data]
    max_len=max(str_len)+2
    
    for keys in disp_cfg_data:
        if disp_cfg_data[keys] != 'CANIL_NO' :
            print '#define '+keys+' '*(max_len-len(keys))+disp_cfg_data[keys]

    if vnim_generic_cfg['CANVNIM_VALIDATE_SIGNAL_API']=="STD_ON":
        print '#define CANIL_CH0MESSAGE_VALIDATION_SUPPORT  STD_ON'
    else:
        print '#define CANIL_CH0MESSAGE_VALIDATION_SUPPORT  STD_OFF'

    if CanVnim_Rx_Num_ErrTaskIds>0:
        print '#define CANIL_RXTOUTINDICATION_API'
        
    if CanVnim_Tx_Num_ErrTaskIds>0:
        print '#define CANIL_TXTOUTINDICATION_API'

        
    print '#define CANIL_IFSUPPORT'
    print '\n\n#endif  /* CAN_IL_CFG_H */ '
    print '\n'

    print footer
    f.close()

def CanIL_util_h():
    global dbc,il_generic_config,footer
    global vnim_code_gen_dir,vnim_data_dir
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanIl_Util_Cfg.h','w')
    
    sys.stdout=f
    
    header = '''#ifndef CANIL_UTIL_CFG_H
#define CANIL_UTIL_CFG_H

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
**  Name:           CanIl_Util_Cfg.h
**
**  Description:    CAN Util configuration parameters
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/'''
    
    print header
    
    includes = '''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/
'''
    print includes
    
    junk = '''#define CANUTIL_CRCSUPPORT

#define CANUTIL_CHECKSUMSUPPORT

#define CANUTIL_PARITYSUPPORT

#define CANUTIL_CRCPOLYNOMIAL              NORMAL

/*#define CANUTIL_ENABLED*/

/*#define CANUTIL_DEBUG_RECORD*/

/*#define CANUTIL_HISTORY_STRUCT_SIZE       50*/

'''
    print junk

    print '#endif /* CANUTIL_CFG_H */'
    
    footer = '''/*****************************************************************************
    R E V I S I O N     N O T E S
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  -
For each change to this file, be sure to record:
1.   Who made the change and when the change was made.
2.   Why the change was made and the intended result.

Date       By         Reason For Change
------------------------------------------------------------------------------

******************************************************************************/
/*****************************************************************************
Date			: 
By			: 
Traceability		: 
Change Description	:
*****************************************************************************/'''
    print footer
    
    f.close()
    
def CanIL_par_h():
    global dbc,il_generic_config
    global vnim_code_gen_dir,vnim_data_dir
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanIl_Par_Cfg.h','w')
    
    sys.stdout=f
    
    header = '''#if !defined(CAN_IL_PAR_H)
#define CAN_IL_PAR_H
/* ===========================================================================
 
                      CONFIDENTIAL VISTEON CORPORATION
 
   This is an unpublished work of authorship, which contains trade secrets,
   created in 2006.  Visteon Corporation owns all rights to this work and
   intends to maintain it in confidence to preserve its trade secret status.
   Visteon Corporation reserves the right, under the copyright laws of the
   United States or those of any other country that may have jurisdiction, to
   protect this work as an unpublished work, in the event of an inadvertent
   or deliberate unauthorized publication.  Visteon Corporation also reserves
   its rights under all copyright laws to protect this work as a published
   work, when appropriate.  Those having access to this work may not copy it,
   use it, modify it or disclose the information contained in it without the
   written authorization of Visteon Corporation.
 
  =========================================================================*/
/* ===========================================================================
  
    Name:           CanIl_Par_Cfg.h
  
    Description:    CAN Interaction Layer Tx, Rx Parameters Header File
  
    Organization:   Multiplex Core Technology
  
   =========================================================================*/'''

    print header,'\n'
    includes='#include "CanIl_Defines.h"'
    print includes,'\n'
    print '''/* ===========================================================================
   P U B L I C   M A C R O S
  =========================================================================*/

/* ===========================================================================
   Interaction Layer Number of Transmit Messages, Signals
  =========================================================================*/'''
    print '\n'
    ##code logic has to be included
    

    il_msg_tx=dbc.get_msg_type(il_generic_config,'tx')
    periodic_count=0
    for mes in il_msg_tx:
        if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5']:
            periodic_count=periodic_count+1
    
    
    #assuming no burst message
    print '#define Can_Channel0_Il_Tx_Num_Burst_Periodic   (0)'
    print '\n'
    print '#define Can_Channel0_Il_Tx_Num_Periodic         ('+str(periodic_count)+')'
    print '\n'
    print '''/* ===========================================================================
   Interaction Layer Number of Receive Messages, Signals
  =========================================================================*/'''

    print '\n'
    il_msg_rx=dbc.get_msg_type(il_generic_config,'rx')

    periodic_count=0
    periodic_sig_count=0
    for mes in il_msg_rx:
        if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5']:
            periodic_count=periodic_count+1
            periodic_sig_count+=len(mes['Sig_List'])
    #define Can_Channel0_Il_Rx_Num_Periodic         (1)
    print '#define Can_Channel0_Il_Rx_Num_Periodic         ('+str(periodic_count)+')'
    print '\n'
    print '#define Can_Channel0_Il_Rx_Num_Periodic_Signals ('+str(periodic_sig_count)+')\n'
    print '#define Can_Channel0_Il_Rx_Num_Req_Frames       (0)\n'
    


    #sorting logic from tcu
    '''for mes in message.iterkeys():
    message_list.append(mes) # creating a list to store message
    sorted_bit=sorted(message[mes],key = lambda x: int(x[1]))'''
    il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: int(x['id']))
    
    #    print il_sorted_mes

    print '''/* ===========================================================================
  Interaction Layer Transmit Message (Frame) Handles
 =========================================================================*/\n'''

    msg_count_tx = 0
    print '''typedef enum
{'''
    for mes in il_sorted_mes_tx:
        if msg_count_tx == 0:
            print 'Can_Channel0_Il_Tx_Message_'+mes['Msg_name']+'_TMH='+str(msg_count_tx)+','
        else:
            print 'Can_Channel0_Il_Tx_Message_'+mes['Msg_name']+'_TMH,'
        print '/*('+str(msg_count_tx)+') */'
        msg_count_tx+=1
    print 'Can_Channel0_Il_Tx_Num_Messages'
    print '/*('+str(msg_count_tx)+') */'
    print '}Can_Channel0_Il_Tx_Msg_Macro;'
                                                                        
    print '\n'

    print '''/* ===========================================================================
   Interaction Layer Transmit Signal Enumerations
   NB: The below tx signal sequence should match one to one with the
         IL Tx Signal description table.
       CAN_IL_SIGNAL const
       Can_Il_Tx_signals[ CAN_IL_TX_NUM_SIGNALS  ]
 
  =========================================================================*/'''

    print '''\ntypedef enum
{'''
    sig_count_tx=0
    for mes in il_sorted_mes_tx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])

        
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
         
        for sig in sig_sorted:
            #Can_Channel0_Il_Tx_Signal_ApplVers_Major = 0,
            if sig_count_tx == 0:
                print 'Can_Channel0_Il_Tx_Signal_'+sig['signal_name']+' = 0,'
                
            else:
                print 'Can_Channel0_Il_Tx_Signal_'+sig['signal_name']+','
            print '/*('+str(sig_count_tx)+') */'
            sig_count_tx+=1

    print ' Can_Channel0_Il_Tx_Num_Signals'
    print '/*('+str(sig_count_tx)+') */'

    print '}Can_Channel0_Il_Tx_Signals_Macro;'

    print '\n'

    print '''/* ===========================================================================
    Interaction Layer Receive Message Enumerations
   =========================================================================*/'''

    il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: int(x['id']))
    msg_count_rx = 0
    print '''typedef enum
{'''
    for mes in il_sorted_mes_rx:
        if msg_count_rx == 0:
            print 'Can_Channel0_Il_Rx_Message_'+mes['Msg_name']+' ='+str(msg_count_rx)+','
        else:
            print 'Can_Channel0_Il_Rx_Message_'+mes['Msg_name']+','
        print '/*('+str(msg_count_rx)+') */'
        msg_count_rx+=1
    print 'Can_Channel0_Il_Rx_Num_Messages'
    print '/*('+str(msg_count_rx)+') */'
    print '}Can_Channel0_Il_Rx_Msg_Macro;'
                                                                        
    print '\n'


    print '''/* ===========================================================================
   Interaction Layer Receive Signal Enumerations
  =========================================================================*/
'''
    print '''\ntypedef enum
{'''
    sig_count_rx=0
    for mes in il_sorted_mes_rx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])

        
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        
         
        for sig in sig_sorted:
            #Can_Channel0_Il_Tx_Signal_ApplVers_Major = 0,
            if sig_count_rx == 0:
                print 'Can_Channel0_Il_Rx_Signal_'+sig['signal_name']+' = 0,        /*('+str(sig_count_rx)+') */'
                
            else:
                print 'Can_Channel0_Il_Rx_Signal_'+sig['signal_name']+',/*('+str(sig_count_rx)+') */'
            #print '/*('+str(sig_count_rx)+') */'
            sig_count_rx+=1

    print 'Can_Channel0_Il_Rx_Num_Signals'
    print '/*('+str(sig_count_rx)+') */'

    print '}Can_Channel0_Il_Rx_Signals_Macro;'

    print '\n'
    
    
        #sorted_mes = sorted(message[mes],key = lambda x: int(x[1]))
    
    print '''/* ===========================================================================
   P U B L I C   M E M O R Y
  =========================================================================*/

extern CAN_IL_SIGNAL          const      Can_Channel0_Il_Tx_Signals[ Can_Channel0_Il_Tx_Num_Signals ];

extern CAN_IL_TX_MESSAGE      const      Can_Channel0_Il_Tx_Messages[ Can_Channel0_Il_Tx_Num_Messages ];

extern CAN_IL_TX_FRAME        const      Can_Channel0_Il_Tx_Frame_Table[ Can_Channel0_Il_Tx_Num_Messages ];

extern CAN_IL_SIGNAL          const      Can_Channel0_Il_Rx_Signals[Can_Channel0_Il_Rx_Num_Signals  ];

/*extern CAN_IL_RX_MESSAGE      const      Can_Channel0_Il_Rx_Messages[ ];*/

extern CAN_IL_RX_FRAME        const      Can_Channel0_Il_Rx_Frame_Table[ Can_Channel0_Il_Rx_Num_Messages ];

/*extern Can_Il_Rx_Data_Pointer const      Can_Channel0_Il_Receive_Data_Table[ ];*/

extern pTxPrecopyfn           const      Can_Channel0_Il_Tx_Precopy_Function_Table[ Can_Channel0_Il_Tx_Num_Messages ];

extern CAN_UINT8
Can_Channel0_Il_Rx_Frame_Data[ Can_Channel0_Il_Rx_Num_Messages ][ CAN_MAX_DATA_LENGTH ];

extern CAN_UINT8
Can_Channel0_Il_Rx_Frame_Status[ Can_Channel0_Il_Rx_Num_Messages ];

extern CAN_UINT16
Can_Channel0_Il_Rx_Timeout_Count[ Can_Channel0_Il_Rx_Num_Messages ];

extern Can_Il_Rx_Data_Pointer
Can_Channel0_Il_Receive_Ptr[ Can_Channel0_Il_Rx_Num_Messages ][ CAN_MAX_DATA_LENGTH ];

#ifdef CAN_IL_TX_BURST_MODE

 #if ( Can_Channel0_Il_Tx_Num_Burst_Periodic > 0 )

 extern CAN_UINT8
 Can_Channel0_Il_Tx_Burst_Count[ Can_Channel0_Il_Tx_Num_Burst_Periodic ];

 #endif

#endif

#endif  /* CAN_IL_PAR_H */
'''

    print footer

    f.close()

def CanIL_Par_Cfg_c():
    global dbc,il_generic_config,footer
    global vnim_code_gen_dir,vnim_data_dir
    if not os.path.exists(vnim_code_gen_dir):
      os.mkdir(vnim_code_gen_dir)
    f=open(vnim_code_gen_dir+'/CanIl_Par_Cfg.c','w')
    sys.stdout=f
    
    vnim_cfg_file = open(vnim_data_dir+"CanILConfiguration.data",'r')
    vnim_cfg_data = json.loads(vnim_cfg_file.read())
    vnim_cfg_file.close()    
    
    header='''/* ===========================================================================

                     CONFIDENTIAL VISTEON CORPORATION

  This is an unpublished work of authorship, which contains trade secrets,
  created in 2006.  Visteon Corporation owns all rights to this work and
  intends to maintain it in confidence to preserve its trade secret status.
  Visteon Corporation reserves the right, under the copyright laws of the
  United States or those of any other country that may have jurisdiction, to
  protect this work as an unpublished work, in the event of an inadvertent
  or deliberate unauthorized publication.  Visteon Corporation also reserves
  its rights under all copyright laws to protect this work as a published
  work, when appropriate.  Those having access to this work may not copy it,
  use it, modify it or disclose the information contained in it without the
  written authorization of Visteon Corporation.

 =========================================================================*/

/* ===========================================================================

  Name:           Can_Il_Par_Cfg.c

  Description:    CAN Interaction Layer Tx and Rx Parameters Configurations

                  Application Specific Tx and Rx Message and Signal
                  Data Structure Definitions

  Organization:   Multiplex Subsystems

 =========================================================================*/

/* ===========================================================================
  I N C L U D E   F I L E S
 =========================================================================*/'''

    print header,'\n'
    includes = '''#ifdef CANIL_IFSUPPORT

#include "Can_GeneralTypes.h"
#include <CclStack_Types.h>

#endif

#include "CanIl_Util.h"
#include "CanIl.h"
#include "CanIl_Par_Cfg.h"'''

    print includes,'\n'
    func_def='''/* ===========================================================================
  Interaction Layer Transmit Frame Status and Data Storage
 =========================================================================*/
CAN_UINT8
Can_Channel0_Il_Tx_Frame_Data[ Can_Channel0_Il_Tx_Num_Messages ][ CAN_MAX_DATA_LENGTH ];


CAN_UINT8
Can_Channel0_Il_Tx_Frame_Status[ Can_Channel0_Il_Tx_Num_Messages ];


CAN_UINT16
Can_Channel0_Il_Tx_Delay_Count[ Can_Channel0_Il_Tx_Num_Messages ];


CAN_UINT16
Can_Channel0_Il_Tx_Periodic_Count[ Can_Channel0_Il_Tx_Num_Periodic ];


#ifdef CAN_IL_TX_BURST_MODE

 #if ( Can_Channel0_Il_Tx_Num_Burst_Periodic > 0 )

CAN_UINT8
Can_Channel0_Il_Tx_Burst_Count[ Can_Channel0_Il_Tx_Num_Burst_Periodic ];

 #endif

#endif

/* ===========================================================================
  M E M O R Y   A L L O C A T I O N
 =========================================================================*/'''

    print func_def,'\n'

    # TRANSMIT DATA STRUCTURES
    print '''/* ===========================================================================
  TRANSMIT DATA STRUCTURES
 =========================================================================*/

/* ===========================================================================
  Interaction Layer Transmit Signal Descriptors

 The Following Table Definition Assumes a Motorola (Big Endian) Byte
 Ordering of Bytes within the CAN Frame. As an example, if a 16bit signal
 is defined in Bytes 0 and 1 of the CAN frame, the MSByte is Byte 0 and the
 LSByte is Byte 1.

 =========================================================================*/'''
    

    il_msg_tx=dbc.get_msg_type(il_generic_config,'tx')
    #sorting messages by ascending order of id
    il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: int(x['id']))
    #sorting messages 
    sig_count_tx=0
    tem_sig_count=0
    print '''CAN_IL_SIGNAL const
Can_Channel0_Il_Tx_Signals[ Can_Channel0_Il_Tx_Num_Signals ] ={\\'''
    print '/*  CAN Frame,                                              Num Bytes,    MS Byte,     MS Bit,      LS Byte,       LS Bit   */\\'


    mes_def_table=''
    
    for mes in il_sorted_mes_tx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])

        
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        #print sig_sorted
        
        
        unused_length=0
        start_bit=0
        ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
        intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
        moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
        sig_byte_total=0
        
        
        mes_def_table=mes_def_table+' /*'+mes['Msg_name']+'_TMH*/\n   {\n'+'        '+\
        str(tem_sig_count)+','+" " *30+' /* Signal handle Start index             */\n        '+\
        str(len(mes['Sig_List']))+','+" " *30+' /* Number of Signals in the Message             */\n'
        
        for signals in sig_sorted:
            tem_sig_count+=1
            temp_byte=0
            if int(signals['Len'])%8 == 0 :
                temp_byte = int(signals['Len'])/8
            else:
                temp_byte = ((int(signals['Len']))/8)+1
            '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
            #motorola or intel check code , logic from TCU toolsignal_occur=0
            signal_length = int(signals['Len'])
            s_start_bit = int(signals['Endbit'])
            
            layout_row=s_start_bit/8
            layout_col=s_start_bit%8
            #signal_length=int(signals['Len'])
            byte_no=0
            signal_occur = 0
            byte_no_1=(signal_length/8)-1 if signal_length %8 == 0 else signal_length /8
            
                
            MS_Byte=layout_row
            MS_Bit=layout_col
            LS_Byte=layout_row
            LS_Bit=layout_col
           

            
            if signals['Order'] == 'Motorola':
                magic_f = 0
                #print signal_length
                if signal_length != 1:
                    
                    for sig_len in range(signal_length-1):
                        #print layout_col
                        if layout_row<=7 and layout_row >=0:
                            if layout_col >=0 and layout_col<=7:
                                if layout_col == 0:
                                    layout_col = 7
                                    magic_f = 1
                                    layout_row=layout_row+1
                                else:
                                    magic_f = 0
                                    layout_col=layout_col-1
                              
                            else:
                              raise ValueError('size invalid col');
                              
                        else:
                            raise ValueError('signal size greater check dbc');
                    
                    if magic_f == 1:
                        LS_Bit = 0
                        LS_Byte = layout_row-1
                    else:
                        LS_Bit = layout_col
                        LS_Byte = layout_row
                    
                elif signals['Order'] == 'Intel':
                    magic_f=0
                    for sig_len in range(signal_length):
                        if layout_row<=7 and layout_row >=0:
                            if layout_col >=0 and layout_col<=7:
                                if layout_col == 0:
                                    layout_col = 7
                                    magic_f=1
                                    layout_row=layout_row-1
                                else:
                                    layout_col=layout_col+1
                              
                            else:
                              raise ValueError('size invalid col');
                        else:
                            raise ValueError('signal size greater check dbc');
                    
                    if magic_f == 1:
                        LS_Bit = 0
                        LS_Byte = layout_row+1
                    else:
                        LS_Bit = layout_col
                        LS_Byte = layout_row
                    
                
            #{  Can_Channel0_Il_Tx_Message_VersionNum_TMH,            1,          0,          7,          0,          0   }  /* ApplVers_Major   */   /* VersionNum Message */
            print "{  Can_Channel0_Il_Tx_Message_"+mes['Msg_name']+'_TMH,'+" "*(30-len(mes['Msg_name']))+str(temp_byte)+','+" "*13+str(MS_Byte)+\
                  ','+" "*13+str(MS_Bit)+','+" "*13+str(LS_Byte)+','+" "*13+str(LS_Bit)+'  },  /*'+signals['signal_name']+\
                  '*/   /*'+mes['Msg_name']+'*/\\'
            
            
        mes_def_table+='        '+str(sig_byte_total)+','+" "*30+' /* Total Number of Signal Bytes in the Message  */\n'
        mes_def_table+='        '+'Can_Channel0_Il_'+str(mes['Msg_name'])+'_Message_Init'+" "*(30-len(mes['Msg_name']))+'/* Pointer to the Initialization Data Bytes     */\n    },'

    print '};'

    #input has to be get from gui or dbc
    #Interaction Layer Transmit Message Initialization Arrays
    print'''/* ===========================================================================
  Interaction Layer Transmit Message Initialization Arrays

  The following transmit message initialization arrays define the initial
  values for all of the transmitted messages.

 =========================================================================*/

/*
 Sample Message Has 7 Signals, Each 1 Byte, for Initialization
 The order of the bytes in this array is as follows:
 Byte 0 - Signal 0, bit 1.7 Value = 0     C_SAMPLE*/'''

    #print 'sample message code that has to be generated'
    #Len
    for mes in il_sorted_mes_tx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])

        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        temp_str=''
        
        
        temp_total_sig_byte=0
        
        for signals in sig_sorted:
            temp_byte=0
            if int(signals['Len'])%8 == 0 :
                temp_byte = int(signals['Len'])/8
            else:
                temp_byte = ((int(signals['Len']))/8)+1
                
            
            if signals['signal_name']+'_init_value' in vnim_cfg_data:
                val = vnim_cfg_data[signals['signal_name']+'_init_value']
            else:
                val=0
            
            temp_value=format(val,'#0'+str((2*temp_byte)+2)+'x')
            temp_value=temp_value[2:]
            step=2
            #print temp_byte
            for i in range(0,len(temp_value),step):
                temp_str+='0x'+temp_value[i:step].upper()+','
                step+=2
                
            '''
            if sig_sorted.index(signals) == (len(sig_sorted)-1):
                temp_str+=str(val)
            else:
                temp_str+=str(val)+','         '''
            temp_total_sig_byte+=temp_byte
        
        print '/*     '+mes['Msg_name']+'   */'
        print 'static CAN_UINT8 const Can_Channel0_Il_'+mes['Msg_name']+'_Message_Init['+str(temp_total_sig_byte)+' ] = {'+temp_str.rstrip(',')+'};'
        
             


    print '''/* ===========================================================================
  Interaction Layer Transmit Message Definition Table

  This table (array of transmit message data structures) defines each
  transmitted message. The data structure defines the number of signals in
  the message, the total number of bytes in the message, a pointer to the
  list of signal handles, and a pointer to the message initialization data
  bytes.

 =========================================================================*/

CAN_IL_TX_MESSAGE const
Can_Channel0_Il_Tx_Messages[ Can_Channel0_Il_Tx_Num_Messages ] =\n {'''

    print mes_def_table
    print '};\n'

    print'''/* ===========================================================================
  Interaction Layer Transmit Message Data (TMD) Structures (Frame Definition)

  !!! IMPORTANT NOTE !!! The transmit message handles must be specified
  sequentially, starting with 0 (zero). These message handles serve as an
  index to the transmit complete function pointers, so each index must map
  to the correct transmit complete callback function pointer in the lookup
  table (array of function pointers) for servicing transmit complete events.

 =========================================================================*/'''
    temp_count = 0
    for mes in il_sorted_mes_tx:
        print '\n/*       '+mes['Msg_name']+'     */'
        print ' static CAN_IL_TMD const Can_Channel0_Il_Tx_Message_'+mes['Msg_name']+'_Tmd ='
        print '{'
        print '     CAN_GPNUM_'+mes['DLC']+',                                                                    /* CAN message data length  */'
        print '     Can_Channel0_Il_Tx_Frame_Data[ '+str(temp_count)+' ],                                             /* Pointer to Data          */'
        print '     Can_Channel0_Il_Tx_Message_'+mes['Msg_name']+'_TMH                                       /* Transmit Message Handle  */'
        print '};'
        temp_count+=1

    print '''/* ===========================================================================
  Interaction Layer Periodic Transmit Table

  This table is an array of data structures that define the periodic
  transmit characteristics for messages that are transmitted periodically.
  Care must be taken so that the each periodic message defined in the
  Interaction Layer Transmit Frame table map correctly to this table so
  that the correct periodic message attributes, and the pointer to the
  periodic timer, is correctly retrieved.

 =========================================================================*/
static CAN_IL_TX_PERIODIC const
Can_Channel0_Il_Tx_Periodic[ Can_Channel0_Il_Tx_Num_Periodic ] =
{'''
    temp_count = 0
    for mes in il_sorted_mes_tx:
        if mes['GenMsgSendType'] == '5' or mes['GenMsgSendType'] == '0':
            print ' /* '+mes['Msg_name']+'  Message */'
            print ' {'
            print '     IL_TIME_IN_TASK_TICS( '+mes['GenMsgCycleTime']+') ,                                   /* Primary Period in Task Tics  */'
            print '     IL_TIME_IN_TASK_TICS( '+str((temp_count+1)*10)+'),                                     /* Offset Delay in Task Tics    */'#internally has to be incremented by 10
            print '     &Can_Channel0_Il_Tx_Periodic_Count[ '+str(temp_count)+' ]                         /* Pointer to Periodic Count    */'
            print ' },'
            temp_count+=1
    print '};'

    print '''/* ===========================================================================
  Interaction Layer Burst Periodic Transmit Table
 =========================================================================*/

/* ===========================================================================
  Interaction Layer Transmit Frame Table

  Each entry in this table defines the attributes for a specific transmit
  frame transmitted by the Interaction Layer.

 =========================================================================*/\n'''
    drv_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r')
    cfg_data = json.loads(drv_file.read())
    drv_file.close()
    periodic_count=0
    temp_count=0
    print '''CAN_IL_TX_FRAME const Can_Channel0_Il_Tx_Frame_Table[ Can_Channel0_Il_Tx_Num_Messages ] = \n{'''
    for mes in il_sorted_mes_tx:
        print ' {'
        print ' /* '+mes['Msg_name']+' Message (CAN periodic, data change or a request ) */'
        if mes['GenMsgSendType'] == '5':
            print '     (IL_TX_ATTR_EVENT | IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY),   /* Frame Transmission Attributes                */'
        elif mes['GenMsgSendType'] == '0':
             print '     (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY),   /* Frame Transmission Attributes                */'
        else:
            print '     (IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY  ),   /* Frame Transmission Attributes                */'
            
        #print '     (IL_TX_ATTR_PERIODIC | | IL_TX_ATTR_TXC_NOTIFY ),      /* Frame Transmission Attributes                */'
        print '     &Can_Channel0_Il_Tx_Frame_Status[ '+str(temp_count)+' ],       /* Pointer to the Frame Status Variable         */'
        print '     Can_Channel0_Il_Tx_Frame_Data[ '+str(temp_count)+' ],          /* Pointer to the Transmitted Frame Data        */'
        print '     &Can_Channel0_Il_Tx_Delay_Count[ '+str(temp_count)+' ],        /* Pointer to the Transmit Delay Count          */ '
        if mes['GenMsgSendType'] == '5' or mes['GenMsgSendType'] == '1':
            print '     IL_TIME_IN_TASK_TICS( 20 ),                   /* Minimum Transmit Delay in Timer Tics         */'#has to be fetched from dbc or gui- Event/cyclicevent transmission has to be set as 20 else 0
        else:
            print '     IL_TIME_IN_TASK_TICS( 0 ),                   /* Minimum Transmit Delay in Timer Tics         */'#has to be fetched from dbc or gui- Event/cyclicevent transmission has to be set as 20 else 0
        if mes['GenMsgSendType'] == '5' or mes['GenMsgSendType'] == '0':   
            print '     &Can_Channel0_Il_Tx_Periodic[ '+str(periodic_count)+' ],           /* Pointer to the Periodic Attributes (or NULL ) */ '
            periodic_count+=1
        else:
            print '     NULL,           /* Pointer to the Periodic Attributes (or NULL ) */ '
        print '     NULL,                                        /* Ptr to Burst Periodic Attributes (or NULL)   */'#has to be fetched from dbc or gui , now not supported
        print '     &Can_Channel0_Il_Tx_Message_'+mes['Msg_name']+'_Tmd,  /* Pointer to CAN Driver TMD Data Structure     */'
        print ' },'
        temp_count+=1
    print '};'

    print '''/* ===========================================================================
  R E C E I V E   D A T A   S T R U C T U R E S
 =========================================================================*/
/* ===========================================================================
  Interaction Layer Receive Signal Descriptors

  This data structure defines each received signal, include the specific
  received CAN frame (sequentially enumerated) in which the signal resides,
  and the specific location of the signal within the CAN frame. The
  signal is assumed to span the bits in the frame from the MSByte.MSBit to
  the LSByte.LSBit. As an example, a 16 bit (2 Byte) wide signal that
  occupies the first two bytes (Byte0, Byte 1) of a CAN frame is specified
  as having endpoints at (Byte 0, Bit 7) and (Byte 1, Bit 0). This table
  definition assumes a Motorola (Big Endian) ordering of bytes within the
  CAN Frame.

 =========================================================================*/
/* Receive messages */'''


    il_msg_rx=dbc.get_msg_type(il_generic_config,'rx')
    il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: int(x['id']))
    print '''CAN_IL_SIGNAL const
Can_Channel0_Il_Rx_Signals[ Can_Channel0_Il_Rx_Num_Signals ] =
{ '''
    print '/*  CAN Frame,                                               Num Bytes,      MS Byte,    MS Bit,     LS Byte,    LS Bit */'
    sig_start = []
    sig_idx=0
    for mes in il_sorted_mes_rx:
        sig_par=[]
        sorted_list=[]
        for signals in mes['Sig_List']:
            mes['Sig_List'][signals]['signal_name']=signals
            sig_par.append(mes['Sig_List'][signals])

        
        sig_sorted =sorted(sig_par,key = lambda x: int(x['Endbit']))
        #print sig_sorted
        mes_def_table=mes_def_table+' /*'+mes['Msg_name']+'*/\n   {\n'+'        '+str(len(mes['Sig_List']))+','+" " *30+' /* Number of Signals in the Message             */\n'
        unused_length=0
        start_bit=0
        ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
        intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
        moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
        sig_byte_total=0
        sig_start.append(sig_idx)
        for signals in sig_sorted:
            sig_idx+=1
            temp_byte=0
            if int(signals['Len'])%8 == 0 :
                temp_byte = int(signals['Len'])/8
            else:
                temp_byte = ((int(signals['Len']))/8)+1
            '''{'GenSigInactiveValue': '0', 'DescriptionE': '', 'signal_name': 'AppTempAdjustReq_DDP', 'CommentRxJ': '', 'CommentRxE': '', 'DescriptionJ': '', 'Len': '8',
                'CommentTxJ': '', 'GenSigSendType': '', 'ValueTableE': '', 'Endbit': '7', 'GenSigStartValue': '0', 'Order': 'Motorola', 'CommentTxE': ''}'''
            #motorola or intel check code , logic from TCU toolsignal_occur=0
            signal_length = int(signals['Len'])
            s_start_bit = int(signals['Endbit'])
            
            layout_row=s_start_bit/8
            layout_col=s_start_bit%8
            #signal_length=int(signals['Len'])
            byte_no=0
            signal_occur = 0
            byte_no_1=(signal_length/8)-1 if signal_length %8 == 0 else signal_length /8
            
                
            MS_Byte=layout_row
            MS_Bit=layout_col
            LS_Byte=layout_row
            LS_Bit=layout_col
           

            
            if signals['Order'] == 'Motorola':
                magic_f = 0
                #print signal_length
                if signal_length != 1:
                    
                    for sig_len in range(signal_length-1):
                        #print layout_col
                        if layout_row<=7 and layout_row >=0:
                            if layout_col >=0 and layout_col<=7:
                                if layout_col == 0:
                                    layout_col = 7
                                    magic_f = 1
                                    layout_row=layout_row+1
                                else:
                                    magic_f = 0
                                    layout_col=layout_col-1
                              
                            else:
                              raise ValueError('size invalid col');
                              
                        else:
                            raise ValueError('signal size greater check dbc');
                    
                    if magic_f == 1:
                        LS_Bit = 0
                        LS_Byte = layout_row-1
                    else:
                        LS_Bit = layout_col
                        LS_Byte = layout_row
                    
                elif signals['Order'] == 'Intel':
                    magic_f=0
                    for sig_len in range(signal_length):
                        if layout_row<=7 and layout_row >=0:
                            if layout_col >=0 and layout_col<=7:
                                if layout_col == 0:
                                    layout_col = 7
                                    magic_f=1
                                    layout_row=layout_row-1
                                else:
                                    layout_col=layout_col+1
                              
                            else:
                              raise ValueError('size invalid col');
                        else:
                            raise ValueError('signal size greater check dbc');
                    
                    if magic_f == 1:
                        LS_Bit = 0
                        LS_Byte = layout_row+1
                    else:
                        LS_Bit = layout_col
                        LS_Byte = layout_row
                        
            #{  Can_Channel0_Il_Tx_Message_VersionNum_TMH,            1,          0,          7,          0,          0   }  /* ApplVers_Major   */   /* VersionNum Message */
            print "{  Can_Channel0_Il_Rx_Message_"+mes['Msg_name']+','+" "*(30-len(mes['Msg_name']))+str(temp_byte)+','+" "*13+str(MS_Byte)+\
                  ','+" "*13+str(MS_Bit)+','+" "*13+str(LS_Byte)+','+" "*13+str(LS_Bit)+'  },  /*'+signals['signal_name']+\
                  '*/   /*'+mes['Msg_name']+'*/'

            shadow_rx_buffer.append(str(temp_byte)+','+" "*13+str(MS_Byte)+\
                  ','+" "*13+str(MS_Bit)+','+" "*13+str(LS_Byte)+','+" "*13+str(LS_Bit)+'  },  /*'+signals['signal_name']+\
                  '*/   /*'+mes['Msg_name']+'*/')
    print'};'


    print '''/* ===========================================================================
  Interaction Layer Receive Frame Data Storage and Status
 =========================================================================*/
CAN_UINT8
Can_Channel0_Il_Rx_Frame_Data[ Can_Channel0_Il_Rx_Num_Messages ][ CAN_MAX_DATA_LENGTH ];

CAN_UINT8
Can_Channel0_Il_Rx_Frame_Status[ Can_Channel0_Il_Rx_Num_Messages ];

CAN_UINT16
Can_Channel0_Il_Rx_Timeout_Count[ Can_Channel0_Il_Rx_Num_Messages ];

Can_Il_Rx_Data_Pointer
Can_Channel0_Il_Receive_Ptr[ Can_Channel0_Il_Rx_Num_Messages ][ CAN_MAX_DATA_LENGTH ];

#if (Can_Channel0_Il_Rx_Num_Req_Frames > 0)

#define CAN_CHANNEL0_IL_DATA_REQ_TX_HANDLE
#define CAN_CHANNEL0_IL_REQ_TX_CANID

static CAN_UINT8  reqCounter[ Can_Channel0_Il_Rx_Num_Req_Frames ];
static CAN_UINT16 reqTimer[ Can_Channel0_Il_Rx_Num_Req_Frames ];
static CAN_UINT8  reqStatus[ Can_Channel0_Il_Rx_Num_Req_Frames ];

static const CAN_UINT8 Can_Channel0_Il_Data_Request[2] = {0x00,0x00};

static const CAN_IL_TMD Can_Channel0_Il_Data_Request_Frame_Tmd[ Can_Channel0_Il_Rx_Num_Req_Frames ] =
{
};

static const Can_Channel0_Il_Rx_Frame_Request Can_Channel0_Il_Rx_Request_Frame_Data[ Can_Channel0_Il_Rx_Num_Req_Frames ] =
{
};

#endif
'''


    
    print '''
/* ===========================================================================
  Received Frame Attributes Lookup Table

  This table includes the attributes for all of the received frames.
  If a received frame is periodic, this table also includes pointers to the
  received frame status and to the receive timeout counter for message
  gain and loss indication. If a transmitted frame request can be issued
  for a received frame, this table includes the pointer to the receive
  frame request attributes.

 =========================================================================*/
CAN_IL_RX_FRAME const
Can_Channel0_Il_Rx_Frame_Table[ Can_Channel0_Il_Rx_Num_Messages ] =
{'''
    temp_count = 0
    enum = dbc.get_enum_values()
    periodic_count=0
    
    for mes in il_sorted_mes_rx:
        print '/* '+mes['Msg_name']+' */'
        print ' {'

        if mes['GenMsgSendType'] == '5' or mes['GenMsgSendType'] == '0':
            '''temp=mes['Msg_name']+'_tx_timeout'
            if cfg_data[temp] == 'on':'''
            print '     ( IL_RX_ATTR_PERIODIC | IL_RX_ATTR_TIMEOUT_MONITOR),'
        else:
            print '     (IL_RX_ATTR_DEFAULT ),'
            
        '''else:
                print '     (IL_RX_ATTR_EVENT | IL_RX_ATTR_PERIODIC),'''
        '''elif mes['GenMsgSendType'] == '0':
            temp=mes['Msg_name']+'_tx_timeout'
            if cfg_data[temp] == 'on':
                print '     (IL_RX_ATTR_PERIODIC | IL_RX_ATTR_TIMEOUT_MONITOR),'
            else:
                print '     (IL_RX_ATTR_PERIODIC),'''
        
        
            
        print '     '+str(sig_start[temp_count])+',	     /* Signal Start Index                   */'
        print '     '+str(len(mes['Sig_List']))+',	    /* Number of Signals in Message         */'
        print '     CAN_GPNUM_'+mes['DLC']+',           /* Minimum Data Length Code             */'
        print '     &Can_Channel0_Il_Rx_Frame_Status[ '+str(temp_count)+'],      /* Pointer to Receive Status            */'
        print '     Can_Channel0_Il_Rx_Frame_Data[ '+str(temp_count)+'],         /* Pointer to Received Frame Data       */'
        if mes['GenMsgSendType'] == '5' or mes['GenMsgSendType'] == '0':       
            print '     &Can_Channel0_Il_Rx_Timeout_Count['+str(periodic_count)+'],         /* Pointer to the Timeout Counter       */'
            periodic_count+=1
        else:
            print '     NULL,        /* Pointer to the Timeout Counter       */'
        print '     IL_TIME_IN_TASK_TICS('+str(int(mes['GenMsgCycleTime'])*10),'),     /* Timeout Count Value                  */'		
        print '     NULL,                                       /* &Can_Channel0_Il_Rx_Frame_Request_Table[ 0 ] */  /* Ptr to Receive Request Attributes    */ '
        print '},'
        temp_count+=1
    print '};'


    print '''pTxPrecopyfn const Can_Channel0_Il_Tx_Precopy_Function_Table[ Can_Channel0_Il_Tx_Num_Messages ] =
{'''
    for mes in il_sorted_mes_rx:
        temp=mes['Msg_name']+'_timeout'
        #not implemented as now , Hence printing NULL for all
        '''if cfg_data[temp] == 'on':
            print '     Can_Channel0_Il_Rx_'+mes['Msg_name']+'_precopy,'
        else:
            print '     NULL  ,' '''
        print '     NULL  ,' 
    print '''};'''

    print footer
    f.close()

if __name__ == "__main__":   
    CanIL_cfg_h()
    CanIL_par_h()
    CanIL_Par_Cfg_c()
    Vnim_par_c()
    Vnim_par_h() 
    Vnim_cfg_h()


