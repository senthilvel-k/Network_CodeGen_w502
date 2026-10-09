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
full_msg="ALL"
time_str=''
footer=''

datatype_8 = 'CAN_UINT8'
datatype_16 = 'CAN_UINT16'
datatype_32 = 'CAN_UINT32'


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

def message_Put_tx():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
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
          
  print('''/* ====================================================================================
  Interaction Layer Receive Signal Tx Put Functions
  =====================================================================================*/
''')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      sig_list =[]
      for signal in mes['Sig_List']:
          mes['Sig_List'][signal]['Sig_name']=signal
          sig_list.append(mes['Sig_List'][signal])
         
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      a=[]
      unused_length=0
      start_bit=0

      ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
      intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
      moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
      #logic for implementing the layout with signal and unused bit

      if sorted_bit:
        for signals in sorted_bit:
          signal_occur=0
          sig_start_bit = int(signals['Endbit'])
          layout_row_start=int(signals['Endbit'])//8
          layout_col_start=int(signals['Endbit'])%8
          signal_length=int(signals['Len'])
          sig_name = signals['Sig_name']
          end_bit=int(signals['Endbit'])+signal_length-1
          layout_row_end = end_bit//8

          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8

    
          if signals['Order'] == 'Intel':  
            if signal_length<=8:
              #print datatype_8+' sigData)'
              #print '   IlEnterCritical(INST0);'
              if layout_row_start != layout_row_end: 
                print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_8+' sigData)')
                print('{')
                bits_left = 8 - (sig_start_bit % 8)
                if (bits_left < signal_length):
                  rem = signal_length
                  cl = 0
                  while (rem > 0):
                    if cl == 0:
                      bits_to_be_filled = bits_left
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled = rem
                      rem -= bits_to_be_filled
                    a = '1' * bits_to_be_filled
                    if a != '11111111':
                      if cl != 0:
                        print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (((sigData) >> '+str(bits_left)+') & ' + "0x%02x" % int(a, 2) + '));')
                      else:
                        print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (sigData & ' + "0x%02x" % int(a, 2) + '));')
                    else:
                      print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') sigData );')
                    cl += 1

                else:
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                    a='1'*bits_to_be_filled
                    if a!='11111111':
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (sigData & '+"0x%02x"%int(a,2)+'));')
                    else:
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') sigData );')
                    cl+=1

              #print '   IlLeaveCritical(INST0);\n}\n'
                print('}\n')

            elif signal_length>8 and signal_length <= 32:
              start_bit=sig_start_bit
              length=signal_length
              rem=length
              cl=0
              path=0
              byt = 0
              
              if signal_length <=16:
                print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_16+' sig_Data)')
                print('{')
                #print'   IlEnterCritical(INST0);'
              elif signal_length >16 and signal_length <= 32:
                print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_32+' sig_Data)')
                print('{') 
              else:
                pass
                
              while(rem>0):
                if start_bit%8!=0:
                  path=1
                  b1=start_bit%8
                  bit_to_be_filled=8-b1
                  rem-=bit_to_be_filled
                  start_bit=start_bit+bit_to_be_filled
                  a='1'*bit_to_be_filled
                  print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((sig_Data) & '+"0x%02x"%int(a,2)+');')
                  cl+=1
                else:
                  if path != 0:
                    if rem >=8:
                      rem=rem-8
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((sig_Data) >> '+str(bit_to_be_filled)+') & 0xff);')
                      bit_to_be_filled+=8
                    elif rem>0 and rem<8:
                      a='1'*rem
                      #((vuint8) ((sigData >> 8) & (vuint8) 0x03u));
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((sig_Data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                      rem=0
                    start_bit+=8
                    cl+=1
                  else:
                    if rem>=8:
                      if cl == 0:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((sig_Data) & 0xff);')
                      else:
                        byt+=8
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((sig_Data) >>' +str(byt)+') & 0xff);')
                        #print 'byte'+str(cl)+'data'+'>>8'
                      rem-=8
                    else:
                      byt += 8
                      a='1'*rem
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((sig_Data) >> ' +str(byt)+') & '+"0x%02x"%int(a,2)+');')
                      #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                      rem-=rem
                    cl+=1
                    #print '   IlLeaveCritical(INST0);\n}\n'
              print('}\n')
          
            elif signal_length <=64 and signal_length >32 :
              co = 0
              print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_8+' const * const pData)')
              print('{\n')
              #print '   IlEnterCritical(INST0);'
              #print co,signal_length
              while (co < signal_length//8):
                print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                co+=1
                #print '   IlLeaveCritical(INST0);\n}\n'
              print('}\n')

            else:
              print('fail')
      
          elif signals['Order'] == 'Motorola':
            if sig_start_bit == 7 and sig_start_bit ==1 :
              start_bit=sig_start_bit
            else:
              start_bit = (sig_start_bit-7) + 8*((signal_length//8)-1)
              
              if signal_length>32 and signal_length<=64:
                print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_8+' const * const pData)')
                print('{\n')
                #print '   IlEnterCritical(INST0);'
                co = 0
                while (co < signal_length//8):
                  print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                  co+=1
                print('}\n')
              elif signal_length>8 and signal_length <= 32:
                  length=signal_length
                  rem=length
                  cl=0
                  path=0
                  byt = 0
                  if signal_length<=16:
                    print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_16+' sig_Data)')
                    print('{')
                    #print'   IlEnterCritical(INST0);'
                  elif signal_length>16 and signal_length <=32:
                    print('void ILPutTx_'+sig_name.upper()+'_data('+datatype_32+' sig_Data)')
                    print('{') 
                  else:
                    pass
                    
                  while(rem>0):
                    if start_bit%8!=0:
                      path=1
                      b1=start_bit%8
                      bit_to_be_filled=8-b1

                      rem-=bit_to_be_filled
                      start_bit=start_bit+bit_to_be_filled
                      a='1'*bit_to_be_filled
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((sig_Data) & '+"0x%02x"%int(a,2)+');')
                      cl+=1
                    else:
                      if path != 0:
                        if rem >=8:
                          rem=rem-8
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((sig_Data) >> '+str(bit_to_be_filled)+') & 0xff);')
                          bit_to_be_filled+=8
                        elif rem>0 and rem<8:
                          a='1'*rem
                          #((vuint8) ((sigData >> 8) & (vuint8) 0x03u));
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((sig_Data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                          rem=0
                        start_bit+=8
                        cl+=1
                      else:
                        if rem>=8:
                          if cl == 0:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((sig_Data) & 0xff);')
                          else:
                            byt+=8
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((sig_Data) >>' +str(byt)+') & 0xff);')
                            #print 'byte'+str(cl)+'data'+'>>8'
                          rem-=8
                        else:
                          a='1'*rem
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((sig_Data) >> 8'+') & '+"0x%02x"%int(a,2)+');')
                          #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                          rem-=rem
                        cl+=1
                  print('}\n')
              elif signal_length <=8 :
                layout_row_start = start_bit//8
                layout_row_end = (sig_start_bit//8)
                if layout_row_start != layout_row_end: 
                  print('void ILPutTx'+sig_name.upper()+'_data('+datatype_8+' sigData)')
                  print('{')
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                    a='1'*bits_to_be_filled
                    if a!='11111111':
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (sigData & '+"0x%02x"%int(a,2)+'));')
                    else:
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') sigData );')
                    cl+=1
                  print('}\n')
                
def message_Put_rx():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()

  il_msg_rx=[]
  nm_msg_rx=[]
  diag_msg_rx=[]
           
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
  
  print('''/* ====================================================================================
  Interaction Layer Receive Signal Rx Put Functions
  =====================================================================================*/
''')

  for mes in il_sorted_mes_rx_ordered:
    #print mes
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Multiplex'] == 'YES':
        mul_msg=dbc.get_multiplex(mes['id'])
        multiplexor_id=mul_msg['Multiplexor']
      sig_list =[]
      for signal in mes['Sig_List']:
          mes['Sig_List'][signal]['Sig_name']=signal
          sig_list.append(mes['Sig_List'][signal])
         
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      a=[]
      unused_length=0
      start_bit=0

      ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
      intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
      moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
      #logic for implementing the layout with signal and unused bit

      if sorted_bit:
        for signals in sorted_bit:
          if mes['Multiplex'] == 'YES':
            multiplexor_index=0
            for sig_list in mul_msg['Multiplex_group']:
              if signals['Sig_name'] in sig_list:
                multiplexor_index=mul_msg['Multiplex_group'].index(sig_list)
          signal_occur=0
          sig_start_bit = int(signals['Endbit'])
          layout_row_start=int(signals['Endbit'])//8
          layout_col_start=int(signals['Endbit'])%8
          signal_length=int(signals['Len'])
          sig_name = signals['Sig_name']
          end_bit=int(signals['Endbit'])+signal_length-1
          layout_row_end = end_bit//8

          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8

    
          if signals['Order'] == 'Intel':  
            if signal_length<=8:
              bits_left = 8 - (sig_start_bit % 8)
              if (bits_left < signal_length):
                # print datatype_8+' sigData)'
                # print '   IlEnterCritical(INST0);'
                if layout_row_start != layout_row_end:
                  print('void ILRxPut_' + sig_name.upper() + '(' + datatype_8 + ' data)')
                  print('{')
                  # print '   CAN_CCR     saveCcr;'
                  print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  # print'   IlEnterCritical(INST0);'
                  rem = signal_length
                  start_bit_1 = sig_start_bit // 8
                  cl = 0
                  while (rem > 0):
                    if cl == 0:
                      bits_to_be_filled = bits_left
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled = rem
                      rem -= bits_to_be_filled
                    a = '1' * bits_to_be_filled
                    if a != '11111111':
                      if cl != 0:
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   ' + mes['Msg_name'].upper() + '.' + mes[
                              'Msg_name'].lower() + '.' + multiplexor_id.lower() + '_data' + '.' + multiplexor_id.lower() + '_' + str( multiplexor_index) + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (((data) >> '+str(bits_left)+') & ' + "0x%02x" % int(a, 2) + '));')
                          else:
                            # print '   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));'
                            print('   ' + mes['Msg_name'].upper() + '.' + mes[
                              'Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (((data) >> '+str(bits_left)+') & ' + "0x%02x" % int(a, 2) + '));')
                        else:
                          print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (((data) >> '+str(bits_left)+') & ' + "0x%02x" % int(a, 2) + '));')
                      else:
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + multiplexor_id.lower() + '_data' + '.' + multiplexor_id.lower() + '_' + str(multiplexor_index) + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (data & ' + "0x%02x" % int(a, 2) + '));')
                          else:
                            # print '   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));'
                            print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (data & ' + "0x%02x" % int(a, 2) + '));')
                        else:
                          print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') (data & ' + "0x%02x" % int(a, 2) + '));')
                    else:
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   ' + mes['Msg_name'].upper() + '.' + mes[
                            'Msg_name'].lower() + '.' + multiplexor_id.lower() + '_data' + '.' + multiplexor_id.lower() + '_' + str(multiplexor_index) + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') data );')
                        else:
                          print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ' = ((' + datatype_8 + ') data );')

                      else:
                        print('   ' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str( cl) + ' = ((' + datatype_8 + ') data );')
                    cl += 1

                  # print '   IlLeaveCritical(INST0);\n}\n'
                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('}\n')
              else:
                #print datatype_8+' sigData)'
                #print '   IlEnterCritical(INST0);'
                if layout_row_start != layout_row_end:
                  print('void ILRxPut_'+sig_name.upper()+'('+datatype_8+' data)')
                  print('{')
                  #print '   CAN_CCR     saveCcr;'
                  print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  #print'   IlEnterCritical(INST0);'
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                    a='1'*bits_to_be_filled
                    if a!='11111111':
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')
                        else:
                          #print '   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));'
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')

                    else:
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')

                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')
                    cl+=1

                #print '   IlLeaveCritical(INST0);\n}\n'
                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('}\n')

            elif signal_length>8 and signal_length <= 32:
              start_bit=sig_start_bit
              length=signal_length
              rem=length
              cl=0
              path=0
              byt = 0
              
              if signal_length <=16:
                print('void ILRxPut_'+sig_name.upper()+'('+datatype_16+' data)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
                #print'   IlEnterCritical(INST0);'
              elif signal_length >16 and signal_length <= 32:
                print('void ILRxPut_'+sig_name.upper()+'('+datatype_32+' data)')
                print('{') 
                #print '   CAN_CCR     saveCcr;'
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              else:
                pass
                
              while(rem>0):
                if start_bit%8!=0:
                  path=1
                  b1=start_bit%8
                  bit_to_be_filled=8-b1
                  rem-=bit_to_be_filled
                  start_bit=start_bit+bit_to_be_filled
                  a='1'*bit_to_be_filled
                  if mes['Multiplex'] == 'YES':
                    if signals['Mul_order'] != 'root':
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                    else:
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                    
                  else:
                    print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                  cl+=1
                else:
                  if path != 0:
                    if rem >=8:
                      rem=rem-8
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                          
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                      bit_to_be_filled+=8
                    elif rem>0 and rem<8:
                      a='1'*rem
                      #((vuint8) ((sigData >> 8) & (vuint8) 0x03u));
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                          
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                      rem=0
                    start_bit+=8
                    cl+=1
                  else:
                    if rem>=8:
                      if cl == 0:
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                          else:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                      else:
                        byt+=8
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                          else:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                            
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                        #print 'byte'+str(cl)+'data'+'>>8'
                      rem-=8
                    else:
                      byt+=8
                      a='1'*rem
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> 8'+') & '+"0x%02x"%int(a,2)+');')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> '+str(byt)+') & '+"0x%02x"%int(a,2)+');')
                        
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> '+str(byt)+') & '+"0x%02x"%int(a,2)+');')
                      #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                      rem-=rem
                    cl+=1
                    #print '   IlLeaveCritical(INST0);\n}\n'
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')
          
            elif signal_length <=64 and signal_length >32 :
              co = 0
              print('void ILRxPut_'+sig_name.upper()+'('+datatype_8+' const * const pData)')
              print('{\n')
              #print '   CAN_CCR     saveCcr;'
              print('    CAN_ENTER_CRITICAL_SECTION(0);')
              #print '   IlEnterCritical(INST0);'
              #print co,signal_length
              while (co < signal_length//8):
                if mes['Multiplex'] == 'YES':
                  if signals['Mul_order'] != 'root':
                    print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                  else:
                    print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                    
                else:
                  print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                co+=1
                #print '   IlLeaveCritical(INST0);\n}\n'
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')

            else:
              print('fail')
      
          elif signals['Order'] == 'Motorola':
            if sig_start_bit == 7 and sig_start_bit ==1 :
              start_bit=sig_start_bit
            else:
              start_bit = (sig_start_bit-7) + 8*((signal_length//8)-1)
              
              if signal_length>32 and signal_length<=64:
                print('void ILRxPut_'+sig_name.upper()+'('+datatype_8+' const * const pData)')
                print('{\n')
                #print '   CAN_CCR     saveCcr;'
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
                #print '   IlEnterCritical(INST0);'
                co = 0
                while (co < signal_length//8):
                  if mes['Multiplex'] == 'YES':
                    if signals['Mul_order'] != 'root':
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                    else:
                      print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                      
                  else:
                    print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co) +' = pData['+str(co)+'];')
                  co+=1
                print('   CAN_EXIT_CRITICAL_SECTION(0);')
                print('}\n')
                
              elif signal_length>8 and signal_length <= 32:
                  length=signal_length
                  rem=length
                  cl=0
                  path=0
                  byt = 0
                  if signal_length<=16:
                    print('void ILRxPut_'+sig_name.upper()+'('+datatype_16+' data)')
                    print('{')
                    #print '   CAN_CCR     saveCcr;'
                    print('    CAN_ENTER_CRITICAL_SECTION(0);')
                    #print'   IlEnterCritical(INST0);'
                  elif signal_length>16 and signal_length <=32:
                    print('void ILRxPut_'+sig_name.upper()+'('+datatype_32+' data)')
                    print('{') 
                    #print '   CAN_CCR     saveCcr;'
                    print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  else:
                    pass
                    
                  while(rem>0):
                    if start_bit%8!=0:
                      path=1
                      b1=start_bit%8
                      bit_to_be_filled=8-b1

                      rem-=bit_to_be_filled
                      start_bit=start_bit+bit_to_be_filled
                      a='1'*bit_to_be_filled
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                          
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & '+"0x%02x"%int(a,2)+');')
                      cl+=1
                    else:
                      if path != 0:
                        if rem >=8:
                          rem=rem-8
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                            else:
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                              
                          else:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & 0xff);')
                          bit_to_be_filled+=8
                        elif rem>0 and rem<8:
                          a='1'*rem
                          #((vuint8) ((sigData >> 8) & (vuint8) 0x03u));
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                            else:
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                              
                          else:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') (((data) >> '+str(bit_to_be_filled)+') & '+"0x%02x"%int(a,2)+');')
                          rem=0
                        start_bit+=8
                        cl+=1
                      else:
                        if rem>=8:
                          if cl == 0:
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                              else:
                                print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                            else:
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = ('+datatype_8+') ((data) & 0xff);')
                          else:
                            byt+=8
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                              else:
                                print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                                
                            else:
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >>' +str(byt)+') & 0xff);')
                            #print 'byte'+str(cl)+'data'+'>>8'
                          rem-=8
                        else:
                          byt+=8
                          a='1'*rem
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> 8'+') & '+"0x%02x"%int(a,2)+');')
                            else:
                              print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> '+str(byt)+') & '+"0x%02x"%int(a,2)+');')
                            
                          else:
                            print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +' = ('+datatype_8+') (((data) >> '+str(byt)+') & '+"0x%02x"%int(a,2)+');')
                          #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                          rem-=rem
                        cl+=1
                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('}\n')
              elif signal_length <=8 :
                layout_row_start = start_bit//8
                layout_row_end = (sig_start_bit//8)
                if layout_row_start != layout_row_end: 
                  print('void ILRxPut_'+sig_name.upper()+'('+datatype_8+' data)')
                  print('{')
                  #print '   CAN_CCR     saveCcr;'
                  print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                    a='1'*bits_to_be_filled
                    if a!='11111111':
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')
                          
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') (data & '+"0x%02x"%int(a,2)+'));')
                    else:
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')
                        else:
                          print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')
                      
                      else:
                        print('   '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+' = (('+datatype_8+') data );')
                    cl+=1
                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('}\n')
       
def message_Get_tx():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
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
  
  print('''/* ====================================================================================
  Interaction Layer Receive Signal Tx Get Functions
  =====================================================================================*/
''')
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      sig_list =[]
      for signal in mes['Sig_List']:
          mes['Sig_List'][signal]['Sig_name']=signal
          sig_list.append(mes['Sig_List'][signal])
         
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      a=[]
      unused_length=0
      start_bit=0

      ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
      intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
      moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
      #logic for implementing the layout with signal and unused bit

      if sorted_bit:
        for signals in sorted_bit:
          signal_occur=0
          sig_start_bit = int(signals['Endbit'])
          layout_row_start=int(signals['Endbit'])//8
          layout_col_start=int(signals['Endbit'])%8
          signal_length=int(signals['Len'])
          sig_name = signals['Sig_name']
          end_bit=int(signals['Endbit'])+signal_length-1
          layout_row_end = end_bit//8

          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8

    
          if signals['Order'] == 'Intel':  
    
            if signal_length<=8:

              if layout_row_start != layout_row_end:
                print(datatype_8+' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_8+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
                bits_left = 8 - (sig_start_bit % 8)
                if (bits_left < signal_length):
                  rem = signal_length
                  cl = 0
                  while (rem > 0):
                    if cl == 0:
                      bits_to_be_filled = signal_length-bits_left
                      rem -= bits_to_be_filled
                      print('   rValue = (' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ';')
                    else:
                      bits_to_be_filled = rem
                      rem -= bits_to_be_filled
                      print('   rValue |= (' + datatype_8 + ')(((' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + \
                            mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ') << ' + str(
                        bits_to_be_filled) + ');')
                    cl += 1
                else:
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                      print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                      print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                    cl+=1

                print('   CAN_EXIT_CRITICAL_SECTION(0);')
                print('   return rValue;')
                print('}\n')

            elif signal_length>8 and signal_length <=32:
              start_bit=sig_start_bit
              length=signal_length
              rem=length
              cl=0
              path=0
              byt = 0
              if length >8 and length<=16:
                print(datatype_16 +' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_16+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              elif length >16 and length <=32:
                print(datatype_8+' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_32+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')

              while(rem>0):
                if start_bit%8!=0:
                  path=1
                  b1=start_bit%8
                  bit_to_be_filled=8-b1

                  rem-=bit_to_be_filled
                  start_bit=start_bit+bit_to_be_filled
                  a='1'*bit_to_be_filled
                  if length <= 16:
                    print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                  elif length >16 and length <= 32:
                    print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                  cl+=1
                else:
                  if path != 0:
                    if rem >=8:
                      rem=rem-8
                      if length <= 16:
                        print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                      elif length>16 and length <= 32:
                        print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                      bit_to_be_filled+=8
                    elif rem>0 and rem<8:
                      a='1'*rem
                      if length <= 16:
                        print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                      elif length >16 and length<=32 :
                        print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')

                      rem=0
                    start_bit+=8
                    cl+=1
                  else:
                    if rem>=8:
                      if cl == 0:
                        if length <=16:
                          print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                        elif length <=32:
                          print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                      else:
                        byt+=8
                        if length <=16:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                        elif length >16 and length <=32:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                        #print 'byte'+str(cl)+'data'+'>>8'
                      rem-=8
                    else:
                      a='1'*rem
                      byt+=8
                      if length <= 16:
                        print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                      elif length <=32 and length >16:
                        print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                      #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                      rem-=rem
                    cl+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('   return rValue;')
              print('}\n')
            elif signal_length <=64 and signal_length >32 :
              co = 0
              print('void ILGetTx_'+sig_name.upper()+'('+datatype_8+' * pData)\n{\n')
              #print '   CAN_CCR     saveCcr;'
              print('    CAN_ENTER_CRITICAL_SECTION(0);')
              while (co < signal_length//8):
                print('    pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co)+';')
                co+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')
          
          elif signals['Order'] == 'Motorola':
            if sig_start_bit== 7 and sig_start_bit ==1 :
              start_bit=sig_start_bit
            else:
              start_bit = (sig_start_bit-7) + 8*((signal_length//8)-1)
                     
            if signal_length <=64 and signal_length >32 :
              co = 0
              print('void ILGetTx_'+sig_name.upper()+'('+datatype_8+' * pData)\n{\n')
              #print '   CAN_CCR     saveCcr;'
              print('    CAN_ENTER_CRITICAL_SECTION(0);')
              while (co < signal_length//8):
                print('   pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_byte'+str(co)+';')
                co+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')
              
            elif signal_length>8 and signal_length <=32:
              rem = signal_length
              length = signal_length
              if signal_length<=16:
                print(datatype_16 +' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_16+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              elif signal_length>16 and signal_length<=32:
                print(datatype_8+' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_32+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              path = 0
              cl = 0
              byt = 0
              while(rem>0):
                  if start_bit%8!=0:
                    path=1
                    b1=start_bit%8
                    bit_to_be_filled=8-b1

                    rem-=bit_to_be_filled
                    start_bit=start_bit+bit_to_be_filled
                    a='1'*bit_to_be_filled
                    if length <= 16:
                      print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    elif length >16 and length <= 32:
                      print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    cl+=1
                  else:
                    if path != 0:
                      if rem >=8:
                        rem=rem-8
                        if length <= 16:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                        elif length>16 and length <= 32:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                        bit_to_be_filled+=8
                      elif rem>0 and rem<8:
                        a='1'*rem
                        if length <= 16:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                        elif length >16 and length<=32 :
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')

                        rem=0
                      start_bit+=8
                      cl+=1
                    else:
                      if rem>=8:
                        if cl == 0:
                          if length <=16:
                            print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                          elif length <=32:
                            print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                        else:
                          byt+=8
                          if length <=16:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          elif length >16 and length <=32:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          #print 'byte'+str(cl)+'data'+'>>8'
                        rem-=8
                      else:
                        a='1'*rem
                        byt+=8
                        if length <= 16:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                        elif length <=32 and length >16:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '++str(byt)+');')
                        #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                        rem-=rem
                      cl+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('   return rValue;')
              print('}\n')
                
            elif signal_length<=8:
              if layout_row_start != layout_row_end:
                layout_row_start = start_bit//8
                layout_row_end = sig_start_bit//8
                print(datatype_8+' ILGetTx_'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_8+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
                    
                rem=signal_length
                start_bit_1=start_bit//8
                cl=0
                while(rem>0):
                  if cl==0:
                    bits_to_be_filled = 8-start_bit_1
                    rem -= bits_to_be_filled
                    print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                  else:
                    bits_to_be_filled=rem
                    rem -= bits_to_be_filled
                    print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                  cl+=1

                print('   CAN_EXIT_CRITICAL_SECTION(0);')
                print('   return rValue;')
                print('}\n')


  
  
def message_Get_rx():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()

  il_msg_rx=[]
  nm_msg_rx=[]
  diag_msg_rx=[]
    
       
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
  
  print('''/* ====================================================================================
  Interaction Layer Receive Signal Rx Get Functions
  =====================================================================================*/
''')
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      if mes['Multiplex'] == 'YES':
        mul_msg=dbc.get_multiplex(mes['id'])
        multiplexor_id=mul_msg['Multiplexor']
      sig_list =[]
      for signal in mes['Sig_List']:
          mes['Sig_List'][signal]['Sig_name']=signal
          sig_list.append(mes['Sig_List'][signal])
         
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      a=[]
      unused_length=0
      start_bit=0

      ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
      intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
      moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
      #logic for implementing the layout with signal and unused bit

      if sorted_bit:
        for signals in sorted_bit:
          if mes['Multiplex'] == 'YES':
            multiplexor_index=0
            for sig_list in mul_msg['Multiplex_group']:
              if signals['Sig_name'] in sig_list:
                multiplexor_index=mul_msg['Multiplex_group'].index(sig_list)
          signal_occur=0
          sig_start_bit = int(signals['Endbit'])
          layout_row_start=int(signals['Endbit'])//8
          layout_col_start=int(signals['Endbit'])%8
          signal_length=int(signals['Len'])
          sig_name = signals['Sig_name']
          end_bit=int(signals['Endbit'])+signal_length-1
          layout_row_end = end_bit//8

          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8

    
          if signals['Order'] == 'Intel':  #signal format is  intel
    
            if signal_length<=8:#signal length less than 8
              bits_left = 8 - (sig_start_bit % 8)
              if (bits_left < signal_length):
                if layout_row_start != layout_row_end:  # if signal is in different byte position seperate function is used to get the value otherwise a macro is generated in par_h py file
                  print(datatype_8 + ' IlRxGet' + sig_name.upper() + '(void)')
                  print('{')
                  # print '   CAN_CCR     saveCcr;'
                  print('   ' + datatype_8 + '  rValue;')
                  print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  rem = signal_length
                  start_bit_1 = sig_start_bit // 8
                  cl = 0
                  while (rem > 0):
                    if cl == 0:
                      bits_to_be_filled = signal_length-bits_left
                      rem -= bits_to_be_filled
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue = (' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + multiplexor_id.lower() + '_data' + '.' + multiplexor_id.lower() + '_' + str(multiplexor_index) + '.' + sig_name.upper() + '_' + str(cl) + ';')
                        else:
                          print('   rValue = (' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ';')
                      else:
                        print('   rValue = (' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ';')
                    else:
                      bits_to_be_filled = rem
                      rem -= bits_to_be_filled
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue |= (' + datatype_8 + ')(((' + datatype_8 + ')' + mes[
                            'Msg_name'].upper() + '.' + mes[
                                  'Msg_name'].lower() + '.' + multiplexor_id.lower() + '_data' + '.' + multiplexor_id.lower() + '_' + str(multiplexor_index) + '.' + sig_name.upper() + '_' + str(cl) + ') << ' + str(bits_to_be_filled) + ');')
                        else:
                          print('   rValue |= (' + datatype_8 + ')(((' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ') << ' + str(bits_to_be_filled) + ');')
                      else:
                        print('   rValue |= (' + datatype_8 + ')(((' + datatype_8 + ')' + mes['Msg_name'].upper() + '.' + mes['Msg_name'].lower() + '.' + sig_name.upper() + '_' + str(cl) + ') << ' + str(bits_to_be_filled) + ');')
                    cl += 1

                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('   return rValue;')
                  print('}\n')
              else:
                if layout_row_start != layout_row_end:#if signal is in different byte position seperate function is used to get the value otherwise a macro is generated in par_h py file
                  print(datatype_8+' IlRxGet'+sig_name.upper()+'(void)')
                  print('{')
                  #print '   CAN_CCR     saveCcr;'
                  print('   '+datatype_8+'  rValue;')
                  print('    CAN_ENTER_CRITICAL_SECTION(0);')
                  rem=signal_length
                  start_bit_1=sig_start_bit//8
                  cl=0
                  while(rem>0):
                    if cl==0:
                      bits_to_be_filled = 8-start_bit_1
                      rem -= bits_to_be_filled
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                        else:
                          print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    else:
                      bits_to_be_filled=rem
                      rem -= bits_to_be_filled
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                        else:
                          print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                      else:
                        print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                    cl+=1

                  print('   CAN_EXIT_CRITICAL_SECTION(0);')
                  print('   return rValue;')
                  print('}\n')

            elif signal_length>8 and signal_length <=32:#if signal length is greater than 8 and less than 32 bytes #for 32bit controller
              start_bit=sig_start_bit #start bit of the signal
              length=signal_length #length  of the signal
              rem=length #variable used to store the remaining length to be processed
              cl=0
              path=0#used to diffrentiate whether the start bit exactly starts at begining of the byte layout
              byt = 0
              if length >8 and length<=16:# signal length between 8 to 16
                print(datatype_16 +' IlRxGet'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_16+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              elif length >16 and length <=32:# signal length between 8 to 16
                print(datatype_32+' IlRxGet'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_32+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')

              while(rem>0):#remaining length greater than zero
                if start_bit%8!=0:#if start bit is not in the begining of the byte
                  path=1
                  b1=start_bit%8
                  bit_to_be_filled=8-b1 #indicates the no of bits of signal that can be allocated in this byte layout

                  rem-=bit_to_be_filled
                  start_bit=start_bit+bit_to_be_filled#incrementing the start bit by adding the bits that has been already allocated in the current byte layout
                  a='1'*bit_to_be_filled #used for conversion to hex
                  if length <= 16:
                    if mes['Multiplex'] == 'YES':
                      if signals['Mul_order'] != 'root':
                        print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    else:    
                      print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                        
                  elif length >16 and length <= 32:
                    if mes['Multiplex'] == 'YES':
                      if signals['Mul_order'] != 'root':
                        print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    else:
                      print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                      
                      
                  cl+=1
                else:#if the start bit is in the start position of the byte layout
                  if path != 0:#if the original start bit of the signal is not in the byte layout starting
                    if rem >=8:#remaining length greater than 8.
                      rem=rem-8
                      if length <= 16:#if signal length is less than equql to 16
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                        else:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                      elif length>16 and length <= 32:#if signal length is greater than 16 and is less than equql to 32
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                        else:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                      else:#if signal length is greater than 32 
                        pass
                      bit_to_be_filled+=8
                    elif rem>0 and rem<8:#if remainder is less than 8 bit
                      a='1'*rem
                      if length <= 16:#if signal length is less than equql to 16
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                        else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                      elif length >16 and length<=32 :#if signal length is greater than 16 and is less than equql to 32
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                        else:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                      else:#if signal length is greater than 32 
                        pass    
                      rem=0
                    start_bit+=8
                    cl+=1
                  else:#if the original start bit of the signal is in the byte layout starting
                    if rem>=8:#remainder length greater than 8
                      if cl == 0:
                        if length <=16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+');')
                            else:
                              print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                          else:
                            print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                            
                        elif length <=32:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+');')
                            else:
                              print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                          else:
                            print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                            
                      else:
                        byt+=8
                        if length <=16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                            else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                            
                            
                        elif length >16 and length <=32:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                            else:
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                        #print 'byte'+str(cl)+'data'+'>>8'
                      rem-=8
                    else:#remainder length less than 8
                      byt+=8
                      a='1'*rem
                      if length <= 16:
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                        else:
                          print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                          
                      elif length <=32 and length >16:
                        if mes['Multiplex'] == 'YES':
                          if signals['Mul_order'] != 'root':
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                        else:
                          print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                          
                      #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                      rem-=rem
                    cl+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('   return rValue;')
              print('}\n')
            elif signal_length <=64 and signal_length >32 :
              co = 0
              print('void IlRxGet'+sig_name.upper()+'('+datatype_8+' * pData)\n{\n')
              #print '   CAN_CCR     saveCcr;'
              print('    CAN_ENTER_CRITICAL_SECTION(0);')
              while (co < signal_length//8):
                if mes['Multiplex'] == 'YES':
                  if signals['Mul_order'] != 'root':
                    print('    pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(co)+';')
                  else:
                    print('    pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co)+';')
                else:
                  print('    pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co)+';')
                  
                co+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')
          
          elif signals['Order'] == 'Motorola':
            if sig_start_bit== 7 and sig_start_bit ==1 :
              start_bit=sig_start_bit
            else:
              start_bit = (sig_start_bit-7) + 8*((signal_length//8)-1)
                     
            if signal_length <=64 and signal_length >32 :
              co = 0
              print('void IlRxGet'+sig_name.upper()+'('+datatype_8+' * pData)\n{\n')
              #print '   CAN_CCR     saveCcr;'
              print('    CAN_ENTER_CRITICAL_SECTION(0);')
              while (co < signal_length//8):
                if mes['Multiplex'] == 'YES':
                  if signals['Mul_order'] != 'root':
                    print('   pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_byte'+str(co)+';')
                  else:
                    print('   pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_byte'+str(co)+';')
                else:
                  print('   pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_byte'+str(co)+';')
                  
                co+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('}\n')
              
            elif signal_length>8 and signal_length <=32:
              rem = signal_length
              length = signal_length
              if signal_length<=16:
                print(datatype_16 +' IlRxGet'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_16+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              elif signal_length>16 and signal_length<=32:
                print(datatype_32+' IlRxGet'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_32+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
              path = 0
              cl = 0
              byt = 0
              while(rem>0):
                  if start_bit%8!=0:
                    path=1
                    b1=start_bit%8
                    bit_to_be_filled=8-b1

                    rem-=bit_to_be_filled
                    start_bit=start_bit+bit_to_be_filled
                    a='1'*bit_to_be_filled
                    if length <= 16:
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                        else:
                          print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                        
                    elif length >16 and length <= 32:
                      if mes['Multiplex'] == 'YES':
                        if signals['Mul_order'] != 'root':
                          print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                        else:
                          print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')                        
                        
                    cl+=1
                  else:
                    if path != 0:
                      if rem >=8:
                        rem=rem-8
                        if length <= 16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                            else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          
                        elif length>16 and length <= 32:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                            else:
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                          
                        bit_to_be_filled+=8
                      elif rem>0 and rem<8:
                        a='1'*rem
                        if length <= 16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                            else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')                            
                        elif length >16 and length<=32 :
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                            else:
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                          else:
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');')
                            
                        rem=0
                      start_bit+=8
                      cl+=1
                    else:
                      if rem>=8:
                        if cl == 0:
                          if length <=16:
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+');')
                              else:
                                print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                            else:
                              print('   rValue = ('+datatype_16+')(('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                          elif length <=32:
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+');')
                              else:
                                print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                            else:
                              print('   rValue = ('+datatype_32+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+');')
                        else:
                          byt+=8
                          if length <=16:
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                              else:
                                print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                            else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          elif length >16 and length <=32:
                            if mes['Multiplex'] == 'YES':
                              if signals['Mul_order'] != 'root':
                                print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                              else:
                                print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                            else:
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');')
                          #print 'byte'+str(cl)+'data'+'>>8'
                        rem-=8
                      else:
                        byt+=8
                        a='1'*rem
                        if length <= 16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                            else:
                              print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                          else:
                            print('   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                        elif length <=32 and length >16:
                          if mes['Multiplex'] == 'YES':
                            if signals['Mul_order'] != 'root':
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');')
                            else:
                              print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                          else:  
                            print('   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << '+str(byt)+');')
                        #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                        rem-=rem
                      cl+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('   return rValue;')
              print('}\n')
                
            elif signal_length<=8:
              if layout_row_start != layout_row_end:
                layout_row_start = start_bit//8
                layout_row_end = sig_start_bit//8
                print(datatype_8+' IlRxGet'+sig_name.upper()+'(void)')
                print('{')
                #print '   CAN_CCR     saveCcr;'
                print('   '+datatype_8+'  rValue;')
                print('    CAN_ENTER_CRITICAL_SECTION(0);')
                    
                rem=signal_length
                start_bit_1=start_bit//8
                cl=0
                while(rem>0):
                  if cl==0:
                    bits_to_be_filled = 8-start_bit_1
                    rem -= bits_to_be_filled
                    if mes['Multiplex'] == 'YES':
                      if signals['Mul_order'] != 'root':
                        print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+';')
                      else:
                        print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                    else:
                      print('   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';')
                  else:
                    bits_to_be_filled=rem
                    rem -= bits_to_be_filled
                    if mes['Multiplex'] == 'YES':
                      if signals['Mul_order'] != 'root':
                        print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                      else:
                        print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                    else:
                      print('   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');')
                  cl+=1

                print('   CAN_EXIT_CRITICAL_SECTION(0);')
                print('   return rValue;')
                print('}\n')

              
def message_precopy():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()

  il_msg_rx=[]
  nm_msg_rx=[]
  diag_msg_rx=[]
    
       
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
  
  print('''/* ====================================================================================
   Interaction Layer Receive Message Precopy Functions
   ==================================================================================*/
''')

  for mes in il_sorted_mes_rx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      sig_list =[]
      if mes['Multiplex'] == 'YES':
        mul_msg=dbc.get_multiplex(mes['id'])
        multiplexor_id=mul_msg['Multiplexor']
      for signal in mes['Sig_List']:
          mes['Sig_List'][signal]['Sig_name']=signal
          sig_list.append(mes['Sig_List'][signal])
         
      sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
      a=[]
      unused_length=0
      start_bit=0

      ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
      intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
      moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
      #logic for implementing the layout with signal and unused bit

      print('void '+mes['Msg_name']+'_PreCopy (void)')
      print('{')
      print('   if (0 == (il_status & ('+datatype_8+') IL_STATUS_SUSPEND))')
      print('   {')
      if sorted_bit:
        for signals in sorted_bit:
          if mes['Multiplex'] == 'YES':
            multiplexor_index=0
            for sig_list in mul_msg['Multiplex_group']:
              if signals['Sig_name'] in sig_list:
                multiplexor_index=mul_msg['Multiplex_group'].index(sig_list)
          precopy = []
          signal_occur=0
          sig_start_bit = int(signals['Endbit'])
          layout_row_start=int(signals['Endbit'])//8
          layout_col_start=int(signals['Endbit'])%8
          signal_length=int(signals['Len'])
          sig_name = signals['Sig_name']
          end_bit=int(signals['Endbit'])+signal_length-1
          layout_row_end = end_bit//8

          byte_no=0
          byte_no_1=(signal_length//8)-1 if signal_length%8 == 0 else signal_length//8

    
          if signals['Order'] == 'Intel':  
    
            if signal_length<=8:

              if layout_row_start != layout_row_end:
                rem=signal_length
                start_bit_1=sig_start_bit//8
                cl=0
                while(rem>0):
                  if cl==0:
                    bits_to_be_filled = 8-start_bit_1
                    rem -= bits_to_be_filled
                    #print '   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  else:
                    bits_to_be_filled=rem
                    rem -= bits_to_be_filled
                    #print '   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  cl+=1
              else:
                precopy.append(sig_name.upper())


            elif signal_length>8 and signal_length <=32:
              start_bit=sig_start_bit
              length=signal_length
              rem=length
              cl=0
              path=0
              byt = 0
              if length >8 and length<=16:
                pass
              elif length >16 and length <=32:
                pass
                
              while(rem>0):
                if start_bit%8!=0:
                  path=1
                  b1=start_bit%8
                  bit_to_be_filled=8-b1

                  rem-=bit_to_be_filled
                  start_bit=start_bit+bit_to_be_filled
                  a='1'*bit_to_be_filled
                  if length <= 16:
                    #print '   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  elif length >16 and length <= 32:
                    #print '   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  cl+=1
                else:
                  if path != 0:
                    if rem >=8:
                      rem=rem-8
                      if length <= 16:
                        #print '   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');'
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      elif length>16 and length <= 32:
                        print('   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');')
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      bit_to_be_filled+=8
                    elif rem>0 and rem<8:
                      a='1'*rem
                      if length <= 16:
                        #print '   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');'
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      elif length >16 and length<=32 :
                        #print '   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');'
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      rem=0
                    start_bit+=8
                    cl+=1
                  else:
                    if rem>=8:
                      if cl == 0:
                        if length <=16:
                          #print '   rValue = ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        elif length <=32:
                          #print '   rValue = ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                      else:
                        byt+=8
                        if length <=16:
                          #print '   rValue |= ('+datatype_16+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        elif length >16 and length <=32:
                          #print '   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        #print 'byte'+str(cl)+'data'+'>>8'
                      rem-=8
                    else:
                      a='1'*rem
                      if length <= 16:
                        #print '   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');'
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      elif length <=32 and length >16:
                        #print '   rValue |= ('+datatype_32+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');'
                        precopy.append(sig_name.upper()+'_'+str(cl))
                      #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                      rem-=rem
                    cl+=1
              
              
            elif signal_length <=64 and signal_length >32 :
              co = 0
              
              while (co < signal_length//8):
                #print '    pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(co)+';'
                precopy.append(sig_name.upper()+'_'+str(co))
                co+=1
            
            temp_str= '     if('
            temp_count = 0
            for sig_buf in precopy:
              if mes['Multiplex'] == 'YES':
                if signals['Mul_order'] != 'root':
                  temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_buf+')'
                else:
                  temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+sig_buf+')'
              else:
                temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+sig_buf+')'
              if temp_count >= (len(precopy)-1):
                temp_str+=')\n'
              else:
                temp_str+=' || \n       '
              temp_count+=1
            temp_str+='     {\n'
            temp_str+='         ILSet_'+sig_name.upper()+'_DataChanged();\n'
            temp_str+='     }\n'
              
            print(temp_str)
            
          elif signals['Order'] == 'Motorola':
            if sig_start_bit== 7 and sig_start_bit ==1 :
              start_bit=sig_start_bit
            else:
              start_bit = (sig_start_bit-7) + 8*((signal_length//8)-1)
            no_print = 1        
            if signal_length <=64 and signal_length >32 :
              co = 0
              
              while (co < signal_length//8):
                #print '   pData['+str(co)+'] = '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_byte'+str(co)+';'
                precopy.append(sig_name.upper()+'_'+str(co))
                co+=1
              
              
            elif signal_length>8 and signal_length <=32:
              rem = signal_length
              length = signal_length
              if signal_length<=16:
                pass
              elif signal_length>16 and signal_length<=32:
                pass
              path = 0
              cl = 0
              byt = 0
              while(rem>0):
                  if start_bit%8!=0:
                    path=1
                    b1=start_bit%8
                    bit_to_be_filled=8-b1

                    rem-=bit_to_be_filled
                    start_bit=start_bit+bit_to_be_filled
                    a='1'*bit_to_be_filled
                    if length <= 16:
                      #print '   rValue = ('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                      precopy.append(sig_name.upper()+'_'+str(cl))
                    elif length >16 and length <= 32:
                      #print '   rValue = ('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                      precopy.append(sig_name.upper()+'_'+str(cl))
                    cl+=1
                  else:
                    if path != 0:
                      if rem >=8:
                        rem=rem-8
                        if length <= 16:
                          #print '   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        elif length>16 and length <= 32:
                          #print '   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bit_to_be_filled)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        bit_to_be_filled+=8
                      elif rem>0 and rem<8:
                        a='1'*rem
                        if length <= 16:
                          #print '   rValue |= ('+datatype_16+')((('+datatype_16+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        elif length >16 and length<=32 :
                          #print '   rValue |= ('+datatype_32+')((('+datatype_32+') '+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') <<'+str(bit_to_be_filled)+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        rem=0
                      start_bit+=8
                      cl+=1
                    else:
                      if rem>=8:
                        if cl == 0:
                          if length <=16:
                            #print '   rValue = ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                            precopy.append(sig_name.upper()+'_'+str(cl))
                          elif length <=32:
                            #print '   rValue = ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                            precopy.append(sig_name.upper()+'_'+str(cl))
                        else:
                          byt+=8
                          if length <=16:
                            #print '   rValue |= ('+datatype_16+')(('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');'
                            precopy.append(sig_name.upper()+'_'+str(cl))
                          elif length >16 and length <=32:
                            #print '   rValue |= ('+datatype_32+')((('+datatype_32+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << ' +str(byt)+');'
                            precopy.append(sig_name.upper()+'_'+str(cl))
                          #print 'byte'+str(cl)+'data'+'>>8'
                        rem-=8
                      else:
                        a='1'*rem
                        if length <= 16:
                          #print '   rValue |= ('+datatype_16+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        elif length <=32 and length >16:
                          #print '   rValue |= ('+datatype_32+')((('+datatype_16+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl) +') << 8'+');'
                          precopy.append(sig_name.upper()+'_'+str(cl))
                        #print 'byte'+str(cl)+'data'+'>>8'+"0x%02x"%int(a,2)
                        rem-=rem
                      cl+=1
              print('   CAN_EXIT_CRITICAL_SECTION(0);')
              print('   return rValue;')
              print('}\n')
                
            elif signal_length<=8:
              layout_row_start = start_bit//8
              layout_row_end = sig_start_bit//8
              if layout_row_start != layout_row_end:
                                  
                rem=signal_length
                start_bit_1=start_bit//8
                cl=0
                while(rem>0):
                  if cl==0:
                    bits_to_be_filled = 8-start_bit_1
                    rem -= bits_to_be_filled
                    #print '   rValue = ('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+';'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  else:
                    bits_to_be_filled=rem
                    rem -= bits_to_be_filled
                    #print '   rValue |= ('+datatype_8+')((('+datatype_8+')'+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_name.upper()+'_'+str(cl)+') << '+str(bits_to_be_filled)+');'
                    precopy.append(sig_name.upper()+'_'+str(cl))
                  cl+=1
              else:
                precopy.append(sig_name.upper())
            else:
              no_print = 0
            
            if no_print == 1:
              temp_str= '     if('
              temp_count = 0
              for sig_buf in precopy:
                if mes['Multiplex'] == 'YES':
                  if signals['Mul_order'] != 'root':
                    temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+multiplexor_id.lower()+'_data'+'.'+multiplexor_id.lower()+'_'+str(multiplexor_index)+'.'+sig_buf+')'
                  else:
                    temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+sig_buf+')'
                else:
                  temp_str+='('+mes['Msg_name'].upper()+'.'+mes['Msg_name'].lower()+'.'+sig_buf+' != Rx_buffer.'+mes['Msg_name'].lower()+'.'+sig_buf+')'
                if temp_count >= (len(precopy)-1):
                  temp_str+=')\n'
                else:
                  temp_str+=' || \n       '
                temp_count+=1
              temp_str+='     {\n'
              temp_str+='         ILSet_'+sig_name.upper()+'_DataChanged();\n'
              temp_str+='     }\n'
                
              print(temp_str)
          
          
    print('   }')
    print('}\n')
    
def buffer_obj():
  global dbc,datatype_16,datatype_8,datatype_32,il_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(il_data_dir+"CanDbcMsgConfiguration.data",'r',encoding='utf-8')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
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
//  M E M O R Y   A L L O C A T I O N
// =========================================================================*/
CAN_UINT8 il_Rx_DataChanged_Flag[ IL_NUM_OF_RX_DATA_CHANGED_FLAG ];

/* ==========================================================================
// Tx and Rx buffer                                
/  ========================================================================*/
/*Tx_Msg_buf             Tx_buffer;*/
Rx_Msg_buf  Rx_buffer;
''')

  print("/* Tx buffer objects */\n")
  for mes in il_sorted_mes_tx:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_tx_enable'] in ['on','On',1,'1','ON']:
      print(mes['Msg_name'].upper()+'_buf '+mes['Msg_name'].upper()+';')
  print("/* Rx buffer objects */\n")
  
  for mes in il_sorted_mes_rx_ordered:
    if vnim_msg_cfg_data[mes['Msg_name'].upper()+'_rx_enable'] in ['on','On',1,'1','ON']:
      print(mes['Msg_name'].upper()+'_buf '+mes['Msg_name'].upper()+';')  


#f=open('nm_il_msg.h','w')
def il_par_c_gen_function():

  global il_code_gen_dir,footer,tp_generic_config,nm_generic_config,il_generic_config

  if not os.path.exists(il_code_gen_dir):
      os.mkdir(il_code_gen_dir)
  f=open_output("nw_il_par.c")



  print('''/* ===========================================================================

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
  /* ===========================================================================

    Name:           nw_il_par.c

    Description:    Interaction Layer Tx and Rx Parameters

                    Application Specific Tx and Rx Message and Signal
                    Data Structure Definitions

    Organization:   Network Subsystem.

   =========================================================================*/

  /* ===========================================================================
    P U B L I C   T Y P E   D E F I N I T I O N S
   ========================================================================*/\n\n''')

  print('#include "can_type.h"')
  print('#include "can_defs.h"')
  print('#include "can_csec.h"')
  print('#include "nw_il.h"')
  print('#include "nw_il_par.h"')

  

  
  buffer_obj()
  
  message_Put_tx()
  message_Get_tx()
  message_Put_rx()
  message_Get_rx()
  message_precopy()
  
  print(footer)
  close_output(f)


if __name__ == '__main__':
  pass
  
  import datetime
  time_print = datetime.datetime.now()
  set_file_node_il('U321_IVN_Communication_Matrix_Base_12216_IS.dbc','IS')
  set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
  il_par_c_gen_function()
  
