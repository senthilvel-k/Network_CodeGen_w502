import sys,json
import os
dbc=None

msg_code_gen_dir = './CODE_GEN'
msg_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgILSupport'
all_parser = 'ALL'
time_str=''
footer=''

dlc_disable = 0 # variable used for structure optimization
union_list=[]
datatype_16 = 'CAN_UINT8'
datatype_8 = 'CAN_UINT8'

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
def message_structure_generation(Dbc_Msg):
  global msg_data_dir,datatype_16,datatype_8,msg_data_dir,tp_generic_config,nm_generic_config,il_generic_config
  message={}
  message_list=[]
  message_enable_dictionary = {}
  vnim_msg_cfg_data={}
  vnim_cfg_file = open(msg_data_dir+"CanDbcMsgConfiguration.data",'r')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  
  # function used to create a layout for each messages 
  structt=[]
  for mes in Dbc_Msg:
    temp_str_chk = 'A5'
    if mes['Msg_name'].upper()+'_tx_enable' in vnim_msg_cfg_data:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        temp_str_chk = mes['Msg_name'].upper()+'_tx_enable'
    elif mes['Msg_name'].upper()+'_rx_enable' in vnim_msg_cfg_data:
      if vnim_msg_cfg_data[mes['Msg_name']+'_msg_type_no_of_events'] == 'Appl':
        temp_str_chk = mes['Msg_name'].upper()+'_rx_enable'
    else:
      temp_str_chk = 'A5'
    if temp_str_chk != 'A5':
      if vnim_msg_cfg_data[temp_str_chk] in ['on','On',1,'1','ON']:
        if mes["Multiplex"] == "NO":
          message_list.append(mes['Msg_name'])
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
          
          for signals in sorted_bit:
            
            signal_occur=0
            layout_row=int(signals['Endbit'])/8
            layout_col=int(signals['Endbit'])%8
            signal_length=int(signals['Len'])
            endbit=int(signals['Endbit'])
            sig_start_bit = int(signals['Endbit'])
            byte_no=0
            
            if signal_length%8 == 0:
              byte_no_1=(signal_length/8)-1
            else:
              byte_no_1=signal_length/8
            #print signals['Order']
            if signals['Order'] == 'Intel':
              for sig_len in range(int(signals['Len'])):
                  if signal_length<=8:
                    bits_left=8-(sig_start_bit%8)
                    if (bits_left<signal_length):
                     ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no)
                    else:
                     ms[layout_row][layout_col] = signals['Sig_name']
                    if layout_col <7:
                      layout_col=layout_col+1
                    elif layout_col >=7 and layout_row<7:
                      byte_no+=1
                      layout_col=0
                      layout_row=layout_row+1
                  elif signal_length>8 :
                    ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no)
                    if layout_col <7:
                      layout_col=layout_col+1
                    elif layout_col >=7 and layout_row<7:
                      byte_no+=1
                      layout_col=0
                      layout_row=layout_row+1
              signal_occur+=endbit+signal_length
              if signal_occur%8 !=0:
                signal_occur=(signal_occur/8)
              else:
                signal_occur=(signal_occur/8)-1
              intel_max.append(signal_occur)
              
            elif signals['Order'] == 'Motorola':
              for sig_len in range(signal_length,0,-1):
                if signal_length<=8:
                  ms[layout_row][layout_col] = signals['Sig_name']
                  if sig_len == 1:
                    start_bit_1=(8*layout_row)+layout_col
                  if layout_col >0 and layout_col<=7:
                    layout_col=layout_col-1
                  elif layout_col ==0 and layout_row<7 :
                    layout_col=7
                    layout_row=layout_row+1
                elif signal_length>8:
                  ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no_1)
                  if sig_len == 1:
                    start_bit_1=(8*layout_row)+layout_col
                  if layout_col >0 and layout_col<=7:
                    layout_col=layout_col-1
                  elif layout_col ==0 and layout_row<7 :
                    layout_col=7
                    layout_row=layout_row+1
                    byte_no_1-=1
              if start_bit_1%8 != 0:
                start_bit_1=(start_bit_1/8)+1
              else:
                start_bit_1=start_bit_1/8
              moto_max.append(start_bit_1)

                
          merged_list=intel_max+moto_max
          
          max_col=max(merged_list)
          #logic for deleting the rows in layout to create structure with the number of signals only , not with dlc
          if dlc_disable == 1:
            length = 7
            if max_col<=7:
              while length>max_col:
                del ms[length]
                length-=1
          
          col=0
          zero_occur=0
          zero=-1
          #logic for creating unused in message layout with byte ordering
          for row in ms:
            zero_occur=0
            for col in range(len(row)):
              serach_element=row[col]
              if row[col]==0:
                if zero_occur== 0:
                  zero+=1
                row[col]='unused'+str(zero)
                zero_occur=1
              else:
                if zero_occur==1:
                  zero_occur=0

          structt.append(ms)    #structt is list contains the signal layout 
        else:
          msg_struct_gen_multiplex(mes)
        
      
  cl=0
  struct_intel=[]
  l=[]
  #logic for signal byte ordering
  for i in structt:
    l=[]
    for mes_temp in i:
      k=[]
      for z in range(len(mes_temp)):
        sig = mes_temp[z]
        count = mes_temp.count(sig)
        if sig+':'+str(count) not in k:
          k.append(sig+':'+str(count))
      l.append(k)
    struct_intel.append(l)
      

  cl=-1
  #for printing the structure in the file 
  for s in struct_intel:
    cl=cl+1
    print '\n/* '+message_list[cl]+' */'
    print 'typedef struct {'
    for i in s:
      for j in i:
        #pass
        print '  '+datatype_8+' '+ j +';'
    print '}'+message_list[cl]+'_msgType;\n'
  
  
  
   
def msg_struct_gen_multiplex(mes):
  global dbc,msg_data_dir,datatype_16,datatype_8,tp_generic_config,nm_generic_config,il_generic_config
  
  vnim_cfg_file = open(msg_data_dir+"CanDbcMsgConfiguration.data",'r')
  vnim_msg_cfg_data = json.loads(vnim_cfg_file.read())
  vnim_cfg_file.close()
  #print mes
  structt=[]
  #message_list_=[]
  #message_list.append(mes['Msg_name'])
  sig_list =[]
  
  #get multiplex msg details
  #{'Multiplexor': 'VIN_INDEX', 'Multiplex_group': {'Group_list': ['VIN_DATA_1', 'VIN_DATA_0', 'VIN_DATA_2'], 'Group_Name': 'VIN_DATA'}}
  '''{'Multiplexor': 'VIN_INDEX',
     'Multiplex_maxval': 2, 
     'Multiplex_group_Name': 'VIN_INDEX_GROUP',
     'Multiplex_group': 
            [
             ['VIN_DATA_0'],
             ['VIN_DATA_1'],
             ['VIN_DATA_2']
            ] 
    }
  '''
  mul_msg=dbc.get_multiplex(mes['id'])
  #print mul_msg
  for signal in mes['Sig_List']:
    mes['Sig_List'][signal]['Sig_name']=signal
    sig_list.append(mes['Sig_List'][signal])
  #print sig_list[0]  
  sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
  a=[]
  unused_length=0
  start_bit=0
  intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
  moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
  #logic for implementing the layout with signal and unused bit
  multiplex_sig_lst=[]
  multiplex_max_len=[]
  
  if mul_msg['Multiplex_maxval'] !=0:
    for multilexor_index in range(mul_msg['Multiplex_maxval']+1):
      #sort signal list 
      for mul_sig in mul_msg['Multiplex_group'][multilexor_index]:
    
        signals = mes['Sig_List'][mul_sig]
        #for signals in sorted_bit:

        multiplex_sig_lst.append(signals['Sig_name'])
        signal_occur=0
        layout_row=int(signals['Endbit'])/8
        layout_col=int(signals['Endbit'])%8
        signal_length=int(signals['Len'])
        endbit=int(signals['Endbit'])
        byte_no=0
        
        if signal_length%8 == 0:
          byte_no_1=(signal_length/8)-1
        else:
          byte_no_1=signal_length/8
          
        if int(signals['Len'])%8 == 0:
          temp_len=(int(signals['Len'])/8)
        else:
          temp_len =(int(signals['Len'])/8)+1
        multiplex_max_len.append(temp_len)
        ms=[[0 for i in range(8)] for i in range(temp_len)] # two dimensional list for creating the layout for each signal
        #print signals['Order']
        if signals['Order'] == 'Intel':
          for sig_len in range(int(signals['Len'])):
              if signal_length<=8:
                ms[layout_row][layout_col] = signals['Sig_name']
                if layout_col <7:
                  layout_col=layout_col+1
                elif layout_col >=7 and layout_row<7:
                  layout_col=0
                  layout_row=layout_row+1
              elif signal_length>8 :
                ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no)
                if layout_col <7:
                  layout_col=layout_col+1
                elif layout_col >=7 and layout_row<7:
                  byte_no+=1
                  layout_col=0
                  layout_row=layout_row+1
          signal_occur+=endbit+signal_length
          if signal_occur%8 !=0:
            signal_occur=(signal_occur/8)
          else:
            signal_occur=(signal_occur/8)-1
          intel_max.append(signal_occur)
          
        elif signals['Order'] == 'Motorola':
          for sig_len in range(signal_length,0,-1):
            if signal_length<=8:
              ms[layout_row][layout_col] = signals['Sig_name']
              if sig_len == 1:
                start_bit_1=(8*layout_row)+layout_col
              if layout_col >0 and layout_col<=7:
                layout_col=layout_col-1
              elif layout_col ==0 and layout_row<7 :
                layout_col=7
                layout_row=layout_row+1
            elif signal_length>8:
              ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no_1)
              if sig_len == 1:
                start_bit_1=(8*layout_row)+layout_col
              if layout_col >0 and layout_col<=7:
                layout_col=layout_col-1
              elif layout_col ==0 and layout_row<7 :
                layout_col=7
                layout_row=layout_row+1
                byte_no_1-=1
          if start_bit_1%8 != 0:
            start_bit_1=(start_bit_1/8)+1
          else:
            start_bit_1=start_bit_1/8
          moto_max.append(start_bit_1)
        
      merged_list=intel_max+moto_max
      max_col=max(merged_list)
      #logic for deleting the rows in layout to create structure with the number of signals only , not with dlc
      
      dlc_disable = 1
      #print temp_len,max_col
      #print len(ms)
      if dlc_disable == 1:
        le=len(ms)-1
        if max_col<=le:
          while le>max_col:
            del ms[le]
            le-=1
    
      col=0
      zero_occur=0
      zero=-1
      #logic for creating unused in message layout with byte ordering
      #print ms
      for row in ms:
        zero_occur=0
        for col in range(len(row)):
          serach_element=row[col]
          if row[col]==0:
            if zero_occur== 0:
              zero+=1
            row[col]='unused'+str(zero)
            zero_occur=1
          else:
            if zero_occur==1:
              zero_occur=0

      structt.append(ms)    #structt is list contains the signal layout 
      cl=0
      struct_intel=[]
      l=[]
      #logic for signal byte ordering
      for i in structt:
        l=[]
        for mes_temp in i:
          k=[]
          for z in range(len(mes_temp)):
            sig = mes_temp[z]
            count = mes_temp.count(sig)
            if sig+':'+str(count) not in k:
              k.append(sig+':'+str(count))
          l.append(k)
      struct_intel.append(l)
        

      cl=-1
      #for printing the structure in the file 
      for s in struct_intel:
        cl=cl+1
        print 'typedef struct {'
        for i in s:
          for j in i:
            print '  '+datatype_8+' '+ j +';'
        print '}'+mul_msg['Multiplexor']+'_'+str(multilexor_index)+'_sigType;\n'
      
  print 'typedef union '
  print '{'
  print '   '+datatype_8+'          sig_buffer['+str(max(multiplex_max_len))+'];'
  for multilexor_index in range(mul_msg['Multiplex_maxval']+1):
    #for mx_sig in mul_msg['Multiplex_group']['Group_list']:
    print '   '+mul_msg['Multiplexor']+'_'+str(multilexor_index)+'_sigType  '+mul_msg['Multiplexor'].lower()+'_'+str(multilexor_index)+';'
  print '}'+mul_msg['Multiplex_group_Name']+'_Sigbuf;'
  
  #done for single signal EMS5_500
  #{'Sig_name': 'VIN_DATA_1', 'Len': '56','Mul_order': '1', 'Endbit': '0', 'Order': 'Intel'}
  
  
  
  #muliplex message structure gen
  sig_list=[]
  sig_list.append(mes['Sig_List'][mul_msg['Multiplexor']])
  sorted_bit=sorted(sig_list,key = lambda x: int(x['Endbit'])) 
  a=[]
  unused_length=0
  start_bit=0
  intel_max=[]  #list contains the startbit of each signla in a message for intel byte order
  moto_max=[]   #list contains the startbit of each signla in a message for Motorola byte order
  #logic for implementing the layout with signal and unused bit
  multiplex_sig_lst=[]
  multiplex_max_len=[]
  ms=[[0 for i in range(8)] for i in range(8)] # two dimensional list for creating the layout for each signal
  for signals in sorted_bit:
      signal_occur=0
      layout_row=int(signals['Endbit'])/8
      layout_col=int(signals['Endbit'])%8
      signal_length=int(signals['Len'])
      endbit=int(signals['Endbit'])
      byte_no=0
      
      if signal_length%8 == 0:
        byte_no_1=(signal_length/8)-1
      else:
        byte_no_1=signal_length/8
        
      if int(signals['Len'])%8 == 0:
        temp_len=(int(signals['Len'])/8)
      else:
        temp_len =(int(signals['Len'])/8)+1
      multiplex_max_len.append(temp_len)
      #ms=[[0 for i in range(8)] for i in range(temp_len)] # two dimensional list for creating the layout for each signal
      #print signals['Order']
      if signals['Order'] == 'Intel':
        for sig_len in range(int(signals['Len'])):
            if signal_length<=8:
              ms[layout_row][layout_col] = signals['Sig_name']
              if layout_col <7:
                layout_col=layout_col+1
              elif layout_col >=7 and layout_row<7:
                layout_col=0
                layout_row=layout_row+1
            elif signal_length>8 :
              ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no)
              if layout_col <7:
                layout_col=layout_col+1
              elif layout_col >=7 and layout_row<7:
                byte_no+=1
                layout_col=0
                layout_row=layout_row+1
        signal_occur+=endbit+signal_length
        if signal_occur%8 !=0:
          signal_occur=(signal_occur/8)
        else:
          signal_occur=(signal_occur/8)-1
        intel_max.append(signal_occur)
        
      elif signals['Order'] == 'Motorola':
        for sig_len in range(signal_length,0,-1):
          if signal_length<=8:
            ms[layout_row][layout_col] = signals['Sig_name']
            if sig_len == 1:
              start_bit_1=(8*layout_row)+layout_col
            if layout_col >0 and layout_col<=7:
              layout_col=layout_col-1
            elif layout_col ==0 and layout_row<7 :
              layout_col=7
              layout_row=layout_row+1
          elif signal_length>8:
            ms[layout_row][layout_col] = signals['Sig_name']+'_'+str(byte_no_1)
            if sig_len == 1:
              start_bit_1=(8*layout_row)+layout_col
            if layout_col >0 and layout_col<=7:
              layout_col=layout_col-1
            elif layout_col ==0 and layout_row<7 :
              layout_col=7
              layout_row=layout_row+1
              byte_no_1-=1
        if start_bit_1%8 != 0:
          start_bit_1=(start_bit_1/8)+1
        else:
          start_bit_1=start_bit_1/8
        moto_max.append(start_bit_1)
      
      merged_list=intel_max+moto_max
      max_col=max(merged_list)
      #logic for deleting the rows in layout to create structure with the number of signals only , not with dlc
      
      dlc_disable = 1
      #print temp_len,max_col
      #print len(ms)
      if dlc_disable == 1:
        le=len(ms)-1
        if max_col<=le:
          while le>max_col:
            del ms[le]
            le-=1
    
      col=0
      zero_occur=0
      zero=-1
      #logic for creating unused in message layout with byte ordering
      #print ms
      for row in ms:
        zero_occur=0
        for col in range(len(row)):
          serach_element=row[col]
          if row[col]==0:
            if zero_occur== 0:
              zero+=1
            row[col]='unused'+str(zero)
            zero_occur=1
          else:
            if zero_occur==1:
              zero_occur=0

      structt.append(ms)    #structt is list contains the signal layout 
      cl=0
      struct_intel=[]
      l=[]
      #logic for signal byte ordering
      for i in structt:
        l=[]
        for mes_temp in i:
          k=[]
          for z in range(len(mes_temp)):
            sig = mes_temp[z]
            count = mes_temp.count(sig)
            if sig+':'+str(count) not in k:
              k.append(sig+':'+str(count))
          l.append(k)
      struct_intel.append(l)
        

      cl=-1
      #for printing the structure in the file 
      #index_start =
      #index_stop =
      mul_sig_index = 6
      print '\n/* '+mes['Msg_name']+' */'
      print 'typedef struct {'
      print '  '+mul_msg['Multiplex_group_Name']+'_Sigbuf  '+mul_msg['Multiplex_group_Name'].lower()+';'
      for s in struct_intel:
        cl=cl+1
        for i in s:
          if s.index(i) > mul_sig_index:
            for j in i:
              print '  '+datatype_8+' '+ j +';'
        print '}'+mes['Msg_name']+'_msgType;\n'
  
  
def msg_struct_generation(): 
  global dbc,footer,msg_code_gen_dir,tp_generic_config,nm_generic_config,il_generic_config
  #dir = './CODE_GEN'
  if not os.path.exists(msg_code_gen_dir):
      os.mkdir(msg_code_gen_dir)
  f=open('./CODE_GEN/nw_il_msg.h','w')

  
  sys.stdout = f
  
  header = '''#if !defined(NW_IL_MSG_H)
#define NW_IL_MSG_H
/* ===========================================================================
//
//                     CONFIDENTIAL VISTEON CORPORATION
//
//  This is an unpublished work of authorship, which contains trade secrets,
//  created in 2009.  Visteon Corporation owns all rights to this work and
//  intends to maintain it in confidence to preserve its trade secret status.
//  Visteon Corporation reserves the right, under the copyright laws of the
//  United States or those of any other country that may have jurisdiction, to
//  protect this work as an unpublished work, in the event of an inadvertent
//  or deliberate unauthorized publication.  Visteon Corporation also reserves
//  its rights under all copyright laws to protect this work as a published
//  work, when appropriate.  Those having access to this work may not copy it,
//  use it, modify it or disclose the information contained in it without the
//  written authorization of Visteon Corporation.
//
// =========================================================================*/
/* ===========================================================================
//
//  Name:           nw_il_msg.h
//
//  Description:    Interaction Layer Message structure definition file.
//
//  Organization:   Network Subsystem.
//
// =========================================================================*/

/* ===========================================================================
//  P U B L I C   T Y P E   D E F I N I T I O N S
// =========================================================================*/
'''
  print header,'\n'

  print '''/*===========================================================================
    Interaction Layer Transmit Message Structure
   =========================================================================*/\n\n'''
  il_msg_tx=dbc.get_msg_type(all_parser,'tx')
  il_sorted_mes_tx = sorted(il_msg_tx,key = lambda x: x['Msg_name'])
  message_structure_generation(il_sorted_mes_tx)
  print '''\n\n/*===========================================================================
    Interaction Layer Receive Message structure
   =========================================================================*/\n'''

  il_msg_rx=dbc.get_msg_type(all_parser,'rx')
  #print il_msg_rx
  il_sorted_mes_rx = sorted(il_msg_rx,key = lambda x: x['Msg_name'])
  message_structure_generation(il_sorted_mes_rx)

  print'''#endif'''
  print footer

  print '''/* End of file ============================================================ */'''

  f.close()

if __name__ == '__main__':
    pass
    '''import datetime
    time_print = datetime.datetime.now()
    set_file_node_il('U321.dbc','IS')
    set_init_global(time_print.strftime("%Y-%m-%d %H:%M"))
    msg_struct_generation()'''
    