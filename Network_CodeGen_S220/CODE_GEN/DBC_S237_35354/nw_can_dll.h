#ifndef NW_CAN_DLL_H
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
 =========================================================================*/
/* ===========================================================================
  I N C L U D E   F I L E S
=== =========================================================================*/
#include "types.h"
#include "can_type.h"
#include "can_defs.h" 
#include "nw_il.h"
#include "nw_il_par.h"
#include "can_bcan.cfg"

/* ===========================================================================
  P U B L I C   T Y P E   D E F I N I T I O N S
 =========================================================================*/

#define DLL_NUM_RX_VECTORS         	(3)
#define DLL_NUM_IL_TX_FRAMES        (35)
#define DLL_NUM_NM_TX_FRAMES        (DLL_NUM_IL_TX_FRAMES)

/* ===========================================================================
**  Macros to Support Rx Qualification and Dispatch and Transmit Complete
**  Dispatch and Notification
** =========================================================================*/

#define DLL_RX_IL_FRAME            (0)
#define DLL_RX_DIAG_FRAME          (1)
#define DLL_RX_TP_FRAME            (2)
#define DLL_RX_NM_FRAME            (3)
#define DLL_RX_FRAME_INVALID       (4)
/* ===========================================================================
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
} DLL_RX_DISPATCH;
/* ===========================================================================
  CAN Hardware Receive Vector Qualification Data Structures

  This set of data structures defines the CAN Identifiers that are received
  by each CAN receive filter/mask combination (termed a receive "vector").
  A specific filter mask/combination may qualify multiple CAN Identifiers,
  so this table is needed to further qualify which CAN ID's that pass a
  specific filter/mask combination are valid and therefore stored in the
  software receive queue for further processing.

 =========================================================================*/

 /* CAN Hardware Receive Vector0*/
static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector0[ ] =
{
   {
       0x385,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ACC1_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x386,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ACC2_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x176,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_AMT5_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x177,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_AMT6_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3a0,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_APA2_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3a1,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_APA3_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3a2,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_APA4_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x296,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_APA_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3ed,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS10_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d2,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS11_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d5,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS14_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x11d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS16_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3ea,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS17_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x150,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS18_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x12d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x12b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS22_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x272,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS2_30_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3e9,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS3_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3e8,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS4_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3e7,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS5_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x339,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS6_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d4,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS7_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x151,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS8_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d3,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS9_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3f6,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS_CLT_HTR1_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3f7,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS_CLT_HTR2_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3f8,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS_CLT_HTR3_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x158,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         6u,
       #endif
       VNIM_BMS_IVT_MSG_RESULT_U1_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x159,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         6u,
       #endif
       VNIM_BMS_IVT_MSG_RESULT_U2_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x160,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         6u,
       #endif
       VNIM_BMS_IVT_MSG_RESULT_U3_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c3,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_BMS_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x302,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_CCM1_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x420,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_CCM3_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x310,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS12_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x312,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS13_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x132,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS14_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x124,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x127,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS21_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x233,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS29_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x125,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS2_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x103,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS30_SP_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x142,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS36_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x585,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS37_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x62d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS38_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x62e,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS39_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x108,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS3_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x62f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS41_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x630,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS42_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x63a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS43_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x63b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS44_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x63c,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS45_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x130,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS4_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x308,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS6_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x126,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS8_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x301,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS9_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x285,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EMS_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x221,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EPS1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x28f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_EPS_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x171,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC10_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x282,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC12_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x33a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC13_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x580,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC14_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x594,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC15_1000_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x2cc,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC2_10_MESSAGE,
       DLL_RX_IL_FRAME
   }
};


 /* CAN Hardware Receive Vector1*/
static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector1[ ] =
{
   {
       0x138,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC3_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x10d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC5_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x170,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC7_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x10f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC8_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x34b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESCL1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d0,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESCL_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x289,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESC_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x242,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ETL1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c5,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ETL_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x300,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FATC1_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x303,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FATC2_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x24d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FCM1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x396,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FCM_HBA_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x22c,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FCM_LKAS1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x299,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FCM_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x57f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FCM_TSR_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x24b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FRM1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x24c,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FRM2_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x30b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FRM3_TEST_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x29a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FRM_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x395,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FVC1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x675,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_GW1_1000_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x283,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_GW_HEARTBEAT_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x398,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_HLCU1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x399,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_HLCU2_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x631,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ICC1_1000_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x2ff,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ICC2_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3dd,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_LDC1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x244,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_LDC2_30_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3df,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_LDC3_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x274,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_LDC4_30_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c6,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_LDC_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x351,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM10_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x33c,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM14_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x491,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM16_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x492,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM17_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x348,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x214,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM5_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x218,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM6_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x21c,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM7_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x21f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM9_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x28a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x326,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM_PAS1_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d6,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MCU1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x118,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MCU2_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x11b,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MCU3_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d7,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MCU5_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c7,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MCU_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3da,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x428,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC2_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3d8,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC3_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x245,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC4_30_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3dc,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC6_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c8,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_OBC_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x353,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x440,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE2_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x342,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_ICU2_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x287,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_ICU_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x10a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_MCM_SP_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x365,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_TEST5_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x217,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_RVC1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x114,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         5u,
       #endif
       VNIM_SAS1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x478,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SBRM1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x250,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SBW1_10_MESSAGE,
       DLL_RX_IL_FRAME
   }
};


 /* CAN Hardware Receive Vector2*/
static DLL_RX_VECTOR_DISPATCH const dllhscanRxIdsVector2[ ] =
{
   {
       0x632,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SCM1_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x2c0,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SRS1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x39a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SVS1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x286,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_SYNC_MSG_SP_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x110,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TC1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x136,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TCU5_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x278,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TCU6_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x295,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TC_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x219,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TPMS1_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x21e,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TPMS2_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x21d,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_TPMS3_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x30a,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU10_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x6c3,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU11_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x2e7,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU11_50_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3ee,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU12_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3f4,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU13_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x259,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU14_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3ef,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU15_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x6c8,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU16_1000_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x590,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU16_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x490,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU17_200_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x1b5,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU18_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x337,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU1_20_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x338,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU2_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x336,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU3_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x241,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU4_20_EV_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x335,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU5_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x3c0,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU5_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x333,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU7_100_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x112,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU8_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x1bb,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU_FC1_10_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x5c9,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU_STS_500_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x6af,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_WLC3_2000_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x329,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_WLC_NSM_MESSAGE,
       DLL_RX_IL_FRAME
   },
   {
       0x750,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_IS_DIAG_REQ_MESSAGE,
       DLL_RX_TP_FRAME
   },
   {
       0x3ac,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_CCM_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3be,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ESCL_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3ba,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_FATC_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3b6,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_HLCU1_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3b5,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ICC_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3c2,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ICC_SLEEP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x9e,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_ICC_WAKEUP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3c1,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3c4,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM_SLEEP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x97,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_MBFM_WAKEUP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3c3,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3c6,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_SLEEP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x96,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_PKE_WAKEUP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3af,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3ae,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU_SLEEP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x9f,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_VCU_WAKEUP_MESSAGE,
       DLL_RX_NM_FRAME
   },
   {
       0x3bc,
       #if (CAN_DLC_CHECK_ENABLE != CAN_DISABLE)
         8u,
       #endif
       VNIM_WLC_ACTIVE_MESSAGE,
       DLL_RX_NM_FRAME
   }
};

#define DLL_CAN_RX_VECTOR_0_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector0)/sizeof(DLL_RX_VECTOR_DISPATCH)))
#define DLL_CAN_RX_VECTOR_1_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector1)/sizeof(DLL_RX_VECTOR_DISPATCH)))
#define DLL_CAN_RX_VECTOR_2_NUM_RX_IDS ((CAN_UINT8)(sizeof(dllhscanRxIdsVector2)/sizeof(DLL_RX_VECTOR_DISPATCH)))
/* ===========================================================================
  Received Frame Dispatch Table

  This data structure is an array of pointers to the data structures that
  define the received CAN ID's that are to be qualified for each hardware
  receive vector. A hardware receive vector corresponds to a CAN filter/mask
  combination that qualifies received CAN messages that may need to be
  further filtered at the software level.

 =========================================================================*/
static DLL_RX_DISPATCH const dllRxDispatchTable[ DLL_NUM_RX_VECTORS ] =
{
   { DLL_CAN_RX_VECTOR_0_NUM_RX_IDS, &dllhscanRxIdsVector0[ 0 ] },
   { DLL_CAN_RX_VECTOR_1_NUM_RX_IDS, &dllhscanRxIdsVector1[ 0 ] },
   { DLL_CAN_RX_VECTOR_2_NUM_RX_IDS, &dllhscanRxIdsVector2[ 0 ] },
};

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
Date                : 2023-11-06 17:58
By                  : VENKI
Traceability        : S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev35354_180923_Edited.dbc
Change Description  : Tool Generated code
*****************************************************************************/
