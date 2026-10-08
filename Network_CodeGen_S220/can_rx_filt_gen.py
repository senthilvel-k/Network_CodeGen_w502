import sys,json
import os
dbc=None
dbc_file_name=None

filter_code_gen_dir = './CODE_GEN'
filter_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgILSupport'
time_str=''
footer=''

datatype_8 = 'NW_UINT8'
datatype_16 = 'NW_UINT16'
datatype_32 = 'NW_UINT32'
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
Date                : '''+time_str+'''
By                  : '''+usr_name+'''
Traceability        : '''+dbc_file_name+'''
Change Description  : Tool Generated code
*****************************************************************************/'''

def filter_gen():
  global dbc,footer,filter_code_gen_dir,filter_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  dir = './CODE_GEN'
  if not os.path.exists(filter_code_gen_dir):
    os.mkdir(filter_code_gen_dir)
  f=open("./CODE_GEN/can_rxrule.cfg",'w')
  sys.stdout = f
  
  filter_cfg_file = open(filter_data_dir+"CanDbcMsgConfiguration.data",'r')
  filter_cfg_data = json.loads(filter_cfg_file.read())
  filter_cfg_file.close()
  
  nm_sorted_mes_rx=[]
  il_sorted_mes_rx=[]
  tp_sorted_mes_rx=[]
  
  il_mes_tx=[]
  all_msg_tx=dbc.get_msg_type('ALL','tx')
  all_mes_sorted_mes_tx = sorted(all_msg_tx,key = lambda x: x['Msg_name'])
  
  for mes in all_mes_sorted_mes_tx:
    if filter_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','ON','On',1,'1']:
      if filter_cfg_data[mes['Msg_name'].upper()+'_msg_type_no_of_events'] == 'Appl':
        il_mes_tx.append(mes)
  
  
  all_mes =[]
  
  all_msg_rx=dbc.get_msg_type('ALL','rx')
  all_mes_sorted_mes_rx = sorted(all_msg_rx,key = lambda x: x['Msg_name'])
  
  
  
  il_mes=[]
  nm_mes =[]
  diag_mes =[]
  
  for mes in all_mes_sorted_mes_rx:
    if filter_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','ON','On',1,'1']:
      if filter_cfg_data[mes['Msg_name'].upper()+'_msg_type_no_of_events'] == 'Appl':
        il_mes.append(mes)
      elif filter_cfg_data[mes['Msg_name'].upper()+'_msg_type_no_of_events'] == 'NM':
        nm_mes.append(mes)
      elif filter_cfg_data[mes['Msg_name'].upper()+'_msg_type_no_of_events'] == 'Diag':
        diag_mes.append(mes)
      else:
        pass
  
  no_of_receive_rule = 256
  
  #print diag_mes
  no_of_rx_msg_available = no_of_receive_rule-(len(nm_mes)-len(diag_mes))
  tx_rx_buf_0 = []
  tx_rx_buf_1 = []
  tx_rx_buf_2 = []
  
  tx_rx_buf_msg_0 = []
  tx_rx_buf_msg_1 = []
  tx_rx_buf_msg_2 = []
  
  header = '''#ifndef CAN_RX_RULECONFIG
#define CAN_RX_RULECONFIG

/* ===========================================================================
    
      Name:         rxrule.cfg
    
      Description:  Receive Rule (Message Filtering Configuration Input File 
					for CAN Controller    	

	  Version :		Initial Version
    
     ==========================================================================*/
'''
  
  print header
  
  print '#include "can_bcan.cfg"','\n'
  
  if (len(il_mes) < no_of_rx_msg_available):
    #alert()
    gui_avail_msg=len(il_mes)+len(nm_mes)+len(diag_mes)
    print '#define MAX_NO_RX_RULES_PER_CH	  '+str(gui_avail_msg),'\n'
    print '#define CAN0_NO_OF_RX_RULES	  '+str(gui_avail_msg),'\n'
    msg_count = 0
    if len(il_mes) <= 32:
      il_mes_max = 15
      if len(il_mes)%2 == 0:
        il_mes_max=(len(il_mes)/2)-1
      else:
        il_mes_max=(len(il_mes)/2)
      #print il_mes_max
      for mes in il_mes:
        if msg_count <= il_mes_max:
          tx_rx_buf_0.append((hex(int(mes['id'])),'0xC00007FF','0x100'))
          tx_rx_buf_msg_0.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        elif msg_count  > il_mes_max:
          tx_rx_buf_1.append((hex(int(mes['id'])),'0xC00007FF','0x200'))
          tx_rx_buf_msg_1.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        else:
          pass
        msg_count+=1
    
    elif len(il_mes) <= 48:
      for mes in il_mes:
        if msg_count <= 15:
          tx_rx_buf_0.append((hex(int(mes['id'])),'0xC00007FF','0x100'))
          tx_rx_buf_msg_0.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        elif msg_count  > 15 and msg_count <32:
          tx_rx_buf_1.append((hex(int(mes['id'])),'0xC00007FF','0x200'))
          tx_rx_buf_msg_1.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        elif msg_count  >= 32 and msg_count <48:
          tx_rx_buf_2.append((hex(int(mes['id'])),'0xC00007FF','0x400'))
          tx_rx_buf_msg_2.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        else:
          pass
        msg_count+=1

    elif len(il_mes) <= no_of_rx_msg_available:
      for mes in il_mes:
        if msg_count < 64:
          tx_rx_buf_0.append((hex(int(mes['id'])),'0xC00007FF','0x100'))
          tx_rx_buf_msg_0.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        elif msg_count  >= 64 and msg_count < 128:
          tx_rx_buf_1.append((hex(int(mes['id'])),'0xC00007FF','0x200'))
          tx_rx_buf_msg_1.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        elif msg_count  >= 128 and msg_count < no_of_rx_msg_available:
          tx_rx_buf_2.append((hex(int(mes['id'])),'0xC00007FF','0x400'))
          tx_rx_buf_msg_2.append((mes['id'],mes['DLC'],mes['Msg_name'],'IL'))
        else:
          pass
        msg_count+=1

    for mes in diag_mes:
      tx_rx_buf_2.append((hex(int(mes['id'])),'0xC0000700','0x400'))
      tx_rx_buf_msg_2.append((mes['id'],mes['DLC'],mes['Msg_name'],'TP'))
    for mes in nm_mes:
      tx_rx_buf_2.append((hex(int(mes['id'])),'0xC00007FF','0x400'))
      tx_rx_buf_msg_2.append((mes['id'],mes['DLC'],mes['Msg_name'],'NM'))

    temp_count = 1
    print '\n/* Message ID Definitions */\n'
    for val in tx_rx_buf_0:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_ID  (CAN_UINT32) '+val[0]+'u'
        temp_count+=1
    for val in tx_rx_buf_1:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_ID  (CAN_UINT32) '+val[0]+'u'
        temp_count+=1
    for val in tx_rx_buf_2:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_ID  (CAN_UINT32) '+val[0]+'u'
        temp_count+=1
    
    temp_count = 1    
    print '\n/* Filter Mask definitions - with RTR, IDE bit always compared */\n'
    for val in tx_rx_buf_0:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_MASK  (CAN_UINT32) '+val[1]+'u'
        temp_count+=1
    for val in tx_rx_buf_1:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_MASK  (CAN_UINT32) '+val[1]+'u'
        temp_count+=1
    for val in tx_rx_buf_2:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_MASK  (CAN_UINT32) '+val[1]+'u'
        temp_count+=1
        
    #below code is generated as it is from TCU 
    temp_count = 1
    print '\n/* Rx Receive Buffer selection (unused) */\n'
    for val in tx_rx_buf_0:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR0  (CAN_UINT32) 0x00'+'u'
        temp_count+=1
    for val in tx_rx_buf_1:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR0  (CAN_UINT32) 0x00'+'u'
        temp_count+=1
    for val in tx_rx_buf_2:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR0  (CAN_UINT32) 0x00'+'u'
        temp_count+=1
        
    #define	CAN0_RX_RULE1_PTR0	(CAN_UINT32) 0x00U  
   
    print '\n/* Tx/Rx FIFO Selection */\n'
    temp_count = 1
    for val in tx_rx_buf_0:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR1  (CAN_UINT32) '+val[2]+'u'
        temp_count+=1
    for val in tx_rx_buf_1:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR1  (CAN_UINT32) '+val[2]+'u'
        temp_count+=1
    for val in tx_rx_buf_2:
      if val != None:
        print '#define  CAN0_RX_RULE'+str(temp_count)+'_PTR1  (CAN_UINT32) '+val[2]+'u'
        temp_count+=1
      
      
    total_buf_len = len(tx_rx_buf_2)+len(tx_rx_buf_1)+len(tx_rx_buf_0)
    print '\n/*Receive Rule table configuration*/\n'
    print '#define CAN0_RX_RULE_TABLE \\'
    print '{  \\'
    
    for val in range(1,total_buf_len+1):
      if val == (total_buf_len):
        print '   {CAN0_RX_RULE'+str(val)+'_ID,CAN0_RX_RULE'+str(val)+'_MASK,CAN0_RX_RULE'+str(val)+'_PTR0,CAN0_RX_RULE'+str(val)+'_PTR1}   \\'   
      else:
        print '   {CAN0_RX_RULE'+str(val)+'_ID,CAN0_RX_RULE'+str(val)+'_MASK,CAN0_RX_RULE'+str(val)+'_PTR0,CAN0_RX_RULE'+str(val)+'_PTR1},  \\'   
    print '}'
  else:  
    app.evaluate_javascript("alert('No of message exceeds receive filter mask range')")
   
  print '\n\n#endif'
  print footer
  f.close()
  
  if not os.path.exists(filter_code_gen_dir):
    os.mkdir(filter_code_gen_dir)
  f=open("./CODE_GEN/nw_can_dll.h",'w')
  sys.stdout = f
  
  header = '''#ifndef NW_CAN_DLL_H
#define NW_CAN_DLL_H
/* ===========================================================================

                     CONFIDENTIAL VISTEON CORPORATION

  This is an unpublished work of authorship, which contains trade secrets,
  created in 2014.  Visteon Corporation owns all rights to this work and
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
  Name:           nw_can_dll.h
  Description:    CAN Data Link Layer Header File  
 =========================================================================*/'''
  print header

  includes ='''/* ===========================================================================
  I N C L U D E   F I L E S
=== =========================================================================*/
#include "types.h"
#include "can_type.h"
#include "can_defs.h" 
#include "nw_il.h"
#include "nw_il_par.h"
#include "can_bcan.cfg"
'''
  print includes
  
  print '''/* ===========================================================================
  P U B L I C   T Y P E   D E F I N I T I O N S
 =========================================================================*/
'''
  
#define DLL_NUM_RX_VECTORS         	(3)
  cntt=0
  if tx_rx_buf_msg_0 !=[]:
    cntt+=1
  if tx_rx_buf_msg_1 !=[]:
    cntt+=1
  if tx_rx_buf_msg_2 !=[]:
    cntt+=1
  print'#define DLL_NUM_RX_VECTORS         	('+str(cntt)+')'
  print'#define DLL_NUM_IL_TX_FRAMES        ('+str(len(il_mes_tx))+')'
  print'#define DLL_NUM_NM_TX_FRAMES        (DLL_NUM_IL_TX_FRAMES)'
  print '''\n/* ===========================================================================
**  Macros to Support Rx Qualification and Dispatch and Transmit Complete
**  Dispatch and Notification
** =========================================================================*/

#define DLL_RX_IL_FRAME            (0)
#define DLL_RX_DIAG_FRAME          (1)
#define DLL_RX_TP_FRAME            (2)
#define DLL_RX_NM_FRAME            (3)
#define DLL_RX_FRAME_INVALID       (4)'''


  print '''/* ===========================================================================
**  P R I V A T E  T Y P E  D E F I N I T I O N S
** =========================================================================*/

typedef struct tagDLL_RX_VECTOR_DISPATCH
{
    CAN_UINT32  const identifier;     /* CAN Frame Identifier         */
	#if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
    CAN_UINT32  const dlc;			  /* For DLC Check */
	#endif
    CAN_UINT16  const frmHandle;      /* CAN Frame Handle (Index)     */
    CAN_UINT8   const frmLayer;       /* Network Layer to Receive Frame  */
} DLL_RX_VECTOR_DISPATCH;


typedef struct tagDLL_RX_DISPATCH
{
    CAN_UINT8   const numIDs;                              /* Number of ID's in the Vector */
    DLL_RX_VECTOR_DISPATCH const * const  pVectorDispatch; /* Pointer to Vector Dispatch   */
} DLL_RX_DISPATCH;'''

  
  print '''/* ===========================================================================
  CAN Hardware Receive Vector Qualification Data Structures

  This set of data structures defines the CAN Identifiers that are received
  by each CAN receive filter/mask combination (termed a receive "vector").
  A specific filter mask/combination may qualify multiple CAN Identifiers,
  so this table is needed to further qualify which CAN ID's that pass a
  specific filter/mask combination are valid and therefore stored in the
  software receive queue for further processing.

 =========================================================================*/'''

  print '\n /* CAN Hardware Receive Vector0*/'
  temp_count = 0
  if tx_rx_buf_msg_0 !=[]:
    print 'static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector0[ ] ='
    print '{'
    for val in tx_rx_buf_msg_0:
      print '   {'
      print '       '+hex(int(val[0]))+','
      print '       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)'
      print '         '+val[1]+'u,'
      print '       #endif'
      print '       VNIM_'+val[2].upper()+'_MESSAGE,'
      print '       DLL_RX_'+val[3]+'_FRAME'
      if temp_count == len(tx_rx_buf_msg_0)-1:
        print '   }'
      else:
        print '   },'
      temp_count+=1
    print '};\n'
    
  print '\n /* CAN Hardware Receive Vector1*/'
  temp_count = 0
  if tx_rx_buf_msg_1 !=[]:
    print 'static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector1[ ] ='
    print '{'
    for val in tx_rx_buf_msg_1:
      print '   {'
      print '       '+hex(int(val[0]))+','
      print '       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)'
      print '         '+val[1]+'u,'
      print '       #endif'
      print '       VNIM_'+val[2].upper()+'_MESSAGE,'
      print '       DLL_RX_'+val[3]+'_FRAME'
      if temp_count == len(tx_rx_buf_msg_1)-1:
        print '   }'
      else:
        print '   },'
      temp_count+=1
    print '};\n'
    
  print '\n /* CAN Hardware Receive Vector2*/'
  temp_count = 0
  if tx_rx_buf_msg_2 !=[]:
    print 'static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector2[ ] ='
    print '{'
    for val in tx_rx_buf_msg_2:
      print '   {'
      print '       '+hex(int(val[0]))+','
      print '       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)'
      print '         '+val[1]+'u,'
      print '       #endif'
      print '       VNIM_'+val[2].upper()+'_MESSAGE,'
      print '       DLL_RX_'+val[3]+'_FRAME'
      if temp_count == len(tx_rx_buf_msg_2)-1:
        print '   }'
      else:
        print '   },'
      temp_count+=1
    print '};\n'
  
  if tx_rx_buf_msg_0 !=[]:
    print '''#define DLL_CAN_RX_VECTOR_0_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector0)/sizeof(DLL_RX_VECTOR_DISPATCH)))'''
  if tx_rx_buf_msg_1 !=[]:
    print '#define DLL_CAN_RX_VECTOR_1_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector1)/sizeof(DLL_RX_VECTOR_DISPATCH)))'
  if tx_rx_buf_msg_2 !=[]:
    print '#define DLL_CAN_RX_VECTOR_2_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector2)/sizeof(DLL_RX_VECTOR_DISPATCH)))'

  print '''/* ===========================================================================
  Received Frame Dispatch Table

  This data structure is an array of pointers to the data structures that
  define the received CAN ID's that are to be qualified for each hardware
  receive vector. A hardware receive vector corresponds to a CAN filter/mask
  combination that qualifies received CAN messages that may need to be
  further filtered at the software level.

 =========================================================================*/
static DLL_RX_DISPATCH const dllRxDispatchTable[ DLL_NUM_RX_VECTORS ] =
{'''
  if tx_rx_buf_msg_0 !=[]: 
    print '   { DLL_CAN_RX_VECTOR_0_NUM_RX_IDS, &dllhscanRxIdsVector0[ 0 ] },'
  if tx_rx_buf_msg_1 !=[]: 
    print '   { DLL_CAN_RX_VECTOR_1_NUM_RX_IDS, &dllhscanRxIdsVector1[ 0 ] },'
  if tx_rx_buf_msg_2 !=[]: 
    print '   { DLL_CAN_RX_VECTOR_2_NUM_RX_IDS, &dllhscanRxIdsVector2[ 0 ] },'
    
  print '''};'''

  print '''
/* ===========================================================================
  P U B L I C   F U N C T I O N   P R O T O T Y P E S
 =========================================================================*/
void DllInit(void);
void DllTxTask( void );
void DllRxTask(void);
void DllDsblMsgs (void);
void DllEnblMsgs (void);
void DllWakeup (void);
void Dll_DsblIntr (void);
void Dll_EnblIntr (void);
void DllSleep(void);
void DllShutdown(void);
CAN_RC DllTransmit (CAN_HMV const hMv, CAN_TMD const * const pTmd);
#endif /* VNIM_MICAN_DLL_H */
/******************************* End of File *********************************/
'''
  print footer
  f.close()
   
  

  

if __name__ == "__main__":
    pass
    '''import datetime
    time_print = datetime.datetime.now()
    set_file_node_il('U321.dbc','IS')
    set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
    
    filter_gen()'''