import sys,json
import os
from cogent_io import open_output, close_output
from py2compat import py2_print as print, Py2Dict  # Python 2 print/dict-order semantics
dbc=None
dbc_file_name=None

vnim_code_gen_dir = './CODE_GEN'
vnim_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgILSupport'
full_msg='ALL'
time_str=''
footer=''

datatype_8 = 'unsigned8'
datatype_16 = 'unsigned16'
datatype_32 = 'unsigned32'
dlc_disable = 1 # variable used for structure optimization

  
def set_file_node_il(file_name,node):
    global dbc,dbc_file_name
    from Dbc_Parser import dbc_parser
    dbc=dbc_parser(file_name,node)
    dbc_file_name=file_name.split('/')[len(file_name.split('/'))-1]
    
def set_init_global(time_st):
    global time_str,footer
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

def msg_order_enum_gen():
  global dbc,datatype_8,datatype_16,datatype_16,vnim_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  vnim_sig_cfg_file = open(vnim_data_dir+"CanDbcSigConfiguration.data",'r',encoding='utf-8')
  vnim_sig_cfg_data = json.loads(vnim_sig_cfg_file.read())
  vnim_sig_cfg_file.close()
  
  il_msg_tx=[]
  il_msg_rx=[]
  
   
  all_message_tx = dbc.get_msg_type(full_msg,'tx')
  for mes in all_message_tx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_tx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_tx.append(mes)
      
  
  il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  
  all_message_rx = dbc.get_msg_type(full_msg,'rx')
  for mes in all_message_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_rx.append(mes)
      
  il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
  
  node_list=[]
  rx_node_cfg={}
  #msg_list=[]
  node_msg_list={}
  for mes in il_sorted_mes_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_key_msg'] in ['on','ON','On',1,'1']:
      rx_node_cfg[vnim_msg_cfg_data[mes['Msg_name']+'_node_name']] = mes['Msg_name']
      if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_list:
        node_list.append(vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper())
    if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_msg_list:      
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()]=[mes['Msg_name']]
    else:
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()].append(mes['Msg_name'])
          
  message_order = []
  timeout_list ={}
  
  il_sorted_mes_rx_ordered = []
  for nd in node_list:
    #il_sorted_mes_rx_ordered.append(rx_node_cfg[nd])
    message_order.append(rx_node_cfg[nd])
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        message_order.append(mes)
        
  
  for order_msg in  message_order:
    for mes in il_sorted_mes_rx:
      if mes['Msg_name'] == order_msg:
        il_sorted_mes_rx_ordered.append(mes)
        
  for nd in node_list:  
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        for mes_prop in il_sorted_mes_rx_ordered:
          if int(mes_prop['GenMsgCycleTime']) !=0:
              timeout_list[nd]=1
              break
              
  #message byte position
  print('static '+datatype_8+' vnim_msg_byte_position[NUM_VNIM_MESSAGES] = ')
  print('{')
  
  
  byte_cnt = 0
  msg_cnt = 0
  temp_str ='    '
  total_mes_cnt = 0
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if  msg_cnt ==7:
        if total_mes_cnt == (len(il_sorted_mes_rx_ordered)-1):
          temp_str+=str(byte_cnt)
        else:
          temp_str+=str(byte_cnt)+',  \\\n    '
        msg_cnt=-1
        byte_cnt+=1
      else:
        if total_mes_cnt == (len(il_sorted_mes_rx_ordered)-1):
          temp_str+=str(byte_cnt)
        else:
          temp_str+=str(byte_cnt)+','
      msg_cnt+=1
      total_mes_cnt+=1
  
  print(temp_str)
  print('};\n')
  
  # bit mask
  print('static unsigned8 vnim_msg_bit_mask[NUM_VNIM_MESSAGES] = ')
  print('{')
  
  bit_signal=1
  total_mes_cnt = 0
  msg_cnt = 0
  temp_str ='    '
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if  msg_cnt ==7:
        if total_mes_cnt == (len(il_sorted_mes_rx_ordered)-1):
          temp_str+=hex(bit_signal)
        else:
          temp_str+=hex(bit_signal)+',  \\\n    '
        msg_cnt=-1
        
      else:
        if total_mes_cnt == (len(il_sorted_mes_rx_ordered)-1):
          temp_str+=hex(bit_signal)
        else:
          temp_str+=hex(bit_signal)+','
      bit_signal=bit_signal<<1
      msg_cnt+=1
      if bit_signal == 256:
        bit_signal=1
      total_mes_cnt+=1
  
  print(temp_str)
  print('};\n')
  
  print('''/* ===========================================================================
      M A C R O   D E F I N I T I O N S
   =========================================================================*/\n''')
  print('#define NUM_STS_BYTES (sizeof(vnim_msg_bit_mask)/sizeof(vnim_msg_bit_mask[0]))\n')
  print('''/*MESSAGE MISSING*/                                 
#define IS_MSG_MISSING(MSG)   (CAN_UINT8)(((nw_can_msg_missing[vnim_msg_byte_position[MSG]]) & \\
                                (vnim_msg_bit_mask[MSG])) == (vnim_msg_bit_mask[MSG]))

#define NM_MSG_MISSING(MSG)   (nw_can_msg_missing[vnim_msg_byte_position[MSG]] |= \\
                                  vnim_msg_bit_mask[MSG])

#define NM_MSG_GAIN(MSG)      (nw_can_msg_missing[vnim_msg_byte_position[MSG]] &= \\
                                  (CAN_UINT8) ~ (vnim_msg_bit_mask[MSG]))

/*DLC FAULT*/                                  
#define IS_MSG_DLC_INVALID(MSG)   (CAN_UINT8)(((nw_can_msg_dlc_fault[vnim_msg_byte_position[MSG]]) & \\
                                (vnim_msg_bit_mask[MSG])) == (vnim_msg_bit_mask[MSG]))

#define NM_MSG_DLC_INVALID(MSG)   (nw_can_msg_dlc_fault[vnim_msg_byte_position[MSG]] |= \\
                                  vnim_msg_bit_mask[MSG])

#define NM_MSG_DLC_VALID(MSG)      (nw_can_msg_dlc_fault[vnim_msg_byte_position[MSG]] &= \\
                                  (CAN_UINT8) ~ (vnim_msg_bit_mask[MSG]))''')
                       
  for nodes in node_list:
    print('#define IS_'+nodes+'_DLC_FAULT(msg_id)  ((IS_'+nodes+'_NODE_DLC_INVALID() != FALSE)   || (IS_MSG_DLC_INVALID(msg_id) != FALSE))')
  

  print('''/* ===========================================================================
     M E M O R Y   A L L O C A T I O N
  =========================================================================*/\n''')
  print('''static CAN_UINT8 Onfail_value_zero[8] = {0,0,0,0,0,0,0,0}; /* Just a dummy array variable for VIN onfail value */                                
static unsigned32 vnim_msg_missing_heal_timecnt[NUM_VNIM_MESSAGES];
static unsigned32 vnim_msg_healing_msgcnt[NUM_VNIM_MESSAGES];
/*static const unsigned16 nw_node_monitoring_timecnt = 5;*/
static unsigned8 vnim_msg_missing[NUM_STS_BYTES];
static unsigned8 nw_can_msg_missing[NUM_STS_BYTES];
static unsigned8 nw_can_msg_dlc_fault[NUM_STS_BYTES];
static unsigned8 vnim_high_prior_data=TRUE;
static CAN_UINT8 MsgDtcFlag_previous[NUM_VNIM_MESSAGES];''')

  print('\n /*Message Timeout Flag for Node*/')
  #Message timeout flags
  #if the number of periodic messages under a node is more than 8,a 16bit flag is generated.
  for nodes in node_list:
    if nodes in timeout_list:
      count=0;
      for mes in il_sorted_mes_rx_ordered:
        if vnim_msg_cfg_data[mes['Msg_name'].upper() + '_rx_enable'] in ['on', 'On', 1, '1', 'ON']:
          if vnim_msg_cfg_data[mes['Msg_name'] + '_node_name']==nodes:
            if mes['Msg_name']!=nodes and int(mes['GenMsgCycleTime']) >0:
              count+=1;
      
      count-=1;    #Reduce the count by 1 to remove the key message          
      if(count <= 8):
        print('static unsigned8 Vnim_' + nodes + '_Timeout_flag  = 0;')
      elif(count <= 16):  
        print('static unsigned16 Vnim_' + nodes + '_Timeout_flag  = 0;')
      elif(count <= 32):
        print('static unsigned32 Vnim_' + nodes + '_Timeout_flag  = 0;')
      else:
        tmpCount = ((count//32) + 1);
        print('static unsigned32 Vnim_' + nodes + '_Timeout_flag[' + str(tmpCount) + '] = {0};')

    
  #os_notify flags
  print('\n/* Datachanged flag*/')
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Msg_name'].upper() != 'EMS5_500':
        delay = 0
        for signal in mes['Sig_List']:
            if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['200ms_Delay_g1','200ms_Delay_g2']:
                delay =1
                break
        if delay ==1:
          print('static unsigned8 '+mes['Msg_name'].upper()+'_msg_changed = FALSE;')
  
  
  
  print('/* variant code status*/')
  print('unsigned8 IS_varcode_st = FALSE;')
  
  for nodes in node_list:
    print('unsigned8 '+nodes.upper()+'_node_cfg_st  = FALSE;')
  
  print('/*node and message list*/')
  print('CAN_UINT8 const vnim_msg_node_list [NUM_VNIM_MESSAGES] = ')
  print('{')
  print('   VNIM_NODE_LIST')
  print('};\n')
  
  
  print('''/* ===========================================================================
     F U N C T I O N   P R O T O T Y P E S
 =========================================================================*/\n''')
  
  print('''static void vnim_message_loss (unsigned8 msg_id);
static void vnim_message_gain (unsigned8 msg_id);
static void vnim_node_loss (unsigned8 node_id);
static void vnim_node_gain (unsigned8 node_id);
static void vnim_error_detect (unsigned8 vnim_msgid,unsigned8 il_msgid ,unsigned16 cnt);
static void vnim_stop_error_healing (unsigned8 vnim_msgid);
static unsigned8 vnim_start_error_healing (unsigned8 vnim_msgid, unsigned8 il_msgid, unsigned16 cnt);
''')
  
  
  print('''/* ===========================================================================
 
  Name:            vnim_message_mon_init
 
  Description:     Function to initialise time count and status flags
 
  Inputs:          void
 
  Returns:         none
 
  =========================================================================*/''')

  print('''void vnim_message_mon_init(void)
{
      unsigned8 idx;''')
  # for vaiant code has to be udpated*/ 
  '''esc_present =  0
    for nodes in node_list:
      if''' 
  print('''   for (idx=0;idx < NUM_VNIM_MESSAGES ;idx++)
    {
        vnim_msg_missing_heal_timecnt[idx] = 0;
        vnim_msg_healing_msgcnt[idx] = 0;
        MsgDtcFlag_previous[idx]=0;
    }
    for (idx=0;idx < NUM_STS_BYTES ;idx++)
    {
        vnim_msg_missing[idx] = 0xFF;      /* L2 Code */
        nw_can_msg_missing[idx]	= 0x00;    /* W207 Code */
        nw_can_msg_dlc_fault[idx]	= 0x00;    
    }''')
    
  #os_notify flags
  print('\n   /* Initilisation of message changed flags */')
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Msg_name'].upper() != 'EMS5_500':
        delay = 0
        for signal in mes['Sig_List']:
            if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['200ms_Delay_g1','200ms_Delay_g2']:
                delay =1
                break
        if delay ==1:
          print('   '+mes['Msg_name'].upper()+'_msg_changed = FALSE;')
  
  print('   /* Initialisation of VIN validation flag */')
  print('   Suppress_VINDTC_Logging = FALSE;')
  print(' 	/* Initialisation of flag for IPCL data */')
  print('   vnim_high_prior_data = TRUE;')
  print('\n   /* Initilisation of Message Timeout Flag for Node*/')
  #Message timeout flags
  for nodes in node_list:
    if nodes in timeout_list:
      count=0;
      for mes in il_sorted_mes_rx_ordered:
        if vnim_msg_cfg_data[mes['Msg_name'].upper() + '_rx_enable'] in ['on', 'On', 1, '1', 'ON']:
          if vnim_msg_cfg_data[mes['Msg_name'] + '_node_name']==nodes:
            if mes['Msg_name']!=nodes and int(mes['GenMsgCycleTime']) >0:
              count+=1;
      
      count-=1;    #Reduce the count by 1 to remove the key message          
      if(count <= 32):      
        print('    Vnim_'+nodes+'_Timeout_flag  = 0;')
      else:
        tmpCount = ((count//32) + 1);
        for i in range(0, tmpCount):
          print('    Vnim_'+nodes+'_Timeout_flag[' + str(i) + '] = 0;')
      
  print('   /* Read VARIENT Config from NVM */')
  print('   IS_varcode_st= nw_read_node_config(CF_OPT_VC); /* Variant coding status */')
  print('   if( IS_varcode_st == CF_OPT_VC_PRSNT)')
  print('   {')
  for node in node_list:
    print('       '+node+'_node_cfg_st= nw_read_node_config(CF_OPT_'+node+');')
  print('   }')
  print('   else')
  print('   {')
  for node in node_list:
    print('       '+node+'_node_cfg_st= CF_OPT_'+node+'_NOT_PRSNT;')
  print('   }')
		
  print('}\n')
  
  print('''/* ===========================================================================
  
  Name:            vnim_clr_missing
  
  Description:     Function to initialise message missing 	flag
  
  Inputs:          void
  
  Returns:         none
  
  =========================================================================*/

void vnim_clr_missing(void)
{
   unsigned8 idx;
   for (idx=0;idx < NUM_STS_BYTES ;idx++)
    {
      nw_can_msg_missing[idx]	= 0x00;	   /* W207 Code */
      nw_can_msg_dlc_fault[idx]	= 0x00;	   /* W207 Code */
    }	
    /*Restart the message dlc monitoring flag */
    for(idx=0;idx<NUM_VNIM_MESSAGES;idx++)
    {
      vnim_dlc_dtc_flagsts(idx); 
      vnim_dlcmonitor_enable(idx,0);
    }
    /*Restart the signal content monitoring flag */
    for(idx=0;idx<NUM_VNIM_SIGCONT_SIGNALS;idx++)
    {
      vnim_sigmointor_enable(idx);
    }
    #if(SRS_PARITY_MONITOR_ENABLED == TRUE)
      vnim_srs_parity_mointor_enable();
    #endif
}\n''')
  
  
  
  print('''\n/* ===========================================================================
 
  Name:            vnim_set_init_signals
 
  Description:     Function to initialise signals with default values.
 
  Inputs:          void
 
  Returns:         none
 
  =========================================================================*/\n''')
  
  print('void vnim_set_init_signals(void) ')
  print('{\n')
  print('/* Tx signal initialisation  */ ')
  for mes in il_sorted_mes_tx:
      if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
        for signals in mes['Sig_List']:
          if int(mes['Sig_List'][signals]['Len']) >32:
            print('   ILPutTx_'+signals.upper()+'_data(&Onfail_value_zero[0]);')
          else: 
            print('   ILPutTx_'+signals.upper()+'_data('+vnim_sig_cfg_data[signals.upper()+'_tx_init_value']+'u);')
            
            
  print('/* Rx signal initialisation  */ ')
  for mes in il_sorted_mes_rx_ordered:
      if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
        for signals in mes['Sig_List']:
          if int(mes['Sig_List'][signals]['Len']) >32:
            print('   ILRxPut_'+signals.upper()+'(&Onfail_value_zero[0]);')
          else:
            print('   ILRxPut_'+signals.upper()+'('+vnim_sig_cfg_data[signals.upper()+'_rx_init_value']+'u);')
            
  print('}\n')
  
  print('''\n/* ===========================================================================
 
  Name:            vnim_tx_il_signal
 
  Description:     Function to Transmit an Interaction Layer Signal
 
  Inputs:          message_id: OS Message ID that Maps to NOS Signal
                   bufptr:     Pointer to Buffer that Holds Signal Data
                               (Up to 8 bytes Maximum)
 
  Returns:         none
 
  =========================================================================*/
void vnim_tx_il_signal (message_id_type message_id, unsigned8 const * bufptr)
{''')
  
  sig_max_count_16 = 0
  sig_max_count_32 = 0
  sig_max_count_64 = 0
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signals in mes['Sig_List']:
        if vnim_sig_cfg_data[signals.upper()+'_tx_debounce'] not in ['on','On',1,'1','ON']:
          if int(mes['Sig_List'][signals]['Len']) > 8 and int(mes['Sig_List'][signals]['Len']) <=16:
            sig_max_count_16 = 1
          elif int(mes['Sig_List'][signals]['Len']) > 16 and int(mes['Sig_List'][signals]['Len']) <=32:
            sig_max_count_32 = 1
          else:
            sig_max_count_64 = 1          
    
  if sig_max_count_16 == 1:
    print('   unsigned16  dataword_U16;')
  if sig_max_count_32 == 1:
    print('   unsigned32  dataword_U32;')
  if sig_max_count_64 == 1:
    print('   unsigned8   dataArray_U8[8] = {0};')
  
  print('   switch(message_id)')
  print('   {')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signals in mes['Sig_List']:
        print('     case VNT_'+signals.upper()+'_MSGID:')
        sig_len = int(mes['Sig_List'][signals]['Len'])
        if sig_len<=8:
          if vnim_sig_cfg_data[signals.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
            print('       '+'Vnim_tx_signal_debounce(VNT_'+signals.upper()+'_MSGID,&bufptr[0]);')
          else:
            print('       '+'ILPutTx_'+signals.upper()+'_data(bufptr[0]);')  
        elif sig_len > 8 and sig_len <= 16:
          if vnim_sig_cfg_data[signals.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
            print('       '+'Vnim_tx_signal_debounce(VNT_'+signals.upper()+'_MSGID,&bufptr[0]);')
          else:
            print('       dataword_U16 = (('+datatype_16+')bufptr[0] << 8);')
            print('       dataword_U16 |= bufptr[1];')
            print('       '+'ILPutTx_'+signals.upper()+'_data(dataword_U16);')
        elif sig_len > 16 and sig_len <= 32:
          if vnim_sig_cfg_data[signals.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
            print('       '+'Vnim_tx_signal_debounce(VNT_'+signals.upper()+'_MSGID,&bufptr[0]);')
          else:
            print('       dataword_U32 = (('+datatype_32+')bufptr[0] << 24);')
            print('       dataword_U32 |= (('+datatype_32+')bufptr[1] << 16);')
            print('       dataword_U32 |= (('+datatype_32+')bufptr[2] << 8);')
            print('       dataword_U32 |= bufptr[3];')
            print('       '+'ILPutTx_'+signals.upper()+'_data(dataword_U32);')
        elif sig_len > 32 and sig_len <= 64:
          if vnim_sig_cfg_data[signals.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
            print('       '+'Vnim_tx_signal_debounce(VNT_'+signals.upper()+'_MSGID,&bufptr[0]);')
          else:
            if signals.upper() == 'GPS_EPOCH_TIMESTAMP' or signals.upper() == 'GPS_MCU_TIMESTAMP':
              print('        nw_host_mgr_inspect_' + signals.upper() + '_data( dataArray_U8 );')
              print('        ILPutTx_' + signals.upper() + '_data( &dataArray_U8[0] );')
            else:
              print('       '+'ILPutTx_'+signals.upper()+'_data(&bufptr[0]);')
        else:
          pass
        print('       break;\n')
    
  print('     default:')
  print('       break;\n')
  print('   }')
  print('}')
    
  print('''\n/* ===========================================================================
 
  Name:            vnim_message_monitoring_periodic
 
  Description:     Function to log/clear message missing and node missing dtc
 
  Inputs:          void
 
  Returns:         none
 
  =========================================================================*/
void vnim_message_monitoring_periodic(void)
{
  unsigned8 idx;
  PRECONDITION_STS vnim_log_cond = PRECONDITION_FALSE;

  if(IS_NM_NODE_MONITORING_ON() == TRUE)
  {
    for(idx =0;idx<NUM_VNIM_MESSAGES ;idx++)
    {
        vnim_log_cond = vnim_precondition_check(idx,VNIM_FAULT_CHECK);    
        if(vnim_content_error_sts[idx]!=0x00)
        {
        MsgDtcFlag[idx]=1u;
        }
        if((MsgDtcFlag[idx] != MsgDtcFlag_previous[idx]) && (vnim_log_cond != PRECONDITION_FALSE)) /* change in the state of DTC */
        {
          if(MsgDtcFlag[idx] == 1) /* DLC error has occured */
          {
            if((idx ==VNIM_VCU5_500_MSGID)&& (Suppress_VINDTC_Logging == TRUE)) 
            {                                                                       
                /* Do Nothing */	                                                                    
            }                                                                       
            else                                                                    
            {  
              if(vnim_msg_node_list[idx] == 0xFF)
              {
                /*Unlog DTC Interface*/
                vnim_msg_content_fault(idx);
              }
              else
              {
                vnim_node_msg_content_fault(vnim_msg_node_list[idx]);
              }
            }                                                                    
          }
          else if(MsgDtcFlag[idx] == 0)/* DLC error is cleared */
          {
              if(vnim_msg_node_list[idx] == 0xFF)
              {
                /*Unlog DTC Interface*/
                vnim_msg_content_gain(idx);
              }
              else
              {
                vnim_node_msg_content_gain(vnim_msg_node_list[idx]);
              }
          }
          else
          {
            /* Do Nothing */
          }
        }
        else
        {
          /* Do Nothing */
        }  
        MsgDtcFlag_previous[idx] = MsgDtcFlag[idx];
    }
  }
  else
  {
    /* Do nothing */
  }

  for(idx=0;idx<NUM_VNIM_MESSAGES ;idx++)
  {
      vnim_log_cond = vnim_precondition_check(idx,VNIM_FAULT_CHECK);
      if (vnim_log_cond != PRECONDITION_FALSE)
      {
          if(vnim_msg_missing_heal_timecnt[idx]!= (unsigned32)0)
          {
            vnim_msg_missing_heal_timecnt[idx]--;
            if(vnim_msg_missing_heal_timecnt[idx] ==(unsigned32) 0)
            {
              if (vnim_msg_healing_msgcnt[idx] ==(unsigned32)0)
              {
                vnim_msg_missing [vnim_msg_byte_position[idx]] &= ((unsigned8)~(vnim_msg_bit_mask[idx]));
                if(vnim_msg_node_list[idx] == 0xFF)
                {
                  /*Unlog DTC Interface*/
                  vnim_message_gain (idx);
                }
                else
                {
                  vnim_node_gain(vnim_msg_node_list[idx]);
                }
              }
              else
              {
                 vnim_msg_missing[vnim_msg_byte_position[idx]] |= vnim_msg_bit_mask[idx];
              }
            }
          }
    }
  }
}

''')


  print('''\n/* ===========================================================================
   Received Interaction Layer Signal Indication Callbacks 
  =========================================================================*/
''')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      msg_name = mes['Msg_name'].upper()
      
      node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
      print('void VnimIlRx_'+msg_name+'_MsgIndication( void )')
      print('{')
      if msg_name != 'EMS5_500':  
        green_en = 0
        signal_content = 0
        no_delay = 0
        for signal in mes['Sig_List']:
          if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
            green_en = 1
          if vnim_sig_cfg_data[signal.upper()+'_signal_content'] in ['on','On',1,'1','ON']:
            signal_content = 1
          if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['No_Delay']:
            no_delay = 1
        if no_delay == 1:
          print('   CAN_UINT8  msg_changed =FALSE;')
        print('   CAN_UINT8  ret= FALSE;') 
        if green_en == 1:
          print('   CAN_UINT8  Greendrive_msg_changed =FALSE;')
        print('   PRECONDITION_STS vnim_notify_sts = PRECONDITION_FALSE;') 
        print('   vnim_notify_sts = vnim_precondition_check(VNIM_'+msg_name+'_MSGID,VNIM_MSG_IND_NOTIFY);')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg'] in ['on','ON',1,'1']:
          print('   if (IS_NM_NODE_MONITORING_ON() == TRUE)')
        else:
          print('   if ((IS_NM_NODE_MONITORING_ON() == TRUE) && ((IS_'+node+'_NODE_MISSING()) == FALSE))')
        print('   {')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg'] in ['on','ON',1,'1']:
          print('       ret = vnim_start_error_healing(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,NODE_ABSENT_HEAL_COUNT);')
        else:
          print('       ret = vnim_start_error_healing(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,MSG_TIMEOUT_HEAL_COUNT);')
        print('       if( ret == TRUE)')
        print('       {')
        for signal in mes['Sig_List']:
          print('           ILSet_'+signal.upper()+'_DataChanged();')
        print('       }')
        if (signal_content == 1):
          print('       /* Check for the signal range for DTC logging, when monitoring is on */')
          if rx_node_cfg[node].upper() == msg_name:
            print('       if (('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+msg_name+'_FC_cfg_st == TRUE) && (IS_'+node+'_NODE_MISSING() == FALSE) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE) && (vnim_notify_sts != PRECONDITION_FALSE))')
          else:
            print('       if (('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+msg_name+'_FC_cfg_st == TRUE) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE) && (vnim_notify_sts != PRECONDITION_FALSE))')
          print('       {')
          for signal in mes['Sig_List']:
            if vnim_sig_cfg_data[signal.upper()+'_signal_content'] in ['on','ON',1,'1']:
              print('           vnim_validate_signal_content_error(NM_'+node+'_NODE,VNIM_'+signal.upper()+'_SIGID);')  
          print('       }')
        print('   }')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg']  in ['on','ON',1,'1']:
          print('   else')
          print('   {')
          print('     /*Do Nothing */')
          print('   }\n')
        else:
          print('   else if((IS_NM_NODE_MONITORING_ON() == TRUE) && (IS_'+node+'_NODE_MISSING() != FALSE))')
          print('   {')
          print('     vnim_stop_error_healing(VNIM_'+msg_name+'_MSGID);')
          print('   }')
          print('   else')
          print('   {')
          print('    /* Do Nothing */')
          print('   }\n')
        print('   if(vnim_notify_sts!= PRECONDITION_FALSE)')
        print('   {')
        print('       if(((IS_NM_NODE_MONITORING_ON() == TRUE) &&') 
        print('          (IS_'+node+'_NODE_MISSING() == FALSE) &&')
        print('          (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE)) ||')
        print('          (IS_NM_NODE_MONITORING_ON() != TRUE))')
        print('      {')
        for signal in mes['Sig_List']:
          print('          if(ILGet_'+signal.upper()+'_DataChanged() != FALSE)')
          print('          {')
          word_str = signal.upper()
          if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['No_Delay']:
            if( (word_str.find('REM_DATA_') == 0) or (word_str == "REM_CRC16") ):
              print('              msg_changed = TRUE;')
            else:
              #if((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('VCU336_COUNTER') == -1) and (word_str.find('VCU337_COUNTER') == -1)):
              if((word_str.find('RES_EXTENSION_COUNTER') != -1) or ((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('_COUNTER') == -1))):
                print('              msg_changed = TRUE;')
          else:
            #if((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('VCU336_COUNTER') == -1) and (word_str.find('VCU337_COUNTER') == -1)):
            if((word_str.find('RES_EXTENSION_COUNTER') != -1) or ((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('_COUNTER') == -1))):
              print('              '+mes['Msg_name'].upper()+'_msg_changed = TRUE;')
          if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
            #if((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('VCU336_COUNTER') == -1) and (word_str.find('VCU337_COUNTER') == -1)):
            if((word_str.find('RES_EXTENSION_COUNTER') != -1) or ((word_str.find('_CRC') == -1) and (word_str.find('_CHECKSUM') == -1) and (word_str.find('_MSG_CNT') == -1) and (word_str.find('_MSG_COUNT') == -1) and (word_str.find('_COUNTER') == -1))):
              print('              Greendrive_msg_changed  = TRUE;')
          
          print('              ILClr_'+signal.upper()+'_DataChanged();')
          print('          }\n')
        if no_delay == 1:    
          print('          if((msg_changed == TRUE) && ('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT))')
          print('          {')
          print('              #if (vnim_notify_used(VNRCL_'+msg_name+'_MSGID) == YES)')
          print('                os_notify(VNRCL_'+msg_name+'_MSGID,0, NULL );')
          print('              #endif')
          print('          }\n') 
        
        if green_en == 1:
          print('          if((Greendrive_msg_changed == TRUE) && ('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT))')
          print('          {')
          print('              #if (vnim_notify_used(VNRCL_GD_'+msg_name+'_MSGID) == YES)')
          print('                os_notify(VNRCL_GD_'+msg_name+'_MSGID,0, NULL );')
          print('              #endif')
          print('          }\n') 
          
        print('      }\n')  
        print('   }\n')    
      else:
        green_en = 0
        signal_content = 0
        for signal in mes['Sig_List']:
          if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
            green_en = 1
          if vnim_sig_cfg_data[signal.upper()+'_signal_content'] in ['on','On',1,'1','ON']:
            signal_content = 1
        print('   PRECONDITION_STS vnim_notify_sts = PRECONDITION_FALSE;') 
        print('   vnim_notify_sts = vnim_precondition_check(VNIM_'+msg_name+'_MSGID,VNIM_MSG_IND_NOTIFY);')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg'] in ['on','ON',1,'1']:
          print('   if (IS_NM_NODE_MONITORING_ON() == TRUE)')
        else:
          print('   if ((IS_NM_NODE_MONITORING_ON() == TRUE) && ((IS_'+node+'_NODE_MISSING()) == FALSE))')
        print('   {')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg'] in ['on','ON',1,'1']:
          print('       (void)vnim_start_error_healing(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,NODE_ABSENT_HEAL_COUNT);')
        else:
          print('       (void)vnim_start_error_healing(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,MSG_TIMEOUT_HEAL_COUNT);')
        if (signal_content == 1):
          print('       /* Check for the signal range for DTC logging, when monitoring is on */')
          if rx_node_cfg[node].upper() == msg_name:
            print('       if (('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+msg_name+'_FC_cfg_st == TRUE) && (IS_'+node+'_NODE_MISSING() == FALSE) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE) && (vnim_notify_sts != PRECONDITION_FALSE))')
          else:
            print('       if (('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+msg_name+'_FC_cfg_st == TRUE) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE) && (vnim_notify_sts != PRECONDITION_FALSE))')
          print('       {')
          for signal in mes['Sig_List']:
            if vnim_sig_cfg_data[signal.upper()+'_signal_content'] in ['on','ON',1,'1']:
              print('           vnim_validate_signal_content_error(VNIM_'+signal.upper()+'_SIGID);')
          print('       }')
        print('   }')
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg']  in ['on','ON',1,'1']:
          print('   else')
          print('   {')
          print('     /*Do Nothing */')
          print('   }\n')
        else:
          print('   else if((IS_NM_NODE_MONITORING_ON() == TRUE) && (IS_'+node+'_NODE_MISSING() != FALSE))')
          print('   {')
          print('     vnim_stop_error_healing(VNIM_'+msg_name+'_MSGID);')
          print('   }')
          print('   else')
          print('   {')
          print('    /* Do Nothing */')
          print('   }\n')
        print('   if(vnim_notify_sts!= PRECONDITION_FALSE)')
        print('   {')
        print('       if(((IS_NM_NODE_MONITORING_ON() == TRUE) &&') 
        print('          (IS_'+node+'_NODE_MISSING() == FALSE) &&')
        print('          (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE)) ||')
        print('          (IS_NM_NODE_MONITORING_ON() != TRUE))')
        print('      {')
          
        print('          if(('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT))')
        print('          {')
        print('              #if (vnim_notify_used(VNRCL_'+msg_name+'_MSGID) == YES)')
        print('                os_notify(VNRCL_'+msg_name+'_MSGID,0, NULL );')
        print('              #endif')
        if green_en == 1:
          print('              #if (vnim_notify_used(VNRCL_GD_'+msg_name+'_MSGID) == YES)')
          print('                os_notify(VNRCL_GD_'+msg_name+'_MSGID,0, NULL );')
          print('              #endif')
        print('          }\n') 
         
        print('      }\n')  
        print('   }\n')    
      print('APP_'+mes['Msg_name'].upper()+'_INDICATION();')
      print('}\n')
    
 
  print('''\n/* ===========================================================================
   Receive Timeout Notifications
  =========================================================================*/''')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      msg_name = mes['Msg_name'].upper()
      node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('void VnimIlRx_'+msg_name+'_Timeout( void )')
        print('{')
        
        if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_key_msg']  in ['on','ON',1,'1']:
          print('   if(IS_NM_NODE_MONITORING_ON() == TRUE) ')
          print('   {')
          print('       vnim_error_detect(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,NODE_ABSENT_ERROR_COUNT);')
          print('   }')
        else:
          print('   if((IS_NM_NODE_MONITORING_ON() == TRUE) && (IS_'+node+'_NODE_MISSING() == FALSE))')
          print('   {')
          print('       vnim_error_detect(VNIM_'+msg_name+'_MSGID,VNIM_'+msg_name+'_MESSAGE,MSG_TIMEOUT_ERROR_COUNT);')
          print('   }')
        green_en = 0
        non_green_drv_sig=''
        green_drv_sig = ''
        for signal in mes['Sig_List']:
          non_green_drv_sig=signal.upper()
          if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
            green_en = 1
            green_drv_sig = signal.upper()
            break
         
        if green_en == 1:
          print('   ILSet_'+green_drv_sig+'_DataChanged();')
        else:
          print('   ILSet_'+non_green_drv_sig+'_DataChanged();')
        print('}\n')
        #print '   vnim_Onfail_Value_update(VNIM_'+msg_name+'_MSGID);'


  
  print('''/* ===========================================================================
 
  Name:            vnim_message_node_gain
 
  Description:     Function to log node gain
 
  Inputs:          node_id
 
  Returns:         none
 
  =========================================================================*/''')
  print('static void vnim_node_gain (unsigned8 node_id)')
  print('{')
  print('   switch (node_id)')
  print('   {')
  for node in node_list:
    print('      case NM_'+node.upper()+'_NODE:')
    print('         if(('+node.upper()+'_node_cfg_st  == CF_OPT_'+node.upper()+'_PRSNT) && ('+rx_node_cfg[node].upper()+'_FC_cfg_st == TRUE))')
    print('         {')
    print('             vnim_dtc_unlog(NM_'+node.upper()+'_NODE,VNIM_NODE_GAIN,VNIM_'+rx_node_cfg[node]+'_MSGID);')
    print('         }')
    for mes in node_msg_list[node]:
      print('         IlEnableRxTimeoutMonitor(VNIM_'+mes.upper()+'_MESSAGE);')
      print('         NM_MSG_GAIN(VNIM_'+mes.upper()+'_MESSAGE);')
    print('         NM_'+node.upper()+'_NODE_GAIN();')
    print('         break;\n')
  print('      default:')
  print('         break;')
  print('   }')
  print('}\n')
  
  print('''/* ===========================================================================
 
  Name:            vnim_message_node_loss
 
  Description:     Function to log node loss
 
  Inputs:          node_id
 
  Returns:         none
 
  =========================================================================*/''')
  print('static void vnim_node_loss (unsigned8 node_id)')
  print('{')
  print('   switch (node_id)')
  print('   {')
  for node in node_list:
    print('      case NM_'+node.upper()+'_NODE:')
    print('         if(('+node.upper()+'_node_cfg_st  == CF_OPT_'+node.upper()+'_PRSNT) && ('+rx_node_cfg[node].upper()+'_FC_cfg_st == TRUE))')
    print('         {')
    print('             vnim_dtc_log(NM_'+node.upper()+'_NODE,VNIM_NODE_LOSS,VNIM_'+rx_node_cfg[node].upper()+'_MSGID);')
    print('         }')
    for mes in node_msg_list[node]:
      print('         vnim_Onfail_Value_update(VNIM_'+mes.upper()+'_MSGID,NW_NODE_ABSENT_FAULT);')
    print('         NM_'+node.upper()+'_NODE_MISSING();')
    print('         break;\n')
  print('      default:')
  print('         break;')
  print('   }')
  print('}\n')
  
  timeout_msg={}
  for mes in il_sorted_mes_rx_ordered:
    if  int(mes['GenMsgCycleTime']) > 0:
      timeout_msg[mes['Msg_name']]='YES'
    else:
      timeout_msg[mes['Msg_name']]='NO'
  
  timeout_msg_cnt={}
  for node in node_list:
    cnt=0
    for mes in node_msg_list[node]:
      if mes.upper() != rx_node_cfg[node].upper():
        if timeout_msg[mes] == 'YES':
          cnt+=1
    timeout_msg_cnt[node]=cnt
  
  print('''/* ===========================================================================
 
  Name:            vnim_message_gain
 
  Description:     Function to log message gain
 
  Inputs:          msg_id
 
  Returns:         none
 
  =========================================================================*/
''')
  print('static void vnim_message_gain(unsigned8 msg_id)')
  print('{')
  print('   switch (msg_id)')
  print('   {')
  for node in node_list:
    indexCount = 0;
    for mes in node_msg_list[node]:
      if mes.upper() != rx_node_cfg[node].upper():
        if timeout_msg[mes] == 'YES':
          indexCount += 1;
          print('      case VNIM_'+mes.upper()+'_MSGID:')
          print('         if(('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+mes.upper()+'_FC_cfg_st == TRUE))')
          print('         {')
          if timeout_msg_cnt[node] <=8:
            print('             Vnim_'+node+'_Timeout_flag &= (unsigned8) (0xFF & ((unsigned8)~VNIM_'+mes.upper()+'_MSGID_BIT));')
          elif timeout_msg_cnt[node] <=16:
            print('             Vnim_'+node+'_Timeout_flag &= (unsigned16) (0xFFFF & ((unsigned16)~VNIM_'+mes.upper()+'_MSGID_BIT));')
          elif timeout_msg_cnt[node] >16 and timeout_msg_cnt[node] <=32:
            print('             Vnim_'+node+'_Timeout_flag &= (unsigned32) (0xFFFFFFF & ((unsigned32)~VNIM_'+mes.upper()+'_MSGID_BIT));')
          else:
            print('             Vnim_'+node+'_Timeout_flag[' + str(indexCount//32) + '] &= (unsigned32) (0xFFFFFFF & ((unsigned32)~VNIM_'+mes.upper()+'_MSGID_BIT));')
                  
          if timeout_msg_cnt[node] <=32:
            print('             if(Vnim_'+node+'_Timeout_flag == 0)')
          else:
            tmpCount = (timeout_msg_cnt[node]//32 + 1);
            if tmpCount == 2:
              print('             if((Vnim_'+node+'_Timeout_flag[0] == 0) && (Vnim_'+node+'_Timeout_flag[1] == 0))')
            else:
              pass
          print('             {')              
          print('                 vnim_dtc_unlog(NM_'+node+'_NODE,VNIM_MSG_GAIN,VNIM_'+mes.upper()+'_MSGID);')
          print('             }')
          print('         }')
          print('         break;\n')
  print('      default:')
  print('         break;')
  print('   }')
  print('   if(msg_id < NUM_VNIM_MESSAGES)')
  print('   {')
  print('       NM_MSG_GAIN(msg_id);')
  print('   }')
  print('}\n')
  
  print('''/* ===========================================================================
 
  Name:            vnim_message_loss
 
  Description:     Function to log message loss
 
  Inputs:          msg_id
 
  Returns:         none
 
  =========================================================================*/''')
  print('static void vnim_message_loss(unsigned8 msg_id)')
  print('{')
  print('   switch (msg_id)')
  print('   {')
  for node in node_list:
    indexCount = 0;
    for mes in node_msg_list[node]:
      if mes.upper() != rx_node_cfg[node].upper():
        if timeout_msg[mes] == 'YES':
          indexCount += 1;
          print('      case VNIM_'+mes.upper()+'_MSGID:')            
          print('         if(('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && ('+mes.upper()+'_FC_cfg_st == TRUE))')
          print('         {')
          if timeout_msg_cnt[node] <=8:
            print('             Vnim_'+node+'_Timeout_flag |= (unsigned8)VNIM_'+mes.upper()+'_MSGID_BIT;')
          elif timeout_msg_cnt[node] <=16:  
            print('             Vnim_'+node+'_Timeout_flag |= (unsigned16)VNIM_'+mes.upper()+'_MSGID_BIT;')
          elif timeout_msg_cnt[node] <=32:  
            print('             Vnim_'+node+'_Timeout_flag |= (unsigned32)VNIM_'+mes.upper()+'_MSGID_BIT;')
          else:
            print('             Vnim_'+node+'_Timeout_flag[' + str(indexCount//32) + '] |= (unsigned32)VNIM_'+mes.upper()+'_MSGID_BIT;')
          print('             vnim_Onfail_Value_update(msg_id,NW_MSG_MISSING_FAULT);')
          print('             vnim_dtc_log(NM_'+node+'_NODE,VNIM_MSG_LOSS,VNIM_'+mes.upper()+'_MSGID);')
          print('         }')
          print('         break;\n')
  print('      default:')
  print('             break;')
  print('   }')
  print('   if(msg_id < NUM_VNIM_MESSAGES)')
  print('   {')
  print('       NM_MSG_MISSING(msg_id);')
  print('   }')
  print('}')      
  
  print('''/* ===========================================================================
 
  Name:            vnim_node_msg_content_gain
 
  Description:     Function to log node dlc gain
 
  Inputs:          node_id
 
  Returns:         none
 
  =========================================================================*/''')
  print('void vnim_node_msg_content_gain (unsigned8 node_id)')
  print('{')
  print('   switch (node_id)')
  print('   {')
  for node in node_list:
    print('      case NM_'+node+'_NODE:')
    print('         if(('+node+'_node_cfg_st  == CF_OPT_'+node+'_PRSNT) && ('+rx_node_cfg[node].upper()+'_FC_cfg_st == TRUE) && (IS_'+node+'_NODE_MISSING() == FALSE))')
    print('         {')
    print('            vnim_dtc_unlog(NM_'+node+'_NODE,VNIM_KEYMSG_CONTENT_GAIN,VNIM_'+rx_node_cfg[node].upper()+'_MSGID); ')
    print('         }')
    print('         NM_'+node+'_NODE_DLC_VALID();')
    print('         NM_MSG_DLC_VALID(VNIM_'+rx_node_cfg[node].upper()+'_MSGID);')
    print('         break;\n')
  print('      default:')
  print('         break;')
  print('   }')
  print('}\n')
  
  print('''/* ===========================================================================
 
  Name:            vnim_node_msg_content_fault
 
  Description:     Function to log node dlc fault
 
  Inputs:          node_id
 
  Returns:         none
 
  =========================================================================*/
''')
  print('void vnim_node_msg_content_fault (unsigned8 node_id)')
  print('{')
  print('   switch (node_id)')
  print('   {')
  for node in node_list:
    print('      case NM_'+node+'_NODE:')
    print('         if(('+node+'_node_cfg_st  == CF_OPT_'+node+'_PRSNT) && ('+rx_node_cfg[node].upper()+'_FC_cfg_st == TRUE) && (IS_'+node+'_NODE_MISSING() == FALSE))')
    print('         {')
    print('            vnim_dtc_log(NM_'+node+'_NODE,VNIM_KEYMSG_CONTENT_FAULT,VNIM_'+rx_node_cfg[node].upper()+'_MSGID); ')
    print('         }')
    for mes in node_msg_list[node]: 
      print('         vnim_Onfail_Value_update(VNIM_'+mes.upper()+'_MSGID,NW_NODE_DLC_MISMATCH_FAULT);') 
    print('         NM_'+node+'_NODE_DLC_INVALID();')
    print('         NM_MSG_DLC_INVALID(VNIM_'+rx_node_cfg[node].upper()+'_MSGID);')
    print('         break;\n')
  print('      default:')
  print('         break;')
  print('   }')
  print('}\n')

  print('''/* ===========================================================================
 
  Name:            vnim_msg_content_gain
 
  Description:     Function to log message gain
 
  Inputs:          msg_id
 
  Returns:         none
 
  =========================================================================*/
''')
  print('void vnim_msg_content_gain (unsigned8 msg_id)')
  print('{')
  print('   switch(msg_id)')
  print('   {')
  for node in node_list:
    for mes in node_msg_list[node]:
      if mes.upper() != rx_node_cfg[node].upper():
        print('      case VNIM_'+mes.upper()+'_MSGID:')
        print('          if(('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && (IS_'+node+'_NODE_MISSING() == FALSE) && (IS_'+node+'_NODE_DLC_INVALID() == FALSE) && ('+mes.upper()+'_FC_cfg_st == TRUE))')  
        print('          {')
        print('              vnim_dtc_unlog(NM_'+node+'_NODE,VNIM_MSG_CONTENT_GAIN,msg_id);')
        print('          }')
        print('          break;\n')
  print('      default:')
  print('          break;')
  print('   }')
  print('   if(msg_id < NUM_VNIM_MESSAGES)')
  print('   {')
  print('      NM_MSG_DLC_VALID(msg_id);')
  print('   }')

  print('}\n')
  
  print('''/* ===========================================================================
 
  Name:            vnim_msg_content_fault
 
  Description:     Function to log message loss
 
  Inputs:          msg_id
 
  Returns:         none
 
  =========================================================================*/''')
  print('void vnim_msg_content_fault(unsigned8 msg_id)')
  print('{')
  print('   switch(msg_id)')
  print('   {')
  for node in node_list:
    for mes in node_msg_list[node]:
      if mes.upper() != rx_node_cfg[node].upper():
        print('      case VNIM_'+mes.upper()+'_MSGID:')
        print('          if(('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && (IS_'+node+'_NODE_MISSING() == FALSE) && (IS_'+node+'_NODE_DLC_INVALID() == FALSE) && ('+mes.upper()+'_FC_cfg_st == TRUE))')
        print('          {')
        print('              vnim_dtc_log(NM_'+node+'_NODE,VNIM_MSG_CONTENT_FAULT,msg_id);') 
        print('          }')
        print('          break;\n')
  print('      default:')
  print('          break;')
  print('   }')
  print('   if(msg_id < NUM_VNIM_MESSAGES)')
  print('   {')
  print('       vnim_Onfail_Value_update(msg_id,NW_DLC_MISMATCH_FAULT);')
  print('       NM_MSG_DLC_INVALID(msg_id);')
  print('   }')
  print('}\n')
  
  print('''\n/* ===========================================================================
 
  Name:            vnim_Onfail_Value_update
 
  Description:     Function to update on fail values and notify the OS
 
  Inputs:          msg_id,payload
 
  Returns:         none
 
  =========================================================================*/
''')
  print('void vnim_Onfail_Value_update (unsigned8 msg_id,unsigned8 payload)')
  print('{')
  print('   PRECONDITION_STS vnim_notify_sts = PRECONDITION_NONE;')
  print('   unsigned8 vnim_fault_sts;\n')
  print('   /*if(msg_id < NUM_VNIM_MESSAGES)')
  print('   {')
  print('       vnim_notify_sts = vnim_precondition_check(msg_id,VNIM_MSG_TO_NOTIFY);')
  print('   }*//*ssuresh9*/')
  print('   vnim_fault_sts = payload;/*QAC FIX*/\n')
  print('   switch (msg_id)')
  print('   {')
  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      msg_name=mes['Msg_name'].upper()
      node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
      print('       case VNIM_'+msg_name+'_MSGID:')
      for signals in mes['Sig_List']:
        if int(mes['Sig_List'][signals]['Len']) <=32:
          print('         ILRxPut_'+signals.upper()+'('+vnim_sig_cfg_data[signals.upper()+'_rx_init_value']+'u);')
        else:
          print('         ILRxPut_'+signals.upper()+'(&Onfail_value_zero[0]);')

      print('         if((NW_MSG_MISSING_FAULT==vnim_fault_sts)||(NW_NODE_ABSENT_FAULT==vnim_fault_sts))')
      print('         {')
      print('          NM_MSG_MISSING(VNIM_'+msg_name+'_MSGID);')
      print('         }')
      green_en = 0
      non_green_drv_sig=''
      green_drv_sig = ''
      for signal in mes['Sig_List']:
        non_green_drv_sig=signal.upper()
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
          green_drv_sig = signal.upper()
          break
       
      if green_en == 1:
        print('         ILSet_'+green_drv_sig+'_DataChanged();')
      else:
        print('         ILSet_'+non_green_drv_sig+'_DataChanged();')
      
      print('         if(('+node+'_node_cfg_st==CF_OPT_'+node+'_PRSNT) && ('+msg_name+'_FC_cfg_st == TRUE) && (vnim_notify_sts!= PRECONDITION_FALSE))')
      print('         {')
      print('             #if(vnim_notify_used(VNRO_'+msg_name+'_MSGID) == YES)')
      print('                 os_notify(VNRO_'+msg_name+'_MSGID,0, &vnim_fault_sts );')
      print('             #endif')
      print('         }')
      print('         break;\n')
  print('       default:')
  print('         VNIM_UNUSED_PARAM(vnim_fault_sts);/*QAC FIX*/')
  print('         break;\n')
  print('   }')
  print('}')
  
            
  print('''/* ===========================================================================
  
   Name:            vnim_ipcl_reqdata_process
  
   Description:     Function to send the request data to host through IPCL
                    whenever HMI needs some data from CAN frame then those 
                    request are satisfied with this function
  
   Inputs:          ipcl_index
  
   Returns:         none
  
   =========================================================================*/
''')
  print('void vnim_ipcl_reqdata_process(unsigned8 ipcl_index)')
  print('{')
  print('     unsigned8 vnim_msgid;\n')
  print('     switch (ipcl_index)')
  print('     {\n')
  all_data_change_list = []
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      msg_name = mes['Msg_name'].upper()
      node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
      
      green_en = 0
      non_green_drv_sig=''
      green_drv_sig = ''
      for signal in mes['Sig_List']:
        non_green_drv_sig=signal.upper()
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
          green_drv_sig = signal.upper()
          break
          
      print('     case '+msg_name+'_IPCL_INDEX:')
      if green_en == 1:
        print('         ILSet_'+green_drv_sig+'_DataChanged();')
        all_data_change_list.append(green_drv_sig)
      else:
        print('         ILSet_'+non_green_drv_sig+'_DataChanged();')
        all_data_change_list.append(non_green_drv_sig)
      
      print('         if( IS_MSG_MISSING(VNIM_'+msg_name+'_MSGID) == TRUE)')
      print('         {')
      print('             vnim_Onfail_Value_update(VNIM_'+msg_name+'_MSGID,NW_MSG_MISSING_FAULT) ; /* Notify the missing to Host */')
      print('         }')
      print('         break;\n')
    
  print('     case ALL_RX_FRAME_IPCL_INDEX:')
  for sig in all_data_change_list:
    print('         ILSet_'+sig+'_DataChanged();')
  print('         /* Check the missing frame and notify the same to host*/')
  print('         for(vnim_msgid=0;vnim_msgid<NUM_VNIM_MESSAGES;vnim_msgid++ )')
  print('         {')
  print('             if( IS_MSG_MISSING(vnim_msgid) == TRUE )')
  print('             {')
  print('                 vnim_Onfail_Value_update(vnim_msgid,NW_MSG_MISSING_FAULT) ;/* Notify the missing to Host */')
  print('             }')
  print('         }')
  print('         break;\n')
  print('     default:')
  print('         break;\n')
  print('   }')
  print('}')
  
  
  print('''/* ===========================================================================
 
  Name:            vnim_hmi_rx_signal_inspect
 
  Description:     Function to copy the message buffer from IL to HMI buffer
 
  Inputs:          msg_id -- OS message Id corresponding to that of message
                   bufptr -- pointer to HMI appln buffer.
 
  Returns:         none
 
  =========================================================================*/''')
  
  print('void vnim_hmi_rx_signal_inspect (message_id_type msg_id, unsigned8 *bufptr)')
  print('{')
  print('   CAN_UINT8 *storeptr;')
  print('   CAN_UINT8 size;\n')
  print('   switch (msg_id)')
  print('   {')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      msg_name = mes['Msg_name'].upper()
      node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
      green_en = 0
      for signal in mes['Sig_List']:
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
      print('     case VNRO_'+msg_name+'_MSGID:')
      print('     case VNRCL_'+msg_name+'_MSGID:')
      if green_en == 1:
        print('     case VNRCL_GD_'+msg_name+'_MSGID:')
      print('         storeptr = &'+msg_name+'.msg_buffer[0];')
      print('         size = sizeof('+msg_name+'_msgType);')
      print('         break;\n')
    
  print('     default:')
  print('       storeptr = NULL;')
  print('       break;\n')
  print('   }')
  print('   if (storeptr != NULL)')
  print('   {')
  print('       Copy_Buffer(storeptr, bufptr, size);')
  print('   }')
  print('}')
  

  print('''static void vnim_error_detect (unsigned8 vnim_msgid, unsigned8 il_msgid, unsigned16 cnt)
{
   PRECONDITION_STS vnim_notify_sts = PRECONDITION_FALSE;
   vnim_notify_sts = vnim_precondition_check(vnim_msgid,VNIM_FAULT_CHECK);
   VNIM_UNUSED_PARAM(il_msgid);/*QAC Fix*/
   VNIM_UNUSED_PARAM(cnt);/*QAC Fix*/
   if (vnim_notify_sts != PRECONDITION_FALSE)
   {
      if(vnim_msg_node_list[vnim_msgid] == 0xFF)
      {
          vnim_message_loss (vnim_msgid);
          /*LOGDTC interface*/
      }
      else
      {
          vnim_node_loss(vnim_msg_node_list[vnim_msgid]);
      }

      vnim_msg_missing[vnim_msg_byte_position[vnim_msgid]] |= vnim_msg_bit_mask[vnim_msgid];
      
      if(vnim_msg_missing_heal_timecnt[vnim_msgid] != (unsigned32)0)
      {
          vnim_msg_missing_heal_timecnt[ vnim_msgid] = 0;
          vnim_msg_healing_msgcnt[vnim_msgid] = 0;
      }
   }
}

static unsigned8 vnim_start_error_healing (unsigned8 vnim_msgid, unsigned8 il_msgid, unsigned16 cnt)
{
    unsigned8 ret = FALSE;
    unsigned16 periodicity = 0;
    unsigned8 node_msg_heal_count_tolerance = 0;
    
    VNIM_UNUSED_PARAM(il_msgid);/*QAC Fix*/
    VNIM_UNUSED_PARAM(cnt);/*QAC Fix*/
    
    if(( (vnim_msg_missing [vnim_msg_byte_position[vnim_msgid]]) & (vnim_msg_bit_mask[vnim_msgid]) ) == (vnim_msg_bit_mask[vnim_msgid]) )
    {
      
      if(vnim_msg_node_list[vnim_msgid] == 0xFF)
      {
        periodicity = ((il_rx_frame_table[il_msgid].timeOut) * IL_TASK_PERIOD_MS)/( MSG_TIMEOUT_ERROR_COUNT);/* for extracting the periodicity */
        vnim_msg_missing_heal_timecnt[vnim_msgid]= (periodicity * MSG_TIMEOUT_HEAL_COUNT) / (IL_TASK_PERIOD_MS);/* loading the heal count */
      }
      else
      {
        periodicity = (((il_rx_frame_table[il_msgid].timeOut) * IL_TASK_PERIOD_MS)/( NODE_ABSENT_ERROR_COUNT));/* for extracting the periodicity */
        vnim_msg_missing_heal_timecnt[vnim_msgid]= (periodicity *NODE_ABSENT_HEAL_COUNT) / (IL_TASK_PERIOD_MS);        /* loading the heal count */
      }
		
      vnim_msg_missing [vnim_msg_byte_position[vnim_msgid]] &=((unsigned8) ~(vnim_msg_bit_mask[vnim_msgid]));

      node_msg_heal_count_tolerance = (cnt*MSG_PERIODICITY_TOLERANCE)/MSG_PERCENTAGE; 
      vnim_msg_healing_msgcnt[vnim_msgid] = (cnt - (node_msg_heal_count_tolerance+1)); /* (+1) -> First received message need to consider*/

      ret = TRUE;
    }
    else
    {
        
        if(vnim_msg_healing_msgcnt[vnim_msgid] > (unsigned32)0)
        {  
            vnim_msg_healing_msgcnt[vnim_msgid]--;
        }
    }
    return (ret);
}

static void vnim_stop_error_healing (unsigned8 vnim_msgid)
{
    vnim_msg_missing_heal_timecnt[vnim_msgid] = 0;
  /*   vnim_msg_missing [vnim_msg_byte_position[vnim_msgid]] &= */
/*         ((unsigned8)~(vnim_msg_bit_mask[vnim_msgid]));       */
    vnim_msg_healing_msgcnt[vnim_msgid] = 0;
}

''')
  
  
  print('''/* ===========================================================================
  
   Name:            vnim_signalTO_IPCL_process
  
   Description:     Function to send the message  from VIP to Host.
                    Due to IPCL load few of the message with less periodicity are delayed and processed at 100ms  
  
   Inputs:          None  
  
   Returns:         none
  
   =========================================================================*/
''')
  print('void vnim_signalTO_IPCL_process(void)')
  print('{\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Msg_name'].upper() != 'EMS5_500':
        msg_name=mes['Msg_name'].upper()
        node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
        delay = 0
        for signal in mes['Sig_List']:
          if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['200ms_Delay_g1']:
            delay=1
            break
            
        if delay == 1:
          print('   /* '+msg_name+' signal notification to host */')
          print('   if(('+msg_name+'_msg_changed == TRUE) && ('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE))')
          print('   {')
          print('       #if (vnim_notify_used(VNRCL_'+msg_name+'_MSGID) == YES)')
          print('           os_notify(VNRCL_'+msg_name+'_MSGID,0, NULL );')
          print('       #endif')
          print('       '+msg_name+'_msg_changed = FALSE;')
          print('   }\n')
      
  print('}\n')


  print('''/* ===========================================================================
  
  Name:            vnim_signalTO_IPCL_145ms
  
  Description:     Function to send the message  from VIP to Host.
                    Due to IPCL load few of the message with less periodicity are delayed and processed at 145ms  
  
  Inputs:          None  
  
  Returns:         none
  
  =========================================================================*/''')
  print('void vnim_signalTO_IPCL_145ms(void)')
  print('{\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Msg_name'].upper() != 'EMS5_500':
        msg_name=mes['Msg_name'].upper()
        node = vnim_msg_cfg_data[mes['Msg_name'].upper()+'_node_name']
        delay = 0
        for signal in mes['Sig_List']:
          if vnim_sig_cfg_data[signal.upper()+'_os_notify_no_of_events'] in ['200ms_Delay_g2']:
            delay=1
            break
        if delay==1:
          print('   /* '+msg_name+' signal notification to host */')
          print('   if(('+msg_name+'_msg_changed == TRUE) && ('+node+'_node_cfg_st == CF_OPT_'+node+'_PRSNT) && (IS_'+node+'_DLC_FAULT(VNIM_'+msg_name+'_MSGID) == FALSE))')
          print('   {')
          print('       #if (vnim_notify_used(VNRCL_'+msg_name+'_MSGID) == YES)')
          print('           os_notify(VNRCL_'+msg_name+'_MSGID,0, NULL );')
          print('       #endif')
          print('       '+msg_name+'_msg_changed = FALSE;')
          print('   }\n')
  
  print('}\n')
  
  print('''/* ===========================================================================
   
   Name:            vnim_signalTO_IPCL
   
   Description:     Function to send the message  from VIP to Host.
                     Due to IPCL load few of the message with less periodicity are delayed and processed   
   
   Inputs:          None  
   
   Returns:         none
   
   =========================================================================*/''')
  print('void vnim_signalTO_IPCL(void)')
  print('{\n')
  print('   if(vnim_high_prior_data == FALSE)')
  print('   {')
  print('       vnim_signalTO_IPCL_145ms();')
  print('       vnim_high_prior_data = TRUE;')
  print('   }')
  print('   else')
  print('   {')
  print('       vnim_signalTO_IPCL_process();')
  print('       vnim_high_prior_data = FALSE;')
  print('   }\n')
  print('}\n')

  print('''/* ===========================================================================
 
  Name:            vnim_dlcmonitor_enable
 
  Description:     Function to clear intialize the flag used for message DLC 
                   fault monitoring.
 
  Inputs:          msg_id - message id for which the flag has to be cleared.
                   status - status of dlc fault dtc
 
  Returns:         none
 
  =========================================================================*/
void vnim_dlcmonitor_enable(unsigned8 msg_id,unsigned8 status)
{
  MsgDtcFlag_previous[msg_id]=status;
  IlClrDlcCount(msg_id);     
}''')


  print('''/* ===========================================================================
 
  Name:            vnim_is_message_missing
 
  Description:     Function to return the missing status of RX messages
 
  Inputs:          msg_id - message id for which the missing flag has to be checked
 
  Returns:         TRUE/FALSE
 
  =========================================================================*/

  BOOL vnim_is_message_missing(unsigned8 vnim_msgid)
  {
    BOOL status;
    if(IS_MSG_MISSING(vnim_msgid)||IS_MSG_DLC_INVALID(vnim_msgid))
    {
      status = (BOOL)TRUE;
    }
    else
    {
      status = (BOOL)FALSE;
    }
    return(status);
  } ''')
   
def vnim_app_c_gen():
  global footer,vnim_code_gen_dir,tp_generic_config,nm_generic_config,il_generic_config
  dir = './CODE_GEN'
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("nw_vnim_app_signals_par.c")
  
  header = '''/* ============================================================================
  
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
    written authorization of Visteon Corporation. tested
  
   =========================================================================*/
  
   /*===========================================================================
  
    Name:           nw_vnim_app_signals_par.c
  
    Description:    VNIM Application Signals
  
    Organization:   Visteon Technical and Services Center
  
   =========================================================================*/
'''
  print(header,'\n\n')
  includes='''#include "types.h" 
#include "can_type.h"
#include "can_defs.h" 
#include "os_if.h"
#include "utility.h"
#include "nw_nm_par.h"
#include "diag_if.h"
#include "nw_nm.h"
#include "nw_il.h"
#include "nw_vnim_app_signals.h"
#include "nw_il_par.h"
#include "vnim_resource.h"
#include "cf_options_if.h"
#include "vnim_if.h"
#include "nw_host_mgr_if.h"
#include "nw_ipcl_cfg.h"
#include "nw_il_msg.h"
#include "nw_vnim_net.h"
#include "vnim_interface.h"
#include "vnim_dummy.h"
'''
  print(includes)
  
  msg_order_enum_gen()

  print('\n',footer)
  close_output(f)

def vnim_app_h_gen():
  global footer,vnim_code_gen_dir,tp_generic_config,nm_generic_config,il_generic_config 
  
  dir = './CODE_GEN'
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("nw_vnim_app_signals_par.h")
  
  header ='''#if !defined(NW_VNIM_APP_SIGNALS_PAR_H)
#define NW_VNIM_APP_SIGNALS_PAR_H
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
 
  =========================================================================*/'''
  print(header)
  print('/* INCLUDES */')
  print('#include "nw_vnim_nvm.h"\n\n')
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcSigConfiguration.data",'r',encoding='utf-8')
  vnim_sig_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  il_msg_tx=[]
  il_msg_rx=[]
  
   
  all_message_tx = dbc.get_msg_type(full_msg,'tx')
  for mes in all_message_tx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_tx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_tx.append(mes)
      
  
  il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  
  all_message_rx = dbc.get_msg_type(full_msg,'rx')
  for mes in all_message_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_rx.append(mes)
      
  il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
  
  node_list=[]
  rx_node_cfg={}
  #msg_list=[]
  node_msg_list={}
  for mes in il_sorted_mes_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_key_msg'] in ['on','ON','On',1,'1']:
      rx_node_cfg[vnim_msg_cfg_data[mes['Msg_name']+'_node_name']] = mes['Msg_name']
      if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_list:
        node_list.append(vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper())
    if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_msg_list:      
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()]=[mes['Msg_name']]
    else:
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()].append(mes['Msg_name'])
          
  message_order = []
  timeout_list ={}
  
  il_sorted_mes_rx_ordered = []
  for nd in node_list:
    #il_sorted_mes_rx_ordered.append(rx_node_cfg[nd])
    message_order.append(rx_node_cfg[nd])
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        message_order.append(mes)
        
  
  for order_msg in  message_order:
    for mes in il_sorted_mes_rx:
      if mes['Msg_name'] == order_msg:
        il_sorted_mes_rx_ordered.append(mes)
        
  for nd in node_list:  
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        for mes_prop in il_sorted_mes_rx_ordered:
          if int(mes_prop['GenMsgCycleTime']) !=0:
              timeout_list[nd]=1
              break
      
  sig_id=[]
  sig_dtd_fault_id={}
  message_sig_list={}
  
  for mes in il_sorted_mes_rx_ordered:
    sig_list=[]
    for signal in mes['Sig_List']:  
      mes['Sig_List'][signal]['Sig_name']=signal
      sig_list.append(mes['Sig_List'][signal])
    sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit']))
    
    for sig in sig_list:
      if vnim_sig_cfg_data[sig['Sig_name'].upper()+'_signal_content'] in ['on','ON','On',1,'1']:
        sig_id.append('VNIM_'+sig['Sig_name'].upper()+'_SIGID')
        sig_dtd_fault_id['VNIM_'+sig['Sig_name'].upper()+'_SIGID']=vnim_sig_cfg_data[sig['Sig_name'].upper()+'_signal_fault_id']
        if mes['Msg_name'] not in message_sig_list:
          message_sig_list[mes['Msg_name']] =['VNIM_'+sig['Sig_name'].upper()+'_SIGID']
        else:
          message_sig_list[mes['Msg_name']].append('VNIM_'+sig['Sig_name'].upper()+'_SIGID')
        
  print('\n /*Signal fault Id list*/')
  print('typedef enum')
  print('{')
  for id in sig_id:
    print('   '+id+',')
  print('   NUM_VNIM_SIGCONT_SIGNALS,')
  print('   VNIM_SIGNAL_FAULT_NONE')
  print('}VNIM_SIGNAL_FAULT;\n')
  
  
      
  print('''/*VNIM Message ENUM*/''')
  print('enum')
  print('{')  
  for node in node_list:
    if len(node_msg_list[node]) > 1:
      print('   VNIM_'+rx_node_cfg[node].upper()+'_MSGID,/*'+node+' Key msg - '+node+' msg start Index*/')
      cnt =0
      for mes in node_msg_list[node]:
        if mes.upper() != rx_node_cfg[node].upper():
          if cnt == (len(node_msg_list[node])-1):
            print('   VNIM_'+mes.upper()+'_MSGID,/*'+node+' msg stop index*/')
          else:
            print('   VNIM_'+mes.upper()+'_MSGID,')
        cnt+=1
    else:
      print('   VNIM_'+rx_node_cfg[node].upper()+'_MSGID,/*'+node+' Key msg - '+node+' msg start/Stop Index*/')
  print('   NUM_VNIM_MESSAGES')
  print('};\n')
  
  
  
  print('/*VNIM NODE LIST*/')
  print('#define VNIM_NODE_LIST  \\')
  node_cnt = 0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   NM_'+node.upper()+'_NODE         /*'+rx_node_cfg[node]+'*/ ', end=' ')
    else:
      print('   NM_'+node.upper()+'_NODE,         /*'+rx_node_cfg[node]+'*/ \\')
    msg_cnt=0
    for mes in node_msg_list[node]:
        if mes.upper() != rx_node_cfg[node].upper():
          if msg_cnt == (len(node_msg_list[node])-1) and node_cnt == (len(node_list)-1):
            print(',\\')
            print('   0xFF         /*'+mes.upper()+'*/ ')
          else:
            print('   0xFF,         /*'+mes.upper()+'*/ \\')
        msg_cnt+=1
    node_cnt+=1
  print('  ')
    
  
  
  
  print('\n') 
  print('/*Node Absent Dtc ID*/')
  print('#define VNIM_NODE_ABSENT_DTC_IDS   \\')
  node_cnt = 0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   '+vnim_msg_cfg_data[rx_node_cfg[node]+'_node_absent'])
    else:
      print('   '+vnim_msg_cfg_data[rx_node_cfg[node]+'_node_absent']+',  \\')
    node_cnt+=1
  print('\n')
  
  
  
  print('\n') 
  print('/*Message Missing Dtc ID*/')
  print('#define VNIM_MSG_TIMEOUT_DTC_IDS   \\')
  node_cnt = 0
  for node in node_list:
    if len(node_msg_list[node])>1:
      diag_id='0xFF'
      id_list=[]
      for mes in node_msg_list[node]:
        if mes.upper() != rx_node_cfg[node].upper():
          if vnim_msg_cfg_data[mes+'_msg_timeout'] != '':
            id_list.append(vnim_msg_cfg_data[mes+'_msg_timeout'])
          else:
            id_list.append('DUMMY_DTC_ID')
            
      list_dict=Py2Dict()
      for id in id_list:
        if id not in list_dict:
          list_dict[id]=1
        else:
          list_dict[id]+=1
          
      if len(list_dict)>1 and "DUMMY_DTC_ID" in list_dict:
        list_dict["DUMMY_DTC_ID"] = 0
        
      diag_id=max(list_dict.keys(), key=lambda k: list_dict[k])

      if node_cnt == (len(node_list)-1):
        print('   '+diag_id)
      else:
        print('   '+diag_id+',  \\')
    else:
      if node_cnt == (len(node_list)-1):
        print('   DUMMY_DTC_ID')
      else:
        print('   DUMMY_DTC_ID, \\')
    node_cnt+=1
  print('\n')
  
  
  print('/*VNIM MSG CONTENT FAILURE DTC LISTS*/')
  print('#define VNIM_MSG_CONTENT_FAILURE_DTC_IDS  \\')
  node_cnt = 0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   '+vnim_msg_cfg_data[rx_node_cfg[node]+'_msg_dlc'], end=' ')
    else:
      print('   '+vnim_msg_cfg_data[rx_node_cfg[node]+'_msg_dlc']+',    \\')
    msg_cnt=0
    for mes in node_msg_list[node]:
        if mes.upper() != rx_node_cfg[node].upper():
          if msg_cnt == (len(node_msg_list[node])-1) and node_cnt == (len(node_list)-1):
            print(',\\')
            print('   '+vnim_msg_cfg_data[mes+'_msg_dlc'])
          else:
            print('   '+vnim_msg_cfg_data[mes+'_msg_dlc']+',    \\')
        msg_cnt+=1
    node_cnt+=1
  print(' ')
  
  print('\n/*Signal Fault DTC ID*/')
  print('#define VNIM_SIGNAL_CONTENT_FAILURE_DTC_IDS  \\')
  sig_cnt = 0
  for id in sig_id:
    if sig_cnt == (len(sig_id)-1):
      print('   '+sig_dtd_fault_id[id])
    else:
      print('   '+sig_dtd_fault_id[id]+',   \\')
    sig_cnt+=1
    
    
  print('\n/*VNIM_SIGNAL_FAULT_LIST - {start signal fault id,end signal fault id}*/')
  print('#define VNIM_SIGNAL_FAULT_LIST \\')
  msg_cnt=0
  for mes in il_sorted_mes_rx_ordered:
    if mes['Msg_name'] not in message_sig_list:
      if msg_cnt == (len(il_sorted_mes_rx_ordered)-1):
        print('   {VNIM_SIGNAL_FAULT_NONE,VNIM_SIGNAL_FAULT_NONE}   /*'+mes['Msg_name']+' msg*/')
      else:
        print('   {VNIM_SIGNAL_FAULT_NONE,VNIM_SIGNAL_FAULT_NONE},   /*'+mes['Msg_name']+' msg*/ \\')
        
    else:
      if msg_cnt == (len(il_sorted_mes_rx_ordered)-1):
        print('   {'+message_sig_list[mes['Msg_name']][0]+','+message_sig_list[mes['Msg_name']][len(message_sig_list[mes['Msg_name']])-1]+'}   /*'+mes['Msg_name']+' msg*/ ') 
      else:
        print('   {'+message_sig_list[mes['Msg_name']][0]+','+message_sig_list[mes['Msg_name']][len(message_sig_list[mes['Msg_name']])-1]+'},   /*'+mes['Msg_name']+' msg*/ \\') 
        
    msg_cnt+=1
    
  print('\n /*VNIM_MSG_LIST - {NODE ID,Start mes id of node,End mes id of node}*/')
  print('#define VNIM_MSG_LIST   \\')
  node_cnt=0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   {NM_'+node.upper()+'_NODE , VNIM_'+rx_node_cfg[node].upper()+'_MSGID  , VNIM_'+node_msg_list[node][len(node_msg_list[node])-1].upper()+'_MSGID}')
    else:
      print('   {NM_'+node.upper()+'_NODE , VNIM_'+rx_node_cfg[node].upper()+'_MSGID  , VNIM_'+node_msg_list[node][len(node_msg_list[node])-1].upper()+'_MSGID},   \\')
    node_cnt+=1
  
  print('''\n/* ===========================================================================
   P U B L I C   F U N C T I O N   P R O T O T Y P E S
  =========================================================================*/
''')
  print('''void vnim_tx_il_signal (message_id_type message_id,unsigned8 const * bufptr);
void vnim_message_monitoring_periodic(void);
void vnim_message_mon_init (void);
void vnim_set_init_signals (void);
void vnim_Onfail_Value_update (unsigned8 msg_id,unsigned8 payload);
void vnim_ipcl_reqdata_process (unsigned8 ipcl_index);
void vnim_signalTO_IPCL(void);
void vnim_clr_missing(void);
void vnim_app_init(void);
void vnim_clr_missing(void);
void vnim_dlcmonitor_enable(unsigned8 msg_id,unsigned8 status); 
void vnim_node_msg_content_fault (unsigned8 node_id);
void vnim_node_msg_content_gain (unsigned8 node_id);
void vnim_msg_content_fault (unsigned8 msg_id);
void vnim_msg_content_gain (unsigned8 msg_id);
BOOL vnim_is_message_missing(unsigned8 vnim_msgid);
''')

  print('''\n/* ===========================================================================
   VNIM MISSING_INTERFACES
  =========================================================================*/
''')
  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
      sig_list=[]
      for signal in mes['Sig_List']:  
        mes['Sig_List'][signal]['Sig_name']=signal
        sig_list.append(mes['Sig_List'][signal])
    
      for sig in sig_list:
         print('#define VNIM_IS_'+sig['Sig_name'].upper()+'_MISSING()    vnim_is_message_missing(VNIM_'+mes['Msg_name']+'_MSGID)')  
        

  print('#endif\n')
  print(footer)
  
  close_output(f)
  
def vnim_resource_gen():
  global dbc,datatype_8,datatype_16,datatype_16,vnim_code_gen_dir,vnim_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcSigConfiguration.data",'r',encoding='utf-8')
  vnim_sig_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  il_msg_tx=[]
  il_msg_rx=[]
  
   
  all_message_tx = dbc.get_msg_type(full_msg,'tx')
  for mes in all_message_tx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_tx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_tx.append(mes)
      
  
  il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  
  all_message_rx = dbc.get_msg_type(full_msg,'rx')
  for mes in all_message_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_rx.append(mes)
      
  il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
  
  node_list=[]
  rx_node_cfg={}
  #msg_list=[]
  node_msg_list={}
  for mes in il_sorted_mes_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_key_msg'] in ['on','ON','On',1,'1']:
      rx_node_cfg[vnim_msg_cfg_data[mes['Msg_name']+'_node_name']] = mes['Msg_name']
      if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_list:
        node_list.append(vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper())
    if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_msg_list:      
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()]=[mes['Msg_name']]
    else:
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()].append(mes['Msg_name'])
          
  message_order = []
  timeout_list ={}
  
  il_sorted_mes_rx_ordered = []
  for nd in node_list:
    #il_sorted_mes_rx_ordered.append(rx_node_cfg[nd])
    message_order.append(rx_node_cfg[nd])
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        message_order.append(mes)
        
  
  for order_msg in  message_order:
    for mes in il_sorted_mes_rx:
      if mes['Msg_name'] == order_msg:
        il_sorted_mes_rx_ordered.append(mes)
        
  for nd in node_list:  
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        for mes_prop in il_sorted_mes_rx_ordered:
          if int(mes_prop['GenMsgCycleTime']) !=0:
              timeout_list[nd]=1
              break
  
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("vnim.msg.resource")
    
  print('''/* ---------------------------------------------------------------------------
  
    Messages
  
    Message are suffixed with "_MSGID" and must be all CAPS. Declaring a
    message makes it public and available for OS inter-component
    communication via the OS message queue.
  
  ------------------------------------------------------------------------ */''')
  
  print('\n/* Transmitted Signal OS Message Handles */\n')
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signals in mes['Sig_List']:
        print('message( VNT_'+signals.upper()+'_MSGID );')
        
  print('\n/* Transmitted Message OS Message Handles */\n')
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('message( VNT_'+mes['Msg_name'].upper()+'_MSGID );')
      
  print('\n/* Received message OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('message( VNRCL_'+mes['Msg_name'].upper()+'_MSGID );')
  
  print('\n/* Green drive messages */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      green_en = 0
      for signal in mes['Sig_List']:
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
        
      if green_en == 1:
        print('message( VNRCL_GD_'+mes['Msg_name'].upper()+'_MSGID );')
    
  print('\n/* Received message Invalid/Timeout OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('message( VNRO_'+mes['Msg_name'].upper()+'_MSGID );')
    
  close_output(f)
  
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("vnim.txrx.resource")
  
  print('\n/* Transmitted Signal OS Message Handles */\n')
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signals in mes['Sig_List']:
        print('notify_rcv( VNT_'+signals.upper()+'_MSGID );')
  
  print('\n/* Transmitted Message OS Message Handles */\n')  
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('notify_rcv( VNT_'+mes['Msg_name'].upper()+'_MSGID );')      
  
  print('\n/* Received message OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('notify( VNRCL_'+mes['Msg_name'].upper()+'_MSGID );')
  
  print('\n/* Green drive messages */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      green_en = 0
      for signal in mes['Sig_List']:
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
        
      if green_en == 1:
        print('notify( VNRCL_GD_'+mes['Msg_name'].upper()+'_MSGID );')
    
  print('\n/* Received message Invalid/Timeout OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('notify( VNRO_'+mes['Msg_name'].upper()+'_MSGID );')
    
  close_output(f)
  
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("nw_host_mgr_txrx.resource")
  
  print('\n/* Transmitted Signal OS Message Handles */\n')
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signals in mes['Sig_List']:
        print('notify( VNT_'+signals.upper()+'_MSGID );')
  
  print('\n/* Transmitted Message OS Message Handles */\n')  
  for mes in il_msg_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('notify( VNT_'+mes['Msg_name'].upper()+'_MSGID );')
  
  print('\n/* Received message OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('notify_rcv( VNRCL_'+mes['Msg_name'].upper()+'_MSGID );')
  
  print('\n/* Green drive messages */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      green_en = 0
      for signal in mes['Sig_List']:
        if vnim_sig_cfg_data[signal.upper()+'_green_drive'] in ['on','On',1,'1','ON']:
          green_en = 1
        
      if green_en == 1:
        print('notify_rcv( VNRCL_GD_'+mes['Msg_name'].upper()+'_MSGID );')
    
  print('\n/* Received message Invalid/Timeout OS Message Handles */\n')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('notify_rcv( VNRO_'+mes['Msg_name'].upper()+'_MSGID );')
    
  close_output(f)

def nm_par_gen():
  global footer,vnim_code_gen_dir,tp_generic_config,nm_generic_config,il_generic_config 
  
  dir = './CODE_GEN'
  if not os.path.exists(vnim_code_gen_dir):
    os.mkdir(vnim_code_gen_dir)
  f=open_output("nw_nm_par.h")
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  vnim_cfg_file = open(vnim_data_dir+"CanDbcSigConfiguration.data",'r',encoding='utf-8')
  vnim_sig_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  il_msg_tx=[]
  nm_msg_tx=[]
  
  il_msg_rx=[]
  
   
  all_message_tx = dbc.get_msg_type(full_msg,'tx')
  for mes in all_message_tx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_tx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_tx.append(mes)
      elif vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'NM':
        nm_msg_tx.append(mes)
      else:
        pass
      
  
  il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  
  all_message_rx = dbc.get_msg_type(full_msg,'rx')
  for mes in all_message_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_enable'] in ['on','ON','On',1,'1']:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        il_msg_rx.append(mes)
      
  il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
  
  node_list=[]
  rx_node_cfg={}
  #msg_list=[]
  node_msg_list={}
  for mes in il_sorted_mes_rx:
    if vnim_msg_cfg_data[mes['Msg_name']+'_rx_key_msg'] in ['on','ON','On',1,'1']:
      rx_node_cfg[vnim_msg_cfg_data[mes['Msg_name']+'_node_name']] = mes['Msg_name']
      if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_list:
        node_list.append(vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper())
    if vnim_msg_cfg_data[mes['Msg_name']+'_node_name'] not in node_msg_list:      
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()]=[mes['Msg_name']]
    else:
      node_msg_list[vnim_msg_cfg_data[mes['Msg_name']+'_node_name'].upper()].append(mes['Msg_name'])
          
  message_order = []
  timeout_list ={}
  
  il_sorted_mes_rx_ordered = []
  for nd in node_list:
    #il_sorted_mes_rx_ordered.append(rx_node_cfg[nd])
    message_order.append(rx_node_cfg[nd])
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        message_order.append(mes)
        
  
  for order_msg in  message_order:
    for mes in il_sorted_mes_rx:
      if mes['Msg_name'] == order_msg:
        il_sorted_mes_rx_ordered.append(mes)
        
  for nd in node_list:  
    for mes in node_msg_list[nd]:
      if mes != rx_node_cfg[nd]:
        for mes_prop in il_sorted_mes_rx_ordered:
          if int(mes_prop['GenMsgCycleTime']) !=0:
              timeout_list[nd]=1
              break
  header = '''/* ===========================================================================
 
                      CONFIDENTIAL VISTEON CORPORATION
 
   This is an unpublished work of authorship, which contains trade secrets,
   created in 2007.  Visteon Corporation owns all rights to this work and
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
 
   Name:           nw_nm_par.h
 
   Description:    Indirect NM Implementation
 
   Organization:   Multiplex Core Technology
 
  =========================================================================*/
#ifndef NW_NM_PAR_H
#define NW_NM_PAR_H'''
  
  print(header)
  
  includes = '''#include"nw_nm_wake.h"
#include"nw_can_dll.h"'''
  print('\n',includes)
  
  print('\n')
  print('#define NM_IS_ACTIVE_TMH  3   /* 0-2 is for TP, 3 is for NM */')
  
  
  print('#define NM_TX_MSG_DATA_STRUCT                            \\')
  print('{                                                                                  \\')
  print('   CAN_GPNUM_8,                                 /* CAN message data length  */     \\')
  if len(nm_msg_tx) != 0:
    print('   '+hex(int(nm_msg_tx[0]['id']))+',                                       /* CAN message identifier   */     \\')
  else:
    print('   0x3C5,                                       /* CAN message identifier   */     \\')
  print('   &Nm_msg_buffer[0],                           /* Pointer to Data          */      \\')
  print('   CANB_TX_STD_DATA,                            /* CAN message options      */      \\')
  print('   (DLL_NUM_IL_TX_FRAMES+1)                               /* Transmit Message Handle  */        \\')
  print('}')

  
  print('typedef enum')
  print('{')
  for node in node_list:
      print('   NM_'+node.upper()+'_NODE,')
  print('   NM_NUMBER_OF_NODES')
  print('}NM_NODE_LIST;\n')
 
  
  
  print('#define NM_NM_NODES_BIT_MASK        \\')
  bit_signal=1
  node_cnt = 0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   '+str(hex(bit_signal))+'   /*NM_'+node.upper()+'_NODE*/')
    else:
      print('   '+str(hex(bit_signal))+',   /*NM_'+node.upper()+'_NODE*/    \\')
      
    bit_signal=bit_signal<<1
    node_cnt+=1
    if bit_signal == 256:
      bit_signal=1
  print('\n')
  
  #node byte position
  print('#define NM_NM_NODES_BYTE_OFFSET             \\')
  byte_cnt = 0
  node_cnt=0
  for node in node_list:
    if node_cnt == (len(node_list)-1):
      print('   '+str(hex(byte_cnt))+'   /*NM_'+node.upper()+'_NODE*/')
    else:
      print('   '+str(hex(byte_cnt))+',   /*NM_'+node.upper()+'_NODE*/   \\')
    node_cnt+=1  
    if (node_cnt%8 == 0):
      byte_cnt+=1
  print('\n')
  # bit mask
  
  print('/*Node Missing Macro*/')
  for node in node_list:
    print('/*NM_'+node.upper()+'_NODE*/')
    print('#define IS_'+node.upper()+'_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]]) & \\')
    print(' '*len('#define IS_'+node.upper()+'_NODE_MISSING()      (CAN_UINT8)(((')+'(nw_nm_bit_mask[NM_'+node.upper()+'_NODE])) == (nw_nm_bit_mask[NM_'+node.upper()+'_NODE]))\n')
    print('#define NM_'+node.upper()+'_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]] |= \\')
    print(' '*len('#define NM_'+node.upper()+'_NODE_MISSING()      (')+'nw_nm_bit_mask[NM_'+node.upper()+'_NODE])\n')
    print('#define NM_'+node.upper()+'_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]] &= \\')
    print(' '*len('#define NM_'+node.upper()+'_NODE_GAIN()      (')+'(CAN_UINT8) ~(nw_nm_bit_mask[NM_'+node.upper()+'_NODE]))\n\n')
   
      
    
  print('/*Node DLC Fault Macro*/')
  for node in node_list:
    print('/*NM_'+node.upper()+'_NODE*/')
    print('#define IS_'+node.upper()+'_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]]) & \\')
    print(' '*len('#define IS_'+node.upper()+'_NODE_DLC_INVALID()     (CAN_UINT8)((')+'(nw_nm_bit_mask[NM_'+node.upper()+'_NODE])) == (nw_nm_bit_mask[NM_'+node.upper()+'_NODE]))\n')
    print('#define NM_'+node.upper()+'_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]] |= \\')
    print(' '*len('#define NM_'+node.upper()+'_NODE_DLC_INVALID()     (')+'nw_nm_bit_mask[NM_'+node.upper()+'_NODE])\n')
    print('#define NM_'+node.upper()+'_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_'+node.upper()+'_NODE]] &= \\')
    print(' '*len('#define NM_'+node.upper()+'_NODE_DLC_VALID()      (')+'(CAN_UINT8) ~(nw_nm_bit_mask[NM_'+node.upper()+'_NODE]))\n\n')
   
  print('#endif')
  print(footer)
  
  close_output(f)
  
if __name__ == "__main__":
    pass
    '''import datetime
    time_print = datetime.datetime.now()
    set_file_node_il('U321.dbc','IS')
    set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
    vnim_app_c_gen()
    vnim_app_h_gen()
    vnim_resource_gen()
    nm_par_gen()'''
    
    