
import json,sys,os

dbc=None
cfg_data = None
filter_data = None
no_of_buffers=32
no_of_controllers=1
CanDisp_Number_Of_Tx_Messages=0
CanDisp_Number_Of_Rx_Messages=0
CanDisp_Number_Of_MBs=0
drv_disp_code_gen_dir = './CODE_GEN'
drv_disp_data_dir='./data/'
tp_generic_config='TpMessage'
nm_generic_config='NmMessage'
il_generic_config='GenMsgIlSupport'

hth=[]
hrh=[]
gptx_range=[]
footer=''
dbc_file_name=''

def set_file_node_drv_disp(file_name,node):
    global dbc,dbc_file_name
    from Dbc_Parser import dbc_parser
    dbc=dbc_parser(file_name,node)
    dbc_file_name=file_name.split('/')[len(file_name.split('/'))-1]
    
def set_init_global(time_st):
    global cfg_data,filter_data,no_of_buffers,no_of_controllers,CanDisp_Number_Of_Tx_Messages,CanDisp_Number_Of_Rx_Messages,CanDisp_Number_Of_MBs
    global time_str,dbc_file_name,footer
    time_str = time_st
    cfg_data=None
    filter_data=None
    drv_file = open(drv_disp_data_dir+"CanDRVConfiguration.data",'r')
    filter_file = open(drv_disp_data_dir+"CanFilterConfiguration.data",'r')

    cfg_data = json.loads(drv_file.read())
    filter_data=json.loads(filter_file.read())
    drv_file.close()
    filter_file.close()
    
    no_of_buffers = 32
    cfg_data['CAN0_NUMBER_OF_BUFFERS']=32
    no_of_controllers=int(cfg_data['CAN_CFG_NUMBER_OF_CONTROLLERS'])
    
    disp_tx=[]
    disp_mailbox=[]
    CanDisp_Number_Of_Tx_Messages = 0
    CanDisp_Number_Of_Rx_Messages = 0
    CanDisp_Number_Of_MBs = 0

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

def can_cfg_gen():

    global drv_disp_code_gen_dir,drv_disp_data_dir,footer
    if not os.path.exists(drv_disp_code_gen_dir):
      os.mkdir(drv_disp_code_gen_dir)
    f=open(drv_disp_code_gen_dir+'/Can_cfg.h','w')
    
    sys.stdout=f
    global dbc
    global hth
    global hrh,gptx_range
    
    
    print '''#if !defined (CAN_CFG_H)
#define CAN_CFG_H'''
    print '\n'
    
    header='''/*===========================================================================

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
/************************************************************************
* FILENAME :        Can_cfg.h
*
* DESCRIPTION :
*       CAN driver configurations
*
* PUBLIC FUNCTIONS :
*
*
* NOTES :
*
*
* AUTHOR :             DATE :    
*
*
*************************************************************************/'''

    print header
    print '\n'
    print '#include "CanMailbox_Cfg.h"'
    print '\n'
    
    
    
    #can_cfg.h
    print '''/* CAN harware loop wait counts for asynchronous events */
#define CANHW_WAITCOUNTMAX_VAL  (Can_loopchkctrType)(1000u)'''
    print '\n'

    print """/** The number of controllers that are configured. */"""
    print '#define CAN_CFG_NUMBER_OF_CONTROLLERS '+str(no_of_controllers)+'u'
    print '\n'
    
    #CAN WAKEUP Feature
    print '#define CAN_WAKUP_ENABLE	'+cfg_data["CAN_WAKUP_ENABLE"]
    print '\n'
    
    #HTH 
    
    print '/** The number of HTHs are configured. */'
    print '#define CAN_CFG_NUMBER_OF_HTHS '+str(len(hth))+'u\n'
    
    #HRH
    
    print '/** The number of HRHs are configured. */'
    print '#define CAN_CFG_NUMBER_OF_HRHS '+str(len(hrh))+'u\n'
    
    #Controller address
    print '''/** CAN controller physical address */'''
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_CONTROLLER_BASE_ADDRESS	(CAN_UINT32)'+cfg_data['CAN'+str(x)+'_CONTROLLER_BASE_ADDRESS']

    
    '''#Wakeup
    for x in range(no_of_controllers):
        print '#define CAN'+str(x)+'_WAKUP_ENABLE	'+cfg_data['CAN'+str(x)+'_WAKUP_ENABLE']'''

    
    print '''/* ===========================================================================

 Name(s):         CANx_NUMBER_OF_TX_BUFFERS

 Description:     Define number of Transmit Mailboxes

                  The Full CAN driver is designed to use the range of
                  mailboxes from Mailbox 0 up to the mailbox defined by
                  this configuration parameter as 
                  transmit mailboxes.

 Templates:       #define CANx_NUMBER_OF_TX_BUFFERS  (2)

 =========================================================================*/'''
    temp_tx=str(len(hth)-1+(gptx_range[1]-gptx_range[0]))
    print '#define CAN0_NUMBER_OF_TX_BUFFERS	'+str(len(hth)-1+(gptx_range[1]-gptx_range[0]))+'u'
    '''for x in range(no_of_controllers):
        print '#define CAN'+str(x)+'_NUMBER_OF_TX_BUFFERS	'+cfg_data['CAN'+str(x)+'_NUMBER_OF_TX_BUFFERS']'''
    print '\n'
    print '''
/* ===========================================================================

 Name(s):         CAN_CLOCK_CFG_VAL 

 Description:     Defines Bit Rate Value. To be written in the BCR Reg.   

 =========================================================================*/'''
    #CANx_CLOCK_CFG_VAL
    for x in range(0,no_of_controllers):
        #define CAN0_PERIPHERAL_CLOCK	((33000000U))
        print  '/**CAN'+str(x)+' Module Pherpheral clock*/'
        print '#define CAN'+str(x)+'_PERIPHERAL_CLOCK	(('+cfg_data['CAN'+str(x)+'_PERIPHERAL_CLOCK']+'U))'
        #define CAN0_BAUD_RATE			((125000uL))
        print  '/**CAN'+str(x)+' Module  Baudrate setting*/'
        br=int(cfg_data["CAN"+str(x)+"_BAUD_RATE"].strip('Kbps'))*1000
        print '#define CAN'+str(x)+'_BAUD_RATE	(('+str(br)+'UL))'
        #define CAN0_TSEG1	8U /* PropSeg + Phase seg1*/
        print  '/**CAN'+str(x)+' ModuleBit rate setting*/'
        print '#define CAN'+str(x)+'_TSEG1	'+cfg_data['CAN'+str(x)+'_TSEG1']+'U  /* PropSeg + Phase seg1*/'
        #define CAN0_TSEG2	2U /* PhaseSeg 2*/
        print '#define CAN'+str(x)+'_TSEG2	'+cfg_data['CAN'+str(x)+'_TSEG2']+'U  /* Phase seg2 */'
        #define CAN0_SJW	2U /* Sync jump width*/
        print '#define CAN'+str(x)+'_SJW	'+cfg_data['CAN'+str(x)+'_SJW']+'U  /*  SJW */'
        #define CAN0_NSAMP	1U /* Number of sample points*/
        print '#define CAN'+str(x)+'_NSAMP	'+cfg_data['CAN'+str(x)+'_NSAMP']+'U  /* Number of sample points */'
    
    print '\n'    
    #/* Baudrate prescalar defines*/
    for x in range(no_of_controllers):
        #define CAN0_BRP ((CAN0_PHERIPHERAL_CLOCK / ((CAN0_TSEG1 + CAN0_TSEG2 + 1u) * CAN0_BAUD_RATE)))
        print '#define CAN'+str(x)+'_BRP ((CAN'+str(x)+'_PERIPHERAL_CLOCK / ((CAN'+str(x)+'_TSEG1 + CAN'+\
              str(x)+'_TSEG2 + 1u) * CAN'+str(x)+'_BAUD_RATE)))'

    print '\n'   
    #define CAN0_MB_TYPES
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_MB_TYPES  \\'
        print '{ \\'
        for y in range(int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])):
            if (y != int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])-1):
                print 'CAN'+str(x)+'_MB_'+str(y)+',  \\'
            else:
                print 'CAN'+str(x)+'_MB_'+str(y)+'  \\'
        print '}\n'
                       
    print '\n'   
    ##define CAN_MAILBOX_TYPES	\
    print '#define CAN_MAILBOX_TYPES	\\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_MB_TYPES,  \\'
        else:
            print 'CAN'+str(x)+'_MB_TYPES  \\'
    print'}\n'

    print '\n'   
    #define CAN0_RX_FID
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_RX_FID  \\'
        print '{ \\'
        for y in range(int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])):
            if (y != int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])-1):
                print 'CAN'+str(x)+'_MSGBUF'+str(y)+'_FID,  \\'
            else:
                print 'CAN'+str(x)+'_MSGBUF'+str(y)+'_FID  \\'
        print '}\n'
    
    print '\n'   
    ##define CAN_RX_FILTER_CONFIGS	\
    print '#define CAN_RX_FILTER_CONFIGS	\\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_RX_FID,  \\'
        else:
            print 'CAN'+str(x)+'_RX_FID  \\'
    print'}\n'

    print '\n'   
    #define CAN0_RX_FILTERMASK 
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_RX_FILTERMASK  \\'
        print '{ \\'
        for y in range(int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])):
            if (y != int(cfg_data['CAN'+str(x)+'_NUMBER_OF_BUFFERS'])-1):
                print 'CAN'+str(x)+'_MSGBUF'+str(y)+'_MASK_VAL,  \\'
            else:
                print 'CAN'+str(x)+'_MSGBUF'+str(y)+'_MASK_VAL  \\'
        print '}\n'

    print '\n'   
    #define #define CAN_RX_MASK_CONFIGS\
    print '#define CAN_RX_MASK_CONFIGS	\\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_RX_FILTERMASK,  \\'
        else:
            print 'CAN'+str(x)+'_RX_FILTERMASK  \\'
    print'}\n'
    
    print '\n'   
    #CAN_HWCFG
    print '''/* ===========================================================================

 Name(s):         CAN_HWCFG

 Description:     Define Interrupts to be Enabled in the Hardware Layer

 =========================================================================*/'''
    print '#ifndef BOOTLOADER'
    disp_cfg_file = open(drv_disp_data_dir+"CanDISPConfiguration.data",'r')
    disp_cfg_data = json.loads(disp_cfg_file.read())
    disp_cfg_file.close()
        
    for x in range(0,no_of_controllers):
        print '    #define CAN'+str(x)+'_CFG_RX_INTERRUPT      '+cfg_data['CAN'+str(x)+'_CFG_RX_INTERRUPT']
        print '    #define CAN'+str(x)+'_CFG_TX_INTERRUPT      '+cfg_data['CAN'+str(x)+'_CFG_TX_INTERRUPT']
        print '    #define CAN'+str(x)+'_CFG_BUSOFF_INTERRUPT  '+cfg_data['CAN'+str(x)+'_CFG_BUSOFF_INTERRUPT']
        print '    #define CAN'+str(x)+'_CFG_WAKEUP_INTERRUPT  '+cfg_data['CAN'+str(x)+'_CFG_WAKEUP_INTERRUPT']
        print '\n'
        if disp_cfg_data['CANDISP_RECEIVE_INDICATION_API'] == 'STD_ON':
            print '    #define CAN'+str(x)+'_DISPNOTIFYRXINDICATION  '+'TRUE'
        else:
            print '    #define CAN'+str(x)+'_DISPNOTIFYRXINDICATION  '+'FALSE'
        
        if disp_cfg_data['CANDISP_TRANSMIT_CONFIRMATION_API'] == 'STD_ON':
            print '    #define CAN'+str(x)+'_DISPNOTIFYTXCONFIRMATION  '+'TRUE'
        else:
            print '    #define CAN'+str(x)+'_DISPNOTIFYTXCONFIRMATION  '+'FALSE'
        
        if disp_cfg_data['CANDISP_BUSOFF_INDICATION_API'] == 'STD_ON':
            print '    #define CAN'+str(x)+'_DISPNOTIFYBUSOFF  '+'TRUE'
        else:
            print '    #define CAN'+str(x)+'_DISPNOTIFYBUSOFF  '+'FALSE'
        
        if disp_cfg_data['CANDISP_RECEIVE_INDICATION_API'] == 'STD_ON':
            print '    #define CAN'+str(x)+'_DISPNOTIFYWAKEUP  '+'TRUE'
        else:
            print '    #define CAN'+str(x)+'_DISPNOTIFYWAKEUP  '+'FALSE'

    print '#else'
    for x in range(0,no_of_controllers):
        print '    #define CAN'+str(x)+'_CFG_RX_INTERRUPT      FALSE'
        print '    #define CAN'+str(x)+'_CFG_TX_INTERRUPT      FALSE'
        print '    #define CAN'+str(x)+'_CFG_BUSOFF_INTERRUPT  FALSE'
        print '    #define CAN'+str(x)+'_CFG_WAKEUP_INTERRUPT  FALSE'
        print '\n'
        print '    #define CAN'+str(x)+'_DISPNOTIFYRXINDICATION  '+'FALSE'
        print '    #define CAN'+str(x)+'_DISPNOTIFYTXCONFIRMATION  '+'FALSE'
        print '    #define CAN'+str(x)+'_DISPNOTIFYBUSOFF  '+'FALSE'
        print '    #define CAN'+str(x)+'_DISPNOTIFYWAKEUP  '+'FALSE'
        
    print '#endif\n'
    
    print '\n'   
    #define CAN0_INTERRUPT_CONFIG_CONTROLLER \
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_INTERRUPT_CONFIG_CONTROLLER \\'
        print '{\\'
        print 'CAN'+str(x)+'_CFG_BUSOFF_INTERRUPT,\\'
        print 'CAN'+str(x)+'_CFG_RX_INTERRUPT,\\'
        print 'CAN'+str(x)+'_CFG_TX_INTERRUPT,\\'
        print 'CAN'+str(x)+'_CFG_WAKEUP_INTERRUPT\\'
        print '}\n'

    #CAN_CFG_INTERRUPTS
    print '\n'   
    print '#define CAN_CFG_INTERRUPTS	\\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_INTERRUPT_CONFIG_CONTROLLER,\\'
        else:
            print 'CAN'+str(x)+'_INTERRUPT_CONFIG_CONTROLLER\\'
    print '}\n'
    print '\n'   
    #/** Part of the initializer to the constant array of controllers. */
    for x in range(0,no_of_controllers):
        print '#define CAN'+str(x)+'_CFG_CONTROLLER \\'
        print '{\\'
        print '/* Pointer to an array of baudrates. */\\'
        print '  (Can_ControllerBaudrateConfigType const * const)(&(Can_Baudrates['+str(x)+'u])), /* CONSTP2(Can_ControllerBaudrateConfigType, TYPEDEF, TYPEDEF) */\\'
        print '  \\'
        print '  /* Id of the controller. */\\'
        print '  (Can_ControllerIdType)'+str(x)+'u, /* CONST(Can_ControllerIdType, TYPEDEF) */\\'
        print '  \\'
        print '  /* Pointer to the default baudrate setting. */\\'
        print '  (Can_ControllerBaudrateConfigType const * const)(&(Can_Baudrates['+str(x)+'u])), /* CONSTP2(Can_ControllerBaudrateConfigType, TYPEDEF, TYPEDEF) */\\'
        print '  \\'
        print '  (Can_ControllerInterruptconfigType const * const)(&(Can_InterruptConfigs['+str(x)+'u])),\\'
        print '  /* Address offset to the message RAM base address where the filters for extended */\\'
        print '  /* messages shall be located. */\\'
        print '  CAN'+str(x)+'_CONTROLLER_BASE_ADDRESS, /* CONST(CAN_UINT32, TYPEDEF) */\\'
        print '  \\'
        print '  /* Address offset to the message RAM base address where the filters for standard */\\'
        print '  /* messages shall be located. */\\'
        print '  0x100u, /* CONST(CAN_UINT16, TYPEDEF) */\\'
        print '  (CAN_UINT8)1u, /* NumberOfBaudrates CONST(CAN_UINT8, TYPEDEF) */\\'
        print '  (CAN_UINT32 const * const )(&(Can_RxFilterConfigs['+str(x)+'][0])),\\'
        print '  (CAN_UINT32 const * const )(&(Can_RxMaskConfigs['+str(x)+'][0])),\\'
        print '  /* Configuration of the dedicated RX buffers. The ElementCount equals the number */\\'
        print '  /* of filter settings in the filter settings list. */\\'
        print '  \\'
        print '  {\\'
        print '  /* The number of elements belonging to the buffer or FIFO, i.e. the buffer/FIFO */\\'
        print '  /* size in elements. */\\'
        print '  CAN'+str(x)+'_NUMBER_OF_TX_BUFFERS, /* CONST(CAN_UINT8, TYPEDEF) */\\'
        print '  \\'
        print '  /* The size of each field in the buffer or FIFO. */\\'
        print '  (Can_ControllerBufferSizeType)'+str(gptx_range[0]+1)+'u, /* CONST(Can_ControllerBufferSizeType, TYPEDEF) */\\'
        print '  \\'
        print '  /* Start address of the buffer or FIFO in bytes relative (offset) to the CAN */\\'
        print '  /* message RAM base address. */\\'
        print '  0x20u /* CONST(CAN_UINT16, TYPEDEF) */\\'
        print '  }, /* CONST(Can_ControllerBufferCfgType, TYPEDEF) */\\'
        print '  \\'
        print '  \\'
        print '  {\\'
        print '  /* The number of elements belonging to the buffer or FIFO, i.e. the buffer/FIFO */\\'
        print '  /* size in elements. */\\'
        print '  '+str(str(gptx_range[0]+1))+'u, /* CONST(CAN_UINT8, TYPEDEF) */\\'
        print '  \\'
        print '  /* The size of each field in the buffer or FIFO. */\\'
        print '  '+str(hrh[0])+'u, /* CONST(Can_ControllerBufferSizeType, TYPEDEF) */\\'
        print '  \\'
        print '  /* Start address of the buffer or FIFO in bytes relative (offset) to the CAN */\\'
        print '  /* message RAM base address. */\\'
        print '  0x20u /* CONST(CAN_UINT16, TYPEDEF) */\\'
        print '  },\\'
        print '  /* The wakeup source id that is passed to EcuM_CheckWakeup. */\\'
        print '  (1uL << 0u),/* CONST(CAN_UINT32, TYPEDEF) */\\'
        print '  (Can_MsgBuffercfg_types const * const)(&(Can_MailboxTypeConfigs['+str(x)+'][0]))\\'
        print '}\n'


    print '\n'   
    #/** Initializer to the constant array of baudrates. */
    print '/** Initializer to the constant array of baudrates. */'
    print '#define CAN_CFG_BAUDRATES \\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_CFG_BAUDRATES,\\'
        else:
            print 'CAN'+str(x)+'_CFG_BAUDRATES \\'
    
    print '}'
    
    print '\n'   
    print '/** Initializer to the constant array of controllers. */'
    print '#define CAN_CFG_CONTROLLERS \\'
    print '{\\'
    for x in range(0,no_of_controllers):
        if x!=no_of_controllers-1:
            print 'CAN'+str(x)+'_CFG_CONTROLLER,\\'
        else:
            print 'CAN'+str(x)+'_CFG_CONTROLLER\\'
    
    print '}'
    
    print '\n'   
    print '/** The number of baudrates that are configured. */'
    print '#define CAN_CFG_NUMBER_OF_BAUDRATES 1u'
    
    print '\n'   
    for x in range(0,no_of_controllers):
        print '''#define CAN'''+str(x)+'''_CFG_BAUDRATES \\
        /* Array of Can_ControllerBaudrateConfigType */\\
        /* The value by which the CAN prescaler output frequency is divided for generating */\\
        /* the bit time quanta. (I.e. there is a global CAN prescaler maintained by */\\
        /* Can_ModuleManager, and an additional individual prescaler per CAN controller.) */\\
        /* The bit time is built up from a multiple of this quanta. */\\
        /* Valid values for the Baud Rate Prescaler are 1 to 1024. */\\
        /* CONST(uint16, TYPEDEF) BaudratePrescaler; */\\
        /*    |      */\\
        /*    |      The value of the baudrate in kbps. */\\
        /*    |      CONST(uint16, TYPEDEF) BaudrateValue; */\\
        /*    |      |    */\\
        /*    |      |    (Re) Synchronization Jump Width: Valid values are 1 to 16. */\\
        /*    |      |    CONST(CAN_UINT8, TYPEDEF) SyncJumpWidth; */\\
        /*    |      |    |    */\\
        /*    |      |    |    Time segment before sample point: Valid values are 2 to 64. */\\
        /*    |      |    |    CONST(CAN_UINT8, TYPEDEF) TSeg1; */\\
        /*    |      |    |    |    */\\
        /*    |      |    |    |    Time segment after sample point: Valid values are 1 to 16. */\\
        /*    |      |    |    |    CONST(CAN_UINT8, TYPEDEF) TSeg2; */\\
        /*    |      |    |    |    |  */\\
        /*    V      V    V    V    V  */\\
        {CAN'''+str(x)+'''_BRP,  CAN'''+str(x)+'''_BAUD_RATE,  CAN'''+str(x)+'''_SJW,  CAN'''+str(x)+'''_TSEG1,  CAN'''+str(x)+'''_TSEG2 ,CAN'''+str(x)+'''_NSAMP}, '''+'/* Array index 0, deviation to configured baudrate 0.0% */\\'

        print '''/***********************************************************************************************/'''
        print '\n'
    
    print '\n'   
    for x in range(0,no_of_controllers):
    
        print '#if CAN_CFG_NUMBER_OF_CONTROLLERS > '+str(x)+'U'

        print '''       #if ((CAN'''+str(x)+'''_TSEG1 < 4) || (CAN'''+str(x)+'''_TSEG1 > 16))
        #error "Violation of TSEG1 setting in Controller '''+str(x)+'''"
        #endif
        #if ((CAN'''+str(x)+'''_TSEG2 == 0) || (CAN'''+str(x)+'''_TSEG2>8))
            #error "Violation of TSEG2 setting in Controller '''+str(x)+'''"
        #endif

        #if (CAN'''+str(x)+'''_SJW >4)
        #error "Violation of SJW setting in Controller '''+str(x)+'''"
        #endif

        #if ((CAN'''+str(x)+'''_NSAMP != 1) && (CAN'''+str(x)+'''_NSAMP !=3))
            #error "Violation of Sample point setting in Controller '''+str(x)+'''"
        #endif
        #if ((CAN'''+str(x)+'''_BRP & 0x01) != 0x01)
            #if (CAN'''+str(x)+'''_BRP > 512U)
                #error "Violation of Baud rate Prescalar in Controller '''+str(x)+'''"
            #endif
        #else
            #error "Violation of Baud rate Prescalar in Controller '''+str(x)+'''0"
        #endif
        #if (CAN0_PERIPHERAL_CLOCK  != (CAN'''+str(x)+'''_BRP * CAN'''+str(x)+'''_BAUD_RATE * (CAN'''+str(x)+'''_TSEG1 + CAN'''+str(x)+'''_TSEG2 + 1u) ))
            #error "Violation of Baud rate Prescalar in Controller '''+str(x)+'''"
        #endif	

#endif'''
        print '\n'
    
    print '\n'   
    print '#if CAN_CFG_NUMBER_OF_CONTROLLERS == 1U'
    print '     #define CAN_NUMBER_OF_TX_BUFFERS	CAN0_NUMBER_OF_TX_BUFFERS'
    print '#endif'
    print '\n'
    print '#endif'
   
    print '\n\n'
    print footer
    

    f.close()



#CanMailbox_cfg.h

#for x in range(no_of_controllers):
#    print '#define CAN'+str(x)+'_NUMBER_OF_TX_BUFFERS	'+cfg_data['CAN'+str(x)+'_NUMBER_OF_TX_BUFFERS']


def CanMailbox_Cfg():
    global dbc,tp_generic_config,nm_generic_config,il_generic_config,footer
    global drv_disp_code_gen_dir,drv_disp_data_dir
    if not os.path.exists(drv_disp_code_gen_dir):
      os.mkdir(drv_disp_code_gen_dir)
    f=open(drv_disp_code_gen_dir+'/CanMailbox_Cfg.h','w')
    
    sys.stdout = f
    
    global hrh,hth
    global no_of_buffers,gptx_range,disp_tx,disp_mailbox
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
            else:
                basic_can_tx.append(i['id'])
        else:
            basic_can_tx.append(i['id'])

    #il full can messages tx
    #print len(full_can_tx)
    #print full_can_tx
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

    #gptx checking
    if gptx!= 0:
        #tx_start = (no_of_buffers-gptx)
        for i in range(tx_start,tx_start-gptx,-1):
            buf_arr[i]='CAN_GENERALPURPOSE_TX_MB'
        hth.append('CAN_GENERALPURPOSE_TX_MB')
        gptx_range=[tx_start-gptx,tx_start]
        
    
    
    
    
    #print dbc.get_msg_type(il_generic_config,'tx')[0]

    remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')
    #nm Rx
    disp_mailbox=[]
    
    il_rx=dbc.get_msg_type(il_generic_config,'rx')
    diag_rx=dbc.get_msg_type(tp_generic_config,'rx')
    nm_rx=dbc.get_msg_type(nm_generic_config,'rx')
    
            
    for i in il_rx:
        if i['Msg_name'] in filter_data:
            if filter_data[i['Msg_name']]=="on":
                full_can_rx.append(i['id'])
            else:
                basic_can_rx.append(i['id'])
        else:
            basic_can_rx.append(i['id'])
    
    ### Code  start for making basic can message as full can message in the remainig buf which are not selected by user as full can  
    if len(nm_rx)!=0:
        remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')-(len(diag_rx)+1)
    else:
        remaining_buf_rx=buf_arr.count('CAN_FULLCAN_RX_MB')-(len(diag_rx))

    full_can_rx_length=len(full_can_rx)
    remaining_buf_rx = remaining_buf_rx-full_can_rx_length
    basic_can_rx_length=len(basic_can_rx)
    
    items_to_remove=[]

    if remaining_buf_rx >= basic_can_rx_length:
        copy_range=basic_can_rx_length
    else:
        copy_range=remaining_buf_rx-1
        
    for i in range(copy_range):
        full_can_rx.append(basic_can_rx[i])
        items_to_remove.append(basic_can_rx[i])

    for rem_mes in items_to_remove:
        basic_can_rx.remove(rem_mes)
        
    ### Code end ##
    
    
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
    
    #print rx_start
    #print full_can_rx
    
    if len(full_can_rx)!= 0:
        for idx in full_can_rx:
            buf_arr[rx_start]='CAN_FULLCAN_RX_MB'
            disp_mailbox.append(('CAN_FULLCAN_RX_MB',idx))
            filter_id[rx_start]=idx
            hrh.append(rx_start)
            mask_value[rx_start]='0xFFFFFFFF'
            rx_start=rx_start+1
    
    
    
    

    print '''#if !defined (CANMAILBOX_CFG_H)
#define CANMAILBOX_CFG_H'''

    header='''/* ===========================================================================

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
/*H**********************************************************************
* FILENAME :        CanMailbox_cfg.h
*
* DESCRIPTION :
*       CAN driver configurations
*
* PUBLIC FUNCTIONS :
*
*
* NOTES :
*
*
* AUTHOR :             DATE :    
*
*
*H***********************************************************************/'''
    print '\n\n'
    print header
    print '\n\n'
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
    print '''/* ===========================================================================

 Name(s):     CAN Filter Parameters

 Description: Specifies the  Filter Configurations

              The controller has 32 mailboxes that may be
              configured as transmit or receive mailboxes. Each mailbox
              has an associated identifier. A receive mailbox uses its
              identifier, mask values, to qualify a received message for storage
              into the mailbox. Transmit mailboxes configured to transmit
              a Data Frame in response to a Remote Frame reception use
              their identifier to qualify the Remote Frame reception.

              Different CAN controllers use different conventions for
              mask bit "Care" and "Don't Care" designation. In the case of
              this , a "1" value is a " Don't Care" bit 
              (The corresponding incoming bit is don't care )and a "0" 
              value is a "Care" bit(The corresponding ID bit is checked 
              against the incoming ID bit) 
 Templates:
              CAN_MASKn_VALUE (n = G, 14, 15)

              This macro defines the Acceptance Mask Value for a specific
              mask. The ColdFire FlexCAN has 1 global mask value, 2 Special
              masks that can be used for MB14 & 15   

              Note that Mask values are specified for 29 bits (28-0)
              that are applied to received messages with "Extended" 29-Bit
              CAN Identifiers. Messages with "Standard" 11-Bit Identifiers
              use the 11 Most Significant bits (28-18) of the 29 bit value
              to qualify the received messages

              Examples:
              #define  CANx_MSGBUFn_MASK_VAL    (0x0000FFFFu)

              This macro specifies if the MASK value is intended to be
              applied for Extended (29 Bit) or Standard (11 Bit) CAN
              Identifiers. For Standard Identifiers, the specified Mask
              value is programmed to accommodate an 11 Bit Identifier by
              left shifting the 11 Bit Identifier into the 11 MSBits of
              the 32(3 bits reserved) Bit Identifier registers. This 
              parameter is either enabled or disabled, as shown in the 
              following examples.

              This macro defines the Filter Identifier value for the "nth"
              mailbox. Extended Messages use 29 bit Identifiers, whereas
              Standard Messages use 11 Bit Identifiers.

              Examples:
              #define  CAN_MSGBUF0_FID    (0x01A2F473Cu)
              #define  CAN_MSGBUF1_FID    (0x3B7u)
              (0x1FFFFFFF) (0x00000000u)

              This macro also defines whether the message type received for
              a given mailbox is an Extended Identifier or a Standard
              Identifier.
=========================================================================*/
    
/**CAN0 module filter mask configuration based on message ID*/'''
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
    
    print '''/**********************************************************************************************
                HTH  Configuration :
**********************************************************************************************
Description:

An unique id(HTH) is assigned to a particular channel's particular mailbox(Incase of Full CAN) or 
a FIFO or a GPTX cluster .
Using that unique identifier above layers can access the hardware mailbox to initiate the 
transmission .Advantage is above layer need not worry about which channel to access and 
which mailbox in that channel to be accessed.
So Disp/If layer generally maps its Message handle objects to HTH's.
Whenever a message object needs to be transmitted, Disp/If layer transmits using its mapped HTH.
Whenever a Transmit confirm indication callout comes from driver layer to Disp/If layer 
,corresponding HTH will be given by the driver layer.
Using the HTH and PduId Disp layer manages to deliver the notification upper layers.

Rules : 
    1) A particular hw MB in a Particular Channel may have maximum of 1 HTH.
    
    3) Multiple message handles in above layer can be mapped to single HTH and the reverse case is never allowed.
    
 HTH configuration: 
/** Provides upper layers multiple channels to transmit eg. upper layer can use HTH ch 0 to transmit the message in FIFo 
(or) HTH ch1 to transmit the messages in dedicated Mailbox 26 and so on...**/
/** Number of HTH ch must be configured through the macro """CAN_CFG_NUMBER_OF_HTHS"""" **/'''

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
    print '''/**********************************************************************************************
**********************************************************************************************
Description:

An unique id(HRH) is assigned to a particular channel's particular mailbox.
Using that unique identifier above layers can access the hardware mailbox contents.
Advantage is above layer need not worry about which channel to access and 
which mailbox in that channel to be accessed.
So Disp/If layer generally maps its Message handle object to HRH.
Whenever a receive indication callout comes from driver layer to Disp/If layer 
,corresponding HRH will be given by the driver layer.
Using the HRH Disp layer manages to find the Message Handle.

Rules : 
    1) A particular hw MB in a Particular Channel may have maximum of 1 HRH.

    2) Entry in the below HRH should be ascending order in both "Channel number"wise as well as "MB index"wise.
    
    3) Multiple message handles in above layer can be mapped to single MB and the reverse case is never allowed.
    
*/'''
  
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

    print footer
    
    f.close()
 
def can_disp_par_c():
    
    global disp_tx,disp_mailbox,CanDisp_Number_Of_Tx_Messages,CanDisp_Number_Of_Rx_Messages,CanDisp_Number_Of_MBs
    global dbc,tp_generic_config,nm_generic_config,il_generic_config,footer
    
    global drv_disp_code_gen_dir,drv_disp_data_dir
    if not os.path.exists(drv_disp_code_gen_dir):
      os.mkdir(drv_disp_code_gen_dir)
    f=open(drv_disp_code_gen_dir+'/CanDisp_Par_Cfg.c','w')
    
    
    sys.stdout = f
    
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
**  Name:           CanDisp_Par_Cfg.c
**
**  Description:    CAN Dispatcher parameter Configuration file for corresponding
**                    Network database
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/
'''

    
    '''CanDisp_MailBoxConfigType const CanDisp_MailBoxConfig[CanDisp_Number_Of_MBs] = {
    /* Index    PduIdFirst                     PduIdLast                     Controller  MailBoxType             */
  { /*     0 */         0U  /* RxPduId 0 */  ,        0U  /* RxPduId 0 */  ,         0U, CANDISP_RxFullCANMailbox  },
  { /*     1 */         1U  /* RxPduId 1 */  ,        1U  /* RxPduId 1 */  ,         0U, CANDISP_RxBasicCANMailbox  },
  { /*     2 */         2U  /* RxPduId 2 */  ,        2U  /* RxPduId 2 */  ,         0U, CANDISP_RxFullCANMailbox  },
  { /*     3 */         3U  /* RxPduId 3 */  ,        3U  /* RxPduId 3 */  ,         0U, CANDISP_RxFullCANMailbox  }
};'''

    print header

    print '\n\n'
    
    include='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/

# include "CanDisp_Par_Cfg.h"
# include "CanIl_Par_Cfg.h"
# include "CanNm_Par_Cfg.h"
# include "CanIl.h"
# include "CanNm.h"
/*# include "CanXcp.h"*/
# include "CanTp.h"

/* ===========================================================================
** M A C R O   D E F I N I T I O N S
** =========================================================================*/


/* ===========================================================================
** G L O B A L   C O N S T A N T   D E F I N I T I O N S
** =========================================================================*/'''

    print include
    print '\n\n'
    print '''/**********************************************************************************************************************
  CanDisp_RxIndicationFctList
**********************************************************************************************************************/
/** 
  \\var    CanDisp_RxIndicationFctList
  \\brief  Rx indication functions table.
  \\details
  Element               Description
  RxIndicationFct       Rx indication function.
  RxIndicationLayout    Layout of Rx indication function.
*/ 
CanDisp_RxIndicationFctListType const CanDisp_RxIndicationFctList[CanDisp_Type_Of_Messages] = {\\
    /* Index    RxIndicationFct                                                RxIndicationLayout                   */\\
  { /*     0 */  { (CanDisp_SimpleRxIndicationFctType)CanIl_RxIndication    }, CanDisp_AdvancedRxIndicationLayout } ,\\
  { /*     1 */  { (CanDisp_SimpleRxIndicationFctType)CanNm_RxIndication    }, CanDisp_AdvancedRxIndicationLayout } ,\\
  { /*     2 */  { (CanDisp_SimpleRxIndicationFctType)CanTp_RxIndication    }, CanDisp_AdvancedRxIndicationLayout } ,\\
  { /*     3 */  { (CanDisp_SimpleRxIndicationFctType)NULL/*CanXcp_RxIndication*/   }, CanDisp_AdvancedRxIndicationLayout } ,\\
  { /*     4 */  { (CanDisp_SimpleRxIndicationFctType)NULL/*CanGw_RxIndication*/   }, CanDisp_AdvancedRxIndicationLayout } \\
};
'''

    print '\n\n'
    no_of_controllers = 1
    temp_i=0
    rx_pdu_count=0
    
    #####################################################################
    ##########CanDisp_MailBoxConfig
    #####################################################################
    
    print '''/**********************************************************************************************************************
  CanDisp_MailBoxConfig
**********************************************************************************************************************/
/** 
  \\var    CanDisp_MailBoxConfig
  \\brief  Mailbox table.
  \\details
  Element        Description
  PduIdFirst     "First" PDU mapped to mailbox.
  PduIdLast      "Last" PDU mapped to mailbox.
  Controller     Handle ID of controller.
  MailBoxType    Type of mailbox: Rx-/Tx- BasicCAN/FullCAN/unused.
*/ '''
    print '\n\n'
    print '''CanDisp_MailBoxConfigType const CanDisp_MailBoxConfig[CanDisp_Number_Of_MBs] = {\\
    /* Index    PduIdFirst                     PduIdLast                     Controller  MailBoxType             */\\'''
    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            print '{ /*     '+str(temp_i)+' */         '+str(rx_pdu_count)+'U   /*RxPduId '+str(rx_pdu_count)+' */  ,        '+str(len(i[1][0]))+'U  /* RxPduId '+str(len(i[1][0]))+' */  ,         '+str(no_of_controllers-1)+'U, CANDISP_RxBasicCANMailbox  },\\'
            temp_i=temp_i+1
            rx_pdu_count = rx_pdu_count+len(i[1][0])
            #print rx_pdu_count
        elif i[0] == 'CAN_BASICCAN_RANGEFILTER_RX_MB':
            print '{ /*     '+str(temp_i)+' */         '+str(rx_pdu_count)+'U   /*RxPduId '+str(rx_pdu_count)+' */  ,        '+str(rx_pdu_count)+'U  /* RxPduId '+str(rx_pdu_count)+' */  ,         '+str(no_of_controllers-1)+'U, CANDISP_RxBasicCANMailbox  },\\'
            temp_i=temp_i+1
            rx_pdu_count = rx_pdu_count+1
            #print rx_pdu_count
        elif i[0] == 'CAN_FULLCAN_RX_MB':
            print '{ /*     '+str(temp_i)+' */         '+str(rx_pdu_count)+'U   /*RxPduId '+str(rx_pdu_count)+' */  ,        '+str(rx_pdu_count)+'U  /* RxPduId '+str(rx_pdu_count)+' */  ,         '+str(no_of_controllers-1)+'U, CANDISP_RxFullCANMailbox  },\\'
            temp_i=temp_i+1
            rx_pdu_count = rx_pdu_count+1
            #print rx_pdu_count
        else:
            pass

    print '};'
    print '\n\n'
    
    CanDisp_Number_Of_MBs=temp_i

    #####################################################################
    ##########CanDisp_RxPduCanId
    #####################################################################

    print '''/**********************************************************************************************************************
  CanDisp_RxPduCanId
**********************************************************************************************************************/
/** 
  \\var    CanDisp_RxPduCanId
  \\brief  Rx-PDU: CAN identifier.
*/ 
'''
    print '\n\n'
    temp_i=0
    print '''CanDisp_RxPduCanIdentType const CanDisp_RxPduCanId[CanDisp_Number_Of_Rx_Messages] = {\\
  /* Index     RxPduCanId       RxOption          */\\'''
    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            for idx in i[1][0]:
                print '/*     '+str(temp_i)+' */ {   '+hex(int(idx))+'U,		CANB_RX_STANDARD   },\\'
                temp_i=temp_i+1
            
        elif i[0] == 'CAN_BASICCAN_RANGEFILTER_RX_MB':
            print '/*     '+str(temp_i)+' */ {   '+hex(int(i[1][0]))+'U,		CANB_RX_STANDARD   },\\'
            temp_i=temp_i+1
           
        elif i[0] == 'CAN_FULLCAN_RX_MB':
            print '/*     '+str(temp_i)+' */ {   '+hex(int(i[1]))+'U,		CANB_RX_STANDARD   },\\'
            temp_i=temp_i+1
        else:
            pass

    print '};'
    print '\n\n'

    
    '''CanDisp_RxPduMaskType const CanDisp_RxPduMask[CanDisp_Number_Of_Rx_Messages] = {
  /* Index    RxPduMask  */
  /*    0 */    0x07FFU
 ,/*    1 */    0x0607U
 ,/*    2 */    0x07FFU
 ,/*    3 */    0x07FFU
};'''

    #####################################################################
    ##########CanDisp_RxPduMask
    #####################################################################
    
    print '''/**********************************************************************************************************************
  CanDisp_RxPduMask
**********************************************************************************************************************/
/** 
  \\var    CanDisp_RxPduMask
  \\brief  Rx-PDU: CAN identifier mask.
*/ '''
    print '\n'
    temp_i=0
    print '''CanDisp_RxPduMaskType const CanDisp_RxPduMask[CanDisp_Number_Of_Rx_Messages] = {\\
  /* Index    RxPduMask  */\\'''
    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            print '/*    '+str(temp_i)+' */    0x07FFU,\\'           
            temp_i=temp_i+1
            
        elif i[0] == 'CAN_BASICCAN_RANGEFILTER_RX_MB':
            
            print '/*    '+str(temp_i)+' */    0x0'+i[1][1]+'U ,\\'           
            temp_i=temp_i+1
           
        elif i[0] == 'CAN_FULLCAN_RX_MB':
            print '/*    '+str(temp_i)+' */    0x07FFU,\\'           
            temp_i=temp_i+1
        else:
            pass

    

    print '};'
    print '\n\n'


    il_rx=dbc.get_msg_type(il_generic_config,'rx')
    nm_rx=dbc.get_msg_type(nm_generic_config,'rx')
    diag_rx=dbc.get_msg_type(tp_generic_config,'rx')
    
    pdu_config={}
    diag_id=[]
    il_id=[]
    il_count_rx =len(il_rx)
    il_count_tx =len(dbc.get_msg_type(il_generic_config,'tx'))
    
    for idx in il_rx:
        il_id.append(str(idx['id']))
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])

    for idx in nm_rx:
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])
        
    for idx in diag_rx:
        diag_id.append(str(idx['id']))
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])
        
    temp_i = 0
    
    #####################################################################
    ##########CanDisp_RxPduConfig
    #####################################################################
    
    print '''/**********************************************************************************************************************
  CanDisp_RxPduConfig
**********************************************************************************************************************/
/** 
  \\var    CanDisp_RxPduConfig
  \\brief  Rx-PDU configuration table.
  \\details
  Element         Description
  UpperPduId      PDU ID defined by upper layer.
  Dlc             Data length code.
  RxIndication    Rx indication function.
*/
'''
    print '\n'
    print '''CanDisp_RxPduConfigType const CanDisp_RxPduConfig[CanDisp_Number_Of_Rx_Messages] = {\\
    /* Index    UpperPduId                                               Dlc  RxIndication                            */\\'''

    
    #print pdu_config
    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            for mes in i[1][0]:
                if mes in pdu_config:
                    print '{ /*     '+str(temp_i)+' */ Can_Channel0_Il_Rx_Message_'+pdu_config[mes][0]+','+" "*(40-len(pdu_config[mes][0])+10)+pdu_config[mes][1]+'U,  1u /*1U*/  /* CanIl_RxIndication  */ },\\'
                    temp_i=temp_i+1
            
        elif i[0] == 'CAN_BASICCAN_RANGEFILTER_RX_MB':
            
            if i[1][2] in pdu_config:
                print '{ /*     '+str(temp_i)+' */ Can_Channel0_Nm_RxMessage_NmRangeMask,'+" "*(30-len(pdu_config[i[1][2]][1])+10)+pdu_config[i[1][2]][1]+'U,  2u/*4U*/  /* CanNm_RxIndication  */ },\\'
                temp_i=temp_i+1
           
        elif i[0] == 'CAN_FULLCAN_RX_MB':
            
            if str(i[1]) in pdu_config:
                
                if  i[1] in diag_id:
                    print '{ /*     '+str(temp_i)+' */ Can_Channel0_Tp_RxMessage_'+pdu_config[i[1]][0]+',  '+" "*(40-len(pdu_config[i[1]][0])+10)+pdu_config[i[1]][1]+'U,  4u/*4U*/  /* CanTp_RxIndication  */ },\\'
                elif i[1] in il_id:
                    print '{ /*     '+str(temp_i)+' */ Can_Channel0_Il_Rx_Message_'+pdu_config[i[1]][0]+', '+" "*(40-len(pdu_config[i[1]][0])+10)+pdu_config[i[1]][1]+'U,  1u /*1U*/  /* CanIl_RxIndication  */ },\\'
                else:
                    pass
            
                temp_i=temp_i+1
        else:
            pass
    print '};\n\n'
    CanDisp_Number_Of_Rx_Messages=temp_i
    
    #####################################################################
    ##########CanDisp_ControllerConfig
    #####################################################################
    


   
        
   
    
    #####################################################################
    ##########CanDisp_TxPduConfig
    #####################################################################
    
    il_tx=dbc.get_msg_type(il_generic_config,'tx')
    
    nm_tx=dbc.get_msg_type(nm_generic_config,'tx')
    diag_tx=dbc.get_msg_type(tp_generic_config,'tx')
    #CAN_DEDICATED_TX_MB CAN_GENERALPURPOSE_TX_MB
    pdu_config={}
    il_id=[]
    diag_id=[]
    nm_id=[]
    
    for idx in il_tx:
        il_id.append(str(idx['id']))
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])

    for idx in nm_tx:
        nm_id.append(str(idx['id']))
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])
        
    for idx in diag_tx:
        diag_id.append(str(idx['id']))
        pdu_config[str(idx['id'])]=(idx['Msg_name'],idx['DLC'])

    hth=-1
    index=0
    temp_gptx_flag=0
    
    
    print '''/**********************************************************************************************************************
  CanDisp_TxPduConfig
**********************************************************************************************************************/
/** 
  \\var    CanDisp_TxPduConfig
  \\brief  Tx-PDUs - configuration.
  \\details
  Element              Description
  Hth                  Hardware transmit handle.
  CanId                CAN identifier (16bit / 32bit).
  UpperLayerTxPduId    Upper layer handle ID (8bit / 16bit).
  Controller           Controller.
  Dlc                  Data length code.
  TxConfirmation       Tx confirmation function.
*/ 
'''

    gptx_index_value=255   
    print '''CanDisp_TxPduConfigType const CanDisp_TxPduConfig[CanDisp_Number_Of_Tx_Messages] = {\\
    /* Index    Hth  CanId    TxOption           UpperLayerTxPduId                              Controller  Dlc  TxConfirmation     Comment */\\'''
    
    
            
    pdu_table_config=[]
    basic_can_hth=-1
    for element in disp_tx:
        #print disp_tx
        if element[0] == 'CAN_DEDICATED_TX_MB':
            hth=hth+1
            if element[1] in il_id:
                
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,  Can_Channel0_Il_Tx_Message_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,             1U  }, /* CanIl_TxConfirmation    */\\')
                

            elif element[1] in  nm_id:
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,  '+'Can_Channel0_Nm_TxMessage_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,             2U  }, /* CanNm_TxConfirmation    */\\')
               
                
            elif element[1] in diag_id:
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,  Can_Channel0_Tp_TxMessage_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,            4U  }, /* CanTp_TxConfirmation    */\\')
            else:
                pass

            temp_gptx_flag=1
            index=index+1

        elif element[0] == 'CAN_GENERALPURPOSE_TX_MB':
            
            if (hth == -1) or temp_gptx_flag ==1 :
                hth=hth+1
                temp_gptx_flag=0
            basic_can_hth = hth
            if element[1] in il_id:
                
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,  Can_Channel0_Il_Tx_Message_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,             1U  }, /* CanIl_TxConfirmation    */\\')
                gptx_index_value = hth
                
            elif element[1] in nm_id:
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,   '+'Can_Channel0_Nm_TxMessage_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,             2U  }, /* CanNm_TxConfirmation    */\\')
                gptx_index_value = hth
                
            elif element[1] in diag_id:
                pdu_table_config.append('{ /*     '+str(index)+' */  '+str(hth)+'U, '+hex(int(element[1]))+', CANB_TX_STANDARD,  Can_Channel0_Tp_TxMessage_'+pdu_config[element[1]][0]+'_TMH,        0U,  '+pdu_config[element[1]][1]+\
                        'U,            4U  }, /* CanTp_TxConfirmation    */\\')
                gptx_index_value = hth
            else:
                pass

            index=index+1

        else:
            pass
            
    CanDisp_Number_Of_Tx_Messages=index
    #print gptx_index_value
    #list txpdu based on upper layer pdu config
    il_tx=dbc.get_msg_type(il_generic_config,'tx')
    il_tx_sorted =  sorted(il_tx,key = lambda x: int(x['id']))
    
    gptx_index_ran=[]
    temp_count=0
    temp_index_count = 0
    for idx in il_tx_sorted:
        for elem in pdu_table_config:
            if hex(int(idx['id'])) in elem:
                print elem
                if gptx_index_value !=255 and str(gptx_index_value)+'U,' in elem :
                    gptx_index_ran.append(temp_count)
                temp_count+=1
                temp_index_count+=1

    #print gptx_index_ran
    nm_tx=dbc.get_msg_type(nm_generic_config,'tx')
    nm_tx_sorted =  sorted(nm_tx,key = lambda x: int(x['id']))
    
    for idx in nm_tx_sorted:
        for elem in pdu_table_config:
            if hex(int(idx['id'])) in elem:
                print elem
                temp_index_count+=1
                
    diag_tx=dbc.get_msg_type(tp_generic_config,'tx')
    diag_tx_sorted =  sorted(diag_tx,key = lambda x: int(x['id']))
    
    for idx in diag_tx_sorted:
        for elem in pdu_table_config:
            if hex(int(idx['id'])) in elem:
                print elem
                temp_index_count+=1
                
    
    print '};\n\n'

    
    print '''/**********************************************************************************************************************
  CanDisp_ControllerConfig
**********************************************************************************************************************/
/** 
  \\var    CanDisp_ControllerConfig
  \\brief  CAN controller configuration - Tx-BasicCAN.
  \\details
  Element           Description
  TxBCStartIndex    Tx-BasicCAN start index
  TxBCStopIndex     Tx-BasicCAN stop index
*/ '''
    #gptx_range[1]-gptx_range[0]
    #logic for hth if basic can range is not available

    print'''CanDisp_ControllerConfigType const CanDisp_ControllerConfig[CAN_NUMBER_OF_CHANNELS] = {
    /* Index    TxBCStartIndex  TxBCStopIndex        Comment */'''
    if basic_can_hth != -1:
        print '     { /*     0 */             '+str(basic_can_hth)+'U}   /* [Basic CAN HTH] */'
    else:
        
        print '     { /*     0 */             0xFFU}   /* [Basic CAN HTH] */'
    
    print '''};'''

    print '\n\n'
    #####################################################################
    ##########CanDisp_TxConfirmationFctList
    #####################################################################
    
    
    print '''/**********************************************************************************************************************
  CanDisp_TxConfirmationFctList
**********************************************************************************************************************/
/** 
  \\var    CanDisp_TxConfirmationFctList
  \\brief  Tx confirmation functions table.
*/ 
CanDisp_TxConfirmationFctType const CanDisp_TxConfirmationFctList[CanDisp_Type_Of_Messages] = {\\
  /* Index    TxConfirmationFctList              */\\
  /*     0 */ (CanDisp_TxConfirmationFctType)CanIl_TxConfirmation            ,\\
  /*     1 */ (CanDisp_TxConfirmationFctType)CanNm_TxConfirmation             ,\\
  /*     2 */ (CanDisp_TxConfirmationFctType)CanTp_TxConfirmation            ,\\
  /*     3 */ (CanDisp_TxConfirmationFctType)NULL/*CanXcp_TxConfirmation*/   ,\\
  /*     4 */ (CanDisp_TxConfirmationFctType)NULL/*CanGw_TxConfirmation*/    \\
};

'''

    basic_can_idx=[]
   
    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            for mes in i[1][0]:
                basic_can_idx.append(int(mes))
    ######Hash Function implementation################               
    if basic_can_idx != []:
        def is_prime(x):#funcion for checking prime number
            if x > 1:
                n = x // 2
                for i in range(2, n + 1):
                    if x % i == 0:
                        return False
                return True
            else:
                return False

        def find_next_prime(num):#function for the nearest next prime number
            while(num):
                if is_prime(num):
                    break
                else:
                    num+=1
            return num

        def hash_func(num,prime_max):#hash function is modulus with prime number
        
            if prime_max>0:
                return num%prime_max
            else:
                raise ValueError("prime max division by 0")
                
        def hash_table_gen(basic_can_idx,step_value):
            canDispRxHashTable=[]
            if len(basic_can_idx)>0:
                no_of_msg_in_mailbox=len(basic_can_idx)*4#size of  hash table--> no_of_ids*4 
                
                prime_max = find_next_prime(no_of_msg_in_mailbox)#finding the next prime number after the num of ids in basic can
                canDispRxHashTable=[255]*prime_max#filling the has table index with default value 255
                
                #following implementation is to map basic can id in the hash table
                for idx in basic_can_idx:
                    disp_idx=hash_func(idx,prime_max)#finding the hash table index from the hash function
                    print disp_idx,idx
                    if disp_idx<prime_max:#hash function returning id must not be greater than hash table size 
                        if canDispRxHashTable[disp_idx] == 255:#if that particular index doesnt have any basic can ids,then the basic can ids can be stored in the particular index
                            canDispRxHashTable[disp_idx]=idx
                        else:#if already a basic can id is present in that index,find for the next index that has 255 in it.
                            temp_i=1
                            start_idx=disp_idx#current idx is stored ,since checking for next free (255) value in hash table will be circular 
                            while(temp_i):
                                disp_idx+=step_value
                                if disp_idx<prime_max:
                                    if disp_idx!=(start_idx-1):
                                        if canDispRxHashTable[disp_idx] == 255:
                                            canDispRxHashTable[disp_idx]=idx
                                            temp_i=0                                
                                    else:
                                        raise ValueError("Hash buffer full!!!")
                                else:
                                    disp_idx=0#index exceeds the hash table size hence intializing the index to zero for start searching from 0th index in hash table
                    else:
                        raise ValueError("Invalid buffer access!!!")
            return canDispRxHashTable
        
       
        disp_cfg_file = open(drv_disp_data_dir+"CanDISPConfiguration.data",'r')
        disp_cfg_data = json.loads(disp_cfg_file.read())
        disp_cfg_file.close()
        
        if disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] == 'CANDISP_HASH':
            canDispRxHashTable=hash_table_gen(basic_can_idx,1)   
        elif disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] == 'CANDISP_DOUBLEHASH':
            canDispRxHashTable=hash_table_gen(basic_can_idx,5) #the step value is made as 5
        else:
            pass
            
        if disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] == 'CANDISP_HASH' or \
            disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] =='CANDISP_DOUBLEHASH':
            
            
            print 'CanDisp_RxPduCanIdType CanDispCh0RxHashTable[CanDispCh0RxSearchTableSize]={'
                                                 
            for mes in canDispRxHashTable:
                print hex(mes)+'u,  \\'
            print '};'
             
            print 'CAN_UINT16 SearchTableSize[CAN_NUMBER_OF_CHANNELS]={'+str(len(canDispRxHashTable))+'};'

    
    print '''/**********************************************************************************************************************
  CanDisp_WakeUpConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_WakeUpConfig
  brief                 Wake-up source configuration
  details
  Element                Description
  WakeUpSource           Wake-up source identifier
  Controller             CAN controller handle ID
  WakeUpTargetAddress    Logical handle ID of target (CAN controller / transceiver)
  WakeUpTargetModule     Target for wake-up source: CAN controller / transceiver
*/ 

CanDisp_WakeUpConfigType const CanDisp_WakeUpConfig[CanDisp_Number_Of_Wake_Channels] = {
    /* Index    WakeUpSource  Controller  WakeUpTargetAddress  WakeUpTargetModule     */
  { /*     0 */         32UL,         0U,                  0U, CANDISP_WAKEUPREQUEST_CAN } 
};

'''  


    
    print footer
    
    f.close()
 
def disp_cfg_par_h():
    global dbc,disp_mailbox,footer
    global CanDisp_Number_Of_Tx_Messages,CanDisp_Number_Of_Rx_Messages,CanDisp_Number_Of_MBs
    
    global drv_disp_code_gen_dir,drv_disp_data_dir
    if not os.path.exists(drv_disp_code_gen_dir):
      os.mkdir(drv_disp_code_gen_dir)
    f=open(drv_disp_code_gen_dir+'/CanDisp_Par_Cfg.h','w')
    
    disp_cfg_file = open(drv_disp_data_dir+"CanDISPConfiguration.data",'r')
    disp_cfg_data = json.loads(disp_cfg_file.read())
    disp_cfg_file.close()
    
    
    sys.stdout=f
    print '#if !defined( CAN_DISP_APP_CFG_H )'
    print '#define CAN_DISP_APP_CFG_H\n'
    
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
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           CanDisp_Par_Cfg.h
**
**  Description:    CAN Dispatcher configuration parameters for configured 
**                    database
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/'''

    print header
    includes='''/* ===========================================================================
** I N C L U D E   F I L E S
** =========================================================================*/

# include "CanDisp_Cfg.h"
# include "CanDisp_Defines.h"\n'''

    print includes

    print '''/*===========================================================================
** M A C R O   D E F I N I T I O N S
** =========================================================================*/

#ifndef ControllerId
#define ControllerId            (0u)
#endif
'''
    
    
    #--------------------------------------------------------------------------------------
    #--------------------------DBC Specific Parameters-------------------------------------
    #--------------------------------------------------------------------------------------
    print '#define CanDisp_Type_Of_Messages             '+'5'+'u'
    print '#define CanDisp_Number_Of_Rx_Messages        '+str(CanDisp_Number_Of_Rx_Messages)+'u'
    print '#define CanDisp_Number_Of_Rx_MBs             '+str(CanDisp_Number_Of_Rx_Messages)+'u'
    print '#define CanDisp_Number_Of_Tx_MBs             '+str(CanDisp_Number_Of_Tx_Messages)+'u'
    print '#define CanDisp_Number_Of_MBs                '+str(CanDisp_Number_Of_MBs)+'u'
    print '#define CanDisp_Number_Of_Tx_Messages        '+str(CanDisp_Number_Of_Tx_Messages)+'u'
    print '#define CanDisp_Number_Of_Wake_Channels	'+str(1)+'u'


    print '''/* ===========================================================================
** G L O B A L   C O N S T A N T   D E C L A R A T I O N S
** =========================================================================*/'''
    
       
    basic_can_idx=[]

    for i in disp_mailbox:
        if i[0] == 'CAN_BASICCAN_PATTERNFILTER_RX_MB':
            for mes in i[1][0]:
                basic_can_idx.append(int(mes))

    if basic_can_idx !=[]:
        def is_prime(x):#funcion for checking prime number
            if x > 1:
                n = x // 2
                for i in range(2, n + 1):
                    if x % i == 0:
                        return False
                return True
            else:
                return False

        def find_next_prime(num):#function for the nearest next prime number
            while(num):
                if is_prime(num):
                    break
                else:
                    num+=1
            return num
            
            
        if disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] == 'CANDISP_HASH' or \
            disp_cfg_data['CANDISP_CH0_SEARCH_ALGORITHM'] =='CANDISP_DOUBLEHASH':
            print '#define CanDispCh0RxSearchTableSize '+str(find_next_prime(len(basic_can_idx)))+'u\n'
            print 'extern CAN_UINT16 const SearchTableSize[CAN_NUMBER_OF_CHANNELS];'
            print 'extern CanDisp_RxPduCanIdType const CanDispCh0RxHashTable[CanDispCh0RxSearchTableSize]'

    #if  cfg_data[' CANDISP_RECEIVE_INDICATION_API'] = 'STD_ON':
    print '''/**********************************************************************************************************************
  CanDisp_RxIndicationFctList
**********************************************************************************************************************/
/** 
  var    CanDisp_RxIndicationFctList
  brief  Rx indication functions table.
  details
  Element               Description
  RxIndicationFct       Rx indication function.
  RxIndicationLayout    Layout of Rx indication function.
*/ 
extern CanDisp_RxIndicationFctListType const CanDisp_RxIndicationFctList[CanDisp_Type_Of_Messages]; '''

    #if cfg_data['
    print '''
/**********************************************************************************************************************
  CanDisp_RxPduConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_RxPduConfig
  brief  Rx-PDU configuration table.
  details
  Element         Description
  UpperPduId      PDU ID defined by upper layer.
  Dlc             Data length code.
  RxIndication    Rx indication function.
*/
extern CanDisp_RxPduConfigType const CanDisp_RxPduConfig[CanDisp_Number_Of_Rx_Messages];

/**********************************************************************************************************************
  CanDisp_RxPduCanId
**********************************************************************************************************************/
/** 
  var    CanDisp_RxPduCanId
  brief  Rx-PDU: CAN identifier.
*/ 
extern CanDisp_RxPduCanIdentType const CanDisp_RxPduCanId[CanDisp_Number_Of_Rx_Messages];

/**********************************************************************************************************************
  CanDisp_ControllerConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_ControllerConfig
  brief  CAN controller configuration - Tx-BasicCAN.
  details
  Element           Description
  TxBCStartIndex    Tx-BasicCAN start index
  TxBCStopIndex     Tx-BasicCAN stop index
*/ 
extern CanDisp_ControllerConfigType const CanDisp_ControllerConfig[CAN_NUMBER_OF_CHANNELS];

/**********************************************************************************************************************
  CanDisp_MailBoxConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_MailBoxConfig
  brief  Mailbox table.
  details
  Element        Description
  PduIdFirst     "First" PDU mapped to mailbox.
  PduIdLast      "Last" PDU mapped to mailbox.
  Controller     Handle ID of controller.
  MailBoxType    Type of mailbox: Rx-/Tx- BasicCAN/FullCAN/unused.
*/ 
extern CanDisp_MailBoxConfigType const CanDisp_MailBoxConfig[CanDisp_Number_Of_MBs];

/**********************************************************************************************************************
  CanDisp_RxPduMask
**********************************************************************************************************************/
/** 
  var    CanDisp_RxPduMask
  brief  Rx-PDU: CAN identifier mask.
*/ 
extern CanDisp_RxPduMaskType const CanDisp_RxPduMask[CanDisp_Number_Of_Rx_Messages];

/**********************************************************************************************************************
  CanDisp_TxConfirmationFctList
**********************************************************************************************************************/
/** 
  var    CanDisp_TxConfirmationFctList
  brief  Tx confirmation functions table.
*/ 
extern CanDisp_TxConfirmationFctType const CanDisp_TxConfirmationFctList[CanDisp_Type_Of_Messages];

/**********************************************************************************************************************
  CanDisp_TxPduConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_TxPduConfig
  brief  Tx-PDUs - configuration.
  details
  Element              Description
  Hth                  Hardware transmit handle.
  CanId                CAN identifier (16bit / 32bit).
  UpperLayerTxPduId    Upper layer handle ID (8bit / 16bit).
  Controller           Controller.
  Dlc                  Data length code.
  TxConfirmation       Tx confirmation function.
*/ 
extern CanDisp_TxPduConfigType const CanDisp_TxPduConfig[CanDisp_Number_Of_Tx_Messages];


/**********************************************************************************************************************
  CanDisp_WakeUpConfig
**********************************************************************************************************************/
/** 
  var    CanDisp_WakeUpConfig
  brief                 Wake-up source configuration
  details
  Element                Description
  WakeUpSource           Wake-up source identifier
  Controller             CAN controller handle ID
  WakeUpTargetAddress    Logical handle ID of target (CAN controller / transceiver)
  WakeUpTargetModule     Target for wake-up source: CAN controller / transceiver
*/

extern CanDisp_WakeUpConfigType const CanDisp_WakeUpConfig[CanDisp_Number_Of_Wake_Channels];'''
    print '\n\n#endif /* CAN_DISP_APP_CFG_H */'
    
    print footer
    f.close()
    
    
def can_disp_cfg_h():
    global dbc,footer
    global drv_disp_code_gen_dir,drv_disp_data_dir 
    disp_cfg_file = open(drv_disp_data_dir+"CanDISPConfiguration.data",'r')
    disp_cfg_data = json.loads(disp_cfg_file.read())
    disp_cfg_file.close()
    
       
    if not os.path.exists(drv_disp_code_gen_dir):
      os.mkdir(drv_disp_code_gen_dir)
    f=open(drv_disp_code_gen_dir+'/CanDisp_Cfg.h','w')
    
    sys.stdout=f
    print '#if !defined( CAN_DISP_CFG_H )'
    print '#define CAN_DISP_CFG_H\n'

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
**   its rights under all copyright laws to protect this work as a published
**   work, when appropriate.  Those having access to this work may not copy it,
**   use it, modify it or disclose the information contained in it without the
**   written authorization of Visteon Corporation.
** 
**  =========================================================================*/

/* ===========================================================================
**
**  Name:           CanDisp_Cfg.h
**
**  Description:    CAN Dispatcher specific configuration parameters
**
**  Organization:   Vehicle Communications
**                  Visteon Corporation
**
**  =========================================================================*/'''
    print header

    print '\n\n'

    print '''/* ===========================================================================
** M A C R O   D E F I N I T I O N S
** =========================================================================*/'''

    print '#define CanDisp_Config_Ptr                         NULL_PTR\n'

    
    print '''/* CAN Number of Hardware Channels */
#define CAN_NUMBER_OF_CHANNELS                     1
#define CAN_MAX_DATA_SIZE                          8\n\n'''

    
    str_len=[len(x) for x in disp_cfg_data]
    max_len=max(str_len)+2
    
    for keys in disp_cfg_data:
        print '#define '+keys+' '*(max_len-len(keys))+disp_cfg_data[keys]

    print '#define CANDISP_CH0_SEARCH_ALGORITHM			'+disp_cfg_data['CANDISP_SEARCH_ALGORITHM']
    print '\n\n#endif /* CAN_DISP_CFG_H */'
    print '\n'

    print footer
    f.close()

if __name__ == "__main__":
    CanMailbox_Cfg()
    can_cfg_gen()
    can_disp_par_c()
    disp_cfg_par_h()
    can_disp_cfg_h()

    
