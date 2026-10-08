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

/* ===========================================================================
 
   Name:           nw_nm_par.h
 
   Description:    Indirect NM Implementation
 
   Organization:   Multiplex Core Technology
 
  =========================================================================*/
#ifndef NW_NM_PAR_H
#define NW_NM_PAR_H

#include"nw_nm_wake.h"
#include"nw_can_dll.h"


#define NM_IS_ACTIVE_TMH  3   /* 0-2 is for TP, 3 is for NM */
#define NM_TX_MSG_DATA_STRUCT                            \
{                                                                                  \
   CAN_GPNUM_8,                                 /* CAN message data length  */     \
   0x234,                                       /* CAN message identifier   */     \
   &Nm_msg_buffer[0],                           /* Pointer to Data          */      \
   CANB_TX_STD_DATA,                            /* CAN message options      */      \
   (DLL_NUM_IL_TX_FRAMES+1)                               /* Transmit Message Handle  */        \
}
typedef enum
{
   NM_ACC_NODE,
   NM_AMT_NODE,
   NM_APA_NODE,
   NM_BMS_NODE,
   NM_CCM_NODE,
   NM_EMS_NODE,
   NM_EPS_NODE,
   NM_ESC_NODE,
   NM_ESCL_NODE,
   NM_ETL_NODE,
   NM_FATC_NODE,
   NM_FCM_NODE,
   NM_FRM_NODE,
   NM_FVC_NODE,
   NM_GW_NODE,
   NM_HLCU_NODE,
   NM_ICC_NODE,
   NM_LDC_NODE,
   NM_MBFM_NODE,
   NM_MCU_NODE,
   NM_OBC_NODE,
   NM_PKE_NODE,
   NM_RVC_NODE,
   NM_SAS_NODE,
   NM_SBRM_NODE,
   NM_SBW_NODE,
   NM_SCM_NODE,
   NM_SRS_NODE,
   NM_SVS_NODE,
   NM_TC_NODE,
   NM_TCU_NODE,
   NM_WLC_NODE,
   NM_NUMBER_OF_NODES
}NM_NODE_LIST;

#define NM_NM_NODES_BIT_MASK        \
   0x1,   /*NM_ACC_NODE*/    \
   0x2,   /*NM_AMT_NODE*/    \
   0x4,   /*NM_APA_NODE*/    \
   0x8,   /*NM_BMS_NODE*/    \
   0x10,   /*NM_CCM_NODE*/    \
   0x20,   /*NM_EMS_NODE*/    \
   0x40,   /*NM_EPS_NODE*/    \
   0x80,   /*NM_ESC_NODE*/    \
   0x1,   /*NM_ESCL_NODE*/    \
   0x2,   /*NM_ETL_NODE*/    \
   0x4,   /*NM_FATC_NODE*/    \
   0x8,   /*NM_FCM_NODE*/    \
   0x10,   /*NM_FRM_NODE*/    \
   0x20,   /*NM_FVC_NODE*/    \
   0x40,   /*NM_GW_NODE*/    \
   0x80,   /*NM_HLCU_NODE*/    \
   0x1,   /*NM_ICC_NODE*/    \
   0x2,   /*NM_LDC_NODE*/    \
   0x4,   /*NM_MBFM_NODE*/    \
   0x8,   /*NM_MCU_NODE*/    \
   0x10,   /*NM_OBC_NODE*/    \
   0x20,   /*NM_PKE_NODE*/    \
   0x40,   /*NM_RVC_NODE*/    \
   0x80,   /*NM_SAS_NODE*/    \
   0x1,   /*NM_SBRM_NODE*/    \
   0x2,   /*NM_SBW_NODE*/    \
   0x4,   /*NM_SCM_NODE*/    \
   0x8,   /*NM_SRS_NODE*/    \
   0x10,   /*NM_SVS_NODE*/    \
   0x20,   /*NM_TC_NODE*/    \
   0x40,   /*NM_TCU_NODE*/    \
   0x80   /*NM_WLC_NODE*/


#define NM_NM_NODES_BYTE_OFFSET             \
   0x0,   /*NM_ACC_NODE*/   \
   0x0,   /*NM_AMT_NODE*/   \
   0x0,   /*NM_APA_NODE*/   \
   0x0,   /*NM_BMS_NODE*/   \
   0x0,   /*NM_CCM_NODE*/   \
   0x0,   /*NM_EMS_NODE*/   \
   0x0,   /*NM_EPS_NODE*/   \
   0x0,   /*NM_ESC_NODE*/   \
   0x1,   /*NM_ESCL_NODE*/   \
   0x1,   /*NM_ETL_NODE*/   \
   0x1,   /*NM_FATC_NODE*/   \
   0x1,   /*NM_FCM_NODE*/   \
   0x1,   /*NM_FRM_NODE*/   \
   0x1,   /*NM_FVC_NODE*/   \
   0x1,   /*NM_GW_NODE*/   \
   0x1,   /*NM_HLCU_NODE*/   \
   0x2,   /*NM_ICC_NODE*/   \
   0x2,   /*NM_LDC_NODE*/   \
   0x2,   /*NM_MBFM_NODE*/   \
   0x2,   /*NM_MCU_NODE*/   \
   0x2,   /*NM_OBC_NODE*/   \
   0x2,   /*NM_PKE_NODE*/   \
   0x2,   /*NM_RVC_NODE*/   \
   0x2,   /*NM_SAS_NODE*/   \
   0x3,   /*NM_SBRM_NODE*/   \
   0x3,   /*NM_SBW_NODE*/   \
   0x3,   /*NM_SCM_NODE*/   \
   0x3,   /*NM_SRS_NODE*/   \
   0x3,   /*NM_SVS_NODE*/   \
   0x3,   /*NM_TC_NODE*/   \
   0x3,   /*NM_TCU_NODE*/   \
   0x3   /*NM_WLC_NODE*/


/*Node Missing Macro*/
/*NM_ACC_NODE*/
#define IS_ACC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ACC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_ACC_NODE])) == (nw_nm_bit_mask[NM_ACC_NODE]))

#define NM_ACC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ACC_NODE]] |= \
                                    nw_nm_bit_mask[NM_ACC_NODE])

#define NM_ACC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ACC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_ACC_NODE]))


/*NM_AMT_NODE*/
#define IS_AMT_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_AMT_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_AMT_NODE])) == (nw_nm_bit_mask[NM_AMT_NODE]))

#define NM_AMT_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_AMT_NODE]] |= \
                                    nw_nm_bit_mask[NM_AMT_NODE])

#define NM_AMT_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_AMT_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_AMT_NODE]))


/*NM_APA_NODE*/
#define IS_APA_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_APA_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_APA_NODE])) == (nw_nm_bit_mask[NM_APA_NODE]))

#define NM_APA_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_APA_NODE]] |= \
                                    nw_nm_bit_mask[NM_APA_NODE])

#define NM_APA_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_APA_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_APA_NODE]))


/*NM_BMS_NODE*/
#define IS_BMS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_BMS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_BMS_NODE])) == (nw_nm_bit_mask[NM_BMS_NODE]))

#define NM_BMS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_BMS_NODE]] |= \
                                    nw_nm_bit_mask[NM_BMS_NODE])

#define NM_BMS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_BMS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_BMS_NODE]))


/*NM_CCM_NODE*/
#define IS_CCM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_CCM_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_CCM_NODE])) == (nw_nm_bit_mask[NM_CCM_NODE]))

#define NM_CCM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_CCM_NODE]] |= \
                                    nw_nm_bit_mask[NM_CCM_NODE])

#define NM_CCM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_CCM_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_CCM_NODE]))


/*NM_EMS_NODE*/
#define IS_EMS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EMS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_EMS_NODE])) == (nw_nm_bit_mask[NM_EMS_NODE]))

#define NM_EMS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EMS_NODE]] |= \
                                    nw_nm_bit_mask[NM_EMS_NODE])

#define NM_EMS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EMS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_EMS_NODE]))


/*NM_EPS_NODE*/
#define IS_EPS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EPS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_EPS_NODE])) == (nw_nm_bit_mask[NM_EPS_NODE]))

#define NM_EPS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EPS_NODE]] |= \
                                    nw_nm_bit_mask[NM_EPS_NODE])

#define NM_EPS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_EPS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_EPS_NODE]))


/*NM_ESC_NODE*/
#define IS_ESC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_ESC_NODE])) == (nw_nm_bit_mask[NM_ESC_NODE]))

#define NM_ESC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESC_NODE]] |= \
                                    nw_nm_bit_mask[NM_ESC_NODE])

#define NM_ESC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_ESC_NODE]))


/*NM_ESCL_NODE*/
#define IS_ESCL_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESCL_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_ESCL_NODE])) == (nw_nm_bit_mask[NM_ESCL_NODE]))

#define NM_ESCL_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESCL_NODE]] |= \
                                     nw_nm_bit_mask[NM_ESCL_NODE])

#define NM_ESCL_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ESCL_NODE]] &= \
                                  (CAN_UINT8) ~(nw_nm_bit_mask[NM_ESCL_NODE]))


/*NM_ETL_NODE*/
#define IS_ETL_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ETL_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_ETL_NODE])) == (nw_nm_bit_mask[NM_ETL_NODE]))

#define NM_ETL_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ETL_NODE]] |= \
                                    nw_nm_bit_mask[NM_ETL_NODE])

#define NM_ETL_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ETL_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_ETL_NODE]))


/*NM_FATC_NODE*/
#define IS_FATC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FATC_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_FATC_NODE])) == (nw_nm_bit_mask[NM_FATC_NODE]))

#define NM_FATC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FATC_NODE]] |= \
                                     nw_nm_bit_mask[NM_FATC_NODE])

#define NM_FATC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FATC_NODE]] &= \
                                  (CAN_UINT8) ~(nw_nm_bit_mask[NM_FATC_NODE]))


/*NM_FCM_NODE*/
#define IS_FCM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FCM_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_FCM_NODE])) == (nw_nm_bit_mask[NM_FCM_NODE]))

#define NM_FCM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FCM_NODE]] |= \
                                    nw_nm_bit_mask[NM_FCM_NODE])

#define NM_FCM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FCM_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_FCM_NODE]))


/*NM_FRM_NODE*/
#define IS_FRM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FRM_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_FRM_NODE])) == (nw_nm_bit_mask[NM_FRM_NODE]))

#define NM_FRM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FRM_NODE]] |= \
                                    nw_nm_bit_mask[NM_FRM_NODE])

#define NM_FRM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FRM_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_FRM_NODE]))


/*NM_FVC_NODE*/
#define IS_FVC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FVC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_FVC_NODE])) == (nw_nm_bit_mask[NM_FVC_NODE]))

#define NM_FVC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FVC_NODE]] |= \
                                    nw_nm_bit_mask[NM_FVC_NODE])

#define NM_FVC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_FVC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_FVC_NODE]))


/*NM_GW_NODE*/
#define IS_GW_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_GW_NODE]]) & \
                                                (nw_nm_bit_mask[NM_GW_NODE])) == (nw_nm_bit_mask[NM_GW_NODE]))

#define NM_GW_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_GW_NODE]] |= \
                                   nw_nm_bit_mask[NM_GW_NODE])

#define NM_GW_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_GW_NODE]] &= \
                                (CAN_UINT8) ~(nw_nm_bit_mask[NM_GW_NODE]))


/*NM_HLCU_NODE*/
#define IS_HLCU_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_HLCU_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_HLCU_NODE])) == (nw_nm_bit_mask[NM_HLCU_NODE]))

#define NM_HLCU_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_HLCU_NODE]] |= \
                                     nw_nm_bit_mask[NM_HLCU_NODE])

#define NM_HLCU_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_HLCU_NODE]] &= \
                                  (CAN_UINT8) ~(nw_nm_bit_mask[NM_HLCU_NODE]))


/*NM_ICC_NODE*/
#define IS_ICC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ICC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_ICC_NODE])) == (nw_nm_bit_mask[NM_ICC_NODE]))

#define NM_ICC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ICC_NODE]] |= \
                                    nw_nm_bit_mask[NM_ICC_NODE])

#define NM_ICC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_ICC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_ICC_NODE]))


/*NM_LDC_NODE*/
#define IS_LDC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_LDC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_LDC_NODE])) == (nw_nm_bit_mask[NM_LDC_NODE]))

#define NM_LDC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_LDC_NODE]] |= \
                                    nw_nm_bit_mask[NM_LDC_NODE])

#define NM_LDC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_LDC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_LDC_NODE]))


/*NM_MBFM_NODE*/
#define IS_MBFM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MBFM_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_MBFM_NODE])) == (nw_nm_bit_mask[NM_MBFM_NODE]))

#define NM_MBFM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MBFM_NODE]] |= \
                                     nw_nm_bit_mask[NM_MBFM_NODE])

#define NM_MBFM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MBFM_NODE]] &= \
                                  (CAN_UINT8) ~(nw_nm_bit_mask[NM_MBFM_NODE]))


/*NM_MCU_NODE*/
#define IS_MCU_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MCU_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_MCU_NODE])) == (nw_nm_bit_mask[NM_MCU_NODE]))

#define NM_MCU_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MCU_NODE]] |= \
                                    nw_nm_bit_mask[NM_MCU_NODE])

#define NM_MCU_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_MCU_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_MCU_NODE]))


/*NM_OBC_NODE*/
#define IS_OBC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_OBC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_OBC_NODE])) == (nw_nm_bit_mask[NM_OBC_NODE]))

#define NM_OBC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_OBC_NODE]] |= \
                                    nw_nm_bit_mask[NM_OBC_NODE])

#define NM_OBC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_OBC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_OBC_NODE]))


/*NM_PKE_NODE*/
#define IS_PKE_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_PKE_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_PKE_NODE])) == (nw_nm_bit_mask[NM_PKE_NODE]))

#define NM_PKE_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_PKE_NODE]] |= \
                                    nw_nm_bit_mask[NM_PKE_NODE])

#define NM_PKE_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_PKE_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_PKE_NODE]))


/*NM_RVC_NODE*/
#define IS_RVC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_RVC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_RVC_NODE])) == (nw_nm_bit_mask[NM_RVC_NODE]))

#define NM_RVC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_RVC_NODE]] |= \
                                    nw_nm_bit_mask[NM_RVC_NODE])

#define NM_RVC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_RVC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_RVC_NODE]))


/*NM_SAS_NODE*/
#define IS_SAS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SAS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_SAS_NODE])) == (nw_nm_bit_mask[NM_SAS_NODE]))

#define NM_SAS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SAS_NODE]] |= \
                                    nw_nm_bit_mask[NM_SAS_NODE])

#define NM_SAS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SAS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_SAS_NODE]))


/*NM_SBRM_NODE*/
#define IS_SBRM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBRM_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_SBRM_NODE])) == (nw_nm_bit_mask[NM_SBRM_NODE]))

#define NM_SBRM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBRM_NODE]] |= \
                                     nw_nm_bit_mask[NM_SBRM_NODE])

#define NM_SBRM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBRM_NODE]] &= \
                                  (CAN_UINT8) ~(nw_nm_bit_mask[NM_SBRM_NODE]))


/*NM_SBW_NODE*/
#define IS_SBW_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBW_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_SBW_NODE])) == (nw_nm_bit_mask[NM_SBW_NODE]))

#define NM_SBW_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBW_NODE]] |= \
                                    nw_nm_bit_mask[NM_SBW_NODE])

#define NM_SBW_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SBW_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_SBW_NODE]))


/*NM_SCM_NODE*/
#define IS_SCM_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SCM_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_SCM_NODE])) == (nw_nm_bit_mask[NM_SCM_NODE]))

#define NM_SCM_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SCM_NODE]] |= \
                                    nw_nm_bit_mask[NM_SCM_NODE])

#define NM_SCM_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SCM_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_SCM_NODE]))


/*NM_SRS_NODE*/
#define IS_SRS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SRS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_SRS_NODE])) == (nw_nm_bit_mask[NM_SRS_NODE]))

#define NM_SRS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SRS_NODE]] |= \
                                    nw_nm_bit_mask[NM_SRS_NODE])

#define NM_SRS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SRS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_SRS_NODE]))


/*NM_SVS_NODE*/
#define IS_SVS_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SVS_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_SVS_NODE])) == (nw_nm_bit_mask[NM_SVS_NODE]))

#define NM_SVS_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SVS_NODE]] |= \
                                    nw_nm_bit_mask[NM_SVS_NODE])

#define NM_SVS_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_SVS_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_SVS_NODE]))


/*NM_TC_NODE*/
#define IS_TC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TC_NODE]]) & \
                                                (nw_nm_bit_mask[NM_TC_NODE])) == (nw_nm_bit_mask[NM_TC_NODE]))

#define NM_TC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TC_NODE]] |= \
                                   nw_nm_bit_mask[NM_TC_NODE])

#define NM_TC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TC_NODE]] &= \
                                (CAN_UINT8) ~(nw_nm_bit_mask[NM_TC_NODE]))


/*NM_TCU_NODE*/
#define IS_TCU_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TCU_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_TCU_NODE])) == (nw_nm_bit_mask[NM_TCU_NODE]))

#define NM_TCU_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TCU_NODE]] |= \
                                    nw_nm_bit_mask[NM_TCU_NODE])

#define NM_TCU_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_TCU_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_TCU_NODE]))


/*NM_WLC_NODE*/
#define IS_WLC_NODE_MISSING()      (CAN_UINT8)(((nw_nm_node_missing_sts[nw_nm_byte_offset[NM_WLC_NODE]]) & \
                                                 (nw_nm_bit_mask[NM_WLC_NODE])) == (nw_nm_bit_mask[NM_WLC_NODE]))

#define NM_WLC_NODE_MISSING()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_WLC_NODE]] |= \
                                    nw_nm_bit_mask[NM_WLC_NODE])

#define NM_WLC_NODE_GAIN()      (nw_nm_node_missing_sts[nw_nm_byte_offset[NM_WLC_NODE]] &= \
                                 (CAN_UINT8) ~(nw_nm_bit_mask[NM_WLC_NODE]))


/*Node DLC Fault Macro*/
/*NM_ACC_NODE*/
#define IS_ACC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ACC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_ACC_NODE])) == (nw_nm_bit_mask[NM_ACC_NODE]))

#define NM_ACC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ACC_NODE]] |= \
                                       nw_nm_bit_mask[NM_ACC_NODE])

#define NM_ACC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ACC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_ACC_NODE]))


/*NM_AMT_NODE*/
#define IS_AMT_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_AMT_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_AMT_NODE])) == (nw_nm_bit_mask[NM_AMT_NODE]))

#define NM_AMT_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_AMT_NODE]] |= \
                                       nw_nm_bit_mask[NM_AMT_NODE])

#define NM_AMT_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_AMT_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_AMT_NODE]))


/*NM_APA_NODE*/
#define IS_APA_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_APA_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_APA_NODE])) == (nw_nm_bit_mask[NM_APA_NODE]))

#define NM_APA_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_APA_NODE]] |= \
                                       nw_nm_bit_mask[NM_APA_NODE])

#define NM_APA_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_APA_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_APA_NODE]))


/*NM_BMS_NODE*/
#define IS_BMS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_BMS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_BMS_NODE])) == (nw_nm_bit_mask[NM_BMS_NODE]))

#define NM_BMS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_BMS_NODE]] |= \
                                       nw_nm_bit_mask[NM_BMS_NODE])

#define NM_BMS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_BMS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_BMS_NODE]))


/*NM_CCM_NODE*/
#define IS_CCM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_CCM_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_CCM_NODE])) == (nw_nm_bit_mask[NM_CCM_NODE]))

#define NM_CCM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_CCM_NODE]] |= \
                                       nw_nm_bit_mask[NM_CCM_NODE])

#define NM_CCM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_CCM_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_CCM_NODE]))


/*NM_EMS_NODE*/
#define IS_EMS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EMS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_EMS_NODE])) == (nw_nm_bit_mask[NM_EMS_NODE]))

#define NM_EMS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EMS_NODE]] |= \
                                       nw_nm_bit_mask[NM_EMS_NODE])

#define NM_EMS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EMS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_EMS_NODE]))


/*NM_EPS_NODE*/
#define IS_EPS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EPS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_EPS_NODE])) == (nw_nm_bit_mask[NM_EPS_NODE]))

#define NM_EPS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EPS_NODE]] |= \
                                       nw_nm_bit_mask[NM_EPS_NODE])

#define NM_EPS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_EPS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_EPS_NODE]))


/*NM_ESC_NODE*/
#define IS_ESC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_ESC_NODE])) == (nw_nm_bit_mask[NM_ESC_NODE]))

#define NM_ESC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESC_NODE]] |= \
                                       nw_nm_bit_mask[NM_ESC_NODE])

#define NM_ESC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_ESC_NODE]))


/*NM_ESCL_NODE*/
#define IS_ESCL_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESCL_NODE]]) & \
                                                    (nw_nm_bit_mask[NM_ESCL_NODE])) == (nw_nm_bit_mask[NM_ESCL_NODE]))

#define NM_ESCL_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESCL_NODE]] |= \
                                        nw_nm_bit_mask[NM_ESCL_NODE])

#define NM_ESCL_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ESCL_NODE]] &= \
                                       (CAN_UINT8) ~(nw_nm_bit_mask[NM_ESCL_NODE]))


/*NM_ETL_NODE*/
#define IS_ETL_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ETL_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_ETL_NODE])) == (nw_nm_bit_mask[NM_ETL_NODE]))

#define NM_ETL_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ETL_NODE]] |= \
                                       nw_nm_bit_mask[NM_ETL_NODE])

#define NM_ETL_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ETL_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_ETL_NODE]))


/*NM_FATC_NODE*/
#define IS_FATC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FATC_NODE]]) & \
                                                    (nw_nm_bit_mask[NM_FATC_NODE])) == (nw_nm_bit_mask[NM_FATC_NODE]))

#define NM_FATC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FATC_NODE]] |= \
                                        nw_nm_bit_mask[NM_FATC_NODE])

#define NM_FATC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FATC_NODE]] &= \
                                       (CAN_UINT8) ~(nw_nm_bit_mask[NM_FATC_NODE]))


/*NM_FCM_NODE*/
#define IS_FCM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FCM_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_FCM_NODE])) == (nw_nm_bit_mask[NM_FCM_NODE]))

#define NM_FCM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FCM_NODE]] |= \
                                       nw_nm_bit_mask[NM_FCM_NODE])

#define NM_FCM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FCM_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_FCM_NODE]))


/*NM_FRM_NODE*/
#define IS_FRM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FRM_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_FRM_NODE])) == (nw_nm_bit_mask[NM_FRM_NODE]))

#define NM_FRM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FRM_NODE]] |= \
                                       nw_nm_bit_mask[NM_FRM_NODE])

#define NM_FRM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FRM_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_FRM_NODE]))


/*NM_FVC_NODE*/
#define IS_FVC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FVC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_FVC_NODE])) == (nw_nm_bit_mask[NM_FVC_NODE]))

#define NM_FVC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FVC_NODE]] |= \
                                       nw_nm_bit_mask[NM_FVC_NODE])

#define NM_FVC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_FVC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_FVC_NODE]))


/*NM_GW_NODE*/
#define IS_GW_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_GW_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_GW_NODE])) == (nw_nm_bit_mask[NM_GW_NODE]))

#define NM_GW_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_GW_NODE]] |= \
                                      nw_nm_bit_mask[NM_GW_NODE])

#define NM_GW_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_GW_NODE]] &= \
                                     (CAN_UINT8) ~(nw_nm_bit_mask[NM_GW_NODE]))


/*NM_HLCU_NODE*/
#define IS_HLCU_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_HLCU_NODE]]) & \
                                                    (nw_nm_bit_mask[NM_HLCU_NODE])) == (nw_nm_bit_mask[NM_HLCU_NODE]))

#define NM_HLCU_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_HLCU_NODE]] |= \
                                        nw_nm_bit_mask[NM_HLCU_NODE])

#define NM_HLCU_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_HLCU_NODE]] &= \
                                       (CAN_UINT8) ~(nw_nm_bit_mask[NM_HLCU_NODE]))


/*NM_ICC_NODE*/
#define IS_ICC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ICC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_ICC_NODE])) == (nw_nm_bit_mask[NM_ICC_NODE]))

#define NM_ICC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ICC_NODE]] |= \
                                       nw_nm_bit_mask[NM_ICC_NODE])

#define NM_ICC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_ICC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_ICC_NODE]))


/*NM_LDC_NODE*/
#define IS_LDC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_LDC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_LDC_NODE])) == (nw_nm_bit_mask[NM_LDC_NODE]))

#define NM_LDC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_LDC_NODE]] |= \
                                       nw_nm_bit_mask[NM_LDC_NODE])

#define NM_LDC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_LDC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_LDC_NODE]))


/*NM_MBFM_NODE*/
#define IS_MBFM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MBFM_NODE]]) & \
                                                    (nw_nm_bit_mask[NM_MBFM_NODE])) == (nw_nm_bit_mask[NM_MBFM_NODE]))

#define NM_MBFM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MBFM_NODE]] |= \
                                        nw_nm_bit_mask[NM_MBFM_NODE])

#define NM_MBFM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MBFM_NODE]] &= \
                                       (CAN_UINT8) ~(nw_nm_bit_mask[NM_MBFM_NODE]))


/*NM_MCU_NODE*/
#define IS_MCU_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MCU_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_MCU_NODE])) == (nw_nm_bit_mask[NM_MCU_NODE]))

#define NM_MCU_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MCU_NODE]] |= \
                                       nw_nm_bit_mask[NM_MCU_NODE])

#define NM_MCU_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_MCU_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_MCU_NODE]))


/*NM_OBC_NODE*/
#define IS_OBC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_OBC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_OBC_NODE])) == (nw_nm_bit_mask[NM_OBC_NODE]))

#define NM_OBC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_OBC_NODE]] |= \
                                       nw_nm_bit_mask[NM_OBC_NODE])

#define NM_OBC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_OBC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_OBC_NODE]))


/*NM_PKE_NODE*/
#define IS_PKE_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_PKE_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_PKE_NODE])) == (nw_nm_bit_mask[NM_PKE_NODE]))

#define NM_PKE_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_PKE_NODE]] |= \
                                       nw_nm_bit_mask[NM_PKE_NODE])

#define NM_PKE_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_PKE_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_PKE_NODE]))


/*NM_RVC_NODE*/
#define IS_RVC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_RVC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_RVC_NODE])) == (nw_nm_bit_mask[NM_RVC_NODE]))

#define NM_RVC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_RVC_NODE]] |= \
                                       nw_nm_bit_mask[NM_RVC_NODE])

#define NM_RVC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_RVC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_RVC_NODE]))


/*NM_SAS_NODE*/
#define IS_SAS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SAS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_SAS_NODE])) == (nw_nm_bit_mask[NM_SAS_NODE]))

#define NM_SAS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SAS_NODE]] |= \
                                       nw_nm_bit_mask[NM_SAS_NODE])

#define NM_SAS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SAS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_SAS_NODE]))


/*NM_SBRM_NODE*/
#define IS_SBRM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBRM_NODE]]) & \
                                                    (nw_nm_bit_mask[NM_SBRM_NODE])) == (nw_nm_bit_mask[NM_SBRM_NODE]))

#define NM_SBRM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBRM_NODE]] |= \
                                        nw_nm_bit_mask[NM_SBRM_NODE])

#define NM_SBRM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBRM_NODE]] &= \
                                       (CAN_UINT8) ~(nw_nm_bit_mask[NM_SBRM_NODE]))


/*NM_SBW_NODE*/
#define IS_SBW_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBW_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_SBW_NODE])) == (nw_nm_bit_mask[NM_SBW_NODE]))

#define NM_SBW_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBW_NODE]] |= \
                                       nw_nm_bit_mask[NM_SBW_NODE])

#define NM_SBW_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SBW_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_SBW_NODE]))


/*NM_SCM_NODE*/
#define IS_SCM_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SCM_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_SCM_NODE])) == (nw_nm_bit_mask[NM_SCM_NODE]))

#define NM_SCM_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SCM_NODE]] |= \
                                       nw_nm_bit_mask[NM_SCM_NODE])

#define NM_SCM_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SCM_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_SCM_NODE]))


/*NM_SRS_NODE*/
#define IS_SRS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SRS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_SRS_NODE])) == (nw_nm_bit_mask[NM_SRS_NODE]))

#define NM_SRS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SRS_NODE]] |= \
                                       nw_nm_bit_mask[NM_SRS_NODE])

#define NM_SRS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SRS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_SRS_NODE]))


/*NM_SVS_NODE*/
#define IS_SVS_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SVS_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_SVS_NODE])) == (nw_nm_bit_mask[NM_SVS_NODE]))

#define NM_SVS_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SVS_NODE]] |= \
                                       nw_nm_bit_mask[NM_SVS_NODE])

#define NM_SVS_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_SVS_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_SVS_NODE]))


/*NM_TC_NODE*/
#define IS_TC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TC_NODE]]) & \
                                                  (nw_nm_bit_mask[NM_TC_NODE])) == (nw_nm_bit_mask[NM_TC_NODE]))

#define NM_TC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TC_NODE]] |= \
                                      nw_nm_bit_mask[NM_TC_NODE])

#define NM_TC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TC_NODE]] &= \
                                     (CAN_UINT8) ~(nw_nm_bit_mask[NM_TC_NODE]))


/*NM_TCU_NODE*/
#define IS_TCU_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TCU_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_TCU_NODE])) == (nw_nm_bit_mask[NM_TCU_NODE]))

#define NM_TCU_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TCU_NODE]] |= \
                                       nw_nm_bit_mask[NM_TCU_NODE])

#define NM_TCU_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_TCU_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_TCU_NODE]))


/*NM_WLC_NODE*/
#define IS_WLC_NODE_DLC_INVALID()     (CAN_UINT8)(((nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_WLC_NODE]]) & \
                                                   (nw_nm_bit_mask[NM_WLC_NODE])) == (nw_nm_bit_mask[NM_WLC_NODE]))

#define NM_WLC_NODE_DLC_INVALID()     (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_WLC_NODE]] |= \
                                       nw_nm_bit_mask[NM_WLC_NODE])

#define NM_WLC_NODE_DLC_VALID()      (nw_nm_node_dlcfault_sts[nw_nm_byte_offset[NM_WLC_NODE]] &= \
                                      (CAN_UINT8) ~(nw_nm_bit_mask[NM_WLC_NODE]))


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
Date			    : 2026-02-26 12:10
By			        : SKUMARA4
Traceability		: S2XX_SMART_CORE_SVNID_40024_25_02_2026_Edited.dbc
Change Description	: Tool Generated code
*****************************************************************************/
