#if !defined (CANMAILBOX_CFG_H)
#define CANMAILBOX_CFG_H



/* ===========================================================================

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
*H***********************************************************************/



/* ===========================================================================

 Name(s):         CANx_MBn

 Description:     Mailbox Direction, Transmit or Receive

 Templates:       #define CAN0_MB_0     CAN_FULLCAN_RX_MB
                  #define CAN0_MB_1     CAN_GENERALPURPOSE_TX_MB

 =========================================================================*/



#define    CAN0_MB_0     CAN_BASICCAN_PATTERNFILTER_RX_MB
#define    CAN0_MB_1     CAN_FULLCAN_RX_MB
#define    CAN0_MB_2     CAN_FULLCAN_RX_MB
#define    CAN0_MB_3     CAN_FULLCAN_RX_MB
#define    CAN0_MB_4     CAN_FULLCAN_RX_MB
#define    CAN0_MB_5     CAN_FULLCAN_RX_MB
#define    CAN0_MB_6     CAN_FULLCAN_RX_MB
#define    CAN0_MB_7     CAN_FULLCAN_RX_MB
#define    CAN0_MB_8     CAN_FULLCAN_RX_MB
#define    CAN0_MB_9     CAN_FULLCAN_RX_MB
#define    CAN0_MB_10    CAN_FULLCAN_RX_MB
#define    CAN0_MB_11    CAN_FULLCAN_RX_MB
#define    CAN0_MB_12    CAN_FULLCAN_RX_MB
#define    CAN0_MB_13    CAN_FULLCAN_RX_MB
#define    CAN0_MB_14    CAN_FULLCAN_RX_MB
#define    CAN0_MB_15    CAN_FULLCAN_RX_MB
#define    CAN0_MB_16    CAN_FULLCAN_RX_MB
#define    CAN0_MB_17    CAN_FULLCAN_RX_MB
#define    CAN0_MB_18    CAN_FULLCAN_RX_MB
#define    CAN0_MB_19    CAN_FULLCAN_RX_MB
#define    CAN0_MB_20    CAN_FULLCAN_RX_MB
#define    CAN0_MB_21    CAN_FULLCAN_RX_MB
#define    CAN0_MB_22    CAN_FULLCAN_RX_MB
#define    CAN0_MB_23    CAN_FULLCAN_RX_MB
#define    CAN0_MB_24    CAN_FULLCAN_RX_MB
#define    CAN0_MB_25    CAN_FULLCAN_RX_MB
#define    CAN0_MB_26    CAN_GENERALPURPOSE_TX_MB
#define    CAN0_MB_27    CAN_GENERALPURPOSE_TX_MB
#define    CAN0_MB_28    CAN_DEDICATED_TX_MB
#define    CAN0_MB_29    CAN_DEDICATED_TX_MB
#define    CAN0_MB_30    CAN_DEDICATED_TX_MB
#define    CAN0_MB_31    CAN_DEDICATED_TX_MB



/* ===========================================================================

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
    
/**CAN0 module filter mask configuration based on message ID*/


/**CAN0 module Accepted Identifier configuration*/


#define    CAN0_MSGBUF0_MASK_VAL     (CAN_UINT32)0xFFFFF800ul
#define    CAN0_MSGBUF1_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF2_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF3_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF4_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF5_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF6_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF7_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF8_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF9_MASK_VAL     (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF10_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF11_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF12_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF13_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF14_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF15_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF16_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF17_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF18_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF19_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF20_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF21_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF22_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF23_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF24_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF25_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF26_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF27_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF28_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF29_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF30_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul
#define    CAN0_MSGBUF31_MASK_VAL    (CAN_UINT32)0xFFFFFFFFul



#define    CAN0_MSGBUF0_FID     (0x0ul)
#define    CAN0_MSGBUF1_FID     (0x4a0ul)
#define    CAN0_MSGBUF2_FID     (0x511ul)
#define    CAN0_MSGBUF3_FID     (0x530ul)
#define    CAN0_MSGBUF4_FID     (0x560ul)
#define    CAN0_MSGBUF5_FID     (0x571ul)
#define    CAN0_MSGBUF6_FID     (0x580ul)
#define    CAN0_MSGBUF7_FID     (0x5c0ul)
#define    CAN0_MSGBUF8_FID     (0x630ul)
#define    CAN0_MSGBUF9_FID     (0x660ul)
#define    CAN0_MSGBUF10_FID    (0x120ul)
#define    CAN0_MSGBUF11_FID    (0x1a0ul)
#define    CAN0_MSGBUF12_FID    (0x280ul)
#define    CAN0_MSGBUF13_FID    (0x281ul)
#define    CAN0_MSGBUF14_FID    (0x318ul)
#define    CAN0_MSGBUF15_FID    (0x319ul)
#define    CAN0_MSGBUF16_FID    (0x322ul)
#define    CAN0_MSGBUF17_FID    (0x350ul)
#define    CAN0_MSGBUF18_FID    (0x370ul)
#define    CAN0_MSGBUF19_FID    (0x0ul)
#define    CAN0_MSGBUF20_FID    (0x0ul)
#define    CAN0_MSGBUF21_FID    (0x0ul)
#define    CAN0_MSGBUF22_FID    (0x0ul)
#define    CAN0_MSGBUF23_FID    (0x0ul)
#define    CAN0_MSGBUF24_FID    (0x0ul)
#define    CAN0_MSGBUF25_FID    (0x0ul)
#define    CAN0_MSGBUF26_FID    (0x0ul)
#define    CAN0_MSGBUF27_FID    (0x0ul)
#define    CAN0_MSGBUF28_FID    (0x6f1ul)
#define    CAN0_MSGBUF29_FID    (0x621ul)
#define    CAN0_MSGBUF30_FID    (0x620ul)
#define    CAN0_MSGBUF31_FID    (0x424ul)



/**********************************************************************************************
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
/** Number of HTH ch must be configured through the macro """CAN_CFG_NUMBER_OF_HTHS"""" **/


#define CAN_CFG_HTHS \
{\
/* Can_TxHandleMappingType */\
  /* The index of the controller where the HTH is allocated. */\
  /* VAR(Can_ControllerIdType, TYPEDEF) ControllerIndex, */\
  /* |    */\
  /* |    The index of the buffer in scope of the controller, */\
  /* |    where the HTH is allocated. */\
  /* |    0..CAN_GPTX_BUFFER_SELECT is a dedicated buffer, */\
  /* |    CAN_GPTX_BUFFER_SELECT is the FIFO. */\
  /* |    VAR(Can_ControllerTxHandleType, TYPEDEF) TxHandle */\
  /* |    |  */\
  /* V    V  */\
  { 0u, 31} , /* This allows mailbox 31s of controller 0 to be used as dedicated buffer for HTH:0*/\
  { 0u, 30} , /* This allows mailbox 30s of controller 0 to be used as dedicated buffer for HTH:1*/\
  { 0u, 29} , /* This allows mailbox 29s of controller 0 to be used as dedicated buffer for HTH:2*/\
  { 0u, 28} , /* This allows mailbox 28s of controller 0 to be used as dedicated buffer for HTH:3*/\
  { 0u, CAN_GPTX_BUFFER_SELECT}, /* Array index 0, TX FIFO */	/* HTH : 4*/\
}


/**********************************************************************************************
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
    
*/
#define CAN_CFG_HRHS \
{/** Array of Can_RxHandleMappingType */\
  /* The index of the controller where the HRH is allocated. */\
  /* VAR(Can_ControllerIdType, TYPEDEF) ControllerIndex, */\
  /* |    */\
  /* |    The index of the buffer in scope of the controller, */\
  /* |    where the HRH is allocated. */\
  /* |    0..CAN_CONTROLLER_RX_BUFFER_MAX is a dedicated buffer, */\
  /* |    CAN_CONTROLLER_RX_FIFO_0/CAN_CONTROLLER_RX_FIFO_1 is a */\
  /* |    respective FIFO. */\
  /* |    VAR(Can_ControllerRxHandleType, TYPEDEF) RxHandle */\
  /* |    |  */\
  /* V    V  */\
  { 0u,  0u }, /* Array index 0, dedicated RX buffer ("HRH = 0 is the Array index")*/\
  { 0u,  1u }, /* Array index 0, dedicated RX buffer ("HRH = 1 is the Array index")*/\
  { 0u,  2u }, /* Array index 0, dedicated RX buffer ("HRH = 2 is the Array index")*/\
  { 0u,  3u }, /* Array index 0, dedicated RX buffer ("HRH = 3 is the Array index")*/\
  { 0u,  4u }, /* Array index 0, dedicated RX buffer ("HRH = 4 is the Array index")*/\
  { 0u,  5u }, /* Array index 0, dedicated RX buffer ("HRH = 5 is the Array index")*/\
  { 0u,  6u }, /* Array index 0, dedicated RX buffer ("HRH = 6 is the Array index")*/\
  { 0u,  7u }, /* Array index 0, dedicated RX buffer ("HRH = 7 is the Array index")*/\
  { 0u,  8u }, /* Array index 0, dedicated RX buffer ("HRH = 8 is the Array index")*/\
  { 0u,  9u }, /* Array index 0, dedicated RX buffer ("HRH = 9 is the Array index")*/\
  { 0u,  10u }, /* Array index 0, dedicated RX buffer ("HRH = 10 is the Array index")*/\
  { 0u,  11u }, /* Array index 0, dedicated RX buffer ("HRH = 11 is the Array index")*/\
  { 0u,  12u }, /* Array index 0, dedicated RX buffer ("HRH = 12 is the Array index")*/\
  { 0u,  13u }, /* Array index 0, dedicated RX buffer ("HRH = 13 is the Array index")*/\
  { 0u,  14u }, /* Array index 0, dedicated RX buffer ("HRH = 14 is the Array index")*/\
  { 0u,  15u }, /* Array index 0, dedicated RX buffer ("HRH = 15 is the Array index")*/\
  { 0u,  16u }, /* Array index 0, dedicated RX buffer ("HRH = 16 is the Array index")*/\
  { 0u,  17u }, /* Array index 0, dedicated RX buffer ("HRH = 17 is the Array index")*/\
  { 0u,  18u }, /* Array index 0, dedicated RX buffer ("HRH = 18 is the Array index")*/\
}


/**********************************************************************************************
**********************************************************************************************/
#endif


/*****************************************************************************
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
*****************************************************************************/
