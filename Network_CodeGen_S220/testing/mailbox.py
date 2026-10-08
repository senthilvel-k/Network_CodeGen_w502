import json
def CanMailbox_Cfg():
    from Dbc_Parser import dbc_parser
    code_gen_di='./'
    data_dir='./'
    dbc=dbc_parser("BAIC_C40D_ICAN_ICM_CAN_0.5.dbc","ICM")
    drv_file = open(data_dir+"CanDRVConfiguration.data",'r')
    filter_file = open(data_dir+"CanFilterConfiguration.data",'r')

    cfg_data = json.loads(drv_file.read())
    filter_data=json.loads(filter_file.read())
    drv_file.close()
    filter_file.close()

    cfg_data["CAN0_MIN_NUMBER_OF_BASIC_BUFFERS_RX"]=1
    tp_generic_config='TpMessage'
    nm_generic_config='NmMessage'
    il_generic_config='GenMsgIlSupport'
    
    
    '''if not os.path.exists(code_gen_dir):
      os.mkdir(code_gen_dir)
    #f=open(code_gen_dir+'/CanMailbox_Cfg.h','w')
    
    #sys.stdout = f'''
    
 
    no_of_buffers=32
    
    gptx_range=[]
    disp_tx=[]
    disp_mailbox=[]
    hrh=[]
    hth=[]
    
    tx_start = no_of_buffers-1
    rx_start = 0
    #f=open('CanMailbox_Cfg.h','w')
    #sys.stdout = f
    
    #filter config parameters
    buf_arr=['CAN_FULLCAN_RX_MB']*no_of_buffers;
    filter_id = [0]*no_of_buffers
    mask_value = ['0xFFFFFFFF']*no_of_buffers
    
    gptx=int(cfg_data["CAN0_MIN_NUMBER_OF_BASIC_BUFFERS_TX"])
    #print gptx
     
    
    
    #tp tx message
    diag=dbc.get_msg_type(tp_generic_config,'tx')
    
    len_temp=0
    
    if (len(diag) != 0):
        #print tx_start-len(diag),tx_start
        for i in range(tx_start,tx_start-len(diag),-1):
            
            buf_arr[i]='CAN_DEDICATED_TX_MB'
            hth.append(i)
            #print diag[len_temp]['id']
            filter_id[i]= diag[len_temp]['id']
            disp_tx.append(('CAN_DEDICATED_TX_MB',diag[len_temp]['id'],'tp'))
            len_temp=len_temp+1
            
        tx_start = tx_start-len(diag)
    print 'After diag TX'
    print buf_arr

    #Nm tx message

    nm=dbc.get_msg_type(nm_generic_config,'tx')

    
    len_temp=0
    if (len(nm) != 0):
        for i in range(tx_start,tx_start-len(nm),-1):
            buf_arr[i]='CAN_DEDICATED_TX_MB'
            hth.append(i)
            filter_id[i]= nm[len_temp]['id']
            disp_tx.append(('CAN_DEDICATED_TX_MB',nm[len_temp]['id'],nm))
            len_temp=len_temp+1
        tx_start = tx_start-len(nm)
    #il tx

    print 'After NM TX'
    print buf_arr

    il_tx=dbc.get_msg_type(il_generic_config,'tx')
    il_filter_t=[]
    full_can_tx=[]
    full_can_rx=[]
    basic_can_rx=[]
    basic_can_tx=[]

    
    for i in il_tx:
        if i['Msg_name'] in filter_data:
            if filter_data[i['Msg_name']]=="on":
                full_can_tx.append(i['id'])
            elif filter_data[i['Msg_name']] == None or filter_data[i['Msg_name']] == '':
                basic_can_tx.append(i['id'])
        else:
            basic_can_tx.append(i['id'])

    #il full can messages tx
    #print len(full_can_tx)
            
    len_temp=0
    if len(full_can_tx) != 0:
        for i in range(tx_start,tx_start-len(full_can_tx),-1):
             buf_arr[i]='CAN_DEDICATED_TX_MB'
             hth.append(i)
             filter_id[i]= full_can_tx[len_temp]
             disp_tx.append(('CAN_DEDICATED_TX_MB',full_can_tx[len_temp],'il'))
             len_temp=len_temp+1
        tx_start = tx_start-len(full_can_tx)

        
    if len(basic_can_tx) != 0:
        for idx in basic_can_tx:
            disp_tx.append(('CAN_GENERALPURPOSE_TX_MB',idx,'il'))

    print 'After fuul can tx'
    print buf_arr

    print tx_start,gptx
    #gptx checking
    if gptx!= 0:
        #tx_start = (no_of_buffers-gptx)
        for i in range(tx_start,tx_start-gptx,-1):
            buf_arr[i]='CAN_GENERALPURPOSE_TX_MB'
        hth.append('CAN_GENERALPURPOSE_TX_MB')
        gptx_range=[tx_start-gptx,tx_start]
        tx_start = tx_start-gptx

    print 'After GPTX'
    print buf_arr
    
   
    #print dbc.get_msg_type(il_generic_config,'tx')[0]

    remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')
    print remaining_buf_rx
    #nm Rx
    disp_mailbox=[]
    
    il_rx=dbc.get_msg_type(il_generic_config,'rx')
    nm_rx=dbc.get_msg_type(nm_generic_config,'rx')
    diag_rx=dbc.get_msg_type(tp_generic_config,'rx')

    
    if len(nm_rx)!=0:
        remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')-(len(diag_rx)+1)
    else:
        remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')-(len(diag_rx))
    
    print remaining_buf_rx
    for i in il_rx:
        if i['Msg_name'] in filter_data:
            if filter_data[i['Msg_name']]=="on":
                full_can_rx.append(i['id'])
            elif filter_data[i['Msg_name']] == None or filter_data[i['Msg_name']] == '':
                basic_can_rx.append(i['id'])
        else:
            basic_can_rx.append(i['id'])

    full_can_rx_length=len(full_can_rx)
    remaining_buf_rx = remaining_buf_rx-full_can_rx_length
    basic_can_rx_length=len(basic_can_rx)
    print remaining_buf_rx,full_can_rx_length,basic_can_rx_length
    if (remaining_buf_rx-1)>=basic_can_rx_length:
        print remaining_buf_rx-basic_can_rx_length

    #if less number of buffers are used for full can , messages from basic can be filled in the full can.
    
    items_to_remove=[]

    if remaining_buf_rx >= basic_can_rx_length:
        copy_range=basic_can_rx_length
    else:
        copy_range=remaining_buf_rx-1
        
    for i in range(basic_can_rx_length):
        full_can_rx.append(basic_can_rx[i])
        items_to_remove.append(basic_can_rx[i])

    for rem_mes in items_to_remove:
        basic_can_rx.remove(rem_mes)

    print basic_can_rx
    
    if len(basic_can_rx)!= 0:
        buf_arr[rx_start]='CAN_BASICCAN_PATTERNFILTER_RX_MB'
        hrh.append(rx_start)
        filter_id[rx_start]= 0
        mask_value[rx_start]='0xFFFFF800'
        disp_mailbox.append(('CAN_BASICCAN_PATTERNFILTER_RX_MB',[basic_can_rx,filter_id[rx_start],mask_value[rx_start]]))
        rx_start=rx_start+1
        
    
    if (len(nm_rx) != 0):
        buf_arr[rx_start]='CAN_BASICCAN_PATTERNFILTER_RX_MB'
        hrh.append(rx_start)
        filter_id[rx_start]= 1537
        mask_value[rx_start]='0xFFFFF607'
        disp_mailbox.append(('CAN_BASICCAN_RANGEFILTER_RX_MB',[filter_id[rx_start],mask_value[rx_start][7:],nm_rx[0]['id']]))
        rx_start=rx_start+1

    #diag_rx
    
    #print len(diag_rx)
    diag_rx_id=[]
    for i in diag_rx:
        diag_rx_id.append(i['id'])

    
    if (len(diag_rx) != 0):
        for i in diag_rx:
            buf_arr[rx_start]='CAN_FULLCAN_RX_MB'
            disp_mailbox.append(('CAN_FULLCAN_RX_MB',i['id']))
            filter_id[rx_start]=i['id']
            hrh.append(rx_start)
            mask_value[rx_start]='0xFFFFFFFF'
            rx_start=rx_start+1
    #il_rx
    remaining_msg=tx_start-rx_start

    if len(full_can_rx)!= 0:
        for idx in full_can_rx:
            buf_arr[rx_start]='CAN_FULLCAN_RX_MB'
            disp_mailbox.append(('CAN_FULLCAN_RX_MB',idx))
            filter_id[rx_start]=idx
            hrh.append(rx_start)
            mask_value[rx_start]='0xFFFFFFFF'
            rx_start=rx_start+1
    
    print filter_id
    
    print '''/* ===========================================================================

 Name(s):         CANx_MBn

 Description:     Mailbox Direction, Transmit or Receive

 Templates:       #define CAN0_MB_0     CAN_FULLCAN_RX_MB
                  #define CAN0_MB_1     CAN_GENERALPURPOSE_TX_MB

 =========================================================================*/'''
    print '\n\n'
    #print #define    CAN0_MB_0    CAN_FULLCAN_RX_MB
    for i in range(len(buf_arr)):
        print '#define'+" "*4+'CAN0_MB_'+str(i)+' '*(6-len(str(i)))+buf_arr[i]

    print '\n\n'
    
    print '\n'
    
    print '/**CAN0 module Accepted Identifier configuration*/'
    print '\n'
    #define	CAN0_MSGBUF0_FID	(CAN_UINT32)0x27Dul
    for i in range(len(buf_arr)):
        print '#define'+" "*4+'CAN0_MSGBUF'+str(i)+'_MASK_VAL'+' '*(6-len(str(i)))+'(CAN_UINT32)'+mask_value[i]+'ul'
    
    print '\n\n'
    
    ##define	CAN0_MSGBUF0_MASK_VAL	(0xFFFFFFFFul)
    for i in range(len(filter_id)):
        #print filter_id[i]
        print '#define'+" "*4+'CAN0_MSGBUF'+str(i)+'_FID'+' '*(6-len(str(i)))+'('+hex(int(filter_id[i]))+'ul)'
    print '\n\n'
    
    

    print '\n'

    print '''#define CAN_CFG_HTHS \\
{\\
/* Can_TxHandleMappingType */\\
  /* The index of the controller where the HTH is allocated. */\\
  /* VAR(Can_ControllerIdType, TYPEDEF) ControllerIndex, */\\
  /* |    */\\
  /* |    The index of the buffer in scope of the controller, */\\
  /* |    where the HTH is allocated. */\\
  /* |    0..CAN_GPTX_BUFFER_SELECT is a dedicated buffer, */\\
  /* |    CAN_GPTX_BUFFER_SELECT is the FIFO. */\\
  /* |    VAR(Can_ControllerTxHandleType, TYPEDEF) TxHandle */\\
  /* |    |  */\\
  /* V    V  */\\'''
    for i in range(len(hth)):
        if hth[i] == 'CAN_GENERALPURPOSE_TX_MB':
            print '  { 0u, CAN_GPTX_BUFFER_SELECT}, /* Array index 0, TX FIFO */	/* HTH : '+str(i)+'*/\\'
        else: 
            print '  { 0u, '+str(hth[i])+'} , /* This allows mailbox '+str(hth[i])+'s of controller 0 to be used as dedicated buffer for HTH:'+str(i)+'*/\\'
    print '}'

    print '\n'
    
    print '''#define CAN_CFG_HRHS \\
{/** Array of Can_RxHandleMappingType */\\
  /* The index of the controller where the HRH is allocated. */\\
  /* VAR(Can_ControllerIdType, TYPEDEF) ControllerIndex, */\\
  /* |    */\\
  /* |    The index of the buffer in scope of the controller, */\\
  /* |    where the HRH is allocated. */\\
  /* |    0..CAN_CONTROLLER_RX_BUFFER_MAX is a dedicated buffer, */\\
  /* |    CAN_CONTROLLER_RX_FIFO_0/CAN_CONTROLLER_RX_FIFO_1 is a */\\
  /* |    respective FIFO. */\\
  /* |    VAR(Can_ControllerRxHandleType, TYPEDEF) RxHandle */\\
  /* |    |  */\\
  /* V    V  */\\'''
    for i in range(len(hrh)):
          print'  { 0u,  '+str(hrh[i])+'u }, /* Array index 0, dedicated RX buffer ("HRH = '+str(i)+' is the Array index")*/\\'
  
    print '}\n\n'

    print '''/**********************************************************************************************
**********************************************************************************************/
#endif'''
    print '\n'

    
    
    #f.close()


CanMailbox_Cfg()
