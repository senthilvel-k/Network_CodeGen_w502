import xlrd
import sys
import re

'''wb = xlrd.open_workbook("autocode_test.xls") #creating a object for excel file   

read_msg_lst_sheet_tx = wb.sheet_by_name('txmessagelist')   #creating an object for each sheet 
read_msg_lst_sheet_rx = wb.sheet_by_name('rxmessagelist')
read_sig_lst_sheet_tx = wb.sheet_by_name('txsignallist')
read_sig_lst_sheet_rx = wb.sheet_by_name('rxsignallist')'''
can_channel_count = 0

def message_structure_generation_rx(rx_signal_list,rx_message_list):
  message={}
  message_list=[]
  message_enable_dictionary={}
  message_dict={}
  event_periodic = {}
  for r in range(1,rx_message_list.nrows):
    msg_name = str(rx_message_list.cell(rowx=r,colx=1).value)
    
    sig_enable1 = int(rx_message_list.cell(rowx=r,colx=7).value)
    message_enable_dictionary[msg_name]=sig_enable1
    event_periodic[msg_name]=int(rx_message_list.cell(rowx=r,colx=5).value)
    
  
  #used to map signals and its attributes  with its message
  #used a dictionary "message" in which "key" is the message and "value" is a list which contains a list of  signals,start_bit,length,byte_order
  for r in range(1,rx_signal_list.nrows):
    msg_name=str(rx_signal_list.cell(rowx=r,colx=1).value)
    sig_name=str(rx_signal_list.cell(rowx=r,colx=2).value)
    length = int(rx_signal_list.cell(rowx=r,colx=3).value)
    startbit =int(rx_signal_list.cell(rowx=r,colx=4).value)
    
    byte_order = str(rx_signal_list.cell(rowx=r,colx=5).value)
    sig_enable = int(rx_signal_list.cell(rowx=r,colx=7).value)
    
    if sig_enable == 1 and message_enable_dictionary[msg_name] == 1:
      if message.has_key(msg_name):
        message[msg_name].append([sig_name,length,byte_order])
      else:
        #signals=[]
        message[msg_name]=[]
        message[msg_name].append([sig_name,length,byte_order])
  tx_message=[]
  
  for r in range(1,rx_message_list.nrows):
    sig_enable1 = int(rx_message_list.cell(rowx=r,colx=7).value)
    if sig_enable1 == 1:
      msg_name= str(rx_message_list.cell(rowx=r,colx=1).value)
      msg_size = int(rx_message_list.cell(rowx=r,colx=2).value)
      msg_id = str(rx_message_list.cell(rowx=r,colx=3).value)
      msg_timeout_enable = int(rx_message_list.cell(rowx=r,colx=8).value)
      
      if ((rx_message_list.cell(rowx=r,colx=4).value)):
        msg_periodicity=int(rx_message_list.cell(rowx=r,colx=6).value)
        
      else:
        msg_periodicity = 0
        
      msg_tx_attribute=int(rx_message_list.cell(rowx=r,colx=5).value)
      '''f ((rx_message_list.cell(rowx=r,colx=5).value)):
      else:
        msg_tx_attribute='NULL'
        '''
      if ((rx_message_list.cell(rowx=r,colx=6).value)):
        msg_timeout=rx_message_list.cell(rowx=r,colx=6).value
      else:
        msg_timeout=0
      tx_message.append(msg_name)
      message_dict[msg_name]=[msg_id,msg_size,msg_periodicity,msg_tx_attribute,msg_timeout,msg_timeout_enable]
   
  tx_message.sort(key = natural_keys)
  
  print'''/* ===========================================================================
    Interaction Layer Number of Receive Messages, Signals
 =========================================================================*/'''
  #creating RX macros 
  print '#define IL_RX_NUM_MSG_INST'+str(can_channel_count)+'  ('+str(len(tx_message))+')'
  total_sig = 0
  for x in message:
    total_sig = total_sig + len(message[x])
  print '#define IL_RX_NUM_SIGNALS_INST'+str(can_channel_count)+'  ('+str(total_sig)+')'
  
  print '#define IL_RX_NUM_FRAMES_INST'+str(can_channel_count)+'  ('+str(len(tx_message))+')'
  
  count1=0
  for mess in tx_message:
    if message_dict[mess][3] != 1 and message_dict[mess][3] != 3 and  message_dict[mess][3] != 6 :
      count1+=1
      
  print '#define IL_RX_NUM_PERIODIC_INST'+str(can_channel_count)+'  (IL_RX_NUM_MSG_INST'+str(can_channel_count)+')'
  
  #print '#define IL_NUM_OF_RX_DATA_CHANGED_FLAG ('+ str((total_sig/8) if (total_sig%8 == 0) else (total_sig/8)+1)+')'
  print "\n\n#if (IL_NUM_INSTANCE > 1)"
  print '''  #if((IL_RX_NUM_MSG_INST1 > IL_RX_NUM_MSG_INST0))
    #define IL_RX_NUM_MESSAGES		IL_RX_NUM_MSG_INST1
  #else
    #define IL_RX_NUM_MESSAGES		IL_RX_NUM_MSG_INST0
  #endif
  #else
    #define IL_RX_NUM_MESSAGES		IL_RX_NUM_MSG_INST0
#endif\n\n'''

  
  print '''/* ===========================================================================
    Interaction Layer Receive Message Enumerations
=========================================================================*/'''
  
  count1=0
  for mess in tx_message:
    print '#define VNIM_'+mess+'_MESSAGE    ('+str(count1)+')'
    count1+=1
   
  
  #print tx_message
  print'''/* ===========================================================================
   Received Frame Attributes Lookup Table

   This table has includes the attributes for all of the received frames.
   If a received frame is periodic, this table also includes pointers to the
   received frame status and to the receive timeout counter for message
   gain and loss indication.

   =========================================================================*/
'''
  

  count1=0
  #IL_RX_ATTR_TABLE_INST
  print "#define IL_RX_ATTR_TABLE_INST"+str(can_channel_count)+"                           \\"
  print '{\\'
  for mess in tx_message:
    
    #print '   /*'+mess+' Message */\\'
    if message_dict[mess][3] == 0 or message_dict[mess][3] == 5: 
      if message_dict[mess][5] == 1:
        print '   (IL_RX_ATTR_PERIODIC | IL_RX_ATTR_TIMEOUT_MONITOR ),         /* Frame  Attributes          */   \\'
      else:
        print '   (IL_RX_ATTR_PERIODIC),         /* Frame  Attributes          */   \\'
    else:
      print '   0,          /* Frame  Attributes          */\\'
  print '}\n'
  
    #print '   &il_rx_frame_status['+str(count1)+'],         /* Pointer to Receive Status */            \\'
  
  #IL_RX_DATA_PTR_TABLE_INST
  print "#define IL_RX_DATA_PTR_TABLE_INST"+str(can_channel_count)+"                           \\"
  print '{\\'
  for mess in tx_message:
    print '   &il_rx_'+mess.lower()+'.byte[0],         /* Pointer to Received Frame Data    */    \\'
  print '}\n'
  
  #IL_RX_PERIODIC_CNT_TABLE_INST
  print "#define IL_RX_PERIODIC_CNT_TABLE_INST"+str(can_channel_count)+"                           \\"
  print '{\\'
  for mess in tx_message:
    print '   IL_TIME_IN_TASK_TICS('+str(int(message_dict[mess][2]))+'),         /* Timeout Count Value                   */     \\'
  print '}\n'
  
  
  
  #IL_RX_INDICATION_FN_TABLE_INST                             \\"
  print "#define IL_RX_INDICATION_FN_TABLE_INST"+str(can_channel_count)+"                             \\"
  print '{\\'
  for mess in tx_message:
    print '   &VnimIlRx_'+mess+'_SigIndication,         /* Receive Callback Function           */    \\'
  print '}\n'
  
  #IL_RX_FRAME_LOSS_IND_FN_TABLE_INST
  print "#define IL_RX_FRAME_LOSS_IND_FN_TABLE_INST"+str(can_channel_count)+"                             \\"
  print '{\\'  
  for mess in tx_message:
    if message_dict[mess][5] == 1:
      print '   &VnimIlRx_'+mess+'_SigTimeout,         /* Rx Msg Timeout Callback Function    */    \\'
    else:
      print '   NULL,       /* Rx Msg Timeout Callback Function    */    \\'
  print '}\n'

  
  #IL_RX_PRECOPY_TABLE_INST
  print "#define IL_RX_PRECOPY_TABLE_INST"+str(can_channel_count)+"                             \\"
  print '{\\'
  for mess in tx_message:  
    
    print '   &'+mess+'_PreCopy,          \\'
  print '}\n'
  
  #IL_RX_DLC_TABLE_INST
  print "#define IL_RX_DLC_TABLE_INST"+str(can_channel_count)+"                             \\"
  print '{\\'
  for mess in tx_message:
    print '   sizeof('+str(mess)+'_buf),          \\'
  print'}\n'
  
  print '''\n/* ===========================================================================
   Received Message (Frame) Callback Functions
   Eg: extern void VnimIlRx_EMS1_10_MsgIndication  ( void );
 =========================================================================*/\n\n'''

  for mess in tx_message:
    print 'void VnimIlRx_'+mess+'_SigIndication(void);'
  print '''\n\n/* ===========================================================================
  Received Message (Frame) Timeout Callback Functions
  Eg: extern void VnimIlRx_EMS1_10_Timeout   ( void );
 =========================================================================*/\n\n'''

  for mess in tx_message:
    if message_dict[mess][4] >0:
      print 'void VnimIlRx_'+mess+'_SigTimeout(void);'
  print '''\n\n/* ===========================================================================
  Interaction Layer Receive Signal Precopy Functions
  Eg: extern void EMS1_10_PreCopy   (void);
 =========================================================================*/\n\n'''

  for mess in tx_message:
    print 'void '+ mess+'_PreCopy(void);'
      
      
      
def message_structure_generation_tx():
  
  
  
 
  for mess in tx_message:
   if message_dict[mess][5] == 1:
    sig=[]
    for signals in message[mess]:
      sig.append(signals[1])
    #if min(sig)<=32 :
    print 'void VnimIlTx_'+mess+'_Confirmation(void);'
    
  
  #creating TX macros 
  print '\n\n'
  print '#define IL_TX_NUM_MSG_INST'+str(can_channel_count)+'  ('+str(len(tx_message))+')'
  total_sig = 0
  for x in message:
    total_sig = total_sig + len(message[x])
  print '#define IL_TX_NUM_SIGNALS_INST'+str(can_channel_count)+'  ('+str(total_sig)+')'
  
  print '#define IL_TX_NUM_IDS_INST'+str(can_channel_count)+'  ('+str(len(tx_message))+')'
  
  count1=0
  for mess in tx_message:
    if message_dict[mess][3] == 0 or message_dict[mess][3] == 5:
      count1+=1
      
  print '#define IL_TX_NUM_PERIODIC_INST'+str(can_channel_count)+'  (IL_TX_NUM_MSG_INST'+str(can_channel_count)+')'
  #print '#define IL_NUM_INSTANCE    1\n'
  print "\n\n#if (IL_NUM_INSTANCE > 1)"
  print '''  #if((IL_TX_NUM_MSG_INST1 > IL_TX_NUM_MSG_INST0))
     #define IL_TX_NUM_MESSAGES IL_TX_NUM_MSG_INST1
  #else
     #define IL_TX_NUM_MESSAGES IL_TX_NUM_MSG_INST0
  #endif
#else
  #define IL_TX_NUM_MESSAGES IL_TX_NUM_MSG_INST0
#endif\n\n'''

  
  print '''/* ===========================================================================
   Interaction Layer Transmit Message Enumerations
   =========================================================================*/'''
  count1 = 0
  for mess in tx_message:
    print  '#define VNIM_'+mess+'_MESSAGE    ('+str(count1)+')'
    count1+=1
  
  #tx frame table
  count1=0
  print'''\n\n/* ===========================================================================
  Interaction Layer Transmit Frame Table

  Each entry in this table defines the attributes for a specific transmit
  frame transmitted by the Interaction Layer.

 =========================================================================*/\n\n'''
  print "#define IL_TX_ATTR_TABLE_INST"+str(can_channel_count)+"       \\"
  print '{\\'
  for mess in tx_message:
    #print '   /*'+mess+' Message */\\'
    if message_dict[mess][3] == 0 :
      if message_dict[mess][4] == 1 and message_dict[mess][5] != 1:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1 and message_dict[mess][4] != 1 :
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1 and message_dict[mess][4] == 1 and message_dict[mess][5] == 1:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_TXC_NOTIFY | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      else:
        print '   (IL_TX_ATTR_PERIODIC),         /* Frame Transmission Attributes              */   \\'
    elif message_dict[mess][3] == 1 :
      if message_dict[mess][4] == 1 and message_dict[mess][5] != 1:
        print '   (IL_TX_ATTR_EVENT | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1 and message_dict[mess][5] != 1:
        print '   (IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1 and message_dict[mess][4] == 1 and message_dict[mess][5] == 1:
        print '   (IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      else:
        print '   (IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\'
    elif message_dict[mess][3] == 5 :
      if message_dict[mess][4] == 1 and message_dict[mess][5] != 1:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1and message_dict[mess][4] != 1:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY),         /* Frame Transmission Attributes              */   \\'
      elif message_dict[mess][5] == 1 and message_dict[mess][4] == 1 and message_dict[mess][5] == 1:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT | IL_TX_ATTR_TXC_NOTIFY | IL_TX_ATTR_INIT),         /* Frame Transmission Attributes              */   \\'
      else:
        print '   (IL_TX_ATTR_PERIODIC | IL_TX_ATTR_EVENT),         /* Frame Transmission Attributes              */   \\'
    else:
      print '   0,         /* Frame Transmission Attributes              */   \\'
  print '}\n'
  
  #IL_TX_DATA_PTR_TABLE_INST
  print '\n#define IL_TX_DATA_PTR_TABLE_INST'+str(can_channel_count)+'       \\'
  print '{\\'
  count1 =0 
  for mess in tx_message:
    #print '   &il_tx_frame_status[ '+str(count1)+' ],         /* Pointer to Transmit Status */            \\'
    print '   &il_tx_'+mess.lower()+'.byte[0],         /* Pointer to Transmit Frame Data    */    \\'
  print '}'
  
  #IL_TX_PERIODIC_CNT_TABLE_INST
  print '\n#define IL_TX_PERIODIC_CNT_TABLE_INST'+str(can_channel_count)+' \\'
  print '{\\'
    #print '   &il_tx_delay_count[ '+str(count1)+' ],         /* Pointer to the Transmit Delay Count          */  \\' 
  for mess in tx_message:  
     if str(message_dict[mess][2])!= 0:
      print '   IL_TIME_IN_TASK_TICS('+str( message_dict[mess][2])+'),           /* Primary Period in Task Tics  */     \\'
     else:
      print '   IL_TIME_IN_TASK_TICS(0),           /* Primary Period in Task Tics  */     \\'
  print '}'
  
  #IL_TX_EVENT_PERIODIC_CNT_TABLE_INST
  
  print "\n#define IL_TX_EVENT_PERIODIC_CNT_TABLE_INST"+str(can_channel_count)+"                           \\"
  print '{\\'
  for mess in tx_message:
    #if message_dict[mess][3] == 5:
    #print '   ('+str(int(message_dict[mess][2]))+'),         /* Primary Period in Task Tics              */     \\'
    print '  IL_TIME_IN_TASK_TICS(0),          /* Primary Period in Task Tics              */     \\'
  print '}\n'
  
  #print '   &il_tx_periodic[ '+str(count1)+' ],     /* Pointer to the Periodic Attributes (or NULL) */  \\'
  #print '   NULL,     /* Pointer to Burst Periodic Frame Attributes   */ \\'
  #print '   &il_tx_can_tmd['+str(count1)+'],         /* Pointer to CAN Driver TMD Data Structure     */  \\'
  
  #IL_TX_CONF_TABLE_INST
  print '\n#define IL_TX_CONF_TABLE_INST'+str(can_channel_count)+'         \\'
  print '{\\'
  for mess in tx_message:  
    if message_dict[mess][5] == 1:
      print '   &VnimIlTx_'+mess+'_Confirmation,         /* Pointer to Tx Complete Callback Function     */  \\'
    else:
      print '   NULL         /* Pointer to Tx Complete Callback Function     */  \\'
  print '}'
  '''if count1 == len(tx_message)-1: 
      print '   }            \\'
    else:
      print '   },            \\'
    count1+=1
  print '\n\n'''
  
  #IL_INIT_TX_PER_DATA_TABLE_INST0
  print '\n#define IL_INIT_TX_PER_DATA_TABLE_INST'+str(can_channel_count)+'       \\'
  print '{\\'
  for mess in tx_message:
    print '   0x0,    \\'
  print '}'
  
  #IL_TX_INIT_OFFSET_CNT_TABLE_INST
  print '\n#define IL_TX_INIT_OFFSET_CNT_TABLE_INST'+str(can_channel_count)+'      \\'
  print '{\\'
  for mess_no in range(1,len(tx_message)+1):
    if mess_no != len(tx_message):
      print '   '+str(mess_no)+',     \\'
    elif mess_no == len(tx_message):
      print '   '+str(mess_no)+'     \\'
  print '}'
  
  #no of repetition
  print '\n#define IL_TX_EVENT_MSG_RPT_CNT_INST'+str(can_channel_count)+'           \\'
  print '{     \\'
  count1=0
  for mess in tx_message:
        count1+=1
        if count1 != len(tx_message):
          print '   '+str(message_dict[mess][8]) +',            \\'
        elif count1 == len(tx_message):
          print '   '+str(message_dict[mess][8]) +'            \\'
  print '}\n\n'  
  
  #gen message delay time
  print '\n#define IL_TX_MIN_DELAY_COUNT_INST'+str(can_channel_count)+'           \\'
  print '{     \\'
  count1=0
  for mess in tx_message:
        count1+=1
        if count1 != len(tx_message):
          print '   IL_TIME_IN_TASK_TICS('+str(message_dict[mess][6]) +'),            \\'
        elif count1 == len(tx_message):
          print '   IL_TIME_IN_TASK_TICS('+str(message_dict[mess][6]) +')            \\'
  print '}\n\n' 
  
  #tx tmd structure
  print'''/* ===========================================================================
  Interaction Layer Transmit Message Data (TMD) Structures (Frame Definition)
										   
  !!! IMPORTANT NOTE !!! The transmit message handles must be specified
  sequentially, starting with 0 (zero). These message handles serve as an
  index to the transmit complete function pointers, so each index must map
  to the correct transmit complete callback function pointer in the lookup
  table (array of function pointers) for servicing transmit complete events.

 =========================================================================*/'''
  print '#define IL_TX_TMD_TABLE_INST'+str(can_channel_count)+'                         \\'
  count1 = 0
  
  for mess in tx_message:
    print '   /*'+mess+' Message */\\'
    print '   {\\'
    
    print '   CAN_GPNUM_'+str(message_dict[mess][1])+',                                   /* CAN message data length  */           \\'
    print '   '+str((message_dict[mess][0]).strip('L'))+',                                         /* CAN message identifier   */           \\'
    print '   &il_tx_'+mess.lower()+'.byte[0],         /* Pointer to Transmit Frame Data    */    \\'
    if int(str((message_dict[mess][0]).strip('L')),16) <= 4095:
      print '   CANB_TX_STD_DATA,                              /* CAN message options      */  \\'
    else:
      print '   CANB_TX_EXTENDED,                              /* CAN message options      */  \\'
    print '   '+mess+'_TMH                                /* Transmit Message Handle  */           \\'
    if count1 == len(tx_message)-1: 
      print '   }            \\'
    else:
      print '   },            \\'
    count1+=1
  print '\n\n'
  

  print'''/* ===========================================================================
    Interaction Layer Transmit Message Handle 
  =========================================================================*/'''
  temp_count=0
  for mess in tx_message:
    print'#define '+mess+'_TMH ('+str(temp_count)+')'
    temp_count+=1
  
  
  

  
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):    
    return [ atoi(c) for c in re.split('(\d+)', text) ]
    

    
if __name__ == "__main__":
  pass
  #f=open('nm_il_rx_frame.h','w')
  #sys.stdout = f
  #message_structure_generation_tx(read_sig_lst_sheet_tx,read_msg_lst_sheet_tx)
  #message_structure_generation_rx(read_sig_lst_sheet_rx,read_msg_lst_sheet_rx)