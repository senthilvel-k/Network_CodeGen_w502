import sys,json
import os
from cogent_io import open_output, close_output
from py2compat import py2_print as print, Py2Dict  # Python 2 print/dict-order semantics
dbc=None
dbc_file_name=None

il_code_gen_dir = './CODE_GEN'
il_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgILSupport'
full_msg='ALL'
time_str=''
footer=''

datatype_8 = 'CAN_UINT8'
datatype_16 = 'CAN_UINT16'
datatype_32 = 'CAN_UINT32'
dlc_disable = 1 # variable used for structure optimization

  #f=open('nm_il_msg.h','w')
  
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

# Function used to generate structure and the input type is the Rx/Tx signal sheet

def message_buf_generation():
  global dbc,datatype_8,datatype_16,datatype_16,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
 
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
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
  
  
  print('''\n/* ===========================================================================
     Tx Message buffer structure type definition 
    ============================================================================*/\n''')
    
  for mes in il_sorted_mes_tx:
      if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
        print('typedef union {')
        print('   '+datatype_8+'  '+'msg_buffer[8];')
        print('   '+mes['Msg_name'].upper()+'_msgType'+' '+mes['Msg_name'].lower()+';')
        print('}'+mes['Msg_name'].upper()+'_buf;\n')
        
  print('''\n\n\n/* ===========================================================================
     RECEIVE Message buffer structure type definition 
    ============================================================================*/	 \n''')
    
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('typedef union {')
      print('   '+datatype_8+'  '+'msg_buffer[8];')
      print('   '+mes['Msg_name'].upper()+'_msgType'+' '+mes['Msg_name'].lower()+';')
      print('}'+mes['Msg_name'].upper()+'_buf;\n')

  print('\n/* CAN Tx Buffer */\n')
  print('typedef union {')
  print('   '+'CAN_UINT8    msg_buffer[8];')

  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('   '+mes['Msg_name'].upper()+'_msgType'+' '+mes['Msg_name'].lower()+';')
  print('}Tx_Msg_buf;\n')

  print('\n/* CAN Rx Buffer */\n')
  print('typedef union {')
  print('   '+'CAN_UINT8    msg_buffer[8];')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('   '+mes['Msg_name'].upper()+'_msgType'+' '+mes['Msg_name'].lower()+';')
  print('}Rx_Msg_buf;\n')
  
  
  print('''/* ==========================================================================
   Tx and Rx buffer                                
   ========================================================================*/
extern Tx_Msg_buf           Tx_buffer;
extern Rx_Msg_buf           Rx_buffer;
''')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('extern '+mes['Msg_name'].upper()+'_buf'+' '+mes['Msg_name'].upper()+';')
 
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('extern '+mes['Msg_name'].upper()+'_buf'+' '+mes['Msg_name'].upper()+';')
  
  print('''/* ===========================================================================
  Interaction Layer Receive Signal Precopy Functions
  =========================================================================*/
''')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('extern void '+mes['Msg_name'].upper()+'_PreCopy   (void);')
 
  
def message_structure_generation_tx_rx():
  global dbc,datatype_8,datatype_16,datatype_16,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  vnim_cfg_file = open(il_data_dir+"CanDbcSigConfiguration.data",'r',encoding='utf-8')
  vnim_sig_cfg_data= json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  il_msg_tx=[]
  il_msg_rx=[]
  nm_msg_rx=[]
  diag_msg_rx=[]
  
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
      elif vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'NM':
        nm_msg_rx.append(mes)
      elif vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Diag':
        diag_msg_rx.append(mes)
      else:
        pass
        
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
     
  print('''/* ===========================================================================
   Interaction Layer Number of Transmit Messages, Signals
  =========================================================================*/
''')
  #creating TX macros 
  temp_tx_count=0
  temp_sig_count = 0
  temp_periodic_count = 0
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      temp_tx_count+=1
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        temp_periodic_count+=1
      for sig in mes['Sig_List']:
        temp_sig_count+=1
      
  print('#define  IL_TX_NUM_MESSAGES'+' '+str(temp_tx_count))
  print('#define  IL_TX_NUM_SIGNALS'+' '+str(temp_sig_count))
  print('#define  IL_TX_NUM_IDS'+' '+str(temp_tx_count))
  print('#define  IL_TX_NUM_BURST_PERIODIC  0')
  print('#define  IL_TX_NUM_PERIODIC         '+str(temp_tx_count))
  print('#define  IL_TX_NUM_OFFSET'+' '+str(temp_tx_count))

  print('''/* ===========================================================================
   Interaction Layer Transmit Message (Frame) Handles
  =========================================================================*/
''')
  temp_count = 0 #Change this count only if new NM,DIAG messsage added
  print('#define IL_TX_MSG_TMH    '+str(temp_count))
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('#define IL_'+mes['Msg_name'].upper()+'_TMH'+'    '+str(temp_count))
      temp_count+=1
  
  print('''/* ===========================================================================
   Interaction Layer Transmit Message Enumerations
  =========================================================================*/''')

  temp_count = 0
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('#define VNIM_'+mes['Msg_name'].upper()+'_MESSAGE'+'    ('+str(temp_count)+')')
      temp_count+=1
  
  
    
  #tx tmd structure
  print('''/* ===========================================================================
  Interaction Layer Transmit Message Data (TMD) Structures (Frame Definition)
										   
  !!! IMPORTANT NOTE !!! The transmit message handles must be specified
  sequentially, starting with 0 (zero). These message handles serve as an
  index to the transmit complete function pointers, so each index must map
  to the correct transmit complete callback function pointer in the lookup
  table (array of function pointers) for servicing transmit complete events.

 =========================================================================*/''')
  print('#define IL_TX_MSG_DATA_STRUCT                       \\')
  temp_count = 0
  
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('   /*'+mes['Msg_name']+' Message */\\')
      print('   {\\')
      print('   CAN_GPNUM_'+str(mes['DLC'])+',                                           /* CAN message data length  */           \\')
      print('   '+hex(int(mes['id']))+',                                                 /* CAN message identifier   */           \\')
      print('   &'+mes['Msg_name'].upper()+'.msg_buffer[ 0 ] ,        /* Pointer to Transmit Frame Data    */    \\')
      if int(mes['id']) > 2047:
        print('   CANB_TX_EXTENDED,                                                   /* CAN message options      */           \\')
      else:
        print('   CANB_TX_STD_DATA,                                                   /* CAN message options      */           \\')
      print('   IL_'+mes['Msg_name'].upper()+'_TMH                                            /* Transmit Message Handle  */           \\')
      if temp_count == len(il_sorted_mes_tx)-1: 
        print('}')
      else:
        print('},            \\')
      temp_count+=1
  print('\n\n')
  
  print('''/* ===========================================================================
  TX Offset values
  =========================================================================*/''')
  
  temp_count = 0
  print('#define IL_TX_OFFSET_TABLE  \\')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      if temp_count == (len(il_sorted_mes_tx )-1):
        print('   '+str((temp_count*4)+1))
      else:
        print('   '+str((temp_count*4)+1)+',      \\')
      temp_count+=1
  
  
  #tx frame table
  print('''\n\n/* ===========================================================================
  Interaction Layer Transmit Frame Table

  Each entry in this table defines the attributes for a specific transmit
  frame transmitted by the Interaction Layer.

 =========================================================================*/\n\n''')
  tx_confirmation = 0
  temp_count = 0
  temp_periodic_count=0
  print("#define IL_TX_FRAME_TABLE"+"                     \\")
  for mes in il_sorted_mes_tx:
    signal_debounce=0
    tx_confirmation=0
    for signal in mes['Sig_List']:
      if  vnim_sig_cfg_data[signal.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
        signal_debounce=1
        tx_confirmation=1
        
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('   /*'+mes['Msg_name']+' Message */\\')
      print('   {\\')
      word_str = mes['Msg_name'].upper()
      if( word_str.find('MCM') == -1 ):
        print('   (NW_HW_ALL_VARIANTS),         /* HW variants              */   \\')
      else:
        print('   (NW_HW_TCU_VARIANTS),         /* HW variants              */   \\')
      if mes['GenMsgSendType'] in ['0','Cyclic',0]:
        if tx_confirmation == 1: 
          print('   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\')
        else:
          print('   (IL_TX_ATTR_PERIODIC),         /* Frame Transmission Attributes              */   \\')
      elif mes['GenMsgSendType'] in ['1','Event',1]:
        if tx_confirmation == 1: 
          print('   (IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\')
        else:
          print('   (IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\')
      elif mes['GenMsgSendType'] in ['5','Cycle and Event',5]:
        if tx_confirmation == 1: 
          print('   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\')
        else:
          print('   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\')
      else:
        print('   IL_TX_ATTR_EVENT,         /* Frame Transmission Attributes              */   \\')
    
      print('   &il_tx_frame_status[ VNIM_' + mes['Msg_name'].upper() + '_MESSAGE ],                               /* Pointer to the Frame Status Variable         */  \\')
      print('   &'+mes['Msg_name'].upper()+'.msg_buffer[ 0 ],           /* Pointer to the Transmitted Frame Data        */  \\')
      print('   &il_tx_delay_count[ VNIM_'+ mes['Msg_name'].upper() + '_MESSAGE ],                                /* Pointer to the Transmit Delay Count          */  \\')
      print('   IL_TIME_IN_TASK_TICS( 0 ),                                           /* Minimum Transmit Delay in Timer Tics         */   \\')
      
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('   &il_tx_periodic[ VNIM_' + mes['Msg_name'].upper() + '_MESSAGE ],                               /* Pointer to the Periodic Attributes (or NULL) */  \\')
        temp_periodic_count+=1
      else:
        print('   NULL,                                                            /* Pointer to the Periodic Attributes (or NULL) */  \\')
        
      print('   NULL,                                                                /* Ptr to Burst Periodic Attributes (or NULL)   */  \\')
      print('   &il_tx_can_tmd[ VNIM_' + mes['Msg_name'].upper() + '_MESSAGE ],                                                   /* Pointer to CAN Driver TMD Data Structure     */  \\')
      #print '   NULL,                                                                /* Pointer to Tx Complete Callback Function     */  \\'
      if signal_debounce ==1:
        print('   &Vnim_'+mes['Msg_name'].upper()+'_Conf,                        			                                   /* Pointer to Tx confirmation function               */	\\')
        print('   &Vnim_'+mes['Msg_name'].upper()+'_PreCopy                        			                                   /* Pointer to Tx Precopy function               */	\\')
      else:
        print('   NULL,                        			                                   /* Pointer to Tx confirmation function               */	\\')
        print('   NULL                        			                                   /* Pointer to Tx Precopy function               */	\\')
      if temp_count == len(il_sorted_mes_tx)-1: 
        print('   }')
      else:
        print('   },                                                                       \\')
      temp_count+=1

  
  print('''/* ===========================================================================
    Interaction Layer Periodic Transmit Table
  
    This table is an array of data structures that define the periodic
    transmit characteristics for messages that are transmitted periodically.
    Care must be taken so that the each periodic message defined in the
    Interaction Layer Transmit Frame table map correctly to this table so
    that the correct periodic message attributes, and the pointer to the
    periodic timer, is correctly retrieved.
  
  =========================================================================*/
''')
  temp_count = 0
  print('#define IL_TX_PERIODIC_TABLE                                                          \\')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print('   /* '+mes['Msg_name'] +'Message is Periodic */                                                     \\')
      print('   {                                                                                 \\')
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('   IL_TIME_IN_TASK_TICS( '+mes['GenMsgCycleTime']+' ),                /* Primary Period in Task Tics  */     \\')
        print('   IL_TIME_IN_TASK_TICS( '+str(150+(temp_count*5))+'),                /* Offset Delay in Task Tics    */    \\')
        print('   &il_tx_periodic_count[ VNIM_' + mes['Msg_name'] + '_MESSAGE ]                      /* Pointer to Periodic Count    */     \\')
      else:
        print('   IL_TIME_IN_TASK_TICS( 0 ),                /* Primary Period in Task Tics  */     \\')
        print('   IL_TIME_IN_TASK_TICS( 0 ),                /* Offset Delay in Task Tics    */    \\')
        print('   &il_tx_periodic_count[ VNIM_' + mes['Msg_name'] + '_MESSAGE ]                      /* Pointer to Periodic Count    */     \\')
      if temp_count == (len(il_sorted_mes_tx)-1):
        print('   }                                                                                 ')
      else:
        print('   },                                                                                  \\')
      temp_count+=1
        


  
  #Rx table definitions
  temp_periodic_count = 0
  temp_count = 0
  temp_sig_count=0
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      temp_count+=1
      temp_sig_count+=len(mes['Sig_List'])
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        temp_periodic_count+=1
        
  print('''/* ===========================================================================
    Transmit Message (Frame) Callback Functions
  =========================================================================*/''')
  for mes in il_sorted_mes_tx:
    signal_debounce=0
    for signal in mes['Sig_List']:
      if  vnim_sig_cfg_data[signal.upper()+'_tx_debounce'] in ['on','On',1,'1','ON']:
        signal_debounce=1
    if signal_debounce == 1:
      print('extern void Vnim_'+mes['Msg_name'].upper()+'_PreCopy(void);')
      print('extern void Vnim_'+mes['Msg_name'].upper()+'_Conf(void);')
      
      
  print('''\n/* ===========================================================================
    Interaction Layer Number of Receive Messages, Signals
  =========================================================================*/''')
    
  print('#define IL_RX_NUM_PERIODIC   '+str(temp_count))
  print('#define IL_RX_NUM_MESSAGES   '+str(temp_count))
  print('#define IL_RX_NUM_FRAMES     '+str(temp_count))
  print('#define IL_NUM_OF_RX_DATA_CHANGED_FLAG   ' +str((temp_sig_count//8) if (temp_sig_count%8 == 0) else (temp_sig_count//8)+1))
 
  print('''/* ===========================================================================
    Interaction Layer Receive Message Enumerations
  =========================================================================*/''')
  temp_count = 0
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('#define VNIM_'+mes['Msg_name'].upper()+'_MESSAGE     '+str(temp_count))
      temp_count+=1

  print('#define VNIM_IL_RX_MESSAGE     '+str(temp_count))
  
  temp_count+=1      
  diag_sorted_mes_rx = sorted(diag_msg_rx,key = lambda x: x['Msg_name'])
  nm_sorted_mes_rx = sorted(nm_msg_rx,key = lambda x: x['Msg_name'])
  
  for mes in diag_sorted_mes_rx:
    print('#define VNIM_'+mes['Msg_name'].upper()+'_MESSAGE     '+str(temp_count))
    temp_count+=1
      
  for mes in nm_sorted_mes_rx:
    print('#define VNIM_'+mes['Msg_name'].upper()+'_MESSAGE     '+str(temp_count))
    temp_count+=1    
      
  print('''
/* ===========================================================================
   P U B L I C   M E M O R Y
  =========================================================================*/
extern IL_TX_FRAME const il_tx_frame_table[ ];

extern IL_RX_FRAME const il_rx_frame_table[ ];

extern CAN_UINT8 il_Rx_DataChanged_Flag[IL_NUM_OF_RX_DATA_CHANGED_FLAG];

extern CAN_TMD const il_IS1_100_tmd ;

extern CAN_UINT8 MsgDtcFlag[IL_RX_NUM_MESSAGES];
extern CAN_UINT8 Suppress_VINDTC_Logging;
extern CAN_UINT8 const vnim_msg_node_list[];
''')
  
  print('''/* ===========================================================================
   Received Frame Attributes Lookup Table
 
   This table has includes the attributes for all of the received frames.
   If a received frame is periodic, this table also includes pointers to the
   received frame status and to the receive timeout counter for message
   gain and loss indication.
 
  =========================================================================*/''')
  temp_count=0
  print('#define IL_RX_FRAME_TABLE                                                                                                        \\')
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('   /* '+mes['Msg_name']+'Message */                                                                                           \\')
      print('   {                                                                                                                           \\')
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('       (IL_RX_ATTR_PERIODIC | IL_RX_ATTR_TIMEOUT_MONITOR),                                                                       \\')
      else:
        print('       (IL_RX_ATTR_DEFAULT),                                                                                                     \\')
        
      print('       &il_rx_frame_status[ VNIM_' + mes['Msg_name'].upper() + '_MESSAGE ],                                           /* Pointer to Receive Status         */    \\')
      print('       &'+mes['Msg_name'].upper()+'.msg_buffer[ 0 ],                                             /* Pointer to Received Frame Data    */    \\')
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('       &il_rx_timeout_count[ VNIM_' + mes['Msg_name'].upper() + '_MESSAGE ],                                                      /* Pointer to the Timeout Counter */       \\')
      else:
        print('       NULL,                                                                           /* Pointer to the Timeout Counter    */    \\')
      if vnim_msg_cfg_data[mes['Msg_name']+'_rx_key_msg'] in ['on','On',1,'1','ON']:
        print('       IL_TIME_IN_TASK_TICS( '+mes['GenMsgCycleTime']+'*NODE_ABSENT_ERROR_COUNT ),       /* Timeout Count Value               */    \\')
      else:
        print('       IL_TIME_IN_TASK_TICS( '+mes['GenMsgCycleTime']+'*MSG_TIMEOUT_ERROR_COUNT ),       /* Timeout Count Value               */    \\')
      print('       &VnimIlRx_'+mes['Msg_name'].upper()+'_MsgIndication,                                      /* Receive Callback Function         */    \\')
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('       &VnimIlRx_'+mes['Msg_name'].upper()+'_Timeout,                                          /* Rx Msg Timeout Callback Function  */    \\')
      else:
        print('       NULL,                                            /* Rx Msg Timeout Callback Function  */    \\')
      print('       NULL,                                                                             /* Rx Msg Gain Callback Function     */    \\')
      print('       &'+mes['Msg_name'].upper()+'_PreCopy                                                                                                 \\')
      if temp_count == len(il_sorted_mes_rx_ordered)-1:
        print('   }\n')                   
      else:
        print('   },                                                                                                                           \\')                   
      temp_count+=1
  
  print('''\n/* ===========================================================================
  Received Message (Frame) Callback Functions
  =========================================================================*/
''')
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print('void VnimIlRx_'+mes['Msg_name'].upper()+'_MsgIndication  ( void );')
    
  print('''/* ===========================================================================
  Received Message (Frame) Timeout Callback Functions
  =========================================================================*/
''')
    
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['GenMsgSendType'] in ['0','Cyclic','Combined(Event/Periodic)','5',0,5] or int(mes['GenMsgCycleTime']) >0:
        print('void VnimIlRx_'+mes['Msg_name'].upper()+'_Timeout   ( void );')
      
      
def signal_get_Put():
  global dbc,datatype_8,datatype_16,datatype_16,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
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
  
  print('''\n/* ===========================================================================
   Interaction Layer Transmit Signal Tx Put Macros
  =========================================================================*/''')

  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = signal
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  == layout_row_end:
              print('#define ILPutTx_'+signal.upper()+'_data(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  == layout_row_end:
              print('#define ILPutTx_'+signal.upper()+'_data(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
            

  print('''\n/* ===========================================================================
   Interaction Layer Transmit Signal Tx Get Macros
  =========================================================================*/''')
  
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  == layout_row_end:
              print('#define ILGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  == layout_row_end:
              print('#define ILGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
            

  print('''/* ===========================================================================
  Interaction Layer Transmit Signal Tx Put Functions
  =========================================================================*/''')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  != layout_row_end:
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
              print('void ILPutTx_'+signal.upper()+'_data('+datatype_8+' sig_Data);')
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  != layout_row_end:
              print('void ILPutTx_'+signal.upper()+'_data('+datatype_8+' sig_Data);')
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
            
        if int(mes['Sig_List'][signal]['Len']) >8 and int(mes['Sig_List'][signal]['Len']) <=16:
          print('void ILPutTx_'+signal.upper()+'_data('+datatype_16+' sig_Data);')
        elif  int(mes['Sig_List'][signal]['Len']) >16 and int(mes['Sig_List'][signal]['Len']) <=32:
          print('void ILPutTx_'+signal.upper()+'_data('+datatype_32+' sig_Data);')
        elif int(mes['Sig_List'][signal]['Len']) >32 and int(mes['Sig_List'][signal]['Len']) <=64:
          print('void ILPutTx_'+signal.upper()+'_data('+datatype_8+' const * const pData);')
        else:
          pass
  
  print('''/* ===========================================================================
  VNIM Interface Macros for Applications.For TX
  =========================================================================*/''')
  
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
       if int(mes['Sig_List'][signal]['Len']) <=32:
        print('#define VNIM_TX_'+signal.upper()+'(a)  ILPutTx_'+signal.upper()+'_data(a)')

  
  print('''\n/* ===========================================================================
   Interaction Layer Transmit Signal Rx Put Macros
  =========================================================================*/''')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Multiplex'] == 'YES':
        mul_msg=dbc.get_multiplex(mes['id'])
        multiplexor_id=mul_msg['Multiplexor']
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          if mes['Multiplex'] == 'YES':
            multiplexor_index=0
            for sig_list in mul_msg['Multiplex_group']:
              if signal in sig_list:
                multiplexor_index=mul_msg['Multiplex_group'].index(sig_list)
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel': 
            if layout_row_start  == layout_row_end:            
              if mes['Multiplex'] == 'YES':
                if mes['Sig_List'][signal]['Mul_order'] != 'root':
                  print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+signal.upper()+'= data')
                else:     
                  print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
              else:
                print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
              
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  == layout_row_end:
              if layout_row_start  == layout_row_end:            
                if mes['Multiplex'] == 'YES':
                  if mes['Sig_List'][signal]['Mul_order'] != 'root':
                    print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+signal.upper()+'= data')
                  else:
                    print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
                else:
                  print('#define ILRxPut_'+signal.upper()+'(data)    '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()+'= data')
              
            
    
  
  print('''\n/* ===========================================================================
   Interaction Layer Receive Signal Rx Get Macros
  =========================================================================*/''')
  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Multiplex'] == 'YES':
        mul_msg=dbc.get_multiplex(mes['id'])
        multiplexor_id=mul_msg['Multiplexor']
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          if mes['Multiplex'] == 'YES':
            multiplexor_index=0
            for sig_list in mul_msg['Multiplex_group']:
              if signal in sig_list:
                multiplexor_index=mul_msg['Multiplex_group'].index(sig_list)
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  == layout_row_end:
              if mes['Multiplex'] == 'YES':
                if mes['Sig_List'][signal]['Mul_order'] != 'root':
                  print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+signal.upper())
                else:
                  print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
              else:
                print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
              
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  == layout_row_end:
              if mes['Multiplex'] == 'YES':
                if mes['Sig_List'][signal]['Mul_order'] != 'root':
                  print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+signal.upper())
                else:
                  print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
              else:
                print('#define IlRxGet'+signal.upper()+'() 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper())
            
    
  
  print('''/* ===========================================================================
  Interaction Layer Receive Signal Rx Put Functions to set application 
  values to Rx buffer
  =========================================================================*/''')
  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  != layout_row_end:
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
              print('void ILRxPut_'+signal.upper()+'('+datatype_8+' data);')
              
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  != layout_row_end:
              print('void ILRxPut_'+signal.upper()+'('+datatype_8+' data);')
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
            
        elif int(mes['Sig_List'][signal]['Len']) >8 and int(mes['Sig_List'][signal]['Len']) <=16:
          print('void ILRxPut_'+signal.upper()+'('+datatype_16+' data);')
        elif  int(mes['Sig_List'][signal]['Len']) >16 and int(mes['Sig_List'][signal]['Len']) <=32:
          print('void ILRxPut_'+signal.upper()+'('+datatype_32+' data);')
        elif int(mes['Sig_List'][signal]['Len']) >32 and int(mes['Sig_List'][signal]['Len']) <=64:
          print('void ILRxPut_'+signal.upper()+'('+datatype_8+' const * const pData);')
        else:
          pass
          
  
  print('''/* ===========================================================================
   Interaction Layer Receive Signal Rx Get Functions 
  =========================================================================*/''')  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=8:
          sig_start_bit = int(mes['Sig_List'][signal]['Endbit'])
          layout_row_start=int(mes['Sig_List'][signal]['Endbit'])//8
          layout_col_start=int(mes['Sig_List'][signal]['Endbit'])%8
          signal_length=int(mes['Sig_List'][signal]['Len'])
          #sig_name = mes['Sig_List'][signal]['Sig_name']
          end_bit=int(mes['Sig_List'][signal]['Endbit'])+signal_length-1
          layout_row_end = end_bit//8
          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8
          
          if mes['Sig_List'][signal]['Order'] == 'Intel':  
            if layout_row_start  != layout_row_end:
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
              print(datatype_8+' IlRxGet'+signal.upper()+'(void);')
                          
          else:
            layout_row_start = start_bit//8
            layout_row_end = sig_start_bit//8
            if layout_row_start  != layout_row_end:
              #print 'void ILRxPut_'+signal.upper()+'('+datatype_8+' data);'
              print(datatype_8+' IlRxGet'+signal.upper()+'(void);')
              #print '#define IlGetTx_'+signal.upper()+' 		'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+signal.upper()
            
        elif int(mes['Sig_List'][signal]['Len']) >8 and int(mes['Sig_List'][signal]['Len']) <=16:
          print(datatype_16+' IlRxGet'+signal.upper()+'(void);')
        elif  int(mes['Sig_List'][signal]['Len']) >16 and int(mes['Sig_List'][signal]['Len']) <=32:
          print(datatype_32+' IlRxGet'+signal.upper()+'(void);')
        elif int(mes['Sig_List'][signal]['Len']) >32 and int(mes['Sig_List'][signal]['Len']) <=64:
          print('void IlRxGet'+signal.upper()+'('+datatype_8+' * pData);')
        else:
          pass
    
  print('''/* ===========================================================================
    VNIM Interface Macros for Applications.For RX
   =========================================================================*/''')   
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      for signal in mes['Sig_List']:
        if int(mes['Sig_List'][signal]['Len']) <=32:
         print('#define VNIM_RX_'+signal.upper()+'() IlRxGet'+signal.upper()+'()')
        
        
        
        
  print('''/* ===========================================================================
    Interaction Layer Receive Message Set Data Changed Macros
   =========================================================================*/''')
  no_signal = 0
  bit_signal=1
  for mes in il_sorted_mes_rx_ordered: 
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      sig_list=[]
      for signal in mes['Sig_List']:
        mes['Sig_List'][signal]['Sig_name']=signal
        sig_list.append(mes['Sig_List'][signal])
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      for sorted_sig in sorted_bit:
        print('#define ILSet_'+sorted_sig['Sig_name'].upper()+'_DataChanged()        '+'(il_Rx_DataChanged_Flag['+str(no_signal)+'] |= ('+datatype_8+') ('+ hex(bit_signal)+'))')
        print('#define ILGet_'+sorted_sig['Sig_name'].upper()+'_DataChanged()        '+'(il_Rx_DataChanged_Flag['+str(no_signal)+'] & ('+datatype_8+') ('+ hex(bit_signal)+'))')
        print('#define ILClr_'+sorted_sig['Sig_name'].upper()+'_DataChanged()        '+'(il_Rx_DataChanged_Flag['+str(no_signal)+'] &= ((('+datatype_8+') (0xff)) & (('+datatype_8+')~'+ hex(bit_signal)+'u)))')
        print('')
        bit_signal=bit_signal<<1
        if bit_signal == 256:
            no_signal+=1
            bit_signal=1
          
          
def il_par_h_gen_function():  
  global footer,il_code_gen_dir,tp_generic_config,nm_generic_config,il_generic_config
  #dir = './CODE_GEN'
  if not os.path.exists(il_code_gen_dir):
    os.mkdir(il_code_gen_dir)
  f=open_output("nw_il_par.h")
  
  header = '''#if !defined(NW_IL_PAR_H)
#define NW_IL_PAR_H

/* ===========================================================================
 
                      CONFIDENTIAL VISTEON CORPORATION
 
   This is an unpublished work of authorship, which contains trade secrets,
   created in 2009.  Visteon Corporation owns all rights to this work and
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
  /*===========================================================================
 
   Name:           nw_il_par.h
 
   Description:    Interaction Layer Tx, Rx Parameters Header File.
 
   Organization:   Network Subsystem.
 
  =========================================================================*/

#include "nw_il_msg.h"

/* ===========================================================================
   P U B L I C   T Y P E   D E F I N I T I O N S
  =========================================================================*/
'''

  print(header) 
  
  message_buf_generation()
  
  print('''\n/* ===========================================================================
   P U B L I C   M A C R O S
  =========================================================================*/
#define IL_TASK_PERIOD_MS      (5)

/* Conversion from Time in Milliseconds to Interaction Layer Task Tics */
#define IL_TIME_IN_TASK_TICS( tMs )  (('''+datatype_16+''') (((tMs)/IL_TASK_PERIOD_MS)))\n
#define IL_NUM_INSTANCE 1u''')

  message_structure_generation_tx_rx()
  signal_get_Put()
  
  print('#endif')
  print(footer)
  print('/* End of file ============================================================ */')
  close_output(f)

  
if __name__ == "__main__":
    pass
    '''import datetime
    time_print = datetime.datetime.now()
    set_file_node_il('U321.dbc','IS')
    set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
    il_par_h_gen_function()'''
