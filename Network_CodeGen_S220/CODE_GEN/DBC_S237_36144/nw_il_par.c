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
  /* ===========================================================================

    Name:           nw_il_par.c

    Description:    Interaction Layer Tx and Rx Parameters

                    Application Specific Tx and Rx Message and Signal
                    Data Structure Definitions

    Organization:   Network Subsystem.

   =========================================================================*/

  /* ===========================================================================
    P U B L I C   T Y P E   D E F I N I T I O N S
   ========================================================================*/


#include "can_type.h"
#include "can_defs.h"
#include "can_csec.h"
#include "nw_il.h"
#include "nw_il_par.h"
/* ===========================================================================
//  M E M O R Y   A L L O C A T I O N
// =========================================================================*/
CAN_UINT8 il_Rx_DataChanged_Flag[ IL_NUM_OF_RX_DATA_CHANGED_FLAG ];

/* ==========================================================================
// Tx and Rx buffer                                
/  ========================================================================*/
/*Tx_Msg_buf             Tx_buffer;*/
Rx_Msg_buf  Rx_buffer;

/* Tx buffer objects */

IC10_1000_TEST_buf IC10_1000_TEST;
IC10_200_buf IC10_200;
IC11_1000_TEST_buf IC11_1000_TEST;
IC11_500_buf IC11_500;
IC12_1000_buf IC12_1000;
IC1_100_buf IC1_100;
IC2_100_buf IC2_100;
IC4_1000_TEST_buf IC4_1000_TEST;
IC6_1000_TEST_buf IC6_1000_TEST;
IC7_1000_TEST_buf IC7_1000_TEST;
IC8_1000_TEST_buf IC8_1000_TEST;
IC9_1000_TEST_buf IC9_1000_TEST;
IC_NSM_buf IC_NSM;
IS11_500_buf IS11_500;
IS12_500_buf IS12_500;
IS13_500_buf IS13_500;
IS14_200_buf IS14_200;
IS16_1000_buf IS16_1000;
IS17_50_buf IS17_50;
IS18_200_buf IS18_200;
IS1_100_buf IS1_100;
IS3_500_buf IS3_500;
IS4_500_buf IS4_500;
IS6_500_buf IS6_500;
IS_NM_TEST_buf IS_NM_TEST;
IS_NSM_buf IS_NSM;
MCM1_SP_buf MCM1_SP;
MCM2_100_buf MCM2_100;
MCM4_1000_buf MCM4_1000;
MCM_NSM_buf MCM_NSM;
MCM_PKE_SP_buf MCM_PKE_SP;
MCM_TEST5_100_buf MCM_TEST5_100;
MCM_WAKEUP_buf MCM_WAKEUP;
TGU1_500_buf TGU1_500;
TGU4_500_buf TGU4_500;
/* Rx buffer objects */

ACC1_500_buf ACC1_500;
ACC2_500_buf ACC2_500;
AMT5_20_buf AMT5_20;
AMT6_20_buf AMT6_20;
APA2_50_buf APA2_50;
APA3_50_buf APA3_50;
APA4_50_buf APA4_50;
APA_NSM_buf APA_NSM;
BMS16_10_buf BMS16_10;
BMS10_100_buf BMS10_100;
BMS11_100_buf BMS11_100;
BMS14_100_buf BMS14_100;
BMS17_100_buf BMS17_100;
BMS18_50_buf BMS18_50;
BMS1_10_buf BMS1_10;
BMS22_100_buf BMS22_100;
BMS2_30_buf BMS2_30;
BMS3_100_buf BMS3_100;
BMS4_100_buf BMS4_100;
BMS5_100_buf BMS5_100;
BMS6_100_buf BMS6_100;
BMS7_100_buf BMS7_100;
BMS8_50_buf BMS8_50;
BMS9_10_buf BMS9_10;
BMS_CLT_HTR1_200_buf BMS_CLT_HTR1_200;
BMS_CLT_HTR2_200_buf BMS_CLT_HTR2_200;
BMS_CLT_HTR3_200_buf BMS_CLT_HTR3_200;
BMS_IVT_MSG_RESULT_U1_buf BMS_IVT_MSG_RESULT_U1;
BMS_IVT_MSG_RESULT_U2_buf BMS_IVT_MSG_RESULT_U2;
BMS_IVT_MSG_RESULT_U3_buf BMS_IVT_MSG_RESULT_U3;
BMS_STS_500_buf BMS_STS_500;
CCM1_200_buf CCM1_200;
CCM3_200_buf CCM3_200;
EMS3_10_buf EMS3_10;
EMS12_200_buf EMS12_200;
EMS13_200_buf EMS13_200;
EMS14_10_buf EMS14_10;
EMS1_10_buf EMS1_10;
EMS21_10_buf EMS21_10;
EMS29_100_buf EMS29_100;
EMS2_10_buf EMS2_10;
EMS30_SP_buf EMS30_SP;
EMS36_10_buf EMS36_10;
EMS37_500_buf EMS37_500;
EMS38_100_buf EMS38_100;
EMS39_100_buf EMS39_100;
EMS41_100_buf EMS41_100;
EMS42_100_buf EMS42_100;
EMS43_100_buf EMS43_100;
EMS44_100_buf EMS44_100;
EMS45_100_buf EMS45_100;
EMS4_20_buf EMS4_20;
EMS6_500_buf EMS6_500;
EMS8_10_buf EMS8_10;
EMS9_500_buf EMS9_500;
EMS_NSM_buf EMS_NSM;
VCU10_100_buf VCU10_100;
VCU11_100_buf VCU11_100;
VCU11_50_buf VCU11_50;
VCU12_100_buf VCU12_100;
VCU13_100_buf VCU13_100;
VCU14_20_buf VCU14_20;
VCU15_100_buf VCU15_100;
VCU16_1000_buf VCU16_1000;
VCU16_500_buf VCU16_500;
VCU17_200_buf VCU17_200;
VCU18_10_buf VCU18_10;
VCU1_20_buf VCU1_20;
VCU2_100_buf VCU2_100;
VCU3_100_buf VCU3_100;
VCU4_20_EV_buf VCU4_20_EV;
VCU5_100_buf VCU5_100;
VCU5_500_buf VCU5_500;
VCU7_100_buf VCU7_100;
VCU8_10_buf VCU8_10;
VCU_FC1_10_buf VCU_FC1_10;
VCU_STS_500_buf VCU_STS_500;
EPS1_100_buf EPS1_100;
EPS_NSM_buf EPS_NSM;
ESC5_10_buf ESC5_10;
ESC10_20_buf ESC10_20;
ESC12_10_buf ESC12_10;
ESC13_100_buf ESC13_100;
ESC14_500_buf ESC14_500;
ESC15_1000_buf ESC15_1000;
ESC16_10_buf ESC16_10;
ESC2_10_buf ESC2_10;
ESC3_20_buf ESC3_20;
ESC7_20_buf ESC7_20;
ESC8_20_buf ESC8_20;
ESC_NSM_buf ESC_NSM;
ESCL1_100_buf ESCL1_100;
ESCL_NSM_buf ESCL_NSM;
ETL1_20_buf ETL1_20;
ETL_STS_500_buf ETL_STS_500;
FATC1_200_buf FATC1_200;
FATC2_200_buf FATC2_200;
FCM_LKAS1_10_buf FCM_LKAS1_10;
FCM1_20_buf FCM1_20;
FCM_HBA_50_buf FCM_HBA_50;
FCM_NSM_buf FCM_NSM;
FCM_TSR_100_buf FCM_TSR_100;
FRM1_20_buf FRM1_20;
FRM2_20_buf FRM2_20;
FRM3_TEST_100_buf FRM3_TEST_100;
FRM_NSM_buf FRM_NSM;
FVC1_100_buf FVC1_100;
GW_HEARTBEAT_buf GW_HEARTBEAT;
GW1_1000_buf GW1_1000;
HLCU1_100_buf HLCU1_100;
HLCU2_100_buf HLCU2_100;
ICC2_50_buf ICC2_50;
ICC1_1000_buf ICC1_1000;
LDC4_30_buf LDC4_30;
LDC1_100_buf LDC1_100;
LDC2_30_buf LDC2_30;
LDC3_100_buf LDC3_100;
LDC_STS_500_buf LDC_STS_500;
MBFM1_100_buf MBFM1_100;
MBFM10_100_buf MBFM10_100;
MBFM14_100_buf MBFM14_100;
MBFM15_10_buf MBFM15_10;
MBFM16_200_buf MBFM16_200;
MBFM17_200_buf MBFM17_200;
MBFM5_100_buf MBFM5_100;
MBFM6_100_buf MBFM6_100;
MBFM7_100_buf MBFM7_100;
MBFM9_500_buf MBFM9_500;
MBFM_NSM_buf MBFM_NSM;
MBFM_PAS1_50_buf MBFM_PAS1_50;
SYNC_MSG_SP_buf SYNC_MSG_SP;
TPMS1_100_buf TPMS1_100;
TPMS2_100_buf TPMS2_100;
TPMS3_100_buf TPMS3_100;
MCU2_10_buf MCU2_10;
MCU1_100_buf MCU1_100;
MCU3_10_buf MCU3_10;
MCU5_100_buf MCU5_100;
MCU_STS_500_buf MCU_STS_500;
OBC3_100_buf OBC3_100;
OBC1_100_buf OBC1_100;
OBC2_100_buf OBC2_100;
OBC4_30_buf OBC4_30;
OBC6_100_buf OBC6_100;
OBC_STS_500_buf OBC_STS_500;
PKE_ICU2_100_buf PKE_ICU2_100;
PKE1_100_buf PKE1_100;
PKE2_200_buf PKE2_200;
PKE_ICU_NSM_buf PKE_ICU_NSM;
PKE_MCM_SP_buf PKE_MCM_SP;
PKE_TEST5_100_buf PKE_TEST5_100;
SAS1_10_buf SAS1_10;
SBRM1_100_buf SBRM1_100;
SBW1_10_buf SBW1_10;
SCM1_500_buf SCM1_500;
SRS1_20_buf SRS1_20;
SVS1_10_buf SVS1_10;
TC1_20_buf TC1_20;
TC_NSM_buf TC_NSM;
TCU5_10_buf TCU5_10;
TCU6_20_buf TCU6_20;
WLC3_2000_buf WLC3_2000;
WLC_NSM_buf WLC_NSM;
/* ====================================================================================
  Interaction Layer Receive Signal Tx Put Functions
  =====================================================================================*/

void ILPutTx_RAWROLL_data(CAN_UINT16 sig_Data)
{
   IC10_1000_TEST.ic10_1000_test.RAWROLL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC10_1000_TEST.ic10_1000_test.RAWROLL_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_RAWPITCH_data(CAN_UINT16 sig_Data)
{
   IC10_1000_TEST.ic10_1000_test.RAWPITCH_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC10_1000_TEST.ic10_1000_test.RAWPITCH_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_ROLLCOMP_data(CAN_UINT16 sig_Data)
{
   IC11_1000_TEST.ic11_1000_test.ROLLCOMP_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC11_1000_TEST.ic11_1000_test.ROLLCOMP_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_PITCHCOMP_data(CAN_UINT16 sig_Data)
{
   IC11_1000_TEST.ic11_1000_test.PITCHCOMP_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC11_1000_TEST.ic11_1000_test.PITCHCOMP_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_DIST_TO_EMPTY_data(CAN_UINT16 sig_Data)
{
   IC1_100.ic1_100.DIST_TO_EMPTY_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC1_100.ic1_100.DIST_TO_EMPTY_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x03);
}

void ILPutTx_INSTANT_KMPL_data(CAN_UINT16 sig_Data)
{
   IC1_100.ic1_100.INSTANT_KMPL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC1_100.ic1_100.INSTANT_KMPL_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_AVG_KMPL_data(CAN_UINT16 sig_Data)
{
   IC1_100.ic1_100.AVG_KMPL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC1_100.ic1_100.AVG_KMPL_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_FUEL_LEVEL_data(CAN_UINT16 sig_Data)
{
   IC1_100.ic1_100.FUEL_LEVEL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC1_100.ic1_100.FUEL_LEVEL_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_ODOMTR_READING_data(CAN_UINT32 sig_Data)
{
   IC2_100.ic2_100.ODOMTR_READING_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC2_100.ic2_100.ODOMTR_READING_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
   IC2_100.ic2_100.ODOMTR_READING_2 = (CAN_UINT8) (((sig_Data) >> 16) & 0x0f);
}

void ILPutTx_AVG_KMPL_GD_data(CAN_UINT16 sig_Data)
{
   IC2_100.ic2_100.AVG_KMPL_GD_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC2_100.ic2_100.AVG_KMPL_GD_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_AFE_ACCUMULATED_DISTANCE_data(CAN_UINT16 sig_Data)
{
   IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_DISTANCE_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_DISTANCE_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x07);
}

void ILPutTx_AFE_ACCUMULATED_FUEL_CONSMP_data(CAN_UINT16 sig_Data)
{
   IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_FUEL_CONSMP_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_FUEL_CONSMP_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x1f);
}

void ILPutTx_FUEL_CONSMP_ACCUMULATED_data(CAN_UINT16 sig_Data)
{
   IC4_1000_TEST.ic4_1000_test.FUEL_CONSMP_ACCUMULATED_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC4_1000_TEST.ic4_1000_test.FUEL_CONSMP_ACCUMULATED_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_FUEL_LVL_RAW_data(CAN_UINT16 sig_Data)
{
   IC6_1000_TEST.ic6_1000_test.FUEL_LVL_RAW_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC6_1000_TEST.ic6_1000_test.FUEL_LVL_RAW_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_FUEL_LVL_DTE_FILTER_data(CAN_UINT16 sig_Data)
{
   IC6_1000_TEST.ic6_1000_test.FUEL_LVL_DTE_FILTER_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC6_1000_TEST.ic6_1000_test.FUEL_LVL_DTE_FILTER_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_FLOAT_RESISTANCE_RAW_data(CAN_UINT16 sig_Data)
{
   IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_RAW_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_RAW_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x03);
}

void ILPutTx_FLOAT_RESISTANCE_FILTER_data(CAN_UINT16 sig_Data)
{
   IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_FILTER_0 = (CAN_UINT8) ((sig_Data) & 0x3f);
   IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_FILTER_1 = (CAN_UINT8) (((sig_Data) >> 6) & 0x0f);
}

void ILPutTx_CALCULATED_AFE_GD_data(CAN_UINT16 sig_Data)
{
   IC6_1000_TEST.ic6_1000_test.CALCULATED_AFE_GD_0 = (CAN_UINT8) ((sig_Data) & 0x0f);
   IC6_1000_TEST.ic6_1000_test.CALCULATED_AFE_GD_1 = (CAN_UINT8) (((sig_Data) >> 4) & 0x1f);
}

void ILPutTx_VEHICLE_SPEED_IC_data(CAN_UINT16 sig_Data)
{
   IC7_1000_TEST.ic7_1000_test.VEHICLE_SPEED_IC_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC7_1000_TEST.ic7_1000_test.VEHICLE_SPEED_IC_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_CALCULATED_AFE_data(CAN_UINT16 sig_Data)
{
   IC7_1000_TEST.ic7_1000_test.CALCULATED_AFE_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC7_1000_TEST.ic7_1000_test.CALCULATED_AFE_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_CALCULATED_DTE_data(CAN_UINT16 sig_Data)
{
   IC7_1000_TEST.ic7_1000_test.CALCULATED_DTE_0 = (CAN_UINT8) ((sig_Data) & 0x7f);
   IC7_1000_TEST.ic7_1000_test.CALCULATED_DTE_1 = (CAN_UINT8) (((sig_Data) >> 7) & 0x07);
}

void ILPutTx_FLOAT_SENSOR_RESISTANCE_RAW_data(CAN_UINT8 sigData)
{
   IC7_1000_TEST.ic7_1000_test.FLOAT_SENSOR_RESISTANCE_RAW_0 = ((CAN_UINT8) (sigData & 0x1f));
   IC7_1000_TEST.ic7_1000_test.FLOAT_SENSOR_RESISTANCE_RAW_1 = ((CAN_UINT8) (((sigData) >> 5) & 0x07));
}

void ILPutTx_DTE_CALCULATED_AFE_data(CAN_UINT16 sig_Data)
{
   IC7_1000_TEST.ic7_1000_test.DTE_CALCULATED_AFE_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC7_1000_TEST.ic7_1000_test.DTE_CALCULATED_AFE_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_ACCEL_data(CAN_UINT16 sig_Data)
{
   IC8_1000_TEST.ic8_1000_test.ACCEL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC8_1000_TEST.ic8_1000_test.ACCEL_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_ROLLRATE_data(CAN_UINT16 sig_Data)
{
   IC8_1000_TEST.ic8_1000_test.ROLLRATE_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC8_1000_TEST.ic8_1000_test.ROLLRATE_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_ROLL_data(CAN_UINT16 sig_Data)
{
   IC9_1000_TEST.ic9_1000_test.ROLL_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC9_1000_TEST.ic9_1000_test.ROLL_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_PITCH_data(CAN_UINT16 sig_Data)
{
   IC9_1000_TEST.ic9_1000_test.PITCH_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IC9_1000_TEST.ic9_1000_test.PITCH_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_RESERVED_IC_data(CAN_UINT8 const * const pData)
{

   IC_NSM.ic_nsm.RESERVED_IC_0 = pData[0];
   IC_NSM.ic_nsm.RESERVED_IC_1 = pData[1];
   IC_NSM.ic_nsm.RESERVED_IC_2 = pData[2];
   IC_NSM.ic_nsm.RESERVED_IC_3 = pData[3];
   IC_NSM.ic_nsm.RESERVED_IC_4 = pData[4];
   IC_NSM.ic_nsm.RESERVED_IC_5 = pData[5];
   IC_NSM.ic_nsm.RESERVED_IC_6 = pData[6];
   IC_NSM.ic_nsm.RESERVED_IC_7 = pData[7];
}

void ILPutTx_TRIP_DIST_data(CAN_UINT16 sig_Data)
{
   IS12_500.is12_500.TRIP_DIST_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS12_500.is12_500.TRIP_DIST_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

void ILPutTx_TOP_SPD_data(CAN_UINT16 sig_Data)
{
   IS12_500.is12_500.TOP_SPD_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS12_500.is12_500.TOP_SPD_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_AVG_SPD_data(CAN_UINT16 sig_Data)
{
   IS12_500.is12_500.AVG_SPD_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS12_500.is12_500.AVG_SPD_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x01);
}

void ILPutTx_ESS_DURATION_data(CAN_UINT16 sig_Data)
{
   IS13_500.is13_500.ESS_DURATION_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS13_500.is13_500.ESS_DURATION_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x0f);
}

void ILPutTx_ALTIMETER_data(CAN_UINT16 sig_Data)
{
   IS16_1000.is16_1000.ALTIMETER_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS16_1000.is16_1000.ALTIMETER_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x1f);
}

void ILPutTx_COMPASS_DIRECTION_data(CAN_UINT8 sigData)
{
   IS16_1000.is16_1000.COMPASS_DIRECTION_0 = ((CAN_UINT8) (sigData & 0x07));
   IS16_1000.is16_1000.COMPASS_DIRECTION_1 = ((CAN_UINT8) (((sigData) >> 3) & 0x01));
}

void ILPutTx_FIRST_TOUCH_COORDINATE_X_IS_data(CAN_UINT16 sig_Data)
{
   IS17_50.is17_50.FIRST_TOUCH_COORDINATE_X_IS_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   IS17_50.is17_50.FIRST_TOUCH_COORDINATE_X_IS_1 = (CAN_UINT8) (((sig_Data) >> 8) & 0x0f);
}

void ILPutTx_FIRST_TOUCH_COORDINATE_Y_IS_data(CAN_UINT16 sig_Data)
{
   IS17_50.is17_50.FIRST_TOUCH_COORDINATE_Y_IS_0 = (CAN_UINT8) ((sig_Data) & 0x0f);
   IS17_50.is17_50.FIRST_TOUCH_COORDINATE_Y_IS_1 = (CAN_UINT8) (((sig_Data) >> 4) & 0xff);
}

void ILPutTx_RESERVED_IS_data(CAN_UINT8 const * const pData)
{

   IS_NSM.is_nsm.RESERVED_IS_0 = pData[0];
   IS_NSM.is_nsm.RESERVED_IS_1 = pData[1];
   IS_NSM.is_nsm.RESERVED_IS_2 = pData[2];
   IS_NSM.is_nsm.RESERVED_IS_3 = pData[3];
   IS_NSM.is_nsm.RESERVED_IS_4 = pData[4];
   IS_NSM.is_nsm.RESERVED_IS_5 = pData[5];
   IS_NSM.is_nsm.RESERVED_IS_6 = pData[6];
   IS_NSM.is_nsm.RESERVED_IS_7 = pData[7];
}

void ILPutTx_RESERVED_MCM_data(CAN_UINT8 const * const pData)
{

   MCM_NSM.mcm_nsm.RESERVED_MCM_0 = pData[0];
   MCM_NSM.mcm_nsm.RESERVED_MCM_1 = pData[1];
   MCM_NSM.mcm_nsm.RESERVED_MCM_2 = pData[2];
   MCM_NSM.mcm_nsm.RESERVED_MCM_3 = pData[3];
   MCM_NSM.mcm_nsm.RESERVED_MCM_4 = pData[4];
   MCM_NSM.mcm_nsm.RESERVED_MCM_5 = pData[5];
   MCM_NSM.mcm_nsm.RESERVED_MCM_6 = pData[6];
   MCM_NSM.mcm_nsm.RESERVED_MCM_7 = pData[7];
}

void ILPutTx_IMMOVAL6_data(CAN_UINT8 const * const pData)
{

   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_0 = pData[0];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_1 = pData[1];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_2 = pData[2];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_3 = pData[3];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_4 = pData[4];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_5 = pData[5];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_6 = pData[6];
   MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_7 = pData[7];
}

void ILPutTx_MCM_WAKEUP_REASON_data(CAN_UINT16 sig_Data)
{
   MCM_WAKEUP.mcm_wakeup.MCM_WAKEUP_REASON_0 = (CAN_UINT8) ((sig_Data) & 0xff);
   MCM_WAKEUP.mcm_wakeup.MCM_WAKEUP_REASON_1 = (CAN_UINT8) (((sig_Data) >>8) & 0xff);
}

/* ====================================================================================
  Interaction Layer Receive Signal Tx Get Functions
  =====================================================================================*/

CAN_UINT16 ILGetTx_RAWROLL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC10_1000_TEST.ic10_1000_test.RAWROLL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC10_1000_TEST.ic10_1000_test.RAWROLL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_RAWPITCH(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC10_1000_TEST.ic10_1000_test.RAWPITCH_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC10_1000_TEST.ic10_1000_test.RAWPITCH_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ROLLCOMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC11_1000_TEST.ic11_1000_test.ROLLCOMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC11_1000_TEST.ic11_1000_test.ROLLCOMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_PITCHCOMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC11_1000_TEST.ic11_1000_test.PITCHCOMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC11_1000_TEST.ic11_1000_test.PITCHCOMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_DIST_TO_EMPTY(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC1_100.ic1_100.DIST_TO_EMPTY_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC1_100.ic1_100.DIST_TO_EMPTY_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_INSTANT_KMPL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC1_100.ic1_100.INSTANT_KMPL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC1_100.ic1_100.INSTANT_KMPL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_AVG_KMPL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC1_100.ic1_100.AVG_KMPL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC1_100.ic1_100.AVG_KMPL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FUEL_LEVEL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC1_100.ic1_100.FUEL_LEVEL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC1_100.ic1_100.FUEL_LEVEL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 ILGetTx_ODOMTR_READING(void)
{
   CAN_UINT32  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT32)((CAN_UINT32)IC2_100.ic2_100.ODOMTR_READING_0);
   rValue |= (CAN_UINT32)(((CAN_UINT32)IC2_100.ic2_100.ODOMTR_READING_1) << 8);
   rValue |= (CAN_UINT32)(((CAN_UINT32)IC2_100.ic2_100.ODOMTR_READING_2) << 16);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_AVG_KMPL_GD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC2_100.ic2_100.AVG_KMPL_GD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC2_100.ic2_100.AVG_KMPL_GD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_AFE_ACCUMULATED_DISTANCE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_DISTANCE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_DISTANCE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_AFE_ACCUMULATED_FUEL_CONSMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_FUEL_CONSMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.AFE_ACCUMULATED_FUEL_CONSMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FUEL_CONSMP_ACCUMULATED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.FUEL_CONSMP_ACCUMULATED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC4_1000_TEST.ic4_1000_test.FUEL_CONSMP_ACCUMULATED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FUEL_LVL_RAW(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FUEL_LVL_RAW_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FUEL_LVL_RAW_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FUEL_LVL_DTE_FILTER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FUEL_LVL_DTE_FILTER_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FUEL_LVL_DTE_FILTER_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FLOAT_RESISTANCE_RAW(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_RAW_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_RAW_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FLOAT_RESISTANCE_FILTER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_FILTER_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) IC6_1000_TEST.ic6_1000_test.FLOAT_RESISTANCE_FILTER_1) <<6);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_CALCULATED_AFE_GD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) IC6_1000_TEST.ic6_1000_test.CALCULATED_AFE_GD_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) IC6_1000_TEST.ic6_1000_test.CALCULATED_AFE_GD_1) <<4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_VEHICLE_SPEED_IC(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.VEHICLE_SPEED_IC_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.VEHICLE_SPEED_IC_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_CALCULATED_AFE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.CALCULATED_AFE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.CALCULATED_AFE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_CALCULATED_DTE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) IC7_1000_TEST.ic7_1000_test.CALCULATED_DTE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) IC7_1000_TEST.ic7_1000_test.CALCULATED_DTE_1) <<7);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 ILGetTx_FLOAT_SENSOR_RESISTANCE_RAW(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)IC7_1000_TEST.ic7_1000_test.FLOAT_SENSOR_RESISTANCE_RAW_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)IC7_1000_TEST.ic7_1000_test.FLOAT_SENSOR_RESISTANCE_RAW_1) << 5);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_DTE_CALCULATED_AFE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.DTE_CALCULATED_AFE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC7_1000_TEST.ic7_1000_test.DTE_CALCULATED_AFE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ACCEL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC8_1000_TEST.ic8_1000_test.ACCEL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC8_1000_TEST.ic8_1000_test.ACCEL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ROLLRATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC8_1000_TEST.ic8_1000_test.ROLLRATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC8_1000_TEST.ic8_1000_test.ROLLRATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ROLL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC9_1000_TEST.ic9_1000_test.ROLL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC9_1000_TEST.ic9_1000_test.ROLL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_PITCH(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IC9_1000_TEST.ic9_1000_test.PITCH_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IC9_1000_TEST.ic9_1000_test.PITCH_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void ILGetTx_RESERVED_IC(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = IC_NSM.ic_nsm.RESERVED_IC_0;
    pData[1] = IC_NSM.ic_nsm.RESERVED_IC_1;
    pData[2] = IC_NSM.ic_nsm.RESERVED_IC_2;
    pData[3] = IC_NSM.ic_nsm.RESERVED_IC_3;
    pData[4] = IC_NSM.ic_nsm.RESERVED_IC_4;
    pData[5] = IC_NSM.ic_nsm.RESERVED_IC_5;
    pData[6] = IC_NSM.ic_nsm.RESERVED_IC_6;
    pData[7] = IC_NSM.ic_nsm.RESERVED_IC_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 ILGetTx_TRIP_DIST(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS12_500.is12_500.TRIP_DIST_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS12_500.is12_500.TRIP_DIST_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_TOP_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS12_500.is12_500.TOP_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS12_500.is12_500.TOP_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_AVG_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS12_500.is12_500.AVG_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS12_500.is12_500.AVG_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ESS_DURATION(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS13_500.is13_500.ESS_DURATION_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS13_500.is13_500.ESS_DURATION_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_ALTIMETER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS16_1000.is16_1000.ALTIMETER_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS16_1000.is16_1000.ALTIMETER_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 ILGetTx_COMPASS_DIRECTION(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)IS16_1000.is16_1000.COMPASS_DIRECTION_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)IS16_1000.is16_1000.COMPASS_DIRECTION_1) << 3);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FIRST_TOUCH_COORDINATE_X_IS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)IS17_50.is17_50.FIRST_TOUCH_COORDINATE_X_IS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)IS17_50.is17_50.FIRST_TOUCH_COORDINATE_X_IS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 ILGetTx_FIRST_TOUCH_COORDINATE_Y_IS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) IS17_50.is17_50.FIRST_TOUCH_COORDINATE_Y_IS_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) IS17_50.is17_50.FIRST_TOUCH_COORDINATE_Y_IS_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void ILGetTx_RESERVED_IS(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = IS_NSM.is_nsm.RESERVED_IS_0;
    pData[1] = IS_NSM.is_nsm.RESERVED_IS_1;
    pData[2] = IS_NSM.is_nsm.RESERVED_IS_2;
    pData[3] = IS_NSM.is_nsm.RESERVED_IS_3;
    pData[4] = IS_NSM.is_nsm.RESERVED_IS_4;
    pData[5] = IS_NSM.is_nsm.RESERVED_IS_5;
    pData[6] = IS_NSM.is_nsm.RESERVED_IS_6;
    pData[7] = IS_NSM.is_nsm.RESERVED_IS_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILGetTx_RESERVED_MCM(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = MCM_NSM.mcm_nsm.RESERVED_MCM_0;
    pData[1] = MCM_NSM.mcm_nsm.RESERVED_MCM_1;
    pData[2] = MCM_NSM.mcm_nsm.RESERVED_MCM_2;
    pData[3] = MCM_NSM.mcm_nsm.RESERVED_MCM_3;
    pData[4] = MCM_NSM.mcm_nsm.RESERVED_MCM_4;
    pData[5] = MCM_NSM.mcm_nsm.RESERVED_MCM_5;
    pData[6] = MCM_NSM.mcm_nsm.RESERVED_MCM_6;
    pData[7] = MCM_NSM.mcm_nsm.RESERVED_MCM_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILGetTx_IMMOVAL6(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_0;
    pData[1] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_1;
    pData[2] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_2;
    pData[3] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_3;
    pData[4] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_4;
    pData[5] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_5;
    pData[6] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_6;
    pData[7] = MCM_PKE_SP.mcm_pke_sp.IMMOVAL6_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 ILGetTx_MCM_WAKEUP_REASON(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCM_WAKEUP.mcm_wakeup.MCM_WAKEUP_REASON_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCM_WAKEUP.mcm_wakeup.MCM_WAKEUP_REASON_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

/* ====================================================================================
  Interaction Layer Receive Signal Rx Put Functions
  =====================================================================================*/

void ILRxPut_ACC_CTRL_OUTPUT_POWER(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_0 = (CAN_UINT8) ((data) & 0xff);
   ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_APA(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   APA_NSM.apa_nsm.RESERVED_APA_0 = pData[0];
   APA_NSM.apa_nsm.RESERVED_APA_1 = pData[1];
   APA_NSM.apa_nsm.RESERVED_APA_2 = pData[2];
   APA_NSM.apa_nsm.RESERVED_APA_3 = pData[3];
   APA_NSM.apa_nsm.RESERVED_APA_4 = pData[4];
   APA_NSM.apa_nsm.RESERVED_APA_5 = pData[5];
   APA_NSM.apa_nsm.RESERVED_APA_6 = pData[6];
   APA_NSM.apa_nsm.RESERVED_APA_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYAVGTEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_0 = (CAN_UINT8) ((data) & 0x0f);
   BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_1 = (CAN_UINT8) (((data) >> 4) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYINLETCOOLANTTEMP(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_0 = (CAN_UINT8) ((data) & 0xff);
   BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYINLETCOOLANTTEMPREQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_0 = (CAN_UINT8) ((data) & 0xff);
   BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYOUTLETCOOLANTTEMP(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_0 = (CAN_UINT8) ((data) & 0x01);
   BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_1 = (CAN_UINT8) (((data) >> 1) & 0xff);
   BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_2 = (CAN_UINT8) (((data) >> 9) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BHEATEROPCOOLANTTEMP(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_0 = (CAN_UINT8) ((data) & 0xff);
   BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_AVEENERGYCONS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS14_100.bms14_100.BMS_AVEENERGYCONS_0 = (CAN_UINT8) ((data) & 0xff);
   BMS14_100.bms14_100.BMS_AVEENERGYCONS_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYINSTANTENERGYCONS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_0 = (CAN_UINT8) ((data) & 0xff);
   BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_AMPEREHOUR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS17_100.bms17_100.BMS_AMPEREHOUR_0 = (CAN_UINT8) ((data) & 0xff);
   BMS17_100.bms17_100.BMS_AMPEREHOUR_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_KILOWATTHOUR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS17_100.bms17_100.BMS_KILOWATTHOUR_0 = (CAN_UINT8) ((data) & 0xff);
   BMS17_100.bms17_100.BMS_KILOWATTHOUR_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_REGEN_AH(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS17_100.bms17_100.BMS_REGEN_AH_0 = (CAN_UINT8) ((data) & 0xff);
   BMS17_100.bms17_100.BMS_REGEN_AH_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CYCLENUMBER(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS18_50.bms18_50.BMS_CYCLENUMBER_0 = (CAN_UINT8) ((data) & 0xff);
   BMS18_50.bms18_50.BMS_CYCLENUMBER_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGECYCLE_TIME(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_0 = (CAN_UINT8) ((data) & 0xff);
   BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_DISCHARGECYCLE_TIME(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_0 = (CAN_UINT8) ((data) & 0xff);
   BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_TOTALCYCLE_TIME(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_0 = (CAN_UINT8) ((data) & 0xff);
   BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYBUSVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKCURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_FC_COUNT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS22_100.bms22_100.BMS_FC_COUNT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS22_100.bms22_100.BMS_FC_COUNT_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_NC_COUNT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS22_100.bms22_100.BMS_NC_COUNT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS22_100.bms22_100.BMS_NC_COUNT_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_ISOLATIONRESIS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS22_100.bms22_100.BMS_ISOLATIONRESIS_0 = (CAN_UINT8) ((data) & 0xff);
   BMS22_100.bms22_100.BMS_ISOLATIONRESIS_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYTBATT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS2_30.bms2_30.BMS_BATTERYTBATT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS2_30.bms2_30.BMS_BATTERYTBATT_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_DISCHARGECURRENTLIMIT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGECURRENTLIMIT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGEVOLTAGELIMIT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_0 = (CAN_UINT8) ((data) & 0xff);
   BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKASOC(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS4_100.bms4_100.BMS_BATTERYPACKASOC_0 = (CAN_UINT8) ((data) & 0xff);
   BMS4_100.bms4_100.BMS_BATTERYPACKASOC_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKRSOC(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_0 = (CAN_UINT8) ((data) & 0xff);
   BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKSOH(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS4_100.bms4_100.BMS_BATTERYPACKSOH_0 = (CAN_UINT8) ((data) & 0xff);
   BMS4_100.bms4_100.BMS_BATTERYPACKSOH_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYAVGCELLVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYMAXCELLVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYMINCELLVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYMAXTEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYMINTEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_DISCHARGEPOWERAVAILABLE_10(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_0 = (CAN_UINT8) ((data) & 0xff);
   BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_DISCHARGEPOWERAVAILABLE_2(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_0 = (CAN_UINT8) ((data) & 0xff);
   BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_BATTERYPACKSOE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS7_100.bms7_100.BMS_BATTERYPACKSOE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS7_100.bms7_100.BMS_BATTERYPACKSOE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CURRENT1SENSORREADING(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_0 = (CAN_UINT8) ((data) & 0xff);
   BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CURRENT2SENSORREADING(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_0 = (CAN_UINT8) ((data) & 0xff);
   BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGEPOWERAVAILABLE_10(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_0 = (CAN_UINT8) ((data) & 0xff);
   BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGEPOWERAVAILABLE_2(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_0 = (CAN_UINT8) ((data) & 0xff);
   BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_CHARGE_CYCLE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS9_10.bms9_10.BMS_CHARGE_CYCLE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS9_10.bms9_10.BMS_CHARGE_CYCLE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_DISCHARGE_CYCLE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_0 = (CAN_UINT8) ((data) & 0xff);
   BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_IVT_RESULT_U1(CAN_UINT32 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_0 = (CAN_UINT8) ((data) & 0xff);
   BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_2 = (CAN_UINT8) (((data) >>16) & 0xff);
   BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_3 = (CAN_UINT8) (((data) >>24) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_IVT_RESULT_U2(CAN_UINT32 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_0 = (CAN_UINT8) ((data) & 0xff);
   BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_2 = (CAN_UINT8) (((data) >>16) & 0xff);
   BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_3 = (CAN_UINT8) (((data) >>24) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BMS_IVT_RESULT_U3(CAN_UINT32 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_0 = (CAN_UINT8) ((data) & 0xff);
   BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_2 = (CAN_UINT8) (((data) >>16) & 0xff);
   BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_3 = (CAN_UINT8) (((data) >>24) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_COMPRESSURE_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   CCM1_200.ccm1_200.COMPRESSURE_SPD_0 = (CAN_UINT8) ((data) & 0xff);
   CCM1_200.ccm1_200.COMPRESSURE_SPD_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_DISCHARGE_LINE_PRESSURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_0 = (CAN_UINT8) ((data) & 0x0f);
   CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_1 = (CAN_UINT8) (((data) >> 4) & 0x1f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_HEATER_INPUT_DC_VOLT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_0 = (CAN_UINT8) ((data) & 0xff);
   CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_TRQ_AFTR_RED(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_0 = (CAN_UINT8) ((data) & 0xff);
   EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_DRIVER_DEMAND_TRQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_0 = (CAN_UINT8) ((data) & 0xff);
   EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_CURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS13_200.ems13_200.IBS_CURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   EMS13_200.ems13_200.IBS_CURRENT_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_BATT_VOLT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS13_200.ems13_200.IBS_BATT_VOLT_0 = (CAN_UINT8) ((data) & 0xff);
   EMS13_200.ems13_200.IBS_BATT_VOLT_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_BATT_TEMP(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS13_200.ems13_200.IBS_BATT_TEMP_0 = (CAN_UINT8) ((data) & 0xff);
   EMS13_200.ems13_200.IBS_BATT_TEMP_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_TURBO_BOOST_PRESSURE_ABSOLUTE(CAN_UINT8 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_0 = ((CAN_UINT8) (data & 0x01));
   EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_1 = ((CAN_UINT8) (((data) >> 1) & 0x0f));
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS1_10.ems1_10.ENG_SPD_0 = (CAN_UINT8) ((data) & 0xff);
   EMS1_10.ems1_10.ENG_SPD_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_INJ_QTY(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS1_10.ems1_10.INJ_QTY_0 = (CAN_UINT8) ((data) & 0xff);
   EMS1_10.ems1_10.INJ_QTY_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_LOSSES(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS21_10.ems21_10.ENG_LOSSES_0 = (CAN_UINT8) ((data) & 0xff);
   EMS21_10.ems21_10.ENG_LOSSES_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_DIST_DEF_EMPTY(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS29_100.ems29_100.DIST_DEF_EMPTY_0 = (CAN_UINT8) ((data) & 0xff);
   EMS29_100.ems29_100.DIST_DEF_EMPTY_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VEHICLE_SPEED_EMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS2_10.ems2_10.VEHICLE_SPEED_EMS_0 = (CAN_UINT8) ((data) & 0xff);
   EMS2_10.ems2_10.VEHICLE_SPEED_EMS_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ODO_DISTANCE_EMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS2_10.ems2_10.ODO_DISTANCE_EMS_0 = (CAN_UINT8) ((data) & 0xff);
   EMS2_10.ems2_10.ODO_DISTANCE_EMS_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_SPD_RATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS2_10.ems2_10.ENG_SPD_RATE_0 = (CAN_UINT8) ((data) & 0xff);
   EMS2_10.ems2_10.ENG_SPD_RATE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IMMOVAL3(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   EMS30_SP.ems30_sp.IMMOVAL3_0 = pData[0];
   EMS30_SP.ems30_sp.IMMOVAL3_1 = pData[1];
   EMS30_SP.ems30_sp.IMMOVAL3_2 = pData[2];
   EMS30_SP.ems30_sp.IMMOVAL3_3 = pData[3];
   EMS30_SP.ems30_sp.IMMOVAL3_4 = pData[4];
   EMS30_SP.ems30_sp.IMMOVAL3_5 = pData[5];
   EMS30_SP.ems30_sp.IMMOVAL3_6 = pData[6];
   EMS30_SP.ems30_sp.IMMOVAL3_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_SPD1(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS36_10.ems36_10.ENG_SPD1_0 = (CAN_UINT8) ((data) & 0xff);
   EMS36_10.ems36_10.ENG_SPD1_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_TRQ_AFTR_RED1(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_0 = (CAN_UINT8) ((data) & 0xff);
   EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_DRIVER_DEMAND_TRQ_EMS36(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_0 = (CAN_UINT8) ((data) & 0x1f);
   EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_1 = (CAN_UINT8) (((data) >> 5) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATT_SENSED_VOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x01);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATT_MIN_VOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.BATT_MIN_VOLTAGE_0 = (CAN_UINT8) ((data) & 0x7f);
   EMS38_100.ems38_100.BATT_MIN_VOLTAGE_1 = (CAN_UINT8) (((data) >> 7) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_TIME_ELAPSED_CRANKING(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_0 = (CAN_UINT8) ((data) & 0x3f);
   EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_1 = (CAN_UINT8) (((data) >> 6) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_COMMANDED_THRTL_ACTR_CTL(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_0 = (CAN_UINT8) ((data) & 0x0f);
   EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_1 = (CAN_UINT8) (((data) >> 4) & 0x7f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MASS_AIR_FLOW_RATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_0 = (CAN_UINT8) ((data) & 0x01);
   EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_1 = (CAN_UINT8) (((data) >> 1) & 0xff);
   EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_2 = (CAN_UINT8) (((data) >> 9) & 0x01);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_CAL_LOAD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS38_100.ems38_100.CAL_LOAD_0 = (CAN_UINT8) ((data) & 0x7f);
   EMS38_100.ems38_100.CAL_LOAD_1 = (CAN_UINT8) (((data) >> 7) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_FUEL_RAIL_PRESSURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_0 = (CAN_UINT8) ((data) & 0xff);
   EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MEUNT_CTCL_FLTACT_CURVAL(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_0 = (CAN_UINT8) ((data) & 0x0f);
   EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_1 = (CAN_UINT8) (((data) >> 4) & 0x7f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MEUNT_SETPOINT_ADPT_CORECT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_0 = (CAN_UINT8) ((data) & 0x01);
   EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_1 = (CAN_UINT8) (((data) >> 1) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MEUNT_SETPOINT_RAIL_PRESSURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_0 = (CAN_UINT8) ((data) & 0xff);
   EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_1 = (CAN_UINT8) (((data) >> 8) & 0x01);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_EGR_ERR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.EGR_ERR_0 = (CAN_UINT8) ((data) & 0x7f);
   EMS39_100.ems39_100.EGR_ERR_1 = (CAN_UINT8) (((data) >> 7) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_COMMANDED_EGR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS39_100.ems39_100.COMMANDED_EGR_0 = (CAN_UINT8) ((data) & 0x0f);
   EMS39_100.ems39_100.COMMANDED_EGR_1 = (CAN_UINT8) (((data) >> 4) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_NOX_DWNSTR_SCR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS41_100.ems41_100.NOX_DWNSTR_SCR_0 = (CAN_UINT8) ((data) & 0xff);
   EMS41_100.ems41_100.NOX_DWNSTR_SCR_1 = (CAN_UINT8) (((data) >> 8) & 0x01);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_NOX_UPSTR_MDL(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS42_100.ems42_100.NOX_UPSTR_MDL_0 = (CAN_UINT8) ((data) & 0xff);
   EMS42_100.ems42_100.NOX_UPSTR_MDL_1 = (CAN_UINT8) (((data) >> 8) & 0x01);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_CRUISE_SET_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS4_20.ems4_20.CRUISE_SET_SPD_0 = (CAN_UINT8) ((data) & 0xff);
   EMS4_20.ems4_20.CRUISE_SET_SPD_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_FUEL_CONSMP_RATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS4_20.ems4_20.FUEL_CONSMP_RATE_0 = (CAN_UINT8) ((data) & 0xff);
   EMS4_20.ems4_20.FUEL_CONSMP_RATE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_ON_TIME(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS6_500.ems6_500.ENG_ON_TIME_0 = (CAN_UINT8) ((data) & 0xff);
   EMS6_500.ems6_500.ENG_ON_TIME_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MAX_ALL_TRQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS8_10.ems8_10.MAX_ALL_TRQ_0 = (CAN_UINT8) ((data) & 0xff);
   EMS8_10.ems8_10.MAX_ALL_TRQ_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MIN_ALL_TRQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS8_10.ems8_10.MIN_ALL_TRQ_0 = (CAN_UINT8) ((data) & 0xff);
   EMS8_10.ems8_10.MIN_ALL_TRQ_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATT_OCV(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   EMS9_500.ems9_500.BATT_OCV_0 = (CAN_UINT8) ((data) & 0x01);
   EMS9_500.ems9_500.BATT_OCV_1 = (CAN_UINT8) (((data) >> 1) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_EMS(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   EMS_NSM.ems_nsm.RESERVED_EMS_0 = pData[0];
   EMS_NSM.ems_nsm.RESERVED_EMS_1 = pData[1];
   EMS_NSM.ems_nsm.RESERVED_EMS_2 = pData[2];
   EMS_NSM.ems_nsm.RESERVED_EMS_3 = pData[3];
   EMS_NSM.ems_nsm.RESERVED_EMS_4 = pData[4];
   EMS_NSM.ems_nsm.RESERVED_EMS_5 = pData[5];
   EMS_NSM.ems_nsm.RESERVED_EMS_6 = pData[6];
   EMS_NSM.ems_nsm.RESERVED_EMS_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEUMAXLIM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_0 = (CAN_UINT8) ((data) & 0xff);
   VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ACT_REGEN_TORQUE_APPLIED(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_0 = (CAN_UINT8) ((data) & 0xff);
   VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MOTOR_PWR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU11_50.vcu11_50.MOTOR_PWR_0 = (CAN_UINT8) ((data) & 0xff);
   VCU11_50.vcu11_50.MOTOR_PWR_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEUMINLIM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_0 = (CAN_UINT8) ((data) & 0xff);
   VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ECONSPERKM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU15_100.vcu15_100.VCU_ECONSPERKM_0 = (CAN_UINT8) ((data) & 0xff);
   VCU15_100.vcu15_100.VCU_ECONSPERKM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_HVACCPOWERCONSUMPTION(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_0 = (CAN_UINT8) ((data) & 0xff);
   VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_TORQUECOASTING(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU15_100.vcu15_100.VCU_TORQUECOASTING_0 = (CAN_UINT8) ((data) & 0xff);
   VCU15_100.vcu15_100.VCU_TORQUECOASTING_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ECONSDISTSAMPLE1(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_0 = (CAN_UINT8) ((data) & 0xff);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ECONSDISTSAMPLE2(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_0 = (CAN_UINT8) ((data) & 0xff);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ECONSDISTSAMPLE3(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_0 = (CAN_UINT8) ((data) & 0xff);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ECONSDISTSAMPLE4(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_0 = (CAN_UINT8) ((data) & 0xff);
   VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_DTE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU16_500.vcu16_500.DTE_0 = (CAN_UINT8) ((data) & 0x03);
   VCU16_500.vcu16_500.DTE_1 = (CAN_UINT8) (((data) >> 2) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATT_COMPRES_SPD_REQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_0 = (CAN_UINT8) ((data) & 0xff);
   VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_EPT_RADIATORFAN_SPEED_REQ(CAN_UINT8 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU17_200.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_0 = ((CAN_UINT8) (data & 0x01));
   VCU17_200.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_1 = ((CAN_UINT8) (((data) >> 1) & 0x01));
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATTERY_INLET_COOLANT_TEMP_REQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_0 = (CAN_UINT8) ((data) & 0xff);
   VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_BATTERY_INLET_COOLANT_TEMP(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_0 = (CAN_UINT8) ((data) & 0x0f);
   VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_1 = (CAN_UINT8) (((data) >> 4) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_NOSM_STATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU18_10.vcu18_10.VCU_NOSM_STATE_0 = (CAN_UINT8) ((data) & 0xff);
   VCU18_10.vcu18_10.VCU_NOSM_STATE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_SMOBC_STATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU18_10.vcu18_10.VCU_SMOBC_STATE_0 = (CAN_UINT8) ((data) & 0xff);
   VCU18_10.vcu18_10.VCU_SMOBC_STATE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_MAXCHARGECURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_MAXDISCHARGECURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_CMDACCHARGETARGETCURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_CMDACCHARGETARGETVOLT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_0 = (CAN_UINT8) ((data) & 0xff);
   VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VEHICLE_SPEED(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_0 = (CAN_UINT8) ((data) & 0xff);
   VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_EXMEDI_IDXDCCHRGNERR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_0 = (CAN_UINT8) ((data) & 0xff);
   VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_HVACCOOLINGPOWER(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_0 = (CAN_UINT8) ((data) & 0xff);
   VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEIMAXLIM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_0 = (CAN_UINT8) ((data) & 0xff);
   VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEIMINLIM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_0 = (CAN_UINT8) ((data) & 0xff);
   VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VIN_DATA_1(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_0 = pData[0];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_1 = pData[1];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_2 = pData[2];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_3 = pData[3];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_4 = pData[4];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_5 = pData[5];
   VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_6 = pData[6];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VIN_DATA_0(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_0 = pData[0];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_1 = pData[1];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_2 = pData[2];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_3 = pData[3];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_4 = pData[4];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_5 = pData[5];
   VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_6 = pData[6];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VIN_DATA_2(CAN_UINT32 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_0 = (CAN_UINT8) ((data) & 0xff);
   VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_2 = (CAN_UINT8) (((data) >>16) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEPRESI(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU7_100.vcu7_100.VCU_VALEVSEPRESI_0 = (CAN_UINT8) ((data) & 0xff);
   VCU7_100.vcu7_100.VCU_VALEVSEPRESI_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_VALEVSEPRESU(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU7_100.vcu7_100.VCU_VALEVSEPRESU_0 = (CAN_UINT8) ((data) & 0xff);
   VCU7_100.vcu7_100.VCU_VALEVSEPRESU_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_TORQUECOMMAND(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU8_10.vcu8_10.VCU_TORQUECOMMAND_0 = (CAN_UINT8) ((data) & 0xff);
   VCU8_10.vcu8_10.VCU_TORQUECOMMAND_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_ISETPOINTCHRGN(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_0 = (CAN_UINT8) ((data) & 0xff);
   VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VCU_USETPOINTCHRGN(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_0 = (CAN_UINT8) ((data) & 0xff);
   VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_EPS(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   EPS_NSM.eps_nsm.RESERVED_EPS_0 = pData[0];
   EPS_NSM.eps_nsm.RESERVED_EPS_1 = pData[1];
   EPS_NSM.eps_nsm.RESERVED_EPS_2 = pData[2];
   EPS_NSM.eps_nsm.RESERVED_EPS_3 = pData[3];
   EPS_NSM.eps_nsm.RESERVED_EPS_4 = pData[4];
   EPS_NSM.eps_nsm.RESERVED_EPS_5 = pData[5];
   EPS_NSM.eps_nsm.RESERVED_EPS_6 = pData[6];
   EPS_NSM.eps_nsm.RESERVED_EPS_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MASTER_CYL_PRESSURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC10_20.esc10_20.MASTER_CYL_PRESSURE_0 = (CAN_UINT8) ((data) & 0xff);
   ESC10_20.esc10_20.MASTER_CYL_PRESSURE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ODO_DISTANCE_ESC12(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC12_10.esc12_10.ODO_DISTANCE_ESC12_0 = (CAN_UINT8) ((data) & 0xff);
   ESC12_10.esc12_10.ODO_DISTANCE_ESC12_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VEHICLE_SPEED_ESC12(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_0 = (CAN_UINT8) ((data) & 0xff);
   ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_VEHICLE_SPEED_ESC(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC2_10.esc2_10.VEHICLE_SPEED_ESC_0 = (CAN_UINT8) ((data) & 0xff);
   ESC2_10.esc2_10.VEHICLE_SPEED_ESC_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ODO_DISTANCE_ESC(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC2_10.esc2_10.ODO_DISTANCE_ESC_0 = (CAN_UINT8) ((data) & 0xff);
   ESC2_10.esc2_10.ODO_DISTANCE_ESC_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LATTERAL_ACCEL(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC7_20.esc7_20.LATTERAL_ACCEL_0 = (CAN_UINT8) ((data) & 0xff);
   ESC7_20.esc7_20.LATTERAL_ACCEL_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LONG_ACCEL(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC7_20.esc7_20.LONG_ACCEL_0 = (CAN_UINT8) ((data) & 0xff);
   ESC7_20.esc7_20.LONG_ACCEL_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_YAW_RATE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC7_20.esc7_20.YAW_RATE_0 = (CAN_UINT8) ((data) & 0xff);
   ESC7_20.esc7_20.YAW_RATE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_WHL_FL_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC8_20.esc8_20.WHL_FL_SPD_0 = (CAN_UINT8) ((data) & 0xff);
   ESC8_20.esc8_20.WHL_FL_SPD_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_WHL_FR_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC8_20.esc8_20.WHL_FR_SPD_0 = (CAN_UINT8) ((data) & 0x0f);
   ESC8_20.esc8_20.WHL_FR_SPD_1 = (CAN_UINT8) (((data) >> 4) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_WHL_RL_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC8_20.esc8_20.WHL_RL_SPD_0 = (CAN_UINT8) ((data) & 0xff);
   ESC8_20.esc8_20.WHL_RL_SPD_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_WHL_RR_SPD(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   ESC8_20.esc8_20.WHL_RR_SPD_0 = (CAN_UINT8) ((data) & 0x0f);
   ESC8_20.esc8_20.WHL_RR_SPD_1 = (CAN_UINT8) (((data) >> 4) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_ESC(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   ESC_NSM.esc_nsm.RESERVED_ESC_0 = pData[0];
   ESC_NSM.esc_nsm.RESERVED_ESC_1 = pData[1];
   ESC_NSM.esc_nsm.RESERVED_ESC_2 = pData[2];
   ESC_NSM.esc_nsm.RESERVED_ESC_3 = pData[3];
   ESC_NSM.esc_nsm.RESERVED_ESC_4 = pData[4];
   ESC_NSM.esc_nsm.RESERVED_ESC_5 = pData[5];
   ESC_NSM.esc_nsm.RESERVED_ESC_6 = pData[6];
   ESC_NSM.esc_nsm.RESERVED_ESC_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_ESCL(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   ESCL_NSM.escl_nsm.RESERVED_ESCL_0 = pData[0];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_1 = pData[1];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_2 = pData[2];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_3 = pData[3];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_4 = pData[4];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_5 = pData[5];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_6 = pData[6];
   ESCL_NSM.escl_nsm.RESERVED_ESCL_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_FCM(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   FCM_NSM.fcm_nsm.RESERVED_FCM_0 = pData[0];
   FCM_NSM.fcm_nsm.RESERVED_FCM_1 = pData[1];
   FCM_NSM.fcm_nsm.RESERVED_FCM_2 = pData[2];
   FCM_NSM.fcm_nsm.RESERVED_FCM_3 = pData[3];
   FCM_NSM.fcm_nsm.RESERVED_FCM_4 = pData[4];
   FCM_NSM.fcm_nsm.RESERVED_FCM_5 = pData[5];
   FCM_NSM.fcm_nsm.RESERVED_FCM_6 = pData[6];
   FCM_NSM.fcm_nsm.RESERVED_FCM_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ACC_SET_DIST(CAN_UINT8 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   FRM1_20.frm1_20.ACC_SET_DIST_0 = ((CAN_UINT8) (data & 0x01));
   FRM1_20.frm1_20.ACC_SET_DIST_1 = ((CAN_UINT8) (((data) >> 1) & 0x03));
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_FRM(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   FRM_NSM.frm_nsm.RESERVED_FRM_0 = pData[0];
   FRM_NSM.frm_nsm.RESERVED_FRM_1 = pData[1];
   FRM_NSM.frm_nsm.RESERVED_FRM_2 = pData[2];
   FRM_NSM.frm_nsm.RESERVED_FRM_3 = pData[3];
   FRM_NSM.frm_nsm.RESERVED_FRM_4 = pData[4];
   FRM_NSM.frm_nsm.RESERVED_FRM_5 = pData[5];
   FRM_NSM.frm_nsm.RESERVED_FRM_6 = pData[6];
   FRM_NSM.frm_nsm.RESERVED_FRM_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IGN_CNTR(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_0 = (CAN_UINT8) ((data) & 0xff);
   GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_FCVOLTAGEVALUE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_SECONDARY_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_PRIMARY_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_MOSFET_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_INPUTVOLTAGEVALUE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_OUTPUTCURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_OUTPUTVOLTAGEVALUE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_0 = (CAN_UINT8) ((data) & 0xff);
   LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_LDC_STAGE(CAN_UINT8 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   LDC3_100.ldc3_100.LDC_STAGE_0 = ((CAN_UINT8) (data & 0x03));
   LDC3_100.ldc3_100.LDC_STAGE_1 = ((CAN_UINT8) (((data) >> 2) & 0x01));
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ENG_OFF_TIME(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM1_100.mbfm1_100.ENG_OFF_TIME_0 = (CAN_UINT8) ((data) & 0xff);
   MBFM1_100.mbfm1_100.ENG_OFF_TIME_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RLS_FW_BRIGHTNESS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_0 = (CAN_UINT8) ((data) & 0xff);
   MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RLS_AMB_BRIGHTNESS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_0 = (CAN_UINT8) ((data) & 0x3f);
   MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_1 = (CAN_UINT8) (((data) >> 6) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_CURRENT_MBFM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_0 = (CAN_UINT8) ((data) & 0xff);
   MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_BATT_VOLT_MBFM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_0 = (CAN_UINT8) ((data) & 0xff);
   MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IBS_BATT_TEMP_MBFM(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_0 = (CAN_UINT8) ((data) & 0xff);
   MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_MBFM(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_0 = pData[0];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_1 = pData[1];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_2 = pData[2];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_3 = pData[3];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_4 = pData[4];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_5 = pData[5];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_6 = pData[6];
   MBFM_NSM.mbfm_nsm.RESERVED_MBFM_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_EMS_SP(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_0 = pData[0];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_1 = pData[1];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_2 = pData[2];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_3 = pData[3];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_4 = pData[4];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_5 = pData[5];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_6 = pData[6];
   SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_MOTORTORQUEESTIMATED(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_0 = (CAN_UINT8) ((data) & 0xff);
   MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_MOTORSPEED(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU2_10.mcu2_10.MCU_MOTORSPEED_0 = (CAN_UINT8) ((data) & 0xff);
   MCU2_10.mcu2_10.MCU_MOTORSPEED_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_REGENTORQUEAVAIL_QUASI(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_0 = (CAN_UINT8) ((data) & 0xff);
   MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_1 = (CAN_UINT8) (((data) >> 8) & 0x7f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_TRACTIONTORQUEAVAIL_QUASI(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_0 = (CAN_UINT8) ((data) & 0xff);
   MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_1 = (CAN_UINT8) (((data) >> 8) & 0x7f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_HIGHPOWERVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_MCU_HIGHPOWERCURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_DCCURRENTCAPABLE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_DCVOLTAGECAPABLE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_PFC_VOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC3_100.obc3_100.OBC_PFC_VOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC3_100.obc3_100.OBC_PFC_VOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_LINE_FREQUENCY(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC3_100.obc3_100.OBC_LINE_FREQUENCY_0 = (CAN_UINT8) ((data) & 0xff);
   OBC3_100.obc3_100.OBC_LINE_FREQUENCY_1 = (CAN_UINT8) (((data) >> 8) & 0x03);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_LV_PWRSUPPLY(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_0 = (CAN_UINT8) ((data) & 0xff);
   OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_PRIMARYSIDE_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_TRANSFORMER_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_COOLINGREQUEST(CAN_UINT8 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC1_100.obc1_100.OBC_COOLINGREQUEST_0 = ((CAN_UINT8) (data & 0x0f));
   OBC1_100.obc1_100.OBC_COOLINGREQUEST_1 = ((CAN_UINT8) (((data) >> 4) & 0x0f));
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_SECONDARYSIDE_TEMPERATURE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_0 = (CAN_UINT8) ((data) & 0x0f);
   OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_1 = (CAN_UINT8) (((data) >> 4) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_INDUCTOR_CURRENT_L1_RMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_0 = (CAN_UINT8) ((data) & 0xff);
   OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_INDUCTOR_CURRENT_L2_RMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_0 = (CAN_UINT8) ((data) & 0xff);
   OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_ACINPUTCURRENTRMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_0 = (CAN_UINT8) ((data) & 0xff);
   OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_ACINPUTVOLTAGERMS(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_0 = (CAN_UINT8) ((data) & 0xff);
   OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_DCOUTPUTCURRENT(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_0 = (CAN_UINT8) ((data) & 0xff);
   OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_1 = (CAN_UINT8) (((data) >> 8) & 0x0f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_OBC_DCOUTPUTVOLTAGE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_0 = (CAN_UINT8) ((data) & 0xff);
   OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_1 = (CAN_UINT8) (((data) >> 8) & 0x3f);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_PKE(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_0 = pData[0];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_1 = pData[1];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_2 = pData[2];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_3 = pData[3];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_4 = pData[4];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_5 = pData[5];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_6 = pData[6];
   PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_IMMOVAL5(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_0 = pData[0];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_1 = pData[1];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_2 = pData[2];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_3 = pData[3];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_4 = pData[4];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_5 = pData[5];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_6 = pData[6];
   PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_ABSOLUTE_ANGLE(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   SAS1_10.sas1_10.ABSOLUTE_ANGLE_0 = (CAN_UINT8) ((data) & 0xff);
   SAS1_10.sas1_10.ABSOLUTE_ANGLE_1 = (CAN_UINT8) (((data) >>8) & 0xff);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_CUR_CARD_SHAFT_TRQ(CAN_UINT16 data)
{
    CAN_ENTER_CRITICAL_SECTION(0);
   TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_0 = (CAN_UINT8) ((data) & 0xff);
   TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_1 = (CAN_UINT8) (((data) >> 8) & 0x07);
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_TC(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   TC_NSM.tc_nsm.RESERVED_TC_0 = pData[0];
   TC_NSM.tc_nsm.RESERVED_TC_1 = pData[1];
   TC_NSM.tc_nsm.RESERVED_TC_2 = pData[2];
   TC_NSM.tc_nsm.RESERVED_TC_3 = pData[3];
   TC_NSM.tc_nsm.RESERVED_TC_4 = pData[4];
   TC_NSM.tc_nsm.RESERVED_TC_5 = pData[5];
   TC_NSM.tc_nsm.RESERVED_TC_6 = pData[6];
   TC_NSM.tc_nsm.RESERVED_TC_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

void ILRxPut_RESERVED_WLC(CAN_UINT8 const * const pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
   WLC_NSM.wlc_nsm.RESERVED_WLC_0 = pData[0];
   WLC_NSM.wlc_nsm.RESERVED_WLC_1 = pData[1];
   WLC_NSM.wlc_nsm.RESERVED_WLC_2 = pData[2];
   WLC_NSM.wlc_nsm.RESERVED_WLC_3 = pData[3];
   WLC_NSM.wlc_nsm.RESERVED_WLC_4 = pData[4];
   WLC_NSM.wlc_nsm.RESERVED_WLC_5 = pData[5];
   WLC_NSM.wlc_nsm.RESERVED_WLC_6 = pData[6];
   WLC_NSM.wlc_nsm.RESERVED_WLC_7 = pData[7];
   CAN_EXIT_CRITICAL_SECTION(0);
}

/* ====================================================================================
  Interaction Layer Receive Signal Rx Get Functions
  =====================================================================================*/

CAN_UINT16 IlRxGetACC_CTRL_OUTPUT_POWER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_APA(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = APA_NSM.apa_nsm.RESERVED_APA_0;
    pData[1] = APA_NSM.apa_nsm.RESERVED_APA_1;
    pData[2] = APA_NSM.apa_nsm.RESERVED_APA_2;
    pData[3] = APA_NSM.apa_nsm.RESERVED_APA_3;
    pData[4] = APA_NSM.apa_nsm.RESERVED_APA_4;
    pData[5] = APA_NSM.apa_nsm.RESERVED_APA_5;
    pData[6] = APA_NSM.apa_nsm.RESERVED_APA_6;
    pData[7] = APA_NSM.apa_nsm.RESERVED_APA_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetBMS_BATTERYAVGTEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYINLETCOOLANTTEMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYINLETCOOLANTTEMPREQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYOUTLETCOOLANTTEMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_1) << 1);
   rValue |= (CAN_UINT16)(((CAN_UINT16) BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_2) <<9);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BHEATEROPCOOLANTTEMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_AVEENERGYCONS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS14_100.bms14_100.BMS_AVEENERGYCONS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS14_100.bms14_100.BMS_AVEENERGYCONS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYINSTANTENERGYCONS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_AMPEREHOUR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS17_100.bms17_100.BMS_AMPEREHOUR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS17_100.bms17_100.BMS_AMPEREHOUR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_KILOWATTHOUR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS17_100.bms17_100.BMS_KILOWATTHOUR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS17_100.bms17_100.BMS_KILOWATTHOUR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_REGEN_AH(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS17_100.bms17_100.BMS_REGEN_AH_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS17_100.bms17_100.BMS_REGEN_AH_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CYCLENUMBER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS18_50.bms18_50.BMS_CYCLENUMBER_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS18_50.bms18_50.BMS_CYCLENUMBER_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGECYCLE_TIME(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_DISCHARGECYCLE_TIME(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_TOTALCYCLE_TIME(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYBUSVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKCURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_FC_COUNT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS22_100.bms22_100.BMS_FC_COUNT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS22_100.bms22_100.BMS_FC_COUNT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_NC_COUNT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS22_100.bms22_100.BMS_NC_COUNT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS22_100.bms22_100.BMS_NC_COUNT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_ISOLATIONRESIS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS22_100.bms22_100.BMS_ISOLATIONRESIS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS22_100.bms22_100.BMS_ISOLATIONRESIS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYTBATT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS2_30.bms2_30.BMS_BATTERYTBATT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS2_30.bms2_30.BMS_BATTERYTBATT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_DISCHARGECURRENTLIMIT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGECURRENTLIMIT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGEVOLTAGELIMIT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKASOC(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKASOC_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKASOC_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKRSOC(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKSOH(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKSOH_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS4_100.bms4_100.BMS_BATTERYPACKSOH_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYAVGCELLVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYMAXCELLVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYMINCELLVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYMAXTEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYMINTEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_DISCHARGEPOWERAVAILABLE_10(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_DISCHARGEPOWERAVAILABLE_2(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_BATTERYPACKSOE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS7_100.bms7_100.BMS_BATTERYPACKSOE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS7_100.bms7_100.BMS_BATTERYPACKSOE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CURRENT1SENSORREADING(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CURRENT2SENSORREADING(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGEPOWERAVAILABLE_10(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGEPOWERAVAILABLE_2(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_CHARGE_CYCLE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGE_CYCLE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS9_10.bms9_10.BMS_CHARGE_CYCLE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBMS_DISCHARGE_CYCLE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT32 IlRxGetBMS_IVT_RESULT_U1(void)
{
   CAN_UINT32  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT32)((CAN_UINT32)BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_0);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_1) << 8);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_2) << 16);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_3) << 24);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT32 IlRxGetBMS_IVT_RESULT_U2(void)
{
   CAN_UINT32  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT32)((CAN_UINT32)BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_0);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_1) << 8);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_2) << 16);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_3) << 24);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT32 IlRxGetBMS_IVT_RESULT_U3(void)
{
   CAN_UINT32  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT32)((CAN_UINT32)BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_0);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_1) << 8);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_2) << 16);
   rValue |= (CAN_UINT32)(((CAN_UINT32)BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_3) << 24);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCOMPRESSURE_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)CCM1_200.ccm1_200.COMPRESSURE_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)CCM1_200.ccm1_200.COMPRESSURE_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetDISCHARGE_LINE_PRESSURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_1) <<4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetHEATER_INPUT_DC_VOLT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_TRQ_AFTR_RED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetDRIVER_DEMAND_TRQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_CURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS13_200.ems13_200.IBS_CURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS13_200.ems13_200.IBS_CURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_BATT_VOLT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS13_200.ems13_200.IBS_BATT_VOLT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS13_200.ems13_200.IBS_BATT_VOLT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_BATT_TEMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS13_200.ems13_200.IBS_BATT_TEMP_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS13_200.ems13_200.IBS_BATT_TEMP_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 IlRxGetTURBO_BOOST_PRESSURE_ABSOLUTE(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_1) << 1);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS1_10.ems1_10.ENG_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS1_10.ems1_10.ENG_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetINJ_QTY(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS1_10.ems1_10.INJ_QTY_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS1_10.ems1_10.INJ_QTY_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_LOSSES(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS21_10.ems21_10.ENG_LOSSES_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS21_10.ems21_10.ENG_LOSSES_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetDIST_DEF_EMPTY(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS29_100.ems29_100.DIST_DEF_EMPTY_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS29_100.ems29_100.DIST_DEF_EMPTY_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVEHICLE_SPEED_EMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS2_10.ems2_10.VEHICLE_SPEED_EMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS2_10.ems2_10.VEHICLE_SPEED_EMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetODO_DISTANCE_EMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS2_10.ems2_10.ODO_DISTANCE_EMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS2_10.ems2_10.ODO_DISTANCE_EMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_SPD_RATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS2_10.ems2_10.ENG_SPD_RATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS2_10.ems2_10.ENG_SPD_RATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetIMMOVAL3(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = EMS30_SP.ems30_sp.IMMOVAL3_0;
    pData[1] = EMS30_SP.ems30_sp.IMMOVAL3_1;
    pData[2] = EMS30_SP.ems30_sp.IMMOVAL3_2;
    pData[3] = EMS30_SP.ems30_sp.IMMOVAL3_3;
    pData[4] = EMS30_SP.ems30_sp.IMMOVAL3_4;
    pData[5] = EMS30_SP.ems30_sp.IMMOVAL3_5;
    pData[6] = EMS30_SP.ems30_sp.IMMOVAL3_6;
    pData[7] = EMS30_SP.ems30_sp.IMMOVAL3_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetENG_SPD1(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS36_10.ems36_10.ENG_SPD1_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS36_10.ems36_10.ENG_SPD1_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_TRQ_AFTR_RED1(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetDRIVER_DEMAND_TRQ_EMS36(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_1) <<5);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATT_SENSED_VOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATT_MIN_VOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS38_100.ems38_100.BATT_MIN_VOLTAGE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.BATT_MIN_VOLTAGE_1) <<7);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetTIME_ELAPSED_CRANKING(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_1) <<6);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCOMMANDED_THRTL_ACTR_CTL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_1) <<4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMASS_AIR_FLOW_RATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_1) << 1);
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_2) <<9);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCAL_LOAD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS38_100.ems38_100.CAL_LOAD_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS38_100.ems38_100.CAL_LOAD_1) <<7);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetFUEL_RAIL_PRESSURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMEUNT_CTCL_FLTACT_CURVAL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_1) <<4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMEUNT_SETPOINT_ADPT_CORECT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_1) << 1);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMEUNT_SETPOINT_RAIL_PRESSURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetEGR_ERR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS39_100.ems39_100.EGR_ERR_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS39_100.ems39_100.EGR_ERR_1) <<7);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCOMMANDED_EGR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS39_100.ems39_100.COMMANDED_EGR_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS39_100.ems39_100.COMMANDED_EGR_1) <<4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetNOX_DWNSTR_SCR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS41_100.ems41_100.NOX_DWNSTR_SCR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS41_100.ems41_100.NOX_DWNSTR_SCR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetNOX_UPSTR_MDL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS42_100.ems42_100.NOX_UPSTR_MDL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS42_100.ems42_100.NOX_UPSTR_MDL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCRUISE_SET_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS4_20.ems4_20.CRUISE_SET_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS4_20.ems4_20.CRUISE_SET_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetFUEL_CONSMP_RATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS4_20.ems4_20.FUEL_CONSMP_RATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS4_20.ems4_20.FUEL_CONSMP_RATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_ON_TIME(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS6_500.ems6_500.ENG_ON_TIME_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS6_500.ems6_500.ENG_ON_TIME_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMAX_ALL_TRQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS8_10.ems8_10.MAX_ALL_TRQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS8_10.ems8_10.MAX_ALL_TRQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMIN_ALL_TRQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)EMS8_10.ems8_10.MIN_ALL_TRQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)EMS8_10.ems8_10.MIN_ALL_TRQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATT_OCV(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) EMS9_500.ems9_500.BATT_OCV_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) EMS9_500.ems9_500.BATT_OCV_1) << 1);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_EMS(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = EMS_NSM.ems_nsm.RESERVED_EMS_0;
    pData[1] = EMS_NSM.ems_nsm.RESERVED_EMS_1;
    pData[2] = EMS_NSM.ems_nsm.RESERVED_EMS_2;
    pData[3] = EMS_NSM.ems_nsm.RESERVED_EMS_3;
    pData[4] = EMS_NSM.ems_nsm.RESERVED_EMS_4;
    pData[5] = EMS_NSM.ems_nsm.RESERVED_EMS_5;
    pData[6] = EMS_NSM.ems_nsm.RESERVED_EMS_6;
    pData[7] = EMS_NSM.ems_nsm.RESERVED_EMS_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetVCU_VALEVSEUMAXLIM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetACT_REGEN_TORQUE_APPLIED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMOTOR_PWR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU11_50.vcu11_50.MOTOR_PWR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU11_50.vcu11_50.MOTOR_PWR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VALEVSEUMINLIM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ECONSPERKM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU15_100.vcu15_100.VCU_ECONSPERKM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU15_100.vcu15_100.VCU_ECONSPERKM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_HVACCPOWERCONSUMPTION(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_TORQUECOASTING(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU15_100.vcu15_100.VCU_TORQUECOASTING_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU15_100.vcu15_100.VCU_TORQUECOASTING_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ECONSDISTSAMPLE1(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ECONSDISTSAMPLE2(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ECONSDISTSAMPLE3(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ECONSDISTSAMPLE4(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetDTE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) VCU16_500.vcu16_500.DTE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) VCU16_500.vcu16_500.DTE_1) << 2);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATT_COMPRES_SPD_REQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 IlRxGetEPT_RADIATORFAN_SPEED_REQ(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)VCU17_200.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)VCU17_200.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_1) << 1);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATTERY_INLET_COOLANT_TEMP_REQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetBATTERY_INLET_COOLANT_TEMP(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_NOSM_STATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU18_10.vcu18_10.VCU_NOSM_STATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU18_10.vcu18_10.VCU_NOSM_STATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_SMOBC_STATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU18_10.vcu18_10.VCU_SMOBC_STATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU18_10.vcu18_10.VCU_SMOBC_STATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_MAXCHARGECURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_MAXDISCHARGECURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_CMDACCHARGETARGETCURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_CMDACCHARGETARGETVOLT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VEHICLE_SPEED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_EXMEDI_IDXDCCHRGNERR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_HVACCOOLINGPOWER(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VALEVSEIMAXLIM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VALEVSEIMINLIM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetVIN_DATA_1(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_0;
    pData[1] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_1;
    pData[2] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_2;
    pData[3] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_3;
    pData[4] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_4;
    pData[5] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_5;
    pData[6] = VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_6;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetVIN_DATA_0(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_0;
    pData[1] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_1;
    pData[2] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_2;
    pData[3] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_3;
    pData[4] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_4;
    pData[5] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_5;
    pData[6] = VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_6;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT32 IlRxGetVIN_DATA_2(void)
{
   CAN_UINT32  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT32)((CAN_UINT32)VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_0);
   rValue |= (CAN_UINT32)(((CAN_UINT32)VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_1) << 8);
   rValue |= (CAN_UINT32)(((CAN_UINT32)VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_2) << 16);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VALEVSEPRESI(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU7_100.vcu7_100.VCU_VALEVSEPRESI_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU7_100.vcu7_100.VCU_VALEVSEPRESI_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_VALEVSEPRESU(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU7_100.vcu7_100.VCU_VALEVSEPRESU_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU7_100.vcu7_100.VCU_VALEVSEPRESU_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_TORQUECOMMAND(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU8_10.vcu8_10.VCU_TORQUECOMMAND_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU8_10.vcu8_10.VCU_TORQUECOMMAND_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_ISETPOINTCHRGN(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVCU_USETPOINTCHRGN(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_EPS(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = EPS_NSM.eps_nsm.RESERVED_EPS_0;
    pData[1] = EPS_NSM.eps_nsm.RESERVED_EPS_1;
    pData[2] = EPS_NSM.eps_nsm.RESERVED_EPS_2;
    pData[3] = EPS_NSM.eps_nsm.RESERVED_EPS_3;
    pData[4] = EPS_NSM.eps_nsm.RESERVED_EPS_4;
    pData[5] = EPS_NSM.eps_nsm.RESERVED_EPS_5;
    pData[6] = EPS_NSM.eps_nsm.RESERVED_EPS_6;
    pData[7] = EPS_NSM.eps_nsm.RESERVED_EPS_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetMASTER_CYL_PRESSURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC10_20.esc10_20.MASTER_CYL_PRESSURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC10_20.esc10_20.MASTER_CYL_PRESSURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetODO_DISTANCE_ESC12(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC12_10.esc12_10.ODO_DISTANCE_ESC12_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC12_10.esc12_10.ODO_DISTANCE_ESC12_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVEHICLE_SPEED_ESC12(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetVEHICLE_SPEED_ESC(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC2_10.esc2_10.VEHICLE_SPEED_ESC_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC2_10.esc2_10.VEHICLE_SPEED_ESC_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetODO_DISTANCE_ESC(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC2_10.esc2_10.ODO_DISTANCE_ESC_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC2_10.esc2_10.ODO_DISTANCE_ESC_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLATTERAL_ACCEL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC7_20.esc7_20.LATTERAL_ACCEL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC7_20.esc7_20.LATTERAL_ACCEL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLONG_ACCEL(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC7_20.esc7_20.LONG_ACCEL_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC7_20.esc7_20.LONG_ACCEL_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetYAW_RATE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC7_20.esc7_20.YAW_RATE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC7_20.esc7_20.YAW_RATE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetWHL_FL_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC8_20.esc8_20.WHL_FL_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC8_20.esc8_20.WHL_FL_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetWHL_FR_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) ESC8_20.esc8_20.WHL_FR_SPD_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) ESC8_20.esc8_20.WHL_FR_SPD_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetWHL_RL_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)ESC8_20.esc8_20.WHL_RL_SPD_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)ESC8_20.esc8_20.WHL_RL_SPD_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetWHL_RR_SPD(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) ESC8_20.esc8_20.WHL_RR_SPD_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) ESC8_20.esc8_20.WHL_RR_SPD_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_ESC(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = ESC_NSM.esc_nsm.RESERVED_ESC_0;
    pData[1] = ESC_NSM.esc_nsm.RESERVED_ESC_1;
    pData[2] = ESC_NSM.esc_nsm.RESERVED_ESC_2;
    pData[3] = ESC_NSM.esc_nsm.RESERVED_ESC_3;
    pData[4] = ESC_NSM.esc_nsm.RESERVED_ESC_4;
    pData[5] = ESC_NSM.esc_nsm.RESERVED_ESC_5;
    pData[6] = ESC_NSM.esc_nsm.RESERVED_ESC_6;
    pData[7] = ESC_NSM.esc_nsm.RESERVED_ESC_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetRESERVED_ESCL(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = ESCL_NSM.escl_nsm.RESERVED_ESCL_0;
    pData[1] = ESCL_NSM.escl_nsm.RESERVED_ESCL_1;
    pData[2] = ESCL_NSM.escl_nsm.RESERVED_ESCL_2;
    pData[3] = ESCL_NSM.escl_nsm.RESERVED_ESCL_3;
    pData[4] = ESCL_NSM.escl_nsm.RESERVED_ESCL_4;
    pData[5] = ESCL_NSM.escl_nsm.RESERVED_ESCL_5;
    pData[6] = ESCL_NSM.escl_nsm.RESERVED_ESCL_6;
    pData[7] = ESCL_NSM.escl_nsm.RESERVED_ESCL_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetRESERVED_FCM(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = FCM_NSM.fcm_nsm.RESERVED_FCM_0;
    pData[1] = FCM_NSM.fcm_nsm.RESERVED_FCM_1;
    pData[2] = FCM_NSM.fcm_nsm.RESERVED_FCM_2;
    pData[3] = FCM_NSM.fcm_nsm.RESERVED_FCM_3;
    pData[4] = FCM_NSM.fcm_nsm.RESERVED_FCM_4;
    pData[5] = FCM_NSM.fcm_nsm.RESERVED_FCM_5;
    pData[6] = FCM_NSM.fcm_nsm.RESERVED_FCM_6;
    pData[7] = FCM_NSM.fcm_nsm.RESERVED_FCM_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT8 IlRxGetACC_SET_DIST(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)FRM1_20.frm1_20.ACC_SET_DIST_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)FRM1_20.frm1_20.ACC_SET_DIST_1) << 1);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_FRM(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = FRM_NSM.frm_nsm.RESERVED_FRM_0;
    pData[1] = FRM_NSM.frm_nsm.RESERVED_FRM_1;
    pData[2] = FRM_NSM.frm_nsm.RESERVED_FRM_2;
    pData[3] = FRM_NSM.frm_nsm.RESERVED_FRM_3;
    pData[4] = FRM_NSM.frm_nsm.RESERVED_FRM_4;
    pData[5] = FRM_NSM.frm_nsm.RESERVED_FRM_5;
    pData[6] = FRM_NSM.frm_nsm.RESERVED_FRM_6;
    pData[7] = FRM_NSM.frm_nsm.RESERVED_FRM_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetIGN_CNTR(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_FCVOLTAGEVALUE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_SECONDARY_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_PRIMARY_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_MOSFET_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_INPUTVOLTAGEVALUE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_OUTPUTCURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetLDC_OUTPUTVOLTAGEVALUE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 IlRxGetLDC_STAGE(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)LDC3_100.ldc3_100.LDC_STAGE_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)LDC3_100.ldc3_100.LDC_STAGE_1) << 2);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetENG_OFF_TIME(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MBFM1_100.mbfm1_100.ENG_OFF_TIME_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MBFM1_100.mbfm1_100.ENG_OFF_TIME_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetRLS_FW_BRIGHTNESS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetRLS_AMB_BRIGHTNESS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_1) <<6);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_CURRENT_MBFM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_BATT_VOLT_MBFM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetIBS_BATT_TEMP_MBFM(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_MBFM(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_0;
    pData[1] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_1;
    pData[2] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_2;
    pData[3] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_3;
    pData[4] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_4;
    pData[5] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_5;
    pData[6] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_6;
    pData[7] = MBFM_NSM.mbfm_nsm.RESERVED_MBFM_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetRESERVED_EMS_SP(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_0;
    pData[1] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_1;
    pData[2] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_2;
    pData[3] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_3;
    pData[4] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_4;
    pData[5] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_5;
    pData[6] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_6;
    pData[7] = SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetMCU_MOTORTORQUEESTIMATED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMCU_MOTORSPEED(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU2_10.mcu2_10.MCU_MOTORSPEED_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU2_10.mcu2_10.MCU_MOTORSPEED_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMCU_REGENTORQUEAVAIL_QUASI(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMCU_TRACTIONTORQUEAVAIL_QUASI(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMCU_HIGHPOWERVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetMCU_HIGHPOWERCURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_DCCURRENTCAPABLE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_DCVOLTAGECAPABLE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_PFC_VOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC3_100.obc3_100.OBC_PFC_VOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC3_100.obc3_100.OBC_PFC_VOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_LINE_FREQUENCY(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC3_100.obc3_100.OBC_LINE_FREQUENCY_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC3_100.obc3_100.OBC_LINE_FREQUENCY_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_LV_PWRSUPPLY(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_PRIMARYSIDE_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_TRANSFORMER_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT8 IlRxGetOBC_COOLINGREQUEST(void)
{
   CAN_UINT8  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT8)OBC1_100.obc1_100.OBC_COOLINGREQUEST_0;
   rValue |= (CAN_UINT8)(((CAN_UINT8)OBC1_100.obc1_100.OBC_COOLINGREQUEST_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_SECONDARYSIDE_TEMPERATURE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16) OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_0;
   rValue |= (CAN_UINT16)(((CAN_UINT16) OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_1) << 4);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_INDUCTOR_CURRENT_L1_RMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_INDUCTOR_CURRENT_L2_RMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_ACINPUTCURRENTRMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_ACINPUTVOLTAGERMS(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_DCOUTPUTCURRENT(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetOBC_DCOUTPUTVOLTAGE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_PKE(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_0;
    pData[1] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_1;
    pData[2] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_2;
    pData[3] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_3;
    pData[4] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_4;
    pData[5] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_5;
    pData[6] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_6;
    pData[7] = PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetIMMOVAL5(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_0;
    pData[1] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_1;
    pData[2] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_2;
    pData[3] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_3;
    pData[4] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_4;
    pData[5] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_5;
    pData[6] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_6;
    pData[7] = PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

CAN_UINT16 IlRxGetABSOLUTE_ANGLE(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)SAS1_10.sas1_10.ABSOLUTE_ANGLE_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)SAS1_10.sas1_10.ABSOLUTE_ANGLE_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

CAN_UINT16 IlRxGetCUR_CARD_SHAFT_TRQ(void)
{
   CAN_UINT16  rValue;
    CAN_ENTER_CRITICAL_SECTION(0);
   rValue = (CAN_UINT16)((CAN_UINT16)TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_0);
   rValue |= (CAN_UINT16)(((CAN_UINT16)TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_1) << 8);
   CAN_EXIT_CRITICAL_SECTION(0);
   return rValue;
}

void IlRxGetRESERVED_TC(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = TC_NSM.tc_nsm.RESERVED_TC_0;
    pData[1] = TC_NSM.tc_nsm.RESERVED_TC_1;
    pData[2] = TC_NSM.tc_nsm.RESERVED_TC_2;
    pData[3] = TC_NSM.tc_nsm.RESERVED_TC_3;
    pData[4] = TC_NSM.tc_nsm.RESERVED_TC_4;
    pData[5] = TC_NSM.tc_nsm.RESERVED_TC_5;
    pData[6] = TC_NSM.tc_nsm.RESERVED_TC_6;
    pData[7] = TC_NSM.tc_nsm.RESERVED_TC_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

void IlRxGetRESERVED_WLC(CAN_UINT8 * pData)
{

    CAN_ENTER_CRITICAL_SECTION(0);
    pData[0] = WLC_NSM.wlc_nsm.RESERVED_WLC_0;
    pData[1] = WLC_NSM.wlc_nsm.RESERVED_WLC_1;
    pData[2] = WLC_NSM.wlc_nsm.RESERVED_WLC_2;
    pData[3] = WLC_NSM.wlc_nsm.RESERVED_WLC_3;
    pData[4] = WLC_NSM.wlc_nsm.RESERVED_WLC_4;
    pData[5] = WLC_NSM.wlc_nsm.RESERVED_WLC_5;
    pData[6] = WLC_NSM.wlc_nsm.RESERVED_WLC_6;
    pData[7] = WLC_NSM.wlc_nsm.RESERVED_WLC_7;
   CAN_EXIT_CRITICAL_SECTION(0);
}

/* ====================================================================================
   Interaction Layer Receive Message Precopy Functions
   ==================================================================================*/

void ACC1_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ACC1_500.acc1_500.ACC_INPUT_DC_CURRENT != Rx_buffer.acc1_500.ACC_INPUT_DC_CURRENT))
     {
         ILSet_ACC_INPUT_DC_CURRENT_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_MOTOR_OVERHEAT_FAULT != Rx_buffer.acc1_500.ACC_MOTOR_OVERHEAT_FAULT))
     {
         ILSet_ACC_MOTOR_OVERHEAT_FAULT_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_UNDERVOLTAGE_FAULT != Rx_buffer.acc1_500.ACC_UNDERVOLTAGE_FAULT))
     {
         ILSet_ACC_UNDERVOLTAGE_FAULT_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_OVERVOLTAGE_FAULT != Rx_buffer.acc1_500.ACC_OVERVOLTAGE_FAULT))
     {
         ILSet_ACC_OVERVOLTAGE_FAULT_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_OVERCURRENT_FAULT != Rx_buffer.acc1_500.ACC_OVERCURRENT_FAULT))
     {
         ILSet_ACC_OVERCURRENT_FAULT_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_CONTROLLER_OVERHEAT_FAULT != Rx_buffer.acc1_500.ACC_CONTROLLER_OVERHEAT_FAULT))
     {
         ILSet_ACC_CONTROLLER_OVERHEAT_FAULT_DataChanged();
     }

     if((ACC1_500.acc1_500.STS_ACC_COMPRESSOR != Rx_buffer.acc1_500.STS_ACC_COMPRESSOR))
     {
         ILSet_STS_ACC_COMPRESSOR_DataChanged();
     }

     if((ACC1_500.acc1_500.ACC_COM_FAULT != Rx_buffer.acc1_500.ACC_COM_FAULT))
     {
         ILSet_ACC_COM_FAULT_DataChanged();
     }

   }
}

void ACC2_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ACC2_500.acc2_500.COMPRESSOR_TEMPERATURE != Rx_buffer.acc2_500.COMPRESSOR_TEMPERATURE))
     {
         ILSet_COMPRESSOR_TEMPERATURE_DataChanged();
     }

     if((ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_0 != Rx_buffer.acc2_500.ACC_CTRL_OUTPUT_POWER_0) || 
       (ACC2_500.acc2_500.ACC_CTRL_OUTPUT_POWER_1 != Rx_buffer.acc2_500.ACC_CTRL_OUTPUT_POWER_1))
     {
         ILSet_ACC_CTRL_OUTPUT_POWER_DataChanged();
     }

     if((ACC2_500.acc2_500.ACC_HVIL_STATUS != Rx_buffer.acc2_500.ACC_HVIL_STATUS))
     {
         ILSet_ACC_HVIL_STATUS_DataChanged();
     }

   }
}

void AMT5_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((AMT5_20.amt5_20.GEAR_ACTUAL_AMT != Rx_buffer.amt5_20.GEAR_ACTUAL_AMT))
     {
         ILSet_GEAR_ACTUAL_AMT_DataChanged();
     }

     if((AMT5_20.amt5_20.TCU_SHIFT_MODE != Rx_buffer.amt5_20.TCU_SHIFT_MODE))
     {
         ILSet_TCU_SHIFT_MODE_DataChanged();
     }

     if((AMT5_20.amt5_20.TGS_MODE_AMT != Rx_buffer.amt5_20.TGS_MODE_AMT))
     {
         ILSet_TGS_MODE_AMT_DataChanged();
     }

     if((AMT5_20.amt5_20.ENGINE_STOP_AMT != Rx_buffer.amt5_20.ENGINE_STOP_AMT))
     {
         ILSet_ENGINE_STOP_AMT_DataChanged();
     }

   }
}

void AMT6_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((AMT6_20.amt6_20.TGS_LEVER_AMT != Rx_buffer.amt6_20.TGS_LEVER_AMT))
     {
         ILSet_TGS_LEVER_AMT_DataChanged();
     }

     if((AMT6_20.amt6_20.AMT_MIL != Rx_buffer.amt6_20.AMT_MIL))
     {
         ILSet_AMT_MIL_DataChanged();
     }

     if((AMT6_20.amt6_20.ALERT_AMT != Rx_buffer.amt6_20.ALERT_AMT))
     {
         ILSet_ALERT_AMT_DataChanged();
     }

     if((AMT6_20.amt6_20.AMT_BUZZER != Rx_buffer.amt6_20.AMT_BUZZER))
     {
         ILSet_AMT_BUZZER_DataChanged();
     }

   }
}

void APA2_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((APA2_50.apa2_50.FL_SEGMENT != Rx_buffer.apa2_50.FL_SEGMENT))
     {
         ILSet_FL_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.FML_SEGMENT != Rx_buffer.apa2_50.FML_SEGMENT))
     {
         ILSet_FML_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.FMR_SEGMENT != Rx_buffer.apa2_50.FMR_SEGMENT))
     {
         ILSet_FMR_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.FR_SEGMENT != Rx_buffer.apa2_50.FR_SEGMENT))
     {
         ILSet_FR_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.RL_SEGMENT != Rx_buffer.apa2_50.RL_SEGMENT))
     {
         ILSet_RL_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.RML_SEGMENT != Rx_buffer.apa2_50.RML_SEGMENT))
     {
         ILSet_RML_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.RMR_SEGMENT != Rx_buffer.apa2_50.RMR_SEGMENT))
     {
         ILSet_RMR_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.RR_SEGMENT != Rx_buffer.apa2_50.RR_SEGMENT))
     {
         ILSet_RR_SEGMENT_DataChanged();
     }

     if((APA2_50.apa2_50.FL_SEG_WARN != Rx_buffer.apa2_50.FL_SEG_WARN))
     {
         ILSet_FL_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.FML_SEG_WARN != Rx_buffer.apa2_50.FML_SEG_WARN))
     {
         ILSet_FML_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.FMR_SEG_WARN != Rx_buffer.apa2_50.FMR_SEG_WARN))
     {
         ILSet_FMR_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.FR_SEG_WARN != Rx_buffer.apa2_50.FR_SEG_WARN))
     {
         ILSet_FR_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.RL_SEG_WARN != Rx_buffer.apa2_50.RL_SEG_WARN))
     {
         ILSet_RL_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.RML_SEG_WARN != Rx_buffer.apa2_50.RML_SEG_WARN))
     {
         ILSet_RML_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.RMR_SEG_WARN != Rx_buffer.apa2_50.RMR_SEG_WARN))
     {
         ILSet_RMR_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.RR_SEG_WARN != Rx_buffer.apa2_50.RR_SEG_WARN))
     {
         ILSet_RR_SEG_WARN_DataChanged();
     }

     if((APA2_50.apa2_50.FRONT_MIN_DIST != Rx_buffer.apa2_50.FRONT_MIN_DIST))
     {
         ILSet_FRONT_MIN_DIST_DataChanged();
     }

     if((APA2_50.apa2_50.REAR_MIN_DIST != Rx_buffer.apa2_50.REAR_MIN_DIST))
     {
         ILSet_REAR_MIN_DIST_DataChanged();
     }

     if((APA2_50.apa2_50.RPAS_ACTIVE_STS1 != Rx_buffer.apa2_50.RPAS_ACTIVE_STS1))
     {
         ILSet_RPAS_ACTIVE_STS1_DataChanged();
     }

     if((APA2_50.apa2_50.FPAS_SPAS_ACTIVE_STS != Rx_buffer.apa2_50.FPAS_SPAS_ACTIVE_STS))
     {
         ILSet_FPAS_SPAS_ACTIVE_STS_DataChanged();
     }

   }
}

void APA3_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((APA3_50.apa3_50.FLS_SEGMENT != Rx_buffer.apa3_50.FLS_SEGMENT))
     {
         ILSet_FLS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.FLMS_SEGMENT != Rx_buffer.apa3_50.FLMS_SEGMENT))
     {
         ILSet_FLMS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.FRMS_SEGMENT != Rx_buffer.apa3_50.FRMS_SEGMENT))
     {
         ILSet_FRMS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.FRS_SEGMENT != Rx_buffer.apa3_50.FRS_SEGMENT))
     {
         ILSet_FRS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.RLS_SEGMENT != Rx_buffer.apa3_50.RLS_SEGMENT))
     {
         ILSet_RLS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.RLMS_SEGMENT != Rx_buffer.apa3_50.RLMS_SEGMENT))
     {
         ILSet_RLMS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.RRMS_SEGMENT != Rx_buffer.apa3_50.RRMS_SEGMENT))
     {
         ILSet_RRMS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.RRS_SEGMENT != Rx_buffer.apa3_50.RRS_SEGMENT))
     {
         ILSet_RRS_SEGMENT_DataChanged();
     }

     if((APA3_50.apa3_50.FLS_SEG_WARN != Rx_buffer.apa3_50.FLS_SEG_WARN))
     {
         ILSet_FLS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.FLMS_SEG_WARN != Rx_buffer.apa3_50.FLMS_SEG_WARN))
     {
         ILSet_FLMS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.FRMS_SEG_WARN != Rx_buffer.apa3_50.FRMS_SEG_WARN))
     {
         ILSet_FRMS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.FRS_SEG_WARN != Rx_buffer.apa3_50.FRS_SEG_WARN))
     {
         ILSet_FRS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.RLS_SEG_WARN != Rx_buffer.apa3_50.RLS_SEG_WARN))
     {
         ILSet_RLS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.RLMS_SEG_WARN != Rx_buffer.apa3_50.RLMS_SEG_WARN))
     {
         ILSet_RLMS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.RRMS_SEG_WARN != Rx_buffer.apa3_50.RRMS_SEG_WARN))
     {
         ILSet_RRMS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.RRS_SEG_WARN != Rx_buffer.apa3_50.RRS_SEG_WARN))
     {
         ILSet_RRS_SEG_WARN_DataChanged();
     }

     if((APA3_50.apa3_50.LEFT_MIN_DIST != Rx_buffer.apa3_50.LEFT_MIN_DIST))
     {
         ILSet_LEFT_MIN_DIST_DataChanged();
     }

     if((APA3_50.apa3_50.RIGHT_MIN_DIST != Rx_buffer.apa3_50.RIGHT_MIN_DIST))
     {
         ILSet_RIGHT_MIN_DIST_DataChanged();
     }

     if((APA3_50.apa3_50.APA_LED_FAULT != Rx_buffer.apa3_50.APA_LED_FAULT))
     {
         ILSet_APA_LED_FAULT_DataChanged();
     }

     if((APA3_50.apa3_50.APA_SWITCH_FAULT != Rx_buffer.apa3_50.APA_SWITCH_FAULT))
     {
         ILSet_APA_SWITCH_FAULT_DataChanged();
     }

   }
}

void APA4_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((APA4_50.apa4_50.APA_PROGRESS_PERCNTG != Rx_buffer.apa4_50.APA_PROGRESS_PERCNTG))
     {
         ILSet_APA_PROGRESS_PERCNTG_DataChanged();
     }

     if((APA4_50.apa4_50.DIST_TO_SAFE_PT != Rx_buffer.apa4_50.DIST_TO_SAFE_PT))
     {
         ILSet_DIST_TO_SAFE_PT_DataChanged();
     }

     if((APA4_50.apa4_50.DIST_TO_SLOT != Rx_buffer.apa4_50.DIST_TO_SLOT))
     {
         ILSet_DIST_TO_SLOT_DataChanged();
     }

     if((APA4_50.apa4_50.SLOT_LENGTH_WIDTH != Rx_buffer.apa4_50.SLOT_LENGTH_WIDTH))
     {
         ILSet_SLOT_LENGTH_WIDTH_DataChanged();
     }

     if((APA4_50.apa4_50.SLOT_DEPTH != Rx_buffer.apa4_50.SLOT_DEPTH))
     {
         ILSet_SLOT_DEPTH_DataChanged();
     }

     if((APA4_50.apa4_50.APA_PARK_DIRCTION != Rx_buffer.apa4_50.APA_PARK_DIRCTION))
     {
         ILSet_APA_PARK_DIRCTION_DataChanged();
     }

     if((APA4_50.apa4_50.APA_DISP_MAIN_PIC != Rx_buffer.apa4_50.APA_DISP_MAIN_PIC))
     {
         ILSet_APA_DISP_MAIN_PIC_DataChanged();
     }

     if((APA4_50.apa4_50.APA_DISP_SUB_PIC != Rx_buffer.apa4_50.APA_DISP_SUB_PIC))
     {
         ILSet_APA_DISP_SUB_PIC_DataChanged();
     }

     if((APA4_50.apa4_50.APA_PARK_MODE != Rx_buffer.apa4_50.APA_PARK_MODE))
     {
         ILSet_APA_PARK_MODE_DataChanged();
     }

     if((APA4_50.apa4_50.APA_DISP != Rx_buffer.apa4_50.APA_DISP))
     {
         ILSet_APA_DISP_DataChanged();
     }

     if((APA4_50.apa4_50.APA_ACTIVE != Rx_buffer.apa4_50.APA_ACTIVE))
     {
         ILSet_APA_ACTIVE_DataChanged();
     }

     if((APA4_50.apa4_50.FPAS_SW_STS != Rx_buffer.apa4_50.FPAS_SW_STS))
     {
         ILSet_FPAS_SW_STS_DataChanged();
     }

     if((APA4_50.apa4_50.MAMS_SWT_STS != Rx_buffer.apa4_50.MAMS_SWT_STS))
     {
         ILSet_MAMS_SWT_STS_DataChanged();
     }

     if((APA4_50.apa4_50.APA_INHIBIT_ST != Rx_buffer.apa4_50.APA_INHIBIT_ST))
     {
         ILSet_APA_INHIBIT_ST_DataChanged();
     }

     if((APA4_50.apa4_50.APA_MAMS_ACTIVE != Rx_buffer.apa4_50.APA_MAMS_ACTIVE))
     {
         ILSet_APA_MAMS_ACTIVE_DataChanged();
     }

   }
}

void APA_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((APA_NSM.apa_nsm.RESERVED_APA_0 != Rx_buffer.apa_nsm.RESERVED_APA_0) || 
       (APA_NSM.apa_nsm.RESERVED_APA_1 != Rx_buffer.apa_nsm.RESERVED_APA_1) || 
       (APA_NSM.apa_nsm.RESERVED_APA_2 != Rx_buffer.apa_nsm.RESERVED_APA_2) || 
       (APA_NSM.apa_nsm.RESERVED_APA_3 != Rx_buffer.apa_nsm.RESERVED_APA_3) || 
       (APA_NSM.apa_nsm.RESERVED_APA_4 != Rx_buffer.apa_nsm.RESERVED_APA_4) || 
       (APA_NSM.apa_nsm.RESERVED_APA_5 != Rx_buffer.apa_nsm.RESERVED_APA_5) || 
       (APA_NSM.apa_nsm.RESERVED_APA_6 != Rx_buffer.apa_nsm.RESERVED_APA_6) || 
       (APA_NSM.apa_nsm.RESERVED_APA_7 != Rx_buffer.apa_nsm.RESERVED_APA_7))
     {
         ILSet_RESERVED_APA_DataChanged();
     }

   }
}

void BMS10_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS10_100.bms10_100.BMS_STS_IGN != Rx_buffer.bms10_100.BMS_STS_IGN))
     {
         ILSet_BMS_STS_IGN_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BMINUSCONTACTORWELD != Rx_buffer.bms10_100.BMS_BMINUSCONTACTORWELD))
     {
         ILSet_BMS_BMINUSCONTACTORWELD_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BPLUSCONTACTORWELD != Rx_buffer.bms10_100.BMS_BPLUSCONTACTORWELD))
     {
         ILSet_BMS_BPLUSCONTACTORWELD_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_CELLVOLTHIGHWARNDEGDFAULT != Rx_buffer.bms10_100.BMS_CELLVOLTHIGHWARNDEGDFAULT))
     {
         ILSet_BMS_CELLVOLTHIGHWARNDEGDFAULT_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BATTERYLOWSOC != Rx_buffer.bms10_100.BMS_BATTERYLOWSOC))
     {
         ILSet_BMS_BATTERYLOWSOC_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BATTBALANCINGCOMPSTA != Rx_buffer.bms10_100.BMS_BATTBALANCINGCOMPSTA))
     {
         ILSet_BMS_BATTBALANCINGCOMPSTA_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_0 != Rx_buffer.bms10_100.BMS_BATTERYAVGTEMPERATURE_0) || 
       (BMS10_100.bms10_100.BMS_BATTERYAVGTEMPERATURE_1 != Rx_buffer.bms10_100.BMS_BATTERYAVGTEMPERATURE_1))
     {
         ILSet_BMS_BATTERYAVGTEMPERATURE_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BCOOLPUMPFBSTA != Rx_buffer.bms10_100.BMS_BCOOLPUMPFBSTA))
     {
         ILSet_BMS_BCOOLPUMPFBSTA_DataChanged();
     }

     if((BMS10_100.bms10_100.BMS_BATTERYBALANCINGSTA != Rx_buffer.bms10_100.BMS_BATTERYBALANCINGSTA))
     {
         ILSet_BMS_BATTERYBALANCINGSTA_DataChanged();
     }

   }
}

void BMS11_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_0 != Rx_buffer.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_0) || 
       (BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_1 != Rx_buffer.bms11_100.BMS_BATTERYINLETCOOLANTTEMP_1))
     {
         ILSet_BMS_BATTERYINLETCOOLANTTEMP_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_CHILLERSOLENIODSTA != Rx_buffer.bms11_100.BMS_CHILLERSOLENIODSTA))
     {
         ILSet_BMS_CHILLERSOLENIODSTA_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_BATTERYPRECONDITIONINGSTA != Rx_buffer.bms11_100.BMS_BATTERYPRECONDITIONINGSTA))
     {
         ILSet_BMS_BATTERYPRECONDITIONINGSTA_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_0 != Rx_buffer.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_0) || 
       (BMS11_100.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_1 != Rx_buffer.bms11_100.BMS_BATTERYINLETCOOLANTTEMPREQ_1))
     {
         ILSet_BMS_BATTERYINLETCOOLANTTEMPREQ_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_COOLINGHEATINGSTA != Rx_buffer.bms11_100.BMS_COOLINGHEATINGSTA))
     {
         ILSet_BMS_COOLINGHEATINGSTA_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_0 != Rx_buffer.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_0) || 
       (BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_1 != Rx_buffer.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_1) || 
       (BMS11_100.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_2 != Rx_buffer.bms11_100.BMS_BATTERYOUTLETCOOLANTTEMP_2))
     {
         ILSet_BMS_BATTERYOUTLETCOOLANTTEMP_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_BHEATERFLT != Rx_buffer.bms11_100.BMS_BHEATERFLT))
     {
         ILSet_BMS_BHEATERFLT_DataChanged();
     }

     if((BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_0 != Rx_buffer.bms11_100.BMS_BHEATEROPCOOLANTTEMP_0) || 
       (BMS11_100.bms11_100.BMS_BHEATEROPCOOLANTTEMP_1 != Rx_buffer.bms11_100.BMS_BHEATEROPCOOLANTTEMP_1))
     {
         ILSet_BMS_BHEATEROPCOOLANTTEMP_DataChanged();
     }

   }
}

void BMS14_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS14_100.bms14_100.BMS_EVWARNING_TT != Rx_buffer.bms14_100.BMS_EVWARNING_TT))
     {
         ILSet_BMS_EVWARNING_TT_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_HIGH_TEMP_LIGHT_OP_TT != Rx_buffer.bms14_100.BMS_HIGH_TEMP_LIGHT_OP_TT))
     {
         ILSet_BMS_HIGH_TEMP_LIGHT_OP_TT_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_HV_BATT_TT != Rx_buffer.bms14_100.BMS_HV_BATT_TT))
     {
         ILSet_BMS_HV_BATT_TT_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_STS_CHARGE_LIGHT_TT != Rx_buffer.bms14_100.BMS_STS_CHARGE_LIGHT_TT))
     {
         ILSet_BMS_STS_CHARGE_LIGHT_TT_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_SERVICE_LIGHT_TT != Rx_buffer.bms14_100.BMS_SERVICE_LIGHT_TT))
     {
         ILSet_BMS_SERVICE_LIGHT_TT_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_ALERT_MSGS != Rx_buffer.bms14_100.BMS_ALERT_MSGS))
     {
         ILSet_BMS_ALERT_MSGS_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_AVEENERGYCONS_0 != Rx_buffer.bms14_100.BMS_AVEENERGYCONS_0) || 
       (BMS14_100.bms14_100.BMS_AVEENERGYCONS_1 != Rx_buffer.bms14_100.BMS_AVEENERGYCONS_1))
     {
         ILSet_BMS_AVEENERGYCONS_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_0 != Rx_buffer.bms14_100.BMS_BATTERYINSTANTENERGYCONS_0) || 
       (BMS14_100.bms14_100.BMS_BATTERYINSTANTENERGYCONS_1 != Rx_buffer.bms14_100.BMS_BATTERYINSTANTENERGYCONS_1))
     {
         ILSet_BMS_BATTERYINSTANTENERGYCONS_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS3D5_COUNTER != Rx_buffer.bms14_100.BMS3D5_COUNTER))
     {
         ILSet_BMS3D5_COUNTER_DataChanged();
     }

     if((BMS14_100.bms14_100.BMS3D5_CRC != Rx_buffer.bms14_100.BMS3D5_CRC))
     {
         ILSet_BMS3D5_CRC_DataChanged();
     }

   }
}

void BMS16_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS16_10.bms16_10.BMS_REASON_DERATING != Rx_buffer.bms16_10.BMS_REASON_DERATING))
     {
         ILSet_BMS_REASON_DERATING_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BATTOVERVOLT_CUTOFF_CHARGE != Rx_buffer.bms16_10.BMS_BATTOVERVOLT_CUTOFF_CHARGE))
     {
         ILSet_BMS_BATTOVERVOLT_CUTOFF_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CELLOVERVOLT_CUTOFF_CHARGE != Rx_buffer.bms16_10.BMS_CELLOVERVOLT_CUTOFF_CHARGE))
     {
         ILSet_BMS_CELLOVERVOLT_CUTOFF_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_REASON_HV_DISCONNECT_REQUEST != Rx_buffer.bms16_10.BMS_REASON_HV_DISCONNECT_REQUEST))
     {
         ILSet_BMS_REASON_HV_DISCONNECT_REQUEST_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTINLET_LOW_TEMP_CHARGE != Rx_buffer.bms16_10.BMS_CLNTINLET_LOW_TEMP_CHARGE))
     {
         ILSet_BMS_CLNTINLET_LOW_TEMP_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTINLET_HIGH_TEMP_CHARGE != Rx_buffer.bms16_10.BMS_CLNTINLET_HIGH_TEMP_CHARGE))
     {
         ILSet_BMS_CLNTINLET_HIGH_TEMP_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_REASON_HV_DISCONNECTED != Rx_buffer.bms16_10.BMS_REASON_HV_DISCONNECTED))
     {
         ILSet_BMS_REASON_HV_DISCONNECTED_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_PLP_STOP_CHARGE != Rx_buffer.bms16_10.BMS_PLP_STOP_CHARGE))
     {
         ILSet_BMS_PLP_STOP_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_REVERSECURRDETECT_CHARGE != Rx_buffer.bms16_10.BMS_REVERSECURRDETECT_CHARGE))
     {
         ILSet_BMS_REVERSECURRDETECT_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTSEN_THRES_FAULT_CHARGE != Rx_buffer.bms16_10.BMS_CLNTSEN_THRES_FAULT_CHARGE))
     {
         ILSet_BMS_CLNTSEN_THRES_FAULT_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTOUTLET_LOW_TEMP_CHARGE != Rx_buffer.bms16_10.BMS_CLNTOUTLET_LOW_TEMP_CHARGE))
     {
         ILSet_BMS_CLNTOUTLET_LOW_TEMP_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTOUTLET_HIGH_TEMP_CHARGE != Rx_buffer.bms16_10.BMS_CLNTOUTLET_HIGH_TEMP_CHARGE))
     {
         ILSet_BMS_CLNTOUTLET_HIGH_TEMP_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CRASHDTCT_P_F_OPEN_COMMON != Rx_buffer.bms16_10.BMS_CRASHDTCT_P_F_OPEN_COMMON))
     {
         ILSet_BMS_CRASHDTCT_P_F_OPEN_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_PUMP_DRYRUN_ERR_COMMON != Rx_buffer.bms16_10.BMS_PUMP_DRYRUN_ERR_COMMON))
     {
         ILSet_BMS_PUMP_DRYRUN_ERR_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_MDLEUNDERTEMP_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_MDLEUNDERTEMP_CUTOFF_COMMON))
     {
         ILSet_BMS_MDLEUNDERTEMP_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_MODULEOVERTEMP_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_MODULEOVERTEMP_CUTOFF_COMMON))
     {
         ILSet_BMS_MODULEOVERTEMP_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BATTUNDERVOLT_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_BATTUNDERVOLT_CUTOFF_COMMON))
     {
         ILSet_BMS_BATTUNDERVOLT_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CELLUNDERVOLT_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_CELLUNDERVOLT_CUTOFF_COMMON))
     {
         ILSet_BMS_CELLUNDERVOLT_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BATTUNDER_TEMP_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_BATTUNDER_TEMP_CUTOFF_COMMON))
     {
         ILSet_BMS_BATTUNDER_TEMP_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BATTOVER_TEMP_CUTOFF_COMMON != Rx_buffer.bms16_10.BMS_BATTOVER_TEMP_CUTOFF_COMMON))
     {
         ILSet_BMS_BATTOVER_TEMP_CUTOFF_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNTSYS_FLT_COMMON != Rx_buffer.bms16_10.BMS_CLNTSYS_FLT_COMMON))
     {
         ILSet_BMS_CLNTSYS_FLT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_MTM_ACTVLIMIT_COMMON != Rx_buffer.bms16_10.BMS_MTM_ACTVLIMIT_COMMON))
     {
         ILSet_BMS_MTM_ACTVLIMIT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_REVIVE_COMMON != Rx_buffer.bms16_10.BMS_REVIVE_COMMON))
     {
         ILSet_BMS_REVIVE_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_PILOTLINE_DETECT_COMMON != Rx_buffer.bms16_10.BMS_PILOTLINE_DETECT_COMMON))
     {
         ILSet_BMS_PILOTLINE_DETECT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_IBATT_392_25SEC_COMMON != Rx_buffer.bms16_10.BMS_IBATT_392_25SEC_COMMON))
     {
         ILSet_BMS_IBATT_392_25SEC_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_SENSOR_FAILURE_COMMON != Rx_buffer.bms16_10.BMS_SENSOR_FAILURE_COMMON))
     {
         ILSet_BMS_SENSOR_FAILURE_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_SHORTCIRCUITCURR_FLT_COMMON != Rx_buffer.bms16_10.BMS_SHORTCIRCUITCURR_FLT_COMMON))
     {
         ILSet_BMS_SHORTCIRCUITCURR_FLT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BATTPACK_PWRLIMITERR_COMMON != Rx_buffer.bms16_10.BMS_BATTPACK_PWRLIMITERR_COMMON))
     {
         ILSet_BMS_BATTPACK_PWRLIMITERR_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BAT_I_EXTCURR_FLT_DISCHRG != Rx_buffer.bms16_10.BMS_BAT_I_EXTCURR_FLT_DISCHRG))
     {
         ILSet_BMS_BAT_I_EXTCURR_FLT_DISCHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BAT_I_OVREXTCURR_FLT_DISCHRG != Rx_buffer.bms16_10.BMS_BAT_I_OVREXTCURR_FLT_DISCHRG))
     {
         ILSet_BMS_BAT_I_OVREXTCURR_FLT_DISCHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BAT_I_OVERCURR_FLT_DISCHARGE != Rx_buffer.bms16_10.BMS_BAT_I_OVERCURR_FLT_DISCHARGE))
     {
         ILSet_BMS_BAT_I_OVERCURR_FLT_DISCHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_LOWSOC_CUTOFF_DISCHARGE != Rx_buffer.bms16_10.BMS_LOWSOC_CUTOFF_DISCHARGE))
     {
         ILSet_BMS_LOWSOC_CUTOFF_DISCHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_ISOFLT_RED_DISCHARGE != Rx_buffer.bms16_10.BMS_ISOFLT_RED_DISCHARGE))
     {
         ILSet_BMS_ISOFLT_RED_DISCHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_HEATER_FLT_COMMON != Rx_buffer.bms16_10.BMS_HEATER_FLT_COMMON))
     {
         ILSet_BMS_HEATER_FLT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CLNT_TEMPSENS_FLT_COMMON != Rx_buffer.bms16_10.BMS_CLNT_TEMPSENS_FLT_COMMON))
     {
         ILSet_BMS_CLNT_TEMPSENS_FLT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_HEATERSYS_FLT_COMMON != Rx_buffer.bms16_10.BMS_HEATERSYS_FLT_COMMON))
     {
         ILSet_BMS_HEATERSYS_FLT_COMMON_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_FSPLP_BACVDRTDMODE != Rx_buffer.bms16_10.BMS_FSPLP_BACVDRTDMODE))
     {
         ILSet_BMS_FSPLP_BACVDRTDMODE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_FSBIM_BACVDRTDMODE != Rx_buffer.bms16_10.BMS_FSBIM_BACVDRTDMODE))
     {
         ILSet_BMS_FSBIM_BACVDRTDMODE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_INITCNTCTROPEN_CHARGE != Rx_buffer.bms16_10.BMS_INITCNTCTROPEN_CHARGE))
     {
         ILSet_BMS_INITCNTCTROPEN_CHARGE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_INITCNTCTROPEN_DISCHRG != Rx_buffer.bms16_10.BMS_INITCNTCTROPEN_DISCHRG))
     {
         ILSet_BMS_INITCNTCTROPEN_DISCHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CNTCTROPEN_RQST_VCU_DISCHRG != Rx_buffer.bms16_10.BMS_CNTCTROPEN_RQST_VCU_DISCHRG))
     {
         ILSet_BMS_CNTCTROPEN_RQST_VCU_DISCHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CNTCTROPEN_RQST_VCU_CHRG != Rx_buffer.bms16_10.BMS_CNTCTROPEN_RQST_VCU_CHRG))
     {
         ILSet_BMS_CNTCTROPEN_RQST_VCU_CHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_NO_CNTCTR_CLOSE != Rx_buffer.bms16_10.BMS_NO_CNTCTR_CLOSE))
     {
         ILSet_BMS_NO_CNTCTR_CLOSE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_HVIL_ERR_DISCHRG != Rx_buffer.bms16_10.BMS_HVIL_ERR_DISCHRG))
     {
         ILSet_BMS_HVIL_ERR_DISCHRG_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_CUM_BACVOWDRTD != Rx_buffer.bms16_10.BMS_CUM_BACVOWDRTD))
     {
         ILSet_BMS_CUM_BACVOWDRTD_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BTFD_BACVREQDRTDMODE != Rx_buffer.bms16_10.BMS_BTFD_BACVREQDRTDMODE))
     {
         ILSet_BMS_BTFD_BACVREQDRTDMODE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BIMBACVREQDRTDMODE != Rx_buffer.bms16_10.BMS_BIMBACVREQDRTDMODE))
     {
         ILSet_BMS_BIMBACVREQDRTDMODE_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_BIM_BACVHIGHRATEDCHADRDT2 != Rx_buffer.bms16_10.BMS_BIM_BACVHIGHRATEDCHADRDT2))
     {
         ILSet_BMS_BIM_BACVHIGHRATEDCHADRDT2_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_ILC_ACVDRTDCDN != Rx_buffer.bms16_10.BMS_ILC_ACVDRTDCDN))
     {
         ILSet_BMS_ILC_ACVDRTDCDN_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_IDMSTSISINERR_YELLOW != Rx_buffer.bms16_10.BMS_IDMSTSISINERR_YELLOW))
     {
         ILSet_BMS_IDMSTSISINERR_YELLOW_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_FSPLP_BACVPACKUNDERUDRTD != Rx_buffer.bms16_10.BMS_FSPLP_BACVPACKUNDERUDRTD))
     {
         ILSet_BMS_FSPLP_BACVPACKUNDERUDRTD_DataChanged();
     }

     if((BMS16_10.bms16_10.BMS_FSPLP_BACVPACKOVERUDRTD != Rx_buffer.bms16_10.BMS_FSPLP_BACVPACKOVERUDRTD))
     {
         ILSet_BMS_FSPLP_BACVPACKOVERUDRTD_DataChanged();
     }

   }
}

void BMS17_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS17_100.bms17_100.BMS_AMPEREHOUR_0 != Rx_buffer.bms17_100.BMS_AMPEREHOUR_0) || 
       (BMS17_100.bms17_100.BMS_AMPEREHOUR_1 != Rx_buffer.bms17_100.BMS_AMPEREHOUR_1))
     {
         ILSet_BMS_AMPEREHOUR_DataChanged();
     }

     if((BMS17_100.bms17_100.BMS_KILOWATTHOUR_0 != Rx_buffer.bms17_100.BMS_KILOWATTHOUR_0) || 
       (BMS17_100.bms17_100.BMS_KILOWATTHOUR_1 != Rx_buffer.bms17_100.BMS_KILOWATTHOUR_1))
     {
         ILSet_BMS_KILOWATTHOUR_DataChanged();
     }

     if((BMS17_100.bms17_100.BMS_REGEN_AH_0 != Rx_buffer.bms17_100.BMS_REGEN_AH_0) || 
       (BMS17_100.bms17_100.BMS_REGEN_AH_1 != Rx_buffer.bms17_100.BMS_REGEN_AH_1))
     {
         ILSet_BMS_REGEN_AH_DataChanged();
     }

   }
}

void BMS18_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS18_50.bms18_50.BMS_CYCLENUMBER_0 != Rx_buffer.bms18_50.BMS_CYCLENUMBER_0) || 
       (BMS18_50.bms18_50.BMS_CYCLENUMBER_1 != Rx_buffer.bms18_50.BMS_CYCLENUMBER_1))
     {
         ILSet_BMS_CYCLENUMBER_DataChanged();
     }

     if((BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_0 != Rx_buffer.bms18_50.BMS_CHARGECYCLE_TIME_0) || 
       (BMS18_50.bms18_50.BMS_CHARGECYCLE_TIME_1 != Rx_buffer.bms18_50.BMS_CHARGECYCLE_TIME_1))
     {
         ILSet_BMS_CHARGECYCLE_TIME_DataChanged();
     }

     if((BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_0 != Rx_buffer.bms18_50.BMS_DISCHARGECYCLE_TIME_0) || 
       (BMS18_50.bms18_50.BMS_DISCHARGECYCLE_TIME_1 != Rx_buffer.bms18_50.BMS_DISCHARGECYCLE_TIME_1))
     {
         ILSet_BMS_DISCHARGECYCLE_TIME_DataChanged();
     }

     if((BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_0 != Rx_buffer.bms18_50.BMS_TOTALCYCLE_TIME_0) || 
       (BMS18_50.bms18_50.BMS_TOTALCYCLE_TIME_1 != Rx_buffer.bms18_50.BMS_TOTALCYCLE_TIME_1))
     {
         ILSet_BMS_TOTALCYCLE_TIME_DataChanged();
     }

   }
}

void BMS1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_0 != Rx_buffer.bms1_10.BMS_BATTERYBUSVOLTAGE_0) || 
       (BMS1_10.bms1_10.BMS_BATTERYBUSVOLTAGE_1 != Rx_buffer.bms1_10.BMS_BATTERYBUSVOLTAGE_1))
     {
         ILSet_BMS_BATTERYBUSVOLTAGE_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_0 != Rx_buffer.bms1_10.BMS_BATTERYPACKCURRENT_0) || 
       (BMS1_10.bms1_10.BMS_BATTERYPACKCURRENT_1 != Rx_buffer.bms1_10.BMS_BATTERYPACKCURRENT_1))
     {
         ILSet_BMS_BATTERYPACKCURRENT_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS_ACTV_DISCHARGE_STS != Rx_buffer.bms1_10.BMS_ACTV_DISCHARGE_STS))
     {
         ILSet_BMS_ACTV_DISCHARGE_STS_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS_BATTERYPACKSTATUS != Rx_buffer.bms1_10.BMS_BATTERYPACKSTATUS))
     {
         ILSet_BMS_BATTERYPACKSTATUS_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS_OPERATIONMODE != Rx_buffer.bms1_10.BMS_OPERATIONMODE))
     {
         ILSet_BMS_OPERATIONMODE_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS273_COUNTER != Rx_buffer.bms1_10.BMS273_COUNTER))
     {
         ILSet_BMS273_COUNTER_DataChanged();
     }

     if((BMS1_10.bms1_10.BMS273_CRC != Rx_buffer.bms1_10.BMS273_CRC))
     {
         ILSet_BMS273_CRC_DataChanged();
     }

   }
}

void BMS22_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS22_100.bms22_100.BMS_FC_COUNT_0 != Rx_buffer.bms22_100.BMS_FC_COUNT_0) || 
       (BMS22_100.bms22_100.BMS_FC_COUNT_1 != Rx_buffer.bms22_100.BMS_FC_COUNT_1))
     {
         ILSet_BMS_FC_COUNT_DataChanged();
     }

     if((BMS22_100.bms22_100.BMS_NC_COUNT_0 != Rx_buffer.bms22_100.BMS_NC_COUNT_0) || 
       (BMS22_100.bms22_100.BMS_NC_COUNT_1 != Rx_buffer.bms22_100.BMS_NC_COUNT_1))
     {
         ILSet_BMS_NC_COUNT_DataChanged();
     }

     if((BMS22_100.bms22_100.BMS_ISOLATIONRESIS_0 != Rx_buffer.bms22_100.BMS_ISOLATIONRESIS_0) || 
       (BMS22_100.bms22_100.BMS_ISOLATIONRESIS_1 != Rx_buffer.bms22_100.BMS_ISOLATIONRESIS_1))
     {
         ILSet_BMS_ISOLATIONRESIS_DataChanged();
     }

   }
}

void BMS2_30_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS2_30.bms2_30.BMS_BATTERYTBATT_0 != Rx_buffer.bms2_30.BMS_BATTERYTBATT_0) || 
       (BMS2_30.bms2_30.BMS_BATTERYTBATT_1 != Rx_buffer.bms2_30.BMS_BATTERYTBATT_1))
     {
         ILSet_BMS_BATTERYTBATT_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_CRASHPYROFUSERESPONSE != Rx_buffer.bms2_30.BMS_CRASHPYROFUSERESPONSE))
     {
         ILSet_BMS_CRASHPYROFUSERESPONSE_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_ISOLATIONFLT != Rx_buffer.bms2_30.BMS_ISOLATIONFLT))
     {
         ILSet_BMS_ISOLATIONFLT_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_DISCONNECTBYBMS != Rx_buffer.bms2_30.BMS_DISCONNECTBYBMS))
     {
         ILSet_BMS_DISCONNECTBYBMS_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_MODULEACTIVEDISCHARGE != Rx_buffer.bms2_30.BMS_MODULEACTIVEDISCHARGE))
     {
         ILSet_BMS_MODULEACTIVEDISCHARGE_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_PILOTLINESTA != Rx_buffer.bms2_30.BMS_PILOTLINESTA))
     {
         ILSet_BMS_PILOTLINESTA_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_HVILSTA != Rx_buffer.bms2_30.BMS_HVILSTA))
     {
         ILSet_BMS_HVILSTA_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_BATTERYHVILSTA != Rx_buffer.bms2_30.BMS_BATTERYHVILSTA))
     {
         ILSet_BMS_BATTERYHVILSTA_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_0 != Rx_buffer.bms2_30.BMS_BATTERYPACKVOLTAGE_0) || 
       (BMS2_30.bms2_30.BMS_BATTERYPACKVOLTAGE_1 != Rx_buffer.bms2_30.BMS_BATTERYPACKVOLTAGE_1))
     {
         ILSet_BMS_BATTERYPACKVOLTAGE_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS_BCONTACTOROFFREQUEST != Rx_buffer.bms2_30.BMS_BCONTACTOROFFREQUEST))
     {
         ILSet_BMS_BCONTACTOROFFREQUEST_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS272_COUNTER != Rx_buffer.bms2_30.BMS272_COUNTER))
     {
         ILSet_BMS272_COUNTER_DataChanged();
     }

     if((BMS2_30.bms2_30.BMS272_CRC != Rx_buffer.bms2_30.BMS272_CRC))
     {
         ILSet_BMS272_CRC_DataChanged();
     }

   }
}

void BMS3_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_0 != Rx_buffer.bms3_100.BMS_DISCHARGECURRENTLIMIT_0) || 
       (BMS3_100.bms3_100.BMS_DISCHARGECURRENTLIMIT_1 != Rx_buffer.bms3_100.BMS_DISCHARGECURRENTLIMIT_1))
     {
         ILSet_BMS_DISCHARGECURRENTLIMIT_DataChanged();
     }

     if((BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_0 != Rx_buffer.bms3_100.BMS_CHARGECURRENTLIMIT_0) || 
       (BMS3_100.bms3_100.BMS_CHARGECURRENTLIMIT_1 != Rx_buffer.bms3_100.BMS_CHARGECURRENTLIMIT_1))
     {
         ILSet_BMS_CHARGECURRENTLIMIT_DataChanged();
     }

     if((BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_0 != Rx_buffer.bms3_100.BMS_CHARGEVOLTAGELIMIT_0) || 
       (BMS3_100.bms3_100.BMS_CHARGEVOLTAGELIMIT_1 != Rx_buffer.bms3_100.BMS_CHARGEVOLTAGELIMIT_1))
     {
         ILSet_BMS_CHARGEVOLTAGELIMIT_DataChanged();
     }

   }
}

void BMS4_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS4_100.bms4_100.BMS_BATTERYPACKASOC_0 != Rx_buffer.bms4_100.BMS_BATTERYPACKASOC_0) || 
       (BMS4_100.bms4_100.BMS_BATTERYPACKASOC_1 != Rx_buffer.bms4_100.BMS_BATTERYPACKASOC_1))
     {
         ILSet_BMS_BATTERYPACKASOC_DataChanged();
     }

     if((BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_0 != Rx_buffer.bms4_100.BMS_BATTERYPACKRSOC_0) || 
       (BMS4_100.bms4_100.BMS_BATTERYPACKRSOC_1 != Rx_buffer.bms4_100.BMS_BATTERYPACKRSOC_1))
     {
         ILSet_BMS_BATTERYPACKRSOC_DataChanged();
     }

     if((BMS4_100.bms4_100.BMS_BATTERYPACKSOH_0 != Rx_buffer.bms4_100.BMS_BATTERYPACKSOH_0) || 
       (BMS4_100.bms4_100.BMS_BATTERYPACKSOH_1 != Rx_buffer.bms4_100.BMS_BATTERYPACKSOH_1))
     {
         ILSet_BMS_BATTERYPACKSOH_DataChanged();
     }

   }
}

void BMS5_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_0 != Rx_buffer.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_0) || 
       (BMS5_100.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_1 != Rx_buffer.bms5_100.BMS_BATTERYAVGCELLVOLTAGE_1))
     {
         ILSet_BMS_BATTERYAVGCELLVOLTAGE_DataChanged();
     }

     if((BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_0 != Rx_buffer.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_0) || 
       (BMS5_100.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_1 != Rx_buffer.bms5_100.BMS_BATTERYMAXCELLVOLTAGE_1))
     {
         ILSet_BMS_BATTERYMAXCELLVOLTAGE_DataChanged();
     }

     if((BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_0 != Rx_buffer.bms5_100.BMS_BATTERYMINCELLVOLTAGE_0) || 
       (BMS5_100.bms5_100.BMS_BATTERYMINCELLVOLTAGE_1 != Rx_buffer.bms5_100.BMS_BATTERYMINCELLVOLTAGE_1))
     {
         ILSet_BMS_BATTERYMINCELLVOLTAGE_DataChanged();
     }

     if((BMS5_100.bms5_100.BMS_BATTERYCONNECTSTA != Rx_buffer.bms5_100.BMS_BATTERYCONNECTSTA))
     {
         ILSet_BMS_BATTERYCONNECTSTA_DataChanged();
     }

     if((BMS5_100.bms5_100.BMS_BATTERYDISCONNECTSTA != Rx_buffer.bms5_100.BMS_BATTERYDISCONNECTSTA))
     {
         ILSet_BMS_BATTERYDISCONNECTSTA_DataChanged();
     }

   }
}

void BMS6_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS6_100.bms6_100.BMS_REQ_BATT_HEATER_PWR != Rx_buffer.bms6_100.BMS_REQ_BATT_HEATER_PWR))
     {
         ILSet_BMS_REQ_BATT_HEATER_PWR_DataChanged();
     }

     if((BMS6_100.bms6_100.BMS_ACTUAL_BATT_HEATER_PWR != Rx_buffer.bms6_100.BMS_ACTUAL_BATT_HEATER_PWR))
     {
         ILSet_BMS_ACTUAL_BATT_HEATER_PWR_DataChanged();
     }

     if((BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_0 != Rx_buffer.bms6_100.BMS_BATTERYMAXTEMPERATURE_0) || 
       (BMS6_100.bms6_100.BMS_BATTERYMAXTEMPERATURE_1 != Rx_buffer.bms6_100.BMS_BATTERYMAXTEMPERATURE_1))
     {
         ILSet_BMS_BATTERYMAXTEMPERATURE_DataChanged();
     }

     if((BMS6_100.bms6_100.BMS_BCOOLINGREQUEST != Rx_buffer.bms6_100.BMS_BCOOLINGREQUEST))
     {
         ILSet_BMS_BCOOLINGREQUEST_DataChanged();
     }

     if((BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_0 != Rx_buffer.bms6_100.BMS_BATTERYMINTEMPERATURE_0) || 
       (BMS6_100.bms6_100.BMS_BATTERYMINTEMPERATURE_1 != Rx_buffer.bms6_100.BMS_BATTERYMINTEMPERATURE_1))
     {
         ILSet_BMS_BATTERYMINTEMPERATURE_DataChanged();
     }

     if((BMS6_100.bms6_100.BMS_CHARGINGSTOP != Rx_buffer.bms6_100.BMS_CHARGINGSTOP))
     {
         ILSet_BMS_CHARGINGSTOP_DataChanged();
     }

   }
}

void BMS7_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_0 != Rx_buffer.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_0) || 
       (BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_1 != Rx_buffer.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_10_1))
     {
         ILSet_BMS_DISCHARGEPOWERAVAILABLE_10_DataChanged();
     }

     if((BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_0 != Rx_buffer.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_0) || 
       (BMS7_100.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_1 != Rx_buffer.bms7_100.BMS_DISCHARGEPOWERAVAILABLE_2_1))
     {
         ILSet_BMS_DISCHARGEPOWERAVAILABLE_2_DataChanged();
     }

     if((BMS7_100.bms7_100.BMS_BATTERYPACKSOE_0 != Rx_buffer.bms7_100.BMS_BATTERYPACKSOE_0) || 
       (BMS7_100.bms7_100.BMS_BATTERYPACKSOE_1 != Rx_buffer.bms7_100.BMS_BATTERYPACKSOE_1))
     {
         ILSet_BMS_BATTERYPACKSOE_DataChanged();
     }

     if((BMS7_100.bms7_100.BMS_BATT_OVERCURRENT_STA != Rx_buffer.bms7_100.BMS_BATT_OVERCURRENT_STA))
     {
         ILSet_BMS_BATT_OVERCURRENT_STA_DataChanged();
     }

   }
}

void BMS8_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_0 != Rx_buffer.bms8_50.BMS_CURRENT1SENSORREADING_0) || 
       (BMS8_50.bms8_50.BMS_CURRENT1SENSORREADING_1 != Rx_buffer.bms8_50.BMS_CURRENT1SENSORREADING_1))
     {
         ILSet_BMS_CURRENT1SENSORREADING_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS_BMAINPLUSCONTACTORSTATE != Rx_buffer.bms8_50.BMS_BMAINPLUSCONTACTORSTATE))
     {
         ILSet_BMS_BMAINPLUSCONTACTORSTATE_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_0 != Rx_buffer.bms8_50.BMS_CURRENT2SENSORREADING_0) || 
       (BMS8_50.bms8_50.BMS_CURRENT2SENSORREADING_1 != Rx_buffer.bms8_50.BMS_CURRENT2SENSORREADING_1))
     {
         ILSet_BMS_CURRENT2SENSORREADING_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS_PRECHARGECONTACTORSTA != Rx_buffer.bms8_50.BMS_PRECHARGECONTACTORSTA))
     {
         ILSet_BMS_PRECHARGECONTACTORSTA_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS_BMAINMINUSCONTACTORSTATE != Rx_buffer.bms8_50.BMS_BMAINMINUSCONTACTORSTATE))
     {
         ILSet_BMS_BMAINMINUSCONTACTORSTATE_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS151_COUNTER != Rx_buffer.bms8_50.BMS151_COUNTER))
     {
         ILSet_BMS151_COUNTER_DataChanged();
     }

     if((BMS8_50.bms8_50.BMS151_CRC != Rx_buffer.bms8_50.BMS151_CRC))
     {
         ILSet_BMS151_CRC_DataChanged();
     }

   }
}

void BMS9_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_0 != Rx_buffer.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_0) || 
       (BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_1 != Rx_buffer.bms9_10.BMS_CHARGEPOWERAVAILABLE_10_1))
     {
         ILSet_BMS_CHARGEPOWERAVAILABLE_10_DataChanged();
     }

     if((BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_0 != Rx_buffer.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_0) || 
       (BMS9_10.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_1 != Rx_buffer.bms9_10.BMS_CHARGEPOWERAVAILABLE_2_1))
     {
         ILSet_BMS_CHARGEPOWERAVAILABLE_2_DataChanged();
     }

     if((BMS9_10.bms9_10.BMS_CHARGE_CYCLE_0 != Rx_buffer.bms9_10.BMS_CHARGE_CYCLE_0) || 
       (BMS9_10.bms9_10.BMS_CHARGE_CYCLE_1 != Rx_buffer.bms9_10.BMS_CHARGE_CYCLE_1))
     {
         ILSet_BMS_CHARGE_CYCLE_DataChanged();
     }

     if((BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_0 != Rx_buffer.bms9_10.BMS_DISCHARGE_CYCLE_0) || 
       (BMS9_10.bms9_10.BMS_DISCHARGE_CYCLE_1 != Rx_buffer.bms9_10.BMS_DISCHARGE_CYCLE_1))
     {
         ILSet_BMS_DISCHARGE_CYCLE_DataChanged();
     }

   }
}

void BMS_CLT_HTR1_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_CLT_HTR1_200.bms_clt_htr1_200.BMS_HTR_CLTALLOWANCE_FLAG != Rx_buffer.bms_clt_htr1_200.BMS_HTR_CLTALLOWANCE_FLAG))
     {
         ILSet_BMS_HTR_CLTALLOWANCE_FLAG_DataChanged();
     }

     if((BMS_CLT_HTR1_200.bms_clt_htr1_200.BMS_HTR_CLTPERF_PERC != Rx_buffer.bms_clt_htr1_200.BMS_HTR_CLTPERF_PERC))
     {
         ILSet_BMS_HTR_CLTPERF_PERC_DataChanged();
     }

     if((BMS_CLT_HTR1_200.bms_clt_htr1_200.BMS_HTR_CLTTEMP_DEGC != Rx_buffer.bms_clt_htr1_200.BMS_HTR_CLTTEMP_DEGC))
     {
         ILSet_BMS_HTR_CLTTEMP_DEGC_DataChanged();
     }

   }
}

void BMS_CLT_HTR2_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_READY_FLAG != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_READY_FLAG))
     {
         ILSet_BMS_HTR_CLT_READY_FLAG_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_STATUS_FLAG != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_STATUS_FLAG))
     {
         ILSet_BMS_HTR_CLT_STATUS_FLAG_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_HVINPUT_V != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_HVINPUT_V))
     {
         ILSet_BMS_HTR_CLT_HVINPUT_V_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_CNSCUR_A != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_CNSCUR_A))
     {
         ILSet_BMS_HTR_CLT_CNSCUR_A_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_CNSPWR_W != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_CNSPWR_W))
     {
         ILSet_BMS_HTR_CLT_CNSPWR_W_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_OUTLETTEMP_DEGC != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_OUTLETTEMP_DEGC))
     {
         ILSet_BMS_HTR_CLT_OUTLETTEMP_DEGC_DataChanged();
     }

     if((BMS_CLT_HTR2_200.bms_clt_htr2_200.BMS_HTR_CLT_CNSDUTY_PER != Rx_buffer.bms_clt_htr2_200.BMS_HTR_CLT_CNSDUTY_PER))
     {
         ILSet_BMS_HTR_CLT_CNSDUTY_PER_DataChanged();
     }

   }
}

void BMS_CLT_HTR3_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_FLAG != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_FLAG))
     {
         ILSet_BMS_HTR_CLT_FAULT_FLAG_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_LIN_COM_ERR_FLAG != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_LIN_COM_ERR_FLAG))
     {
         ILSet_BMS_HTR_CLT_LIN_COM_ERR_FLAG_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVUNDER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVUNDER))
     {
         ILSet_BMS_HTR_CLT_FAULT_LVUNDER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVOVER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVOVER))
     {
         ILSet_BMS_HTR_CLT_FAULT_LVOVER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVUNDER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVUNDER))
     {
         ILSet_BMS_HTR_CLT_FAULT_HVUNDER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVOVER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVOVER))
     {
         ILSet_BMS_HTR_CLT_FAULT_HVOVER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVOVERCUR != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVOVERCUR))
     {
         ILSet_BMS_HTR_CLT_FAULT_HVOVERCUR_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_OUTLETTEMPOVER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_OUTLETTEMPOVER))
     {
         ILSet_BMS_HTR_CLT_FAULT_OUTLETTEMPOVER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_PCBTEMPOVER != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_PCBTEMPOVER))
     {
         ILSet_BMS_HTR_CLT_FAULT_PCBTEMPOVER_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LOSTCTRLMSG != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LOSTCTRLMSG))
     {
         ILSet_BMS_HTR_CLT_FAULT_LOSTCTRLMSG_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVSEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_LVSEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_LVSEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVSEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVSEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_HVSEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVCURSEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_HVCURSEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_HVCURSEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_OUTLETTEMPSEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_OUTLETTEMPSEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_OUTLETTEMPSEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_PCBTEMPSEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_PCBTEMPSEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_PCBTEMPSEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTOPEN != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTOPEN))
     {
         ILSet_BMS_HTR_CLT_FAULT_IGBTOPEN_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTSHORT != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTSHORT))
     {
         ILSet_BMS_HTR_CLT_FAULT_IGBTSHORT_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTDRIVERIC != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_FAULT_IGBTDRIVERIC))
     {
         ILSet_BMS_HTR_CLT_FAULT_IGBTDRIVERIC_DataChanged();
     }

     if((BMS_CLT_HTR3_200.bms_clt_htr3_200.BMS_HTR_CLT_SOFTWAREVERSION_NUM != Rx_buffer.bms_clt_htr3_200.BMS_HTR_CLT_SOFTWAREVERSION_NUM))
     {
         ILSet_BMS_HTR_CLT_SOFTWAREVERSION_NUM_DataChanged();
     }

   }
}

void BMS_IVT_MSG_RESULT_U1_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_0 != Rx_buffer.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_0) || 
       (BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_1 != Rx_buffer.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_1) || 
       (BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_2 != Rx_buffer.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_2) || 
       (BMS_IVT_MSG_RESULT_U1.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_3 != Rx_buffer.bms_ivt_msg_result_u1.BMS_IVT_RESULT_U1_3))
     {
         ILSet_BMS_IVT_RESULT_U1_DataChanged();
     }

   }
}

void BMS_IVT_MSG_RESULT_U2_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_0 != Rx_buffer.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_0) || 
       (BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_1 != Rx_buffer.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_1) || 
       (BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_2 != Rx_buffer.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_2) || 
       (BMS_IVT_MSG_RESULT_U2.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_3 != Rx_buffer.bms_ivt_msg_result_u2.BMS_IVT_RESULT_U2_3))
     {
         ILSet_BMS_IVT_RESULT_U2_DataChanged();
     }

   }
}

void BMS_IVT_MSG_RESULT_U3_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_0 != Rx_buffer.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_0) || 
       (BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_1 != Rx_buffer.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_1) || 
       (BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_2 != Rx_buffer.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_2) || 
       (BMS_IVT_MSG_RESULT_U3.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_3 != Rx_buffer.bms_ivt_msg_result_u3.BMS_IVT_RESULT_U3_3))
     {
         ILSet_BMS_IVT_RESULT_U3_DataChanged();
     }

   }
}

void BMS_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((BMS_STS_500.bms_sts_500.BMS_STS_IGN_NM != Rx_buffer.bms_sts_500.BMS_STS_IGN_NM))
     {
         ILSet_BMS_STS_IGN_NM_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_VARIANT_CODE_ERR_STS != Rx_buffer.bms_sts_500.BMS_VARIANT_CODE_ERR_STS))
     {
         ILSet_BMS_VARIANT_CODE_ERR_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_COMFLT_SGN_CONTFAIL != Rx_buffer.bms_sts_500.BMS_COMFLT_SGN_CONTFAIL))
     {
         ILSet_BMS_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_FEATURE_CODE_ERR_STS != Rx_buffer.bms_sts_500.BMS_FEATURE_CODE_ERR_STS))
     {
         ILSet_BMS_FEATURE_CODE_ERR_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_COMFLT_MSGTOUT_STS != Rx_buffer.bms_sts_500.BMS_COMFLT_MSGTOUT_STS))
     {
         ILSet_BMS_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_COMFLT_NODEABS_STS != Rx_buffer.bms_sts_500.BMS_COMFLT_NODEABS_STS))
     {
         ILSet_BMS_COMFLT_NODEABS_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_UV_STS != Rx_buffer.bms_sts_500.BMS_UV_STS))
     {
         ILSet_BMS_UV_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_OV_STS != Rx_buffer.bms_sts_500.BMS_OV_STS))
     {
         ILSet_BMS_OV_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_AUX_BATT_VOLT != Rx_buffer.bms_sts_500.BMS_AUX_BATT_VOLT))
     {
         ILSet_BMS_AUX_BATT_VOLT_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_SW_VERSION != Rx_buffer.bms_sts_500.BMS_SW_VERSION))
     {
         ILSet_BMS_SW_VERSION_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_NM_ACTIVE_STS != Rx_buffer.bms_sts_500.BMS_NM_ACTIVE_STS))
     {
         ILSet_BMS_NM_ACTIVE_STS_DataChanged();
     }

     if((BMS_STS_500.bms_sts_500.BMS_COMFLT_MSG_CONTFAIL != Rx_buffer.bms_sts_500.BMS_COMFLT_MSG_CONTFAIL))
     {
         ILSet_BMS_COMFLT_MSG_CONTFAIL_DataChanged();
     }

   }
}

void CCM1_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((CCM1_200.ccm1_200.COMPRESSURE_SPD_0 != Rx_buffer.ccm1_200.COMPRESSURE_SPD_0) || 
       (CCM1_200.ccm1_200.COMPRESSURE_SPD_1 != Rx_buffer.ccm1_200.COMPRESSURE_SPD_1))
     {
         ILSet_COMPRESSURE_SPD_DataChanged();
     }

     if((CCM1_200.ccm1_200.STS_PTC_HEATER != Rx_buffer.ccm1_200.STS_PTC_HEATER))
     {
         ILSet_STS_PTC_HEATER_DataChanged();
     }

     if((CCM1_200.ccm1_200.REQ_ACC_ON != Rx_buffer.ccm1_200.REQ_ACC_ON))
     {
         ILSet_REQ_ACC_ON_DataChanged();
     }

     if((CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_0 != Rx_buffer.ccm1_200.DISCHARGE_LINE_PRESSURE_0) || 
       (CCM1_200.ccm1_200.DISCHARGE_LINE_PRESSURE_1 != Rx_buffer.ccm1_200.DISCHARGE_LINE_PRESSURE_1))
     {
         ILSet_DISCHARGE_LINE_PRESSURE_DataChanged();
     }

   }
}

void CCM3_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((CCM3_200.ccm3_200.AC_OFF_CODE != Rx_buffer.ccm3_200.AC_OFF_CODE))
     {
         ILSet_AC_OFF_CODE_DataChanged();
     }

     if((CCM3_200.ccm3_200.CABIN_HEATER_POWER_CONSUMPTION != Rx_buffer.ccm3_200.CABIN_HEATER_POWER_CONSUMPTION))
     {
         ILSet_CABIN_HEATER_POWER_CONSUMPTION_DataChanged();
     }

     if((CCM3_200.ccm3_200.REMOTE_HVAC_STS_CCM != Rx_buffer.ccm3_200.REMOTE_HVAC_STS_CCM))
     {
         ILSet_REMOTE_HVAC_STS_CCM_DataChanged();
     }

     if((CCM3_200.ccm3_200.CABIN_HVAC_STS_CCM != Rx_buffer.ccm3_200.CABIN_HVAC_STS_CCM))
     {
         ILSet_CABIN_HVAC_STS_CCM_DataChanged();
     }

     if((CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_0 != Rx_buffer.ccm3_200.HEATER_INPUT_DC_VOLT_0) || 
       (CCM3_200.ccm3_200.HEATER_INPUT_DC_VOLT_1 != Rx_buffer.ccm3_200.HEATER_INPUT_DC_VOLT_1))
     {
         ILSet_HEATER_INPUT_DC_VOLT_DataChanged();
     }

   }
}

void EMS12_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS12_200.ems12_200.IBS_SOC != Rx_buffer.ems12_200.IBS_SOC))
     {
         ILSet_IBS_SOC_DataChanged();
     }

     if((EMS12_200.ems12_200.IBS_SOH != Rx_buffer.ems12_200.IBS_SOH))
     {
         ILSet_IBS_SOH_DataChanged();
     }

     if((EMS12_200.ems12_200.IBS_SOF != Rx_buffer.ems12_200.IBS_SOF))
     {
         ILSet_IBS_SOF_DataChanged();
     }

     if((EMS12_200.ems12_200.ALTERNATOR_MODE != Rx_buffer.ems12_200.ALTERNATOR_MODE))
     {
         ILSet_ALTERNATOR_MODE_DataChanged();
     }

     if((EMS12_200.ems12_200.BATT_CHARGE_LAMP_INDC != Rx_buffer.ems12_200.BATT_CHARGE_LAMP_INDC))
     {
         ILSet_BATT_CHARGE_LAMP_INDC_DataChanged();
     }

     if((EMS12_200.ems12_200.STS_ESS_DEACTIVATION != Rx_buffer.ems12_200.STS_ESS_DEACTIVATION))
     {
         ILSet_STS_ESS_DEACTIVATION_DataChanged();
     }

     if((EMS12_200.ems12_200.BATT_RESET_FLG != Rx_buffer.ems12_200.BATT_RESET_FLG))
     {
         ILSet_BATT_RESET_FLG_DataChanged();
     }

   }
}

void EMS13_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS13_200.ems13_200.IBS_CURRENT_0 != Rx_buffer.ems13_200.IBS_CURRENT_0) || 
       (EMS13_200.ems13_200.IBS_CURRENT_1 != Rx_buffer.ems13_200.IBS_CURRENT_1))
     {
         ILSet_IBS_CURRENT_DataChanged();
     }

     if((EMS13_200.ems13_200.IBS_BATT_VOLT_0 != Rx_buffer.ems13_200.IBS_BATT_VOLT_0) || 
       (EMS13_200.ems13_200.IBS_BATT_VOLT_1 != Rx_buffer.ems13_200.IBS_BATT_VOLT_1))
     {
         ILSet_IBS_BATT_VOLT_DataChanged();
     }

     if((EMS13_200.ems13_200.IBS_BATT_TEMP_0 != Rx_buffer.ems13_200.IBS_BATT_TEMP_0) || 
       (EMS13_200.ems13_200.IBS_BATT_TEMP_1 != Rx_buffer.ems13_200.IBS_BATT_TEMP_1))
     {
         ILSet_IBS_BATT_TEMP_DataChanged();
     }

   }
}

void EMS14_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_RATIO != Rx_buffer.ems14_10.TURBO_BOOST_PRESSURE_RATIO))
     {
         ILSet_TURBO_BOOST_PRESSURE_RATIO_DataChanged();
     }

     if((EMS14_10.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_0 != Rx_buffer.ems14_10.TURBO_BOOST_PRESSURE_ABSOLUTE_0))
     {
         ILSet_TURBO_BOOST_PRESSURE_ABSOLUTE_DataChanged();
     }

     if((EMS14_10.ems14_10.T50_STATUS != Rx_buffer.ems14_10.T50_STATUS))
     {
         ILSet_T50_STATUS_DataChanged();
     }

   }
}

void EMS1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS1_10.ems1_10.ACC_PED != Rx_buffer.ems1_10.ACC_PED))
     {
         ILSet_ACC_PED_DataChanged();
     }

     if((EMS1_10.ems1_10.ENG_SPD_0 != Rx_buffer.ems1_10.ENG_SPD_0) || 
       (EMS1_10.ems1_10.ENG_SPD_1 != Rx_buffer.ems1_10.ENG_SPD_1))
     {
         ILSet_ENG_SPD_DataChanged();
     }

     if((EMS1_10.ems1_10.INJ_QTY_0 != Rx_buffer.ems1_10.INJ_QTY_0) || 
       (EMS1_10.ems1_10.INJ_QTY_1 != Rx_buffer.ems1_10.INJ_QTY_1))
     {
         ILSet_INJ_QTY_DataChanged();
     }

     if((EMS1_10.ems1_10.STS_CRUISE_KEYPAD != Rx_buffer.ems1_10.STS_CRUISE_KEYPAD))
     {
         ILSet_STS_CRUISE_KEYPAD_DataChanged();
     }

     if((EMS1_10.ems1_10.INDC_CRUISE != Rx_buffer.ems1_10.INDC_CRUISE))
     {
         ILSet_INDC_CRUISE_DataChanged();
     }

     if((EMS1_10.ems1_10.CURRENT_GEAR_MT != Rx_buffer.ems1_10.CURRENT_GEAR_MT))
     {
         ILSet_CURRENT_GEAR_MT_DataChanged();
     }

     if((EMS1_10.ems1_10.STS_WATER_IN_FUEL != Rx_buffer.ems1_10.STS_WATER_IN_FUEL))
     {
         ILSet_STS_WATER_IN_FUEL_DataChanged();
     }

     if((EMS1_10.ems1_10.BRK_PEDAL != Rx_buffer.ems1_10.BRK_PEDAL))
     {
         ILSet_BRK_PEDAL_DataChanged();
     }

     if((EMS1_10.ems1_10.STS_AC_COMPRESSOR != Rx_buffer.ems1_10.STS_AC_COMPRESSOR))
     {
         ILSet_STS_AC_COMPRESSOR_DataChanged();
     }

     if((EMS1_10.ems1_10.INDC_GLOW_PLUG != Rx_buffer.ems1_10.INDC_GLOW_PLUG))
     {
         ILSet_INDC_GLOW_PLUG_DataChanged();
     }

     if((EMS1_10.ems1_10.STS_ENG != Rx_buffer.ems1_10.STS_ENG))
     {
         ILSet_STS_ENG_DataChanged();
     }

     if((EMS1_10.ems1_10.ENG_TEMP != Rx_buffer.ems1_10.ENG_TEMP))
     {
         ILSet_ENG_TEMP_DataChanged();
     }

   }
}

void EMS21_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS21_10.ems21_10.BRK_PEDAL1 != Rx_buffer.ems21_10.BRK_PEDAL1))
     {
         ILSet_BRK_PEDAL1_DataChanged();
     }

     if((EMS21_10.ems21_10.ACC_PED_ACTUAL != Rx_buffer.ems21_10.ACC_PED_ACTUAL))
     {
         ILSet_ACC_PED_ACTUAL_DataChanged();
     }

     if((EMS21_10.ems21_10.ENG_LOSSES_0 != Rx_buffer.ems21_10.ENG_LOSSES_0) || 
       (EMS21_10.ems21_10.ENG_LOSSES_1 != Rx_buffer.ems21_10.ENG_LOSSES_1))
     {
         ILSet_ENG_LOSSES_DataChanged();
     }

     if((EMS21_10.ems21_10.EMS21_MSG_CNT != Rx_buffer.ems21_10.EMS21_MSG_CNT))
     {
         ILSet_EMS21_MSG_CNT_DataChanged();
     }

     if((EMS21_10.ems21_10.EMS21_CRC != Rx_buffer.ems21_10.EMS21_CRC))
     {
         ILSet_EMS21_CRC_DataChanged();
     }

   }
}

void EMS29_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS29_100.ems29_100.STS_DEF != Rx_buffer.ems29_100.STS_DEF))
     {
         ILSet_STS_DEF_DataChanged();
     }

     if((EMS29_100.ems29_100.DIST_DEF_EMPTY_0 != Rx_buffer.ems29_100.DIST_DEF_EMPTY_0) || 
       (EMS29_100.ems29_100.DIST_DEF_EMPTY_1 != Rx_buffer.ems29_100.DIST_DEF_EMPTY_1))
     {
         ILSet_DIST_DEF_EMPTY_DataChanged();
     }

     if((EMS29_100.ems29_100.DEF_DOSING_MALFUNC != Rx_buffer.ems29_100.DEF_DOSING_MALFUNC))
     {
         ILSet_DEF_DOSING_MALFUNC_DataChanged();
     }

     if((EMS29_100.ems29_100.INCORRECT_DEF != Rx_buffer.ems29_100.INCORRECT_DEF))
     {
         ILSet_INCORRECT_DEF_DataChanged();
     }

     if((EMS29_100.ems29_100.INDC_REGEN != Rx_buffer.ems29_100.INDC_REGEN))
     {
         ILSet_INDC_REGEN_DataChanged();
     }

     if((EMS29_100.ems29_100.DEF_LEVEL != Rx_buffer.ems29_100.DEF_LEVEL))
     {
         ILSet_DEF_LEVEL_DataChanged();
     }

     if((EMS29_100.ems29_100.UREA_LEVEL_PERCENTAGE != Rx_buffer.ems29_100.UREA_LEVEL_PERCENTAGE))
     {
         ILSet_UREA_LEVEL_PERCENTAGE_DataChanged();
     }

   }
}

void EMS2_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS2_10.ems2_10.VEHICLE_SPEED_EMS_0 != Rx_buffer.ems2_10.VEHICLE_SPEED_EMS_0) || 
       (EMS2_10.ems2_10.VEHICLE_SPEED_EMS_1 != Rx_buffer.ems2_10.VEHICLE_SPEED_EMS_1))
     {
         ILSet_VEHICLE_SPEED_EMS_DataChanged();
     }

     if((EMS2_10.ems2_10.ODO_DISTANCE_EMS_0 != Rx_buffer.ems2_10.ODO_DISTANCE_EMS_0) || 
       (EMS2_10.ems2_10.ODO_DISTANCE_EMS_1 != Rx_buffer.ems2_10.ODO_DISTANCE_EMS_1))
     {
         ILSet_ODO_DISTANCE_EMS_DataChanged();
     }

     if((EMS2_10.ems2_10.ENG_SPD_RATE_0 != Rx_buffer.ems2_10.ENG_SPD_RATE_0) || 
       (EMS2_10.ems2_10.ENG_SPD_RATE_1 != Rx_buffer.ems2_10.ENG_SPD_RATE_1))
     {
         ILSet_ENG_SPD_RATE_DataChanged();
     }

   }
}

void EMS30_SP_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS30_SP.ems30_sp.IMMOVAL3_0 != Rx_buffer.ems30_sp.IMMOVAL3_0) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_1 != Rx_buffer.ems30_sp.IMMOVAL3_1) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_2 != Rx_buffer.ems30_sp.IMMOVAL3_2) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_3 != Rx_buffer.ems30_sp.IMMOVAL3_3) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_4 != Rx_buffer.ems30_sp.IMMOVAL3_4) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_5 != Rx_buffer.ems30_sp.IMMOVAL3_5) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_6 != Rx_buffer.ems30_sp.IMMOVAL3_6) || 
       (EMS30_SP.ems30_sp.IMMOVAL3_7 != Rx_buffer.ems30_sp.IMMOVAL3_7))
     {
         ILSet_IMMOVAL3_DataChanged();
     }

   }
}

void EMS36_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS36_10.ems36_10.ACC_PED1 != Rx_buffer.ems36_10.ACC_PED1))
     {
         ILSet_ACC_PED1_DataChanged();
     }

     if((EMS36_10.ems36_10.ENG_SPD1_0 != Rx_buffer.ems36_10.ENG_SPD1_0) || 
       (EMS36_10.ems36_10.ENG_SPD1_1 != Rx_buffer.ems36_10.ENG_SPD1_1))
     {
         ILSet_ENG_SPD1_DataChanged();
     }

     if((EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_0 != Rx_buffer.ems36_10.ENG_TRQ_AFTR_RED1_0) || 
       (EMS36_10.ems36_10.ENG_TRQ_AFTR_RED1_1 != Rx_buffer.ems36_10.ENG_TRQ_AFTR_RED1_1))
     {
         ILSet_ENG_TRQ_AFTR_RED1_DataChanged();
     }

     if((EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_0 != Rx_buffer.ems36_10.DRIVER_DEMAND_TRQ_EMS36_0) || 
       (EMS36_10.ems36_10.DRIVER_DEMAND_TRQ_EMS36_1 != Rx_buffer.ems36_10.DRIVER_DEMAND_TRQ_EMS36_1))
     {
         ILSet_DRIVER_DEMAND_TRQ_EMS36_DataChanged();
     }

     if((EMS36_10.ems36_10.EMS36_MSG_CNT != Rx_buffer.ems36_10.EMS36_MSG_CNT))
     {
         ILSet_EMS36_MSG_CNT_DataChanged();
     }

     if((EMS36_10.ems36_10.EMS36_CRC != Rx_buffer.ems36_10.EMS36_CRC))
     {
         ILSet_EMS36_CRC_DataChanged();
     }

   }
}

void EMS37_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS37_500.ems37_500.ENG_OIL_TEMP != Rx_buffer.ems37_500.ENG_OIL_TEMP))
     {
         ILSet_ENG_OIL_TEMP_DataChanged();
     }

     if((EMS37_500.ems37_500.ENG_OIL_PRESSURE_VAL != Rx_buffer.ems37_500.ENG_OIL_PRESSURE_VAL))
     {
         ILSet_ENG_OIL_PRESSURE_VAL_DataChanged();
     }

     if((EMS37_500.ems37_500.STS_ADAPTV_SPEED_CNTRL_MODE != Rx_buffer.ems37_500.STS_ADAPTV_SPEED_CNTRL_MODE))
     {
         ILSet_STS_ADAPTV_SPEED_CNTRL_MODE_DataChanged();
     }

     if((EMS37_500.ems37_500.DRV_MODE_CUSTOM1 != Rx_buffer.ems37_500.DRV_MODE_CUSTOM1))
     {
         ILSet_DRV_MODE_CUSTOM1_DataChanged();
     }

     if((EMS37_500.ems37_500.ADAPTIVE_SPD_EMS_FB != Rx_buffer.ems37_500.ADAPTIVE_SPD_EMS_FB))
     {
         ILSet_ADAPTIVE_SPD_EMS_FB_DataChanged();
     }

     if((EMS37_500.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ1 != Rx_buffer.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ1))
     {
         ILSet_FUEL_INJECTOR_DRIFT_PRED_INJ1_DataChanged();
     }

     if((EMS37_500.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ2 != Rx_buffer.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ2))
     {
         ILSet_FUEL_INJECTOR_DRIFT_PRED_INJ2_DataChanged();
     }

     if((EMS37_500.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ3 != Rx_buffer.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ3))
     {
         ILSet_FUEL_INJECTOR_DRIFT_PRED_INJ3_DataChanged();
     }

     if((EMS37_500.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ4 != Rx_buffer.ems37_500.FUEL_INJECTOR_DRIFT_PRED_INJ4))
     {
         ILSet_FUEL_INJECTOR_DRIFT_PRED_INJ4_DataChanged();
     }

   }
}

void EMS38_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_0 != Rx_buffer.ems38_100.BATT_SENSED_VOLTAGE_0) || 
       (EMS38_100.ems38_100.BATT_SENSED_VOLTAGE_1 != Rx_buffer.ems38_100.BATT_SENSED_VOLTAGE_1))
     {
         ILSet_BATT_SENSED_VOLTAGE_DataChanged();
     }

     if((EMS38_100.ems38_100.BATT_MIN_VOLTAGE_0 != Rx_buffer.ems38_100.BATT_MIN_VOLTAGE_0) || 
       (EMS38_100.ems38_100.BATT_MIN_VOLTAGE_1 != Rx_buffer.ems38_100.BATT_MIN_VOLTAGE_1))
     {
         ILSet_BATT_MIN_VOLTAGE_DataChanged();
     }

     if((EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_0 != Rx_buffer.ems38_100.TIME_ELAPSED_CRANKING_0) || 
       (EMS38_100.ems38_100.TIME_ELAPSED_CRANKING_1 != Rx_buffer.ems38_100.TIME_ELAPSED_CRANKING_1))
     {
         ILSet_TIME_ELAPSED_CRANKING_DataChanged();
     }

     if((EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_0 != Rx_buffer.ems38_100.COMMANDED_THRTL_ACTR_CTL_0) || 
       (EMS38_100.ems38_100.COMMANDED_THRTL_ACTR_CTL_1 != Rx_buffer.ems38_100.COMMANDED_THRTL_ACTR_CTL_1))
     {
         ILSet_COMMANDED_THRTL_ACTR_CTL_DataChanged();
     }

     if((EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_0 != Rx_buffer.ems38_100.MASS_AIR_FLOW_RATE_0) || 
       (EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_1 != Rx_buffer.ems38_100.MASS_AIR_FLOW_RATE_1) || 
       (EMS38_100.ems38_100.MASS_AIR_FLOW_RATE_2 != Rx_buffer.ems38_100.MASS_AIR_FLOW_RATE_2))
     {
         ILSet_MASS_AIR_FLOW_RATE_DataChanged();
     }

     if((EMS38_100.ems38_100.CAL_LOAD_0 != Rx_buffer.ems38_100.CAL_LOAD_0) || 
       (EMS38_100.ems38_100.CAL_LOAD_1 != Rx_buffer.ems38_100.CAL_LOAD_1))
     {
         ILSet_CAL_LOAD_DataChanged();
     }

     if((EMS38_100.ems38_100.DPF_HIGH_FUEL_OIL_DILUTION != Rx_buffer.ems38_100.DPF_HIGH_FUEL_OIL_DILUTION))
     {
         ILSet_DPF_HIGH_FUEL_OIL_DILUTION_DataChanged();
     }

     if((EMS38_100.ems38_100.NOX_DWNSTR_VLD != Rx_buffer.ems38_100.NOX_DWNSTR_VLD))
     {
         ILSet_NOX_DWNSTR_VLD_DataChanged();
     }

   }
}

void EMS39_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_0 != Rx_buffer.ems39_100.FUEL_RAIL_PRESSURE_0) || 
       (EMS39_100.ems39_100.FUEL_RAIL_PRESSURE_1 != Rx_buffer.ems39_100.FUEL_RAIL_PRESSURE_1))
     {
         ILSet_FUEL_RAIL_PRESSURE_DataChanged();
     }

     if((EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_0 != Rx_buffer.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_0) || 
       (EMS39_100.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_1 != Rx_buffer.ems39_100.MEUNT_CTCL_FLTACT_CURVAL_1))
     {
         ILSet_MEUNT_CTCL_FLTACT_CURVAL_DataChanged();
     }

     if((EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_0 != Rx_buffer.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_0) || 
       (EMS39_100.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_1 != Rx_buffer.ems39_100.MEUNT_SETPOINT_ADPT_CORECT_1))
     {
         ILSet_MEUNT_SETPOINT_ADPT_CORECT_DataChanged();
     }

     if((EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_0 != Rx_buffer.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_0) || 
       (EMS39_100.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_1 != Rx_buffer.ems39_100.MEUNT_SETPOINT_RAIL_PRESSURE_1))
     {
         ILSet_MEUNT_SETPOINT_RAIL_PRESSURE_DataChanged();
     }

     if((EMS39_100.ems39_100.EGR_ERR_0 != Rx_buffer.ems39_100.EGR_ERR_0) || 
       (EMS39_100.ems39_100.EGR_ERR_1 != Rx_buffer.ems39_100.EGR_ERR_1))
     {
         ILSet_EGR_ERR_DataChanged();
     }

     if((EMS39_100.ems39_100.COMMANDED_EGR_0 != Rx_buffer.ems39_100.COMMANDED_EGR_0) || 
       (EMS39_100.ems39_100.COMMANDED_EGR_1 != Rx_buffer.ems39_100.COMMANDED_EGR_1))
     {
         ILSet_COMMANDED_EGR_DataChanged();
     }

     if((EMS39_100.ems39_100.FUEL_PUMP_PREDICTION != Rx_buffer.ems39_100.FUEL_PUMP_PREDICTION))
     {
         ILSet_FUEL_PUMP_PREDICTION_DataChanged();
     }

   }
}

void EMS3_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS3_10.ems3_10.INTAKE_AIR_TEMP != Rx_buffer.ems3_10.INTAKE_AIR_TEMP))
     {
         ILSet_INTAKE_AIR_TEMP_DataChanged();
     }

     if((EMS3_10.ems3_10.ODO_ERROR_FLAG_EMS != Rx_buffer.ems3_10.ODO_ERROR_FLAG_EMS))
     {
         ILSet_ODO_ERROR_FLAG_EMS_DataChanged();
     }

     if((EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_0 != Rx_buffer.ems3_10.ENG_TRQ_AFTR_RED_0) || 
       (EMS3_10.ems3_10.ENG_TRQ_AFTR_RED_1 != Rx_buffer.ems3_10.ENG_TRQ_AFTR_RED_1))
     {
         ILSet_ENG_TRQ_AFTR_RED_DataChanged();
     }

     if((EMS3_10.ems3_10.STS_ENG_LIMP_HOME != Rx_buffer.ems3_10.STS_ENG_LIMP_HOME))
     {
         ILSet_STS_ENG_LIMP_HOME_DataChanged();
     }

     if((EMS3_10.ems3_10.STS_DPF_REGENERATION != Rx_buffer.ems3_10.STS_DPF_REGENERATION))
     {
         ILSet_STS_DPF_REGENERATION_DataChanged();
     }

     if((EMS3_10.ems3_10.CLUTCH_STS != Rx_buffer.ems3_10.CLUTCH_STS))
     {
         ILSet_CLUTCH_STS_DataChanged();
     }

     if((EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_0 != Rx_buffer.ems3_10.DRIVER_DEMAND_TRQ_0) || 
       (EMS3_10.ems3_10.DRIVER_DEMAND_TRQ_1 != Rx_buffer.ems3_10.DRIVER_DEMAND_TRQ_1))
     {
         ILSet_DRIVER_DEMAND_TRQ_DataChanged();
     }

     if((EMS3_10.ems3_10.BARO_PRS != Rx_buffer.ems3_10.BARO_PRS))
     {
         ILSet_BARO_PRS_DataChanged();
     }

     if((EMS3_10.ems3_10.STS_ESS_INDC != Rx_buffer.ems3_10.STS_ESS_INDC))
     {
         ILSet_STS_ESS_INDC_DataChanged();
     }

     if((EMS3_10.ems3_10.ALTERNATOR_CUTOFF_REQ != Rx_buffer.ems3_10.ALTERNATOR_CUTOFF_REQ))
     {
         ILSet_ALTERNATOR_CUTOFF_REQ_DataChanged();
     }

   }
}

void EMS41_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS41_100.ems41_100.SOOT_DELTA_PRESSURE != Rx_buffer.ems41_100.SOOT_DELTA_PRESSURE))
     {
         ILSet_SOOT_DELTA_PRESSURE_DataChanged();
     }

     if((EMS41_100.ems41_100.SCR_MEAN_TEMP != Rx_buffer.ems41_100.SCR_MEAN_TEMP))
     {
         ILSet_SCR_MEAN_TEMP_DataChanged();
     }

     if((EMS41_100.ems41_100.SCR_STORE_NH3 != Rx_buffer.ems41_100.SCR_STORE_NH3))
     {
         ILSet_SCR_STORE_NH3_DataChanged();
     }

     if((EMS41_100.ems41_100.EXHAUST_MASS_FLOW != Rx_buffer.ems41_100.EXHAUST_MASS_FLOW))
     {
         ILSet_EXHAUST_MASS_FLOW_DataChanged();
     }

     if((EMS41_100.ems41_100.DEF_DOSING_AMT != Rx_buffer.ems41_100.DEF_DOSING_AMT))
     {
         ILSet_DEF_DOSING_AMT_DataChanged();
     }

     if((EMS41_100.ems41_100.FAN_MODE != Rx_buffer.ems41_100.FAN_MODE))
     {
         ILSet_FAN_MODE_DataChanged();
     }

     if((EMS41_100.ems41_100.NOX_DWNSTR_SCR_0 != Rx_buffer.ems41_100.NOX_DWNSTR_SCR_0) || 
       (EMS41_100.ems41_100.NOX_DWNSTR_SCR_1 != Rx_buffer.ems41_100.NOX_DWNSTR_SCR_1))
     {
         ILSet_NOX_DWNSTR_SCR_DataChanged();
     }

     if((EMS41_100.ems41_100.ENG_OPERATION_MODE != Rx_buffer.ems41_100.ENG_OPERATION_MODE))
     {
         ILSet_ENG_OPERATION_MODE_DataChanged();
     }

   }
}

void EMS42_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS42_100.ems42_100.NOX_UPSTR_MDL_0 != Rx_buffer.ems42_100.NOX_UPSTR_MDL_0) || 
       (EMS42_100.ems42_100.NOX_UPSTR_MDL_1 != Rx_buffer.ems42_100.NOX_UPSTR_MDL_1))
     {
         ILSet_NOX_UPSTR_MDL_DataChanged();
     }

   }
}

void EMS43_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS43_100.ems43_100.AC_PRESSURE != Rx_buffer.ems43_100.AC_PRESSURE))
     {
         ILSet_AC_PRESSURE_DataChanged();
     }

     if((EMS43_100.ems43_100.ENG_ROUGHNESS_0 != Rx_buffer.ems43_100.ENG_ROUGHNESS_0))
     {
         ILSet_ENG_ROUGHNESS_0_DataChanged();
     }

     if((EMS43_100.ems43_100.ENG_ROUGHNESS_1 != Rx_buffer.ems43_100.ENG_ROUGHNESS_1))
     {
         ILSet_ENG_ROUGHNESS_1_DataChanged();
     }

     if((EMS43_100.ems43_100.ENG_ROUGHNESS_2 != Rx_buffer.ems43_100.ENG_ROUGHNESS_2))
     {
         ILSet_ENG_ROUGHNESS_2_DataChanged();
     }

     if((EMS43_100.ems43_100.ENG_ROUGHNESS_3 != Rx_buffer.ems43_100.ENG_ROUGHNESS_3))
     {
         ILSet_ENG_ROUGHNESS_3_DataChanged();
     }

     if((EMS43_100.ems43_100.FAN_SPEED != Rx_buffer.ems43_100.FAN_SPEED))
     {
         ILSet_FAN_SPEED_DataChanged();
     }

     if((EMS43_100.ems43_100.MISFIRE_INHIBIT_STATE != Rx_buffer.ems43_100.MISFIRE_INHIBIT_STATE))
     {
         ILSet_MISFIRE_INHIBIT_STATE_DataChanged();
     }

     if((EMS43_100.ems43_100.ROUGH_ROAD_COND != Rx_buffer.ems43_100.ROUGH_ROAD_COND))
     {
         ILSet_ROUGH_ROAD_COND_DataChanged();
     }

   }
}

void EMS44_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS44_100.ems44_100.KNOCK_SIGNALS_0 != Rx_buffer.ems44_100.KNOCK_SIGNALS_0))
     {
         ILSet_KNOCK_SIGNALS_0_DataChanged();
     }

     if((EMS44_100.ems44_100.KNOCK_SIGNALS_1 != Rx_buffer.ems44_100.KNOCK_SIGNALS_1))
     {
         ILSet_KNOCK_SIGNALS_1_DataChanged();
     }

     if((EMS44_100.ems44_100.KNOCK_SIGNALS_2 != Rx_buffer.ems44_100.KNOCK_SIGNALS_2))
     {
         ILSet_KNOCK_SIGNALS_2_DataChanged();
     }

     if((EMS44_100.ems44_100.KNOCK_SIGNALS_3 != Rx_buffer.ems44_100.KNOCK_SIGNALS_3))
     {
         ILSet_KNOCK_SIGNALS_3_DataChanged();
     }

     if((EMS44_100.ems44_100.MASS_AIR_FLOW != Rx_buffer.ems44_100.MASS_AIR_FLOW))
     {
         ILSet_MASS_AIR_FLOW_DataChanged();
     }

     if((EMS44_100.ems44_100.MISFIRE_DETECT_THRESHOLD != Rx_buffer.ems44_100.MISFIRE_DETECT_THRESHOLD))
     {
         ILSet_MISFIRE_DETECT_THRESHOLD_DataChanged();
     }

     if((EMS44_100.ems44_100.MISFIRE_SUM_A != Rx_buffer.ems44_100.MISFIRE_SUM_A))
     {
         ILSet_MISFIRE_SUM_A_DataChanged();
     }

     if((EMS44_100.ems44_100.MISFIRE_SUM_B != Rx_buffer.ems44_100.MISFIRE_SUM_B))
     {
         ILSet_MISFIRE_SUM_B_DataChanged();
     }

   }
}

void EMS45_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS45_100.ems45_100.MISFIRE_CTR_A_0 != Rx_buffer.ems45_100.MISFIRE_CTR_A_0))
     {
         ILSet_MISFIRE_CTR_A_0_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_A_1 != Rx_buffer.ems45_100.MISFIRE_CTR_A_1))
     {
         ILSet_MISFIRE_CTR_A_1_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_A_2 != Rx_buffer.ems45_100.MISFIRE_CTR_A_2))
     {
         ILSet_MISFIRE_CTR_A_2_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_A_3 != Rx_buffer.ems45_100.MISFIRE_CTR_A_3))
     {
         ILSet_MISFIRE_CTR_A_3_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_B_0 != Rx_buffer.ems45_100.MISFIRE_CTR_B_0))
     {
         ILSet_MISFIRE_CTR_B_0_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_B_1 != Rx_buffer.ems45_100.MISFIRE_CTR_B_1))
     {
         ILSet_MISFIRE_CTR_B_1_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_B_2 != Rx_buffer.ems45_100.MISFIRE_CTR_B_2))
     {
         ILSet_MISFIRE_CTR_B_2_DataChanged();
     }

     if((EMS45_100.ems45_100.MISFIRE_CTR_B_3 != Rx_buffer.ems45_100.MISFIRE_CTR_B_3))
     {
         ILSet_MISFIRE_CTR_B_3_DataChanged();
     }

   }
}

void EMS4_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS4_20.ems4_20.CRUISE_SET_SPD_0 != Rx_buffer.ems4_20.CRUISE_SET_SPD_0) || 
       (EMS4_20.ems4_20.CRUISE_SET_SPD_1 != Rx_buffer.ems4_20.CRUISE_SET_SPD_1))
     {
         ILSet_CRUISE_SET_SPD_DataChanged();
     }

     if((EMS4_20.ems4_20.FUEL_CONSMP_RATE_0 != Rx_buffer.ems4_20.FUEL_CONSMP_RATE_0) || 
       (EMS4_20.ems4_20.FUEL_CONSMP_RATE_1 != Rx_buffer.ems4_20.FUEL_CONSMP_RATE_1))
     {
         ILSet_FUEL_CONSMP_RATE_DataChanged();
     }

     if((EMS4_20.ems4_20.ENG_OIL_PRESSURE != Rx_buffer.ems4_20.ENG_OIL_PRESSURE))
     {
         ILSet_ENG_OIL_PRESSURE_DataChanged();
     }

     if((EMS4_20.ems4_20.INDC_SYS_LAMP != Rx_buffer.ems4_20.INDC_SYS_LAMP))
     {
         ILSet_INDC_SYS_LAMP_DataChanged();
     }

     if((EMS4_20.ems4_20.INDC_MIL != Rx_buffer.ems4_20.INDC_MIL))
     {
         ILSet_INDC_MIL_DataChanged();
     }

     if((EMS4_20.ems4_20.ERROR_FLAG_VCU != Rx_buffer.ems4_20.ERROR_FLAG_VCU))
     {
         ILSet_ERROR_FLAG_VCU_DataChanged();
     }

     if((EMS4_20.ems4_20.INDC_DPF_REGEN != Rx_buffer.ems4_20.INDC_DPF_REGEN))
     {
         ILSet_INDC_DPF_REGEN_DataChanged();
     }

     if((EMS4_20.ems4_20.ENGINE_DRIVE_MODE != Rx_buffer.ems4_20.ENGINE_DRIVE_MODE))
     {
         ILSet_ENGINE_DRIVE_MODE_DataChanged();
     }

     if((EMS4_20.ems4_20.STS_EMS_DRV_ADV_MODE != Rx_buffer.ems4_20.STS_EMS_DRV_ADV_MODE))
     {
         ILSet_STS_EMS_DRV_ADV_MODE_DataChanged();
     }

     if((EMS4_20.ems4_20.CRUISE_ALERT != Rx_buffer.ems4_20.CRUISE_ALERT))
     {
         ILSet_CRUISE_ALERT_DataChanged();
     }

     if((EMS4_20.ems4_20.ACC_READY != Rx_buffer.ems4_20.ACC_READY))
     {
         ILSet_ACC_READY_DataChanged();
     }

     if((EMS4_20.ems4_20.EMS_DRIVE_ALERT != Rx_buffer.ems4_20.EMS_DRIVE_ALERT))
     {
         ILSet_EMS_DRIVE_ALERT_DataChanged();
     }

   }
}

void EMS6_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS6_500.ems6_500.VALET_MODE_STATUS != Rx_buffer.ems6_500.VALET_MODE_STATUS))
     {
         ILSet_VALET_MODE_STATUS_DataChanged();
     }

     if((EMS6_500.ems6_500.STS_REMOTE_ENG != Rx_buffer.ems6_500.STS_REMOTE_ENG))
     {
         ILSet_STS_REMOTE_ENG_DataChanged();
     }

     if((EMS6_500.ems6_500.DISP_AMBT_TEMP_EMS != Rx_buffer.ems6_500.DISP_AMBT_TEMP_EMS))
     {
         ILSet_DISP_AMBT_TEMP_EMS_DataChanged();
     }

     if((EMS6_500.ems6_500.ENG_ON_TIME_0 != Rx_buffer.ems6_500.ENG_ON_TIME_0) || 
       (EMS6_500.ems6_500.ENG_ON_TIME_1 != Rx_buffer.ems6_500.ENG_ON_TIME_1))
     {
         ILSet_ENG_ON_TIME_DataChanged();
     }

   }
}

void EMS8_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS8_10.ems8_10.MAX_ALL_TRQ_0 != Rx_buffer.ems8_10.MAX_ALL_TRQ_0) || 
       (EMS8_10.ems8_10.MAX_ALL_TRQ_1 != Rx_buffer.ems8_10.MAX_ALL_TRQ_1))
     {
         ILSet_MAX_ALL_TRQ_DataChanged();
     }

     if((EMS8_10.ems8_10.HYBRID_LAMP_INDC != Rx_buffer.ems8_10.HYBRID_LAMP_INDC))
     {
         ILSet_HYBRID_LAMP_INDC_DataChanged();
     }

     if((EMS8_10.ems8_10.GEAR_UP_FLG != Rx_buffer.ems8_10.GEAR_UP_FLG))
     {
         ILSet_GEAR_UP_FLG_DataChanged();
     }

     if((EMS8_10.ems8_10.GEAR_DOWN_FLG != Rx_buffer.ems8_10.GEAR_DOWN_FLG))
     {
         ILSet_GEAR_DOWN_FLG_DataChanged();
     }

     if((EMS8_10.ems8_10.MIN_ALL_TRQ_0 != Rx_buffer.ems8_10.MIN_ALL_TRQ_0) || 
       (EMS8_10.ems8_10.MIN_ALL_TRQ_1 != Rx_buffer.ems8_10.MIN_ALL_TRQ_1))
     {
         ILSet_MIN_ALL_TRQ_DataChanged();
     }

     if((EMS8_10.ems8_10.TARGET_GEAR_GSI != Rx_buffer.ems8_10.TARGET_GEAR_GSI))
     {
         ILSet_TARGET_GEAR_GSI_DataChanged();
     }

   }
}

void EMS9_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS9_500.ems9_500.DPF_BAD_REGEN_EFFICIENCY != Rx_buffer.ems9_500.DPF_BAD_REGEN_EFFICIENCY))
     {
         ILSet_DPF_BAD_REGEN_EFFICIENCY_DataChanged();
     }

     if((EMS9_500.ems9_500.DPF_ANAMOLY_RESERVED != Rx_buffer.ems9_500.DPF_ANAMOLY_RESERVED))
     {
         ILSet_DPF_ANAMOLY_RESERVED_DataChanged();
     }

     if((EMS9_500.ems9_500.REMAINING_OIL_LIFE_PERCENT != Rx_buffer.ems9_500.REMAINING_OIL_LIFE_PERCENT))
     {
         ILSet_REMAINING_OIL_LIFE_PERCENT_DataChanged();
     }

     if((EMS9_500.ems9_500.BATT_OCV_0 != Rx_buffer.ems9_500.BATT_OCV_0) || 
       (EMS9_500.ems9_500.BATT_OCV_1 != Rx_buffer.ems9_500.BATT_OCV_1))
     {
         ILSet_BATT_OCV_DataChanged();
     }

   }
}

void EMS_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EMS_NSM.ems_nsm.RESERVED_EMS_0 != Rx_buffer.ems_nsm.RESERVED_EMS_0) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_1 != Rx_buffer.ems_nsm.RESERVED_EMS_1) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_2 != Rx_buffer.ems_nsm.RESERVED_EMS_2) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_3 != Rx_buffer.ems_nsm.RESERVED_EMS_3) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_4 != Rx_buffer.ems_nsm.RESERVED_EMS_4) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_5 != Rx_buffer.ems_nsm.RESERVED_EMS_5) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_6 != Rx_buffer.ems_nsm.RESERVED_EMS_6) || 
       (EMS_NSM.ems_nsm.RESERVED_EMS_7 != Rx_buffer.ems_nsm.RESERVED_EMS_7))
     {
         ILSet_RESERVED_EMS_DataChanged();
     }

   }
}

void EPS1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EPS1_100.eps1_100.EPS_DRV_ADV_MODE != Rx_buffer.eps1_100.EPS_DRV_ADV_MODE))
     {
         ILSet_EPS_DRV_ADV_MODE_DataChanged();
     }

     if((EPS1_100.eps1_100.EPS_FLEX_DISP != Rx_buffer.eps1_100.EPS_FLEX_DISP))
     {
         ILSet_EPS_FLEX_DISP_DataChanged();
     }

     if((EPS1_100.eps1_100.INDC_EPS != Rx_buffer.eps1_100.INDC_EPS))
     {
         ILSet_INDC_EPS_DataChanged();
     }

     if((EPS1_100.eps1_100.EPS_STEERING_MODE_ALERT != Rx_buffer.eps1_100.EPS_STEERING_MODE_ALERT))
     {
         ILSet_EPS_STEERING_MODE_ALERT_DataChanged();
     }

     if((EPS1_100.eps1_100.EPS_STEERING_MODE != Rx_buffer.eps1_100.EPS_STEERING_MODE))
     {
         ILSet_EPS_STEERING_MODE_DataChanged();
     }

     if((EPS1_100.eps1_100.STS_EPS_STEERING_MODE != Rx_buffer.eps1_100.STS_EPS_STEERING_MODE))
     {
         ILSet_STS_EPS_STEERING_MODE_DataChanged();
     }

     if((EPS1_100.eps1_100.EPS1_MSG_COUNT != Rx_buffer.eps1_100.EPS1_MSG_COUNT))
     {
         ILSet_EPS1_MSG_COUNT_DataChanged();
     }

     if((EPS1_100.eps1_100.EPS1_CRC != Rx_buffer.eps1_100.EPS1_CRC))
     {
         ILSet_EPS1_CRC_DataChanged();
     }

   }
}

void EPS_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((EPS_NSM.eps_nsm.RESERVED_EPS_0 != Rx_buffer.eps_nsm.RESERVED_EPS_0) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_1 != Rx_buffer.eps_nsm.RESERVED_EPS_1) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_2 != Rx_buffer.eps_nsm.RESERVED_EPS_2) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_3 != Rx_buffer.eps_nsm.RESERVED_EPS_3) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_4 != Rx_buffer.eps_nsm.RESERVED_EPS_4) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_5 != Rx_buffer.eps_nsm.RESERVED_EPS_5) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_6 != Rx_buffer.eps_nsm.RESERVED_EPS_6) || 
       (EPS_NSM.eps_nsm.RESERVED_EPS_7 != Rx_buffer.eps_nsm.RESERVED_EPS_7))
     {
         ILSet_RESERVED_EPS_DataChanged();
     }

   }
}

void ESC10_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC10_20.esc10_20.MASTER_CYL_PRESSURE_0 != Rx_buffer.esc10_20.MASTER_CYL_PRESSURE_0) || 
       (ESC10_20.esc10_20.MASTER_CYL_PRESSURE_1 != Rx_buffer.esc10_20.MASTER_CYL_PRESSURE_1))
     {
         ILSet_MASTER_CYL_PRESSURE_DataChanged();
     }

   }
}

void ESC12_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC12_10.esc12_10.ODO_DISTANCE_ESC12_0 != Rx_buffer.esc12_10.ODO_DISTANCE_ESC12_0) || 
       (ESC12_10.esc12_10.ODO_DISTANCE_ESC12_1 != Rx_buffer.esc12_10.ODO_DISTANCE_ESC12_1))
     {
         ILSet_ODO_DISTANCE_ESC12_DataChanged();
     }

     if((ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_0 != Rx_buffer.esc12_10.VEHICLE_SPEED_ESC12_0) || 
       (ESC12_10.esc12_10.VEHICLE_SPEED_ESC12_1 != Rx_buffer.esc12_10.VEHICLE_SPEED_ESC12_1))
     {
         ILSet_VEHICLE_SPEED_ESC12_DataChanged();
     }

     if((ESC12_10.esc12_10.ESC12_MSG_CNT != Rx_buffer.esc12_10.ESC12_MSG_CNT))
     {
         ILSet_ESC12_MSG_CNT_DataChanged();
     }

     if((ESC12_10.esc12_10.ESC12_CRC != Rx_buffer.esc12_10.ESC12_CRC))
     {
         ILSet_ESC12_CRC_DataChanged();
     }

   }
}

void ESC13_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC13_100.esc13_100.STS_DDD != Rx_buffer.esc13_100.STS_DDD))
     {
         ILSet_STS_DDD_DataChanged();
     }

     if((ESC13_100.esc13_100.DROWSINESS_INDEX != Rx_buffer.esc13_100.DROWSINESS_INDEX))
     {
         ILSet_DROWSINESS_INDEX_DataChanged();
     }

     if((ESC13_100.esc13_100.STS_ESC_DRV_ADV_MODE != Rx_buffer.esc13_100.STS_ESC_DRV_ADV_MODE))
     {
         ILSet_STS_ESC_DRV_ADV_MODE_DataChanged();
     }

     if((ESC13_100.esc13_100.ESC_ADV_MOD_REQ != Rx_buffer.esc13_100.ESC_ADV_MOD_REQ))
     {
         ILSet_ESC_ADV_MOD_REQ_DataChanged();
     }

     if((ESC13_100.esc13_100.ADV_MODE_ALERT != Rx_buffer.esc13_100.ADV_MODE_ALERT))
     {
         ILSet_ADV_MODE_ALERT_DataChanged();
     }

     if((ESC13_100.esc13_100.INDC_PITCH != Rx_buffer.esc13_100.INDC_PITCH))
     {
         ILSet_INDC_PITCH_DataChanged();
     }

     if((ESC13_100.esc13_100.INDC_ROLL != Rx_buffer.esc13_100.INDC_ROLL))
     {
         ILSet_INDC_ROLL_DataChanged();
     }

     if((ESC13_100.esc13_100.STS_TVB != Rx_buffer.esc13_100.STS_TVB))
     {
         ILSet_STS_TVB_DataChanged();
     }

   }
}

void ESC14_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC14_500.esc14_500.PARK_BRK_ACTIVE_STS != Rx_buffer.esc14_500.PARK_BRK_ACTIVE_STS))
     {
         ILSet_PARK_BRK_ACTIVE_STS_DataChanged();
     }

     if((ESC14_500.esc14_500.RR_PARK_BRK_ACTIVE_STS != Rx_buffer.esc14_500.RR_PARK_BRK_ACTIVE_STS))
     {
         ILSet_RR_PARK_BRK_ACTIVE_STS_DataChanged();
     }

     if((ESC14_500.esc14_500.RL_PARK_BRK_ACTIVE_STS != Rx_buffer.esc14_500.RL_PARK_BRK_ACTIVE_STS))
     {
         ILSet_RL_PARK_BRK_ACTIVE_STS_DataChanged();
     }

     if((ESC14_500.esc14_500.EPB_ALERT != Rx_buffer.esc14_500.EPB_ALERT))
     {
         ILSet_EPB_ALERT_DataChanged();
     }

     if((ESC14_500.esc14_500.AVH_FUNCTION_STS != Rx_buffer.esc14_500.AVH_FUNCTION_STS))
     {
         ILSet_AVH_FUNCTION_STS_DataChanged();
     }

     if((ESC14_500.esc14_500.AVH_ACTIVE_STS != Rx_buffer.esc14_500.AVH_ACTIVE_STS))
     {
         ILSet_AVH_ACTIVE_STS_DataChanged();
     }

     if((ESC14_500.esc14_500.STS_EPB != Rx_buffer.esc14_500.STS_EPB))
     {
         ILSet_STS_EPB_DataChanged();
     }

     if((ESC14_500.esc14_500.ESC14_MSG_CNT != Rx_buffer.esc14_500.ESC14_MSG_CNT))
     {
         ILSet_ESC14_MSG_CNT_DataChanged();
     }

     if((ESC14_500.esc14_500.ESC14_CRC != Rx_buffer.esc14_500.ESC14_CRC))
     {
         ILSet_ESC14_CRC_DataChanged();
     }

   }
}

void ESC15_1000_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC15_1000.esc15_1000.BRAKE_PREDICTION_STS != Rx_buffer.esc15_1000.BRAKE_PREDICTION_STS))
     {
         ILSet_BRAKE_PREDICTION_STS_DataChanged();
     }

   }
}

void ESC16_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC16_10.esc16_10.STS_ITA != Rx_buffer.esc16_10.STS_ITA))
     {
         ILSet_STS_ITA_DataChanged();
     }

     if((ESC16_10.esc16_10.ITA_ACTIVE != Rx_buffer.esc16_10.ITA_ACTIVE))
     {
         ILSet_ITA_ACTIVE_DataChanged();
     }

     if((ESC16_10.esc16_10.CCO_ACTIVE != Rx_buffer.esc16_10.CCO_ACTIVE))
     {
         ILSet_CCO_ACTIVE_DataChanged();
     }

     if((ESC16_10.esc16_10.CCO_SET_SPD != Rx_buffer.esc16_10.CCO_SET_SPD))
     {
         ILSet_CCO_SET_SPD_DataChanged();
     }

     if((ESC16_10.esc16_10.CCO_WARNING != Rx_buffer.esc16_10.CCO_WARNING))
     {
         ILSet_CCO_WARNING_DataChanged();
     }

   }
}

void ESC2_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC2_10.esc2_10.VEHICLE_SPEED_ESC_0 != Rx_buffer.esc2_10.VEHICLE_SPEED_ESC_0) || 
       (ESC2_10.esc2_10.VEHICLE_SPEED_ESC_1 != Rx_buffer.esc2_10.VEHICLE_SPEED_ESC_1))
     {
         ILSet_VEHICLE_SPEED_ESC_DataChanged();
     }

     if((ESC2_10.esc2_10.ODO_DISTANCE_ESC_0 != Rx_buffer.esc2_10.ODO_DISTANCE_ESC_0) || 
       (ESC2_10.esc2_10.ODO_DISTANCE_ESC_1 != Rx_buffer.esc2_10.ODO_DISTANCE_ESC_1))
     {
         ILSet_ODO_DISTANCE_ESC_DataChanged();
     }

     if((ESC2_10.esc2_10.STS_ABS != Rx_buffer.esc2_10.STS_ABS))
     {
         ILSet_STS_ABS_DataChanged();
     }

     if((ESC2_10.esc2_10.STS_EBD != Rx_buffer.esc2_10.STS_EBD))
     {
         ILSet_STS_EBD_DataChanged();
     }

     if((ESC2_10.esc2_10.HDC_ACTIVE != Rx_buffer.esc2_10.HDC_ACTIVE))
     {
         ILSet_HDC_ACTIVE_DataChanged();
     }

     if((ESC2_10.esc2_10.STS_HDC != Rx_buffer.esc2_10.STS_HDC))
     {
         ILSet_STS_HDC_DataChanged();
     }

     if((ESC2_10.esc2_10.STS_HHC != Rx_buffer.esc2_10.STS_HHC))
     {
         ILSet_STS_HHC_DataChanged();
     }

     if((ESC2_10.esc2_10.HHC_ACTIVE != Rx_buffer.esc2_10.HHC_ACTIVE))
     {
         ILSet_HHC_ACTIVE_DataChanged();
     }

   }
}

void ESC3_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC3_20.esc3_20.VACCUM_PUMP_LIFE != Rx_buffer.esc3_20.VACCUM_PUMP_LIFE))
     {
         ILSet_VACCUM_PUMP_LIFE_DataChanged();
     }

     if((ESC3_20.esc3_20.VACCUM_CONTROL != Rx_buffer.esc3_20.VACCUM_CONTROL))
     {
         ILSet_VACCUM_CONTROL_DataChanged();
     }

   }
}

void ESC5_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC5_10.esc5_10.ESC_ACTIVE != Rx_buffer.esc5_10.ESC_ACTIVE))
     {
         ILSet_ESC_ACTIVE_DataChanged();
     }

     if((ESC5_10.esc5_10.ABS_ACTIVE != Rx_buffer.esc5_10.ABS_ACTIVE))
     {
         ILSet_ABS_ACTIVE_DataChanged();
     }

     if((ESC5_10.esc5_10.STS_ESC != Rx_buffer.esc5_10.STS_ESC))
     {
         ILSet_STS_ESC_DataChanged();
     }

     if((ESC5_10.esc5_10.EBD_ACTIVE != Rx_buffer.esc5_10.EBD_ACTIVE))
     {
         ILSet_EBD_ACTIVE_DataChanged();
     }

     if((ESC5_10.esc5_10.ESC5_MSG_CNT != Rx_buffer.esc5_10.ESC5_MSG_CNT))
     {
         ILSet_ESC5_MSG_CNT_DataChanged();
     }

     if((ESC5_10.esc5_10.ESC5_CRC != Rx_buffer.esc5_10.ESC5_CRC))
     {
         ILSet_ESC5_CRC_DataChanged();
     }

   }
}

void ESC7_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC7_20.esc7_20.LATTERAL_ACCEL_0 != Rx_buffer.esc7_20.LATTERAL_ACCEL_0) || 
       (ESC7_20.esc7_20.LATTERAL_ACCEL_1 != Rx_buffer.esc7_20.LATTERAL_ACCEL_1))
     {
         ILSet_LATTERAL_ACCEL_DataChanged();
     }

     if((ESC7_20.esc7_20.LONG_ACCEL_0 != Rx_buffer.esc7_20.LONG_ACCEL_0) || 
       (ESC7_20.esc7_20.LONG_ACCEL_1 != Rx_buffer.esc7_20.LONG_ACCEL_1))
     {
         ILSet_LONG_ACCEL_DataChanged();
     }

     if((ESC7_20.esc7_20.YAW_RATE_0 != Rx_buffer.esc7_20.YAW_RATE_0) || 
       (ESC7_20.esc7_20.YAW_RATE_1 != Rx_buffer.esc7_20.YAW_RATE_1))
     {
         ILSet_YAW_RATE_DataChanged();
     }

     if((ESC7_20.esc7_20.ESC7_MSG_CNT != Rx_buffer.esc7_20.ESC7_MSG_CNT))
     {
         ILSet_ESC7_MSG_CNT_DataChanged();
     }

     if((ESC7_20.esc7_20.ESC7_CRC != Rx_buffer.esc7_20.ESC7_CRC))
     {
         ILSet_ESC7_CRC_DataChanged();
     }

   }
}

void ESC8_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC8_20.esc8_20.WHL_FL_SPD_0 != Rx_buffer.esc8_20.WHL_FL_SPD_0) || 
       (ESC8_20.esc8_20.WHL_FL_SPD_1 != Rx_buffer.esc8_20.WHL_FL_SPD_1))
     {
         ILSet_WHL_FL_SPD_DataChanged();
     }

     if((ESC8_20.esc8_20.WHL_FR_SPD_0 != Rx_buffer.esc8_20.WHL_FR_SPD_0) || 
       (ESC8_20.esc8_20.WHL_FR_SPD_1 != Rx_buffer.esc8_20.WHL_FR_SPD_1))
     {
         ILSet_WHL_FR_SPD_DataChanged();
     }

     if((ESC8_20.esc8_20.WHL_RL_SPD_0 != Rx_buffer.esc8_20.WHL_RL_SPD_0) || 
       (ESC8_20.esc8_20.WHL_RL_SPD_1 != Rx_buffer.esc8_20.WHL_RL_SPD_1))
     {
         ILSet_WHL_RL_SPD_DataChanged();
     }

     if((ESC8_20.esc8_20.WHL_RR_SPD_0 != Rx_buffer.esc8_20.WHL_RR_SPD_0) || 
       (ESC8_20.esc8_20.WHL_RR_SPD_1 != Rx_buffer.esc8_20.WHL_RR_SPD_1))
     {
         ILSet_WHL_RR_SPD_DataChanged();
     }

     if((ESC8_20.esc8_20.STS_IGN_ESC != Rx_buffer.esc8_20.STS_IGN_ESC))
     {
         ILSet_STS_IGN_ESC_DataChanged();
     }

     if((ESC8_20.esc8_20.ESC8_MSG_CNT != Rx_buffer.esc8_20.ESC8_MSG_CNT))
     {
         ILSet_ESC8_MSG_CNT_DataChanged();
     }

     if((ESC8_20.esc8_20.ESC8_CRC != Rx_buffer.esc8_20.ESC8_CRC))
     {
         ILSet_ESC8_CRC_DataChanged();
     }

   }
}

void ESCL1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESCL1_100.escl1_100.ESCL_WRN_FUNC != Rx_buffer.escl1_100.ESCL_WRN_FUNC))
     {
         ILSet_ESCL_WRN_FUNC_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL_WRN_SFTY != Rx_buffer.escl1_100.ESCL_WRN_SFTY))
     {
         ILSet_ESCL_WRN_SFTY_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL_STEER_WHL_JAM_WRN != Rx_buffer.escl1_100.ESCL_STEER_WHL_JAM_WRN))
     {
         ILSet_ESCL_STEER_WHL_JAM_WRN_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL_NOT_LOCK_WRN != Rx_buffer.escl1_100.ESCL_NOT_LOCK_WRN))
     {
         ILSet_ESCL_NOT_LOCK_WRN_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL_NOT_LEARNED_WRN != Rx_buffer.escl1_100.ESCL_NOT_LEARNED_WRN))
     {
         ILSet_ESCL_NOT_LEARNED_WRN_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL1_MSG_CNT != Rx_buffer.escl1_100.ESCL1_MSG_CNT))
     {
         ILSet_ESCL1_MSG_CNT_DataChanged();
     }

     if((ESCL1_100.escl1_100.ESCL1_CRC != Rx_buffer.escl1_100.ESCL1_CRC))
     {
         ILSet_ESCL1_CRC_DataChanged();
     }

   }
}

void ESCL_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESCL_NSM.escl_nsm.RESERVED_ESCL_0 != Rx_buffer.escl_nsm.RESERVED_ESCL_0) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_1 != Rx_buffer.escl_nsm.RESERVED_ESCL_1) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_2 != Rx_buffer.escl_nsm.RESERVED_ESCL_2) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_3 != Rx_buffer.escl_nsm.RESERVED_ESCL_3) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_4 != Rx_buffer.escl_nsm.RESERVED_ESCL_4) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_5 != Rx_buffer.escl_nsm.RESERVED_ESCL_5) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_6 != Rx_buffer.escl_nsm.RESERVED_ESCL_6) || 
       (ESCL_NSM.escl_nsm.RESERVED_ESCL_7 != Rx_buffer.escl_nsm.RESERVED_ESCL_7))
     {
         ILSet_RESERVED_ESCL_DataChanged();
     }

   }
}

void ESC_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ESC_NSM.esc_nsm.RESERVED_ESC_0 != Rx_buffer.esc_nsm.RESERVED_ESC_0) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_1 != Rx_buffer.esc_nsm.RESERVED_ESC_1) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_2 != Rx_buffer.esc_nsm.RESERVED_ESC_2) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_3 != Rx_buffer.esc_nsm.RESERVED_ESC_3) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_4 != Rx_buffer.esc_nsm.RESERVED_ESC_4) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_5 != Rx_buffer.esc_nsm.RESERVED_ESC_5) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_6 != Rx_buffer.esc_nsm.RESERVED_ESC_6) || 
       (ESC_NSM.esc_nsm.RESERVED_ESC_7 != Rx_buffer.esc_nsm.RESERVED_ESC_7))
     {
         ILSet_RESERVED_ESC_DataChanged();
     }

   }
}

void ETL1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ETL1_20.etl1_20.ETL_OPERATIONMODE != Rx_buffer.etl1_20.ETL_OPERATIONMODE))
     {
         ILSet_ETL_OPERATIONMODE_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL_PMOTORPOSITIONSTATUS != Rx_buffer.etl1_20.ETL_PMOTORPOSITIONSTATUS))
     {
         ILSet_ETL_PMOTORPOSITIONSTATUS_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL_PMOTORERRORLEVEL != Rx_buffer.etl1_20.ETL_PMOTORERRORLEVEL))
     {
         ILSet_ETL_PMOTORERRORLEVEL_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL_PMOTOR_POSITION_FAILURE != Rx_buffer.etl1_20.ETL_PMOTOR_POSITION_FAILURE))
     {
         ILSet_ETL_PMOTOR_POSITION_FAILURE_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL_SERVICE_WRN_IND != Rx_buffer.etl1_20.ETL_SERVICE_WRN_IND))
     {
         ILSet_ETL_SERVICE_WRN_IND_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL_SHIFTING_IN_PROGRESS != Rx_buffer.etl1_20.ETL_SHIFTING_IN_PROGRESS))
     {
         ILSet_ETL_SHIFTING_IN_PROGRESS_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL242_COUNTER != Rx_buffer.etl1_20.ETL242_COUNTER))
     {
         ILSet_ETL242_COUNTER_DataChanged();
     }

     if((ETL1_20.etl1_20.ETL242_CRC != Rx_buffer.etl1_20.ETL242_CRC))
     {
         ILSet_ETL242_CRC_DataChanged();
     }

   }
}

void ETL_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ETL_STS_500.etl_sts_500.ETL_STS_IGN != Rx_buffer.etl_sts_500.ETL_STS_IGN))
     {
         ILSet_ETL_STS_IGN_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_COMFLT_SGN_CONTFAIL != Rx_buffer.etl_sts_500.ETL_COMFLT_SGN_CONTFAIL))
     {
         ILSet_ETL_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_COMFLT_MSGTOUT_STS != Rx_buffer.etl_sts_500.ETL_COMFLT_MSGTOUT_STS))
     {
         ILSet_ETL_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_COMFLT_NODEABS_STS != Rx_buffer.etl_sts_500.ETL_COMFLT_NODEABS_STS))
     {
         ILSet_ETL_COMFLT_NODEABS_STS_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_UV_STS != Rx_buffer.etl_sts_500.ETL_UV_STS))
     {
         ILSet_ETL_UV_STS_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_OV_STS != Rx_buffer.etl_sts_500.ETL_OV_STS))
     {
         ILSet_ETL_OV_STS_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_AUX_BATT_VOLT != Rx_buffer.etl_sts_500.ETL_AUX_BATT_VOLT))
     {
         ILSet_ETL_AUX_BATT_VOLT_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_SW_VERSION != Rx_buffer.etl_sts_500.ETL_SW_VERSION))
     {
         ILSet_ETL_SW_VERSION_DataChanged();
     }

     if((ETL_STS_500.etl_sts_500.ETL_COMFLT_MSG_CONTFAIL != Rx_buffer.etl_sts_500.ETL_COMFLT_MSG_CONTFAIL))
     {
         ILSet_ETL_COMFLT_MSG_CONTFAIL_DataChanged();
     }

   }
}

void FATC1_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FATC1_200.fatc1_200.INCAR_TEMP != Rx_buffer.fatc1_200.INCAR_TEMP))
     {
         ILSet_INCAR_TEMP_DataChanged();
     }

     if((FATC1_200.fatc1_200.MEM_DISP != Rx_buffer.fatc1_200.MEM_DISP))
     {
         ILSet_MEM_DISP_DataChanged();
     }

     if((FATC1_200.fatc1_200.DISP_MODE != Rx_buffer.fatc1_200.DISP_MODE))
     {
         ILSet_DISP_MODE_DataChanged();
     }

     if((FATC1_200.fatc1_200.DISP_BLOWER != Rx_buffer.fatc1_200.DISP_BLOWER))
     {
         ILSet_DISP_BLOWER_DataChanged();
     }

     if((FATC1_200.fatc1_200.FRONT_RIGHT_SET_TEMP != Rx_buffer.fatc1_200.FRONT_RIGHT_SET_TEMP))
     {
         ILSet_FRONT_RIGHT_SET_TEMP_DataChanged();
     }

     if((FATC1_200.fatc1_200.FRONT_LEFT_SET_TEMP != Rx_buffer.fatc1_200.FRONT_LEFT_SET_TEMP))
     {
         ILSet_FRONT_LEFT_SET_TEMP_DataChanged();
     }

     if((FATC1_200.fatc1_200.FATC_AUTO != Rx_buffer.fatc1_200.FATC_AUTO))
     {
         ILSet_FATC_AUTO_DataChanged();
     }

     if((FATC1_200.fatc1_200.DISP_DUAL != Rx_buffer.fatc1_200.DISP_DUAL))
     {
         ILSet_DISP_DUAL_DataChanged();
     }

     if((FATC1_200.fatc1_200.FATC_ECON != Rx_buffer.fatc1_200.FATC_ECON))
     {
         ILSet_FATC_ECON_DataChanged();
     }

     if((FATC1_200.fatc1_200.AUTO_RECIRC != Rx_buffer.fatc1_200.AUTO_RECIRC))
     {
         ILSet_AUTO_RECIRC_DataChanged();
     }

     if((FATC1_200.fatc1_200.AC_SWT_STS != Rx_buffer.fatc1_200.AC_SWT_STS))
     {
         ILSet_AC_SWT_STS_DataChanged();
     }

     if((FATC1_200.fatc1_200.DISP_AC != Rx_buffer.fatc1_200.DISP_AC))
     {
         ILSet_DISP_AC_DataChanged();
     }

     if((FATC1_200.fatc1_200.STS_REAR_AC != Rx_buffer.fatc1_200.STS_REAR_AC))
     {
         ILSet_STS_REAR_AC_DataChanged();
     }

     if((FATC1_200.fatc1_200.FRESH_RECIRC != Rx_buffer.fatc1_200.FRESH_RECIRC))
     {
         ILSet_FRESH_RECIRC_DataChanged();
     }

     if((FATC1_200.fatc1_200.DISP_OFF != Rx_buffer.fatc1_200.DISP_OFF))
     {
         ILSet_DISP_OFF_DataChanged();
     }

     if((FATC1_200.fatc1_200.STS_IONIZER != Rx_buffer.fatc1_200.STS_IONIZER))
     {
         ILSet_STS_IONIZER_DataChanged();
     }

     if((FATC1_200.fatc1_200.AUTO_DEFROST != Rx_buffer.fatc1_200.AUTO_DEFROST))
     {
         ILSet_AUTO_DEFROST_DataChanged();
     }

   }
}

void FATC2_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FATC2_200.fatc2_200.DISP_AMBT_TEMP_FATC != Rx_buffer.fatc2_200.DISP_AMBT_TEMP_FATC))
     {
         ILSet_DISP_AMBT_TEMP_FATC_DataChanged();
     }

     if((FATC2_200.fatc2_200.PASSIVE_VENT_FATC_STS != Rx_buffer.fatc2_200.PASSIVE_VENT_FATC_STS))
     {
         ILSet_PASSIVE_VENT_FATC_STS_DataChanged();
     }

   }
}

void FCM1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FCM1_20.fcm1_20.AEB_ZONE_STS_FCM != Rx_buffer.fcm1_20.AEB_ZONE_STS_FCM))
     {
         ILSet_AEB_ZONE_STS_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.AEB_WARN_SET_STA_FCM != Rx_buffer.fcm1_20.AEB_WARN_SET_STA_FCM))
     {
         ILSet_AEB_WARN_SET_STA_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.AEB_WRN_FCM != Rx_buffer.fcm1_20.AEB_WRN_FCM))
     {
         ILSet_AEB_WRN_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.AEB_FAIL_INFO_FCM != Rx_buffer.fcm1_20.AEB_FAIL_INFO_FCM))
     {
         ILSet_AEB_FAIL_INFO_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.AEB_ON_OFF_STA_FCM != Rx_buffer.fcm1_20.AEB_ON_OFF_STA_FCM))
     {
         ILSet_AEB_ON_OFF_STA_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.STS_FCM != Rx_buffer.fcm1_20.STS_FCM))
     {
         ILSet_STS_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.AEB_OBJ_CLASSIFICATION_FCM != Rx_buffer.fcm1_20.AEB_OBJ_CLASSIFICATION_FCM))
     {
         ILSet_AEB_OBJ_CLASSIFICATION_FCM_DataChanged();
     }

     if((FCM1_20.fcm1_20.FCM2_MSG_COUNT != Rx_buffer.fcm1_20.FCM2_MSG_COUNT))
     {
         ILSet_FCM2_MSG_COUNT_DataChanged();
     }

     if((FCM1_20.fcm1_20.FCM2_CRC != Rx_buffer.fcm1_20.FCM2_CRC))
     {
         ILSet_FCM2_CRC_DataChanged();
     }

   }
}

void FCM_HBA_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FCM_HBA_50.fcm_hba_50.HBA_LAMP_STS != Rx_buffer.fcm_hba_50.HBA_LAMP_STS))
     {
         ILSet_HBA_LAMP_STS_DataChanged();
     }

     if((FCM_HBA_50.fcm_hba_50.HBA_STS != Rx_buffer.fcm_hba_50.HBA_STS))
     {
         ILSet_HBA_STS_DataChanged();
     }

     if((FCM_HBA_50.fcm_hba_50.HBA_USM_FB != Rx_buffer.fcm_hba_50.HBA_USM_FB))
     {
         ILSet_HBA_USM_FB_DataChanged();
     }

     if((FCM_HBA_50.fcm_hba_50.HBA_MSG_CNT != Rx_buffer.fcm_hba_50.HBA_MSG_CNT))
     {
         ILSet_HBA_MSG_CNT_DataChanged();
     }

     if((FCM_HBA_50.fcm_hba_50.HBA_CRC != Rx_buffer.fcm_hba_50.HBA_CRC))
     {
         ILSet_HBA_CRC_DataChanged();
     }

   }
}

void FCM_LKAS1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FCM_LKAS1_10.fcm_lkas1_10.LDW_LKA_MODE != Rx_buffer.fcm_lkas1_10.LDW_LKA_MODE))
     {
         ILSet_LDW_LKA_MODE_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.TJA_MODE != Rx_buffer.fcm_lkas1_10.TJA_MODE))
     {
         ILSet_TJA_MODE_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.TJA_STATE != Rx_buffer.fcm_lkas1_10.TJA_STATE))
     {
         ILSet_TJA_STATE_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LDW_LKA_SYS_STATE != Rx_buffer.fcm_lkas1_10.LDW_LKA_SYS_STATE))
     {
         ILSet_LDW_LKA_SYS_STATE_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LKA_HANDSOFF_AUDIO_WARNING != Rx_buffer.fcm_lkas1_10.LKA_HANDSOFF_AUDIO_WARNING))
     {
         ILSet_LKA_HANDSOFF_AUDIO_WARNING_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.TJA_HANDSOFF_WARNING != Rx_buffer.fcm_lkas1_10.TJA_HANDSOFF_WARNING))
     {
         ILSet_TJA_HANDSOFF_WARNING_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LDW_LKA_WARNING != Rx_buffer.fcm_lkas1_10.LDW_LKA_WARNING))
     {
         ILSet_LDW_LKA_WARNING_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LDW_LKA_LANE_RECOGN != Rx_buffer.fcm_lkas1_10.LDW_LKA_LANE_RECOGN))
     {
         ILSet_LDW_LKA_LANE_RECOGN_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LKA_HANDSOFF_DISPLAY_WARNING != Rx_buffer.fcm_lkas1_10.LKA_HANDSOFF_DISPLAY_WARNING))
     {
         ILSet_LKA_HANDSOFF_DISPLAY_WARNING_DataChanged();
     }

     if((FCM_LKAS1_10.fcm_lkas1_10.LKA_SENSITIVITY != Rx_buffer.fcm_lkas1_10.LKA_SENSITIVITY))
     {
         ILSet_LKA_SENSITIVITY_DataChanged();
     }

   }
}

void FCM_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FCM_NSM.fcm_nsm.RESERVED_FCM_0 != Rx_buffer.fcm_nsm.RESERVED_FCM_0) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_1 != Rx_buffer.fcm_nsm.RESERVED_FCM_1) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_2 != Rx_buffer.fcm_nsm.RESERVED_FCM_2) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_3 != Rx_buffer.fcm_nsm.RESERVED_FCM_3) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_4 != Rx_buffer.fcm_nsm.RESERVED_FCM_4) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_5 != Rx_buffer.fcm_nsm.RESERVED_FCM_5) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_6 != Rx_buffer.fcm_nsm.RESERVED_FCM_6) || 
       (FCM_NSM.fcm_nsm.RESERVED_FCM_7 != Rx_buffer.fcm_nsm.RESERVED_FCM_7))
     {
         ILSet_RESERVED_FCM_DataChanged();
     }

   }
}

void FCM_TSR_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FCM_TSR_100.fcm_tsr_100.TSR_DSP_SPD != Rx_buffer.fcm_tsr_100.TSR_DSP_SPD))
     {
         ILSet_TSR_DSP_SPD_DataChanged();
     }

     if((FCM_TSR_100.fcm_tsr_100.TSR_SYS_STATE != Rx_buffer.fcm_tsr_100.TSR_SYS_STATE))
     {
         ILSet_TSR_SYS_STATE_DataChanged();
     }

     if((FCM_TSR_100.fcm_tsr_100.FCM_TSR_OPT_USM != Rx_buffer.fcm_tsr_100.FCM_TSR_OPT_USM))
     {
         ILSet_FCM_TSR_OPT_USM_DataChanged();
     }

     if((FCM_TSR_100.fcm_tsr_100.TSR_OVER_TAKE_SIGN != Rx_buffer.fcm_tsr_100.TSR_OVER_TAKE_SIGN))
     {
         ILSet_TSR_OVER_TAKE_SIGN_DataChanged();
     }

   }
}

void FRM1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FRM1_20.frm1_20.ACC_VEH_SET_SPD != Rx_buffer.frm1_20.ACC_VEH_SET_SPD))
     {
         ILSet_ACC_VEH_SET_SPD_DataChanged();
     }

     if((FRM1_20.frm1_20.ACC_SET_DIST_0 != Rx_buffer.frm1_20.ACC_SET_DIST_0))
     {
         ILSet_ACC_SET_DIST_DataChanged();
     }

     if((FRM1_20.frm1_20.ACC_MODE != Rx_buffer.frm1_20.ACC_MODE))
     {
         ILSet_ACC_MODE_DataChanged();
     }

     if((FRM1_20.frm1_20.FRM1_MSG_COUNT != Rx_buffer.frm1_20.FRM1_MSG_COUNT))
     {
         ILSet_FRM1_MSG_COUNT_DataChanged();
     }

     if((FRM1_20.frm1_20.FRM1_CRC != Rx_buffer.frm1_20.FRM1_CRC))
     {
         ILSet_FRM1_CRC_DataChanged();
     }

   }
}

void FRM2_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FRM2_20.frm2_20.AEB_ZONE_STS_FRM != Rx_buffer.frm2_20.AEB_ZONE_STS_FRM))
     {
         ILSet_AEB_ZONE_STS_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.AEB_WARN_SET_STA_FRM != Rx_buffer.frm2_20.AEB_WARN_SET_STA_FRM))
     {
         ILSet_AEB_WARN_SET_STA_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.AEB_WRN_FRM != Rx_buffer.frm2_20.AEB_WRN_FRM))
     {
         ILSet_AEB_WRN_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.AEB_FAIL_INFO_FRM != Rx_buffer.frm2_20.AEB_FAIL_INFO_FRM))
     {
         ILSet_AEB_FAIL_INFO_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.AEB_ON_OFF_STA_FRM != Rx_buffer.frm2_20.AEB_ON_OFF_STA_FRM))
     {
         ILSet_AEB_ON_OFF_STA_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.STS_FRM != Rx_buffer.frm2_20.STS_FRM))
     {
         ILSet_STS_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_OBJ_CLASSIFICATION_FRM != Rx_buffer.frm2_20.ACC_OBJ_CLASSIFICATION_FRM))
     {
         ILSet_ACC_OBJ_CLASSIFICATION_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.AEB_OBJ_CLASSIFICATION_FRM != Rx_buffer.frm2_20.AEB_OBJ_CLASSIFICATION_FRM))
     {
         ILSet_AEB_OBJ_CLASSIFICATION_FRM_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_DRIVE_MODE != Rx_buffer.frm2_20.ACC_DRIVE_MODE))
     {
         ILSet_ACC_DRIVE_MODE_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_TGT_VALIDITY != Rx_buffer.frm2_20.ACC_TGT_VALIDITY))
     {
         ILSet_ACC_TGT_VALIDITY_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_SYS_FAILURE != Rx_buffer.frm2_20.ACC_SYS_FAILURE))
     {
         ILSet_ACC_SYS_FAILURE_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_SYS_STATE != Rx_buffer.frm2_20.ACC_SYS_STATE))
     {
         ILSet_ACC_SYS_STATE_DataChanged();
     }

     if((FRM2_20.frm2_20.ACC_SYS_INFO != Rx_buffer.frm2_20.ACC_SYS_INFO))
     {
         ILSet_ACC_SYS_INFO_DataChanged();
     }

     if((FRM2_20.frm2_20.FRM2_MSG_COUNT != Rx_buffer.frm2_20.FRM2_MSG_COUNT))
     {
         ILSet_FRM2_MSG_COUNT_DataChanged();
     }

     if((FRM2_20.frm2_20.FRM2_CRC != Rx_buffer.frm2_20.FRM2_CRC))
     {
         ILSet_FRM2_CRC_DataChanged();
     }

   }
}

void FRM3_TEST_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FRM3_TEST_100.frm3_test_100.TIME_GAP_FRM != Rx_buffer.frm3_test_100.TIME_GAP_FRM))
     {
         ILSet_TIME_GAP_FRM_DataChanged();
     }

   }
}

void FRM_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FRM_NSM.frm_nsm.RESERVED_FRM_0 != Rx_buffer.frm_nsm.RESERVED_FRM_0) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_1 != Rx_buffer.frm_nsm.RESERVED_FRM_1) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_2 != Rx_buffer.frm_nsm.RESERVED_FRM_2) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_3 != Rx_buffer.frm_nsm.RESERVED_FRM_3) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_4 != Rx_buffer.frm_nsm.RESERVED_FRM_4) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_5 != Rx_buffer.frm_nsm.RESERVED_FRM_5) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_6 != Rx_buffer.frm_nsm.RESERVED_FRM_6) || 
       (FRM_NSM.frm_nsm.RESERVED_FRM_7 != Rx_buffer.frm_nsm.RESERVED_FRM_7))
     {
         ILSet_RESERVED_FRM_DataChanged();
     }

   }
}

void FVC1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((FVC1_100.fvc1_100.FVC_BUTTON_GROUP != Rx_buffer.fvc1_100.FVC_BUTTON_GROUP))
     {
         ILSet_FVC_BUTTON_GROUP_DataChanged();
     }

     if((FVC1_100.fvc1_100.FVC_OPERATION_STATE != Rx_buffer.fvc1_100.FVC_OPERATION_STATE))
     {
         ILSet_FVC_OPERATION_STATE_DataChanged();
     }

   }
}

void GW1_1000_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((GW1_1000.gw1_1000.STS_CODE_FOTA != Rx_buffer.gw1_1000.STS_CODE_FOTA))
     {
         ILSet_STS_CODE_FOTA_DataChanged();
     }

     if((GW1_1000.gw1_1000.METADATA_ID_FOTA != Rx_buffer.gw1_1000.METADATA_ID_FOTA))
     {
         ILSet_METADATA_ID_FOTA_DataChanged();
     }

     if((GW1_1000.gw1_1000.LAST_EXECUTED_STEP_FOTA != Rx_buffer.gw1_1000.LAST_EXECUTED_STEP_FOTA))
     {
         ILSet_LAST_EXECUTED_STEP_FOTA_DataChanged();
     }

     if((GW1_1000.gw1_1000.READY_UPDATE_DOWNLOAD_FOTA != Rx_buffer.gw1_1000.READY_UPDATE_DOWNLOAD_FOTA))
     {
         ILSet_READY_UPDATE_DOWNLOAD_FOTA_DataChanged();
     }

     if((GW1_1000.gw1_1000.REQ_REPROG_FOTA != Rx_buffer.gw1_1000.REQ_REPROG_FOTA))
     {
         ILSet_REQ_REPROG_FOTA_DataChanged();
     }

     if((GW1_1000.gw1_1000.PRECNT_COMPLETION != Rx_buffer.gw1_1000.PRECNT_COMPLETION))
     {
         ILSet_PRECNT_COMPLETION_DataChanged();
     }

   }
}

void GW_HEARTBEAT_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((GW_HEARTBEAT.gw_heartbeat.IGN_STS != Rx_buffer.gw_heartbeat.IGN_STS))
     {
         ILSet_IGN_STS_DataChanged();
     }

     if((GW_HEARTBEAT.gw_heartbeat.BATT_VOLTAGE != Rx_buffer.gw_heartbeat.BATT_VOLTAGE))
     {
         ILSet_BATT_VOLTAGE_DataChanged();
     }

     if((GW_HEARTBEAT.gw_heartbeat.GW_CH_STS != Rx_buffer.gw_heartbeat.GW_CH_STS))
     {
         ILSet_GW_CH_STS_DataChanged();
     }

     if((GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_0 != Rx_buffer.gw_heartbeat.IGN_CNTR_0) || 
       (GW_HEARTBEAT.gw_heartbeat.IGN_CNTR_1 != Rx_buffer.gw_heartbeat.IGN_CNTR_1))
     {
         ILSet_IGN_CNTR_DataChanged();
     }

   }
}

void HLCU1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((HLCU1_100.hlcu1_100.STS_HIGHBEAM_BOOSTER != Rx_buffer.hlcu1_100.STS_HIGHBEAM_BOOSTER))
     {
         ILSet_STS_HIGHBEAM_BOOSTER_DataChanged();
     }

     if((HLCU1_100.hlcu1_100.HEADLAMP_AUTO_LEVEL != Rx_buffer.hlcu1_100.HEADLAMP_AUTO_LEVEL))
     {
         ILSet_HEADLAMP_AUTO_LEVEL_DataChanged();
     }

   }
}

void HLCU2_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((HLCU2_100.hlcu2_100.STS_HIGHBEAM_BOOSTER_1 != Rx_buffer.hlcu2_100.STS_HIGHBEAM_BOOSTER_1))
     {
         ILSet_STS_HIGHBEAM_BOOSTER_1_DataChanged();
     }

   }
}

void ICC1_1000_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ICC1_1000.icc1_1000.TRANSFER_MODE_ICC != Rx_buffer.icc1_1000.TRANSFER_MODE_ICC))
     {
         ILSet_TRANSFER_MODE_ICC_DataChanged();
     }

     if((ICC1_1000.icc1_1000.ICC_ALERT_MSG != Rx_buffer.icc1_1000.ICC_ALERT_MSG))
     {
         ILSet_ICC_ALERT_MSG_DataChanged();
     }

   }
}

void ICC2_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((ICC2_50.icc2_50.BUTTON1_STS != Rx_buffer.icc2_50.BUTTON1_STS))
     {
         ILSet_BUTTON1_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.BUTTON2_STS != Rx_buffer.icc2_50.BUTTON2_STS))
     {
         ILSet_BUTTON2_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.BUTTON3_STS != Rx_buffer.icc2_50.BUTTON3_STS))
     {
         ILSet_BUTTON3_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.BUTTON4_STS != Rx_buffer.icc2_50.BUTTON4_STS))
     {
         ILSet_BUTTON4_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.JOYSTICK_LB_STS != Rx_buffer.icc2_50.JOYSTICK_LB_STS))
     {
         ILSet_JOYSTICK_LB_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.JOYSTICK_RB_STS != Rx_buffer.icc2_50.JOYSTICK_RB_STS))
     {
         ILSet_JOYSTICK_RB_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.JOYSTICK_UB_STS != Rx_buffer.icc2_50.JOYSTICK_UB_STS))
     {
         ILSet_JOYSTICK_UB_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.JOYSTICK_DB_STS != Rx_buffer.icc2_50.JOYSTICK_DB_STS))
     {
         ILSet_JOYSTICK_DB_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.CENTER_BUTTON_STS != Rx_buffer.icc2_50.CENTER_BUTTON_STS))
     {
         ILSet_CENTER_BUTTON_STS_DataChanged();
     }

     if((ICC2_50.icc2_50.ROTARY_ENCODER != Rx_buffer.icc2_50.ROTARY_ENCODER))
     {
         ILSet_ROTARY_ENCODER_DataChanged();
     }

   }
}

void LDC1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((LDC1_100.ldc1_100.LDC_COOLINGREQUEST != Rx_buffer.ldc1_100.LDC_COOLINGREQUEST))
     {
         ILSet_LDC_COOLINGREQUEST_DataChanged();
     }

     if((LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_0 != Rx_buffer.ldc1_100.LDC_SECONDARY_TEMPERATURE_0) || 
       (LDC1_100.ldc1_100.LDC_SECONDARY_TEMPERATURE_1 != Rx_buffer.ldc1_100.LDC_SECONDARY_TEMPERATURE_1))
     {
         ILSet_LDC_SECONDARY_TEMPERATURE_DataChanged();
     }

     if((LDC1_100.ldc1_100.LDC_PROTECTIONMODE != Rx_buffer.ldc1_100.LDC_PROTECTIONMODE))
     {
         ILSet_LDC_PROTECTIONMODE_DataChanged();
     }

     if((LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_0 != Rx_buffer.ldc1_100.LDC_PRIMARY_TEMPERATURE_0) || 
       (LDC1_100.ldc1_100.LDC_PRIMARY_TEMPERATURE_1 != Rx_buffer.ldc1_100.LDC_PRIMARY_TEMPERATURE_1))
     {
         ILSet_LDC_PRIMARY_TEMPERATURE_DataChanged();
     }

     if((LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_0 != Rx_buffer.ldc1_100.LDC_MOSFET_TEMPERATURE_0) || 
       (LDC1_100.ldc1_100.LDC_MOSFET_TEMPERATURE_1 != Rx_buffer.ldc1_100.LDC_MOSFET_TEMPERATURE_1))
     {
         ILSet_LDC_MOSFET_TEMPERATURE_DataChanged();
     }

   }
}

void LDC2_30_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_0 != Rx_buffer.ldc2_30.LDC_INPUTVOLTAGEVALUE_0) || 
       (LDC2_30.ldc2_30.LDC_INPUTVOLTAGEVALUE_1 != Rx_buffer.ldc2_30.LDC_INPUTVOLTAGEVALUE_1))
     {
         ILSet_LDC_INPUTVOLTAGEVALUE_DataChanged();
     }

     if((LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_0 != Rx_buffer.ldc2_30.LDC_OUTPUTCURRENT_0) || 
       (LDC2_30.ldc2_30.LDC_OUTPUTCURRENT_1 != Rx_buffer.ldc2_30.LDC_OUTPUTCURRENT_1))
     {
         ILSet_LDC_OUTPUTCURRENT_DataChanged();
     }

     if((LDC2_30.ldc2_30.LDC_INPUTCURRENTVALUE != Rx_buffer.ldc2_30.LDC_INPUTCURRENTVALUE))
     {
         ILSet_LDC_INPUTCURRENTVALUE_DataChanged();
     }

     if((LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_0 != Rx_buffer.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_0) || 
       (LDC2_30.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_1 != Rx_buffer.ldc2_30.LDC_OUTPUTVOLTAGEVALUE_1))
     {
         ILSet_LDC_OUTPUTVOLTAGEVALUE_DataChanged();
     }

   }
}

void LDC3_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((LDC3_100.ldc3_100.LDC_AMB_OVER_TEMP_SHUTDOWN != Rx_buffer.ldc3_100.LDC_AMB_OVER_TEMP_SHUTDOWN))
     {
         ILSet_LDC_AMB_OVER_TEMP_SHUTDOWN_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_AMB_OVER_TEMP_WNG != Rx_buffer.ldc3_100.LDC_AMB_OVER_TEMP_WNG))
     {
         ILSet_LDC_AMB_OVER_TEMP_WNG_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_SHUTDOWN != Rx_buffer.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_SHUTDOWN))
     {
         ILSet_LDC_HEAT_SINK_OVER_TEMP_SHUTDOWN_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_0 != Rx_buffer.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_0))
     {
         ILSet_LDC_HEAT_SINK_OVER_TEMP_WNG_0_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_1 != Rx_buffer.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_1))
     {
         ILSet_LDC_HEAT_SINK_OVER_TEMP_WNG_1_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_2 != Rx_buffer.ldc3_100.LDC_HEAT_SINK_OVER_TEMP_WNG_2))
     {
         ILSet_LDC_HEAT_SINK_OVER_TEMP_WNG_2_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_INPUT_OVER_VOLTAGE != Rx_buffer.ldc3_100.LDC_INPUT_OVER_VOLTAGE))
     {
         ILSet_LDC_INPUT_OVER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_INPUT_UNDER_VOLTAGE != Rx_buffer.ldc3_100.LDC_INPUT_UNDER_VOLTAGE))
     {
         ILSet_LDC_INPUT_UNDER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_LPS_OVER_VOLTAGE != Rx_buffer.ldc3_100.LDC_LPS_OVER_VOLTAGE))
     {
         ILSet_LDC_LPS_OVER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_LPS_UNDER_VOLTAGE != Rx_buffer.ldc3_100.LDC_LPS_UNDER_VOLTAGE))
     {
         ILSet_LDC_LPS_UNDER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_OUTPUT_OVER_CURRENT != Rx_buffer.ldc3_100.LDC_OUTPUT_OVER_CURRENT))
     {
         ILSet_LDC_OUTPUT_OVER_CURRENT_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_OUTPUT_OVER_VOLTAGE != Rx_buffer.ldc3_100.LDC_OUTPUT_OVER_VOLTAGE))
     {
         ILSet_LDC_OUTPUT_OVER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_OUTPUT_UNDER_VOLTAGE != Rx_buffer.ldc3_100.LDC_OUTPUT_UNDER_VOLTAGE))
     {
         ILSet_LDC_OUTPUT_UNDER_VOLTAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_SHORT_CIRCUIT != Rx_buffer.ldc3_100.LDC_SHORT_CIRCUIT))
     {
         ILSet_LDC_SHORT_CIRCUIT_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_EEPROM_FAILURE != Rx_buffer.ldc3_100.LDC_EEPROM_FAILURE))
     {
         ILSet_LDC_EEPROM_FAILURE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_IPC_COMM_ERR_OBC != Rx_buffer.ldc3_100.LDC_IPC_COMM_ERR_OBC))
     {
         ILSet_LDC_IPC_COMM_ERR_OBC_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_TEMP_SENSING_FAILURE != Rx_buffer.ldc3_100.LDC_TEMP_SENSING_FAILURE))
     {
         ILSet_LDC_TEMP_SENSING_FAILURE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_VCU_NODE_ABSENT != Rx_buffer.ldc3_100.LDC_VCU_NODE_ABSENT))
     {
         ILSet_LDC_VCU_NODE_ABSENT_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_WATCHDOG_FAILURE != Rx_buffer.ldc3_100.LDC_WATCHDOG_FAILURE))
     {
         ILSet_LDC_WATCHDOG_FAILURE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_INPUT_OVER_CURRENT != Rx_buffer.ldc3_100.LDC_INPUT_OVER_CURRENT))
     {
         ILSet_LDC_INPUT_OVER_CURRENT_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_INTERNAL_FAIL != Rx_buffer.ldc3_100.LDC_INTERNAL_FAIL))
     {
         ILSet_LDC_INTERNAL_FAIL_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_IPV_CIRCUIT_ERROR != Rx_buffer.ldc3_100.LDC_IPV_CIRCUIT_ERROR))
     {
         ILSet_LDC_IPV_CIRCUIT_ERROR_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_OPV_CIRCUIT_ERROR != Rx_buffer.ldc3_100.LDC_OPV_CIRCUIT_ERROR))
     {
         ILSet_LDC_OPV_CIRCUIT_ERROR_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_LOW_TEMP_SHUTDOWN != Rx_buffer.ldc3_100.LDC_LOW_TEMP_SHUTDOWN))
     {
         ILSet_LDC_LOW_TEMP_SHUTDOWN_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_VPROG_OUT_OF_RANGE != Rx_buffer.ldc3_100.LDC_VPROG_OUT_OF_RANGE))
     {
         ILSet_LDC_VPROG_OUT_OF_RANGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_DEBOUNCE_COUNT != Rx_buffer.ldc3_100.LDC_DEBOUNCE_COUNT))
     {
         ILSet_LDC_DEBOUNCE_COUNT_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_STAGE_0 != Rx_buffer.ldc3_100.LDC_STAGE_0))
     {
         ILSet_LDC_STAGE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HW_ENABLE != Rx_buffer.ldc3_100.LDC_HW_ENABLE))
     {
         ILSet_LDC_HW_ENABLE_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_BURST_MODE_STS != Rx_buffer.ldc3_100.LDC_BURST_MODE_STS))
     {
         ILSet_LDC_BURST_MODE_STS_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_CC_CV_STS != Rx_buffer.ldc3_100.LDC_CC_CV_STS))
     {
         ILSet_LDC_CC_CV_STS_DataChanged();
     }

     if((LDC3_100.ldc3_100.LDC_HVDC_SIDE_RELAY_STS != Rx_buffer.ldc3_100.LDC_HVDC_SIDE_RELAY_STS))
     {
         ILSet_LDC_HVDC_SIDE_RELAY_STS_DataChanged();
     }

   }
}

void LDC4_30_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((LDC4_30.ldc4_30.LDC_HVIL_INTERLOCK1 != Rx_buffer.ldc4_30.LDC_HVIL_INTERLOCK1))
     {
         ILSet_LDC_HVIL_INTERLOCK1_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_HVIL_INTERLOCK2 != Rx_buffer.ldc4_30.LDC_HVIL_INTERLOCK2))
     {
         ILSet_LDC_HVIL_INTERLOCK2_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_HVIL_INTERLOCK3 != Rx_buffer.ldc4_30.LDC_HVIL_INTERLOCK3))
     {
         ILSet_LDC_HVIL_INTERLOCK3_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_HVIL_INTERLOCK4 != Rx_buffer.ldc4_30.LDC_HVIL_INTERLOCK4))
     {
         ILSet_LDC_HVIL_INTERLOCK4_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_LID_STS != Rx_buffer.ldc4_30.LDC_LID_STS))
     {
         ILSet_LDC_LID_STS_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_ACTV_DISCHARGE_STS != Rx_buffer.ldc4_30.LDC_ACTV_DISCHARGE_STS))
     {
         ILSet_LDC_ACTV_DISCHARGE_STS_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_0 != Rx_buffer.ldc4_30.LDC_FCVOLTAGEVALUE_0) || 
       (LDC4_30.ldc4_30.LDC_FCVOLTAGEVALUE_1 != Rx_buffer.ldc4_30.LDC_FCVOLTAGEVALUE_1))
     {
         ILSet_LDC_FCVOLTAGEVALUE_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC_OPERATIONMODE != Rx_buffer.ldc4_30.LDC_OPERATIONMODE))
     {
         ILSet_LDC_OPERATIONMODE_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC274_COUNTER != Rx_buffer.ldc4_30.LDC274_COUNTER))
     {
         ILSet_LDC274_COUNTER_DataChanged();
     }

     if((LDC4_30.ldc4_30.LDC274_CRC != Rx_buffer.ldc4_30.LDC274_CRC))
     {
         ILSet_LDC274_CRC_DataChanged();
     }

   }
}

void LDC_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((LDC_STS_500.ldc_sts_500.LDC_STS_IGN_NM != Rx_buffer.ldc_sts_500.LDC_STS_IGN_NM))
     {
         ILSet_LDC_STS_IGN_NM_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_VARIANT_CODE_ERR_STS != Rx_buffer.ldc_sts_500.LDC_VARIANT_CODE_ERR_STS))
     {
         ILSet_LDC_VARIANT_CODE_ERR_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_COMFLT_SGN_CONTFAIL != Rx_buffer.ldc_sts_500.LDC_COMFLT_SGN_CONTFAIL))
     {
         ILSet_LDC_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_FEATURE_CODE_ERR_STS != Rx_buffer.ldc_sts_500.LDC_FEATURE_CODE_ERR_STS))
     {
         ILSet_LDC_FEATURE_CODE_ERR_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_COMFLT_MSGTOUT_STS != Rx_buffer.ldc_sts_500.LDC_COMFLT_MSGTOUT_STS))
     {
         ILSet_LDC_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_COMFLT_NODEABS_STS != Rx_buffer.ldc_sts_500.LDC_COMFLT_NODEABS_STS))
     {
         ILSet_LDC_COMFLT_NODEABS_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_UV_STS != Rx_buffer.ldc_sts_500.LDC_UV_STS))
     {
         ILSet_LDC_UV_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_OV_STS != Rx_buffer.ldc_sts_500.LDC_OV_STS))
     {
         ILSet_LDC_OV_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_AUX_BATT_VOLT != Rx_buffer.ldc_sts_500.LDC_AUX_BATT_VOLT))
     {
         ILSet_LDC_AUX_BATT_VOLT_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_SW_VERSION != Rx_buffer.ldc_sts_500.LDC_SW_VERSION))
     {
         ILSet_LDC_SW_VERSION_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_NM_ACTIVE_STS != Rx_buffer.ldc_sts_500.LDC_NM_ACTIVE_STS))
     {
         ILSet_LDC_NM_ACTIVE_STS_DataChanged();
     }

     if((LDC_STS_500.ldc_sts_500.LDC_COMFLT_MSG_CONTFAIL != Rx_buffer.ldc_sts_500.LDC_COMFLT_MSG_CONTFAIL))
     {
         ILSet_LDC_COMFLT_MSG_CONTFAIL_DataChanged();
     }

   }
}

void MBFM10_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM10_100.mbfm10_100.TPMS_SENSOR_BAT_STS != Rx_buffer.mbfm10_100.TPMS_SENSOR_BAT_STS))
     {
         ILSet_TPMS_SENSOR_BAT_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.TPMS_SENSOR_FAULT_STS != Rx_buffer.mbfm10_100.TPMS_SENSOR_FAULT_STS))
     {
         ILSet_TPMS_SENSOR_FAULT_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_SIREN != Rx_buffer.mbfm10_100.STS_SIREN))
     {
         ILSet_STS_SIREN_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.RF_INTERFERENCE_STS != Rx_buffer.mbfm10_100.RF_INTERFERENCE_STS))
     {
         ILSet_RF_INTERFERENCE_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.TIRE_BALANCE_STS != Rx_buffer.mbfm10_100.TIRE_BALANCE_STS))
     {
         ILSet_TIRE_BALANCE_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_AUTO_LOCATION != Rx_buffer.mbfm10_100.STS_AUTO_LOCATION))
     {
         ILSet_STS_AUTO_LOCATION_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.SENSOR_LEARNT_STS != Rx_buffer.mbfm10_100.SENSOR_LEARNT_STS))
     {
         ILSet_SENSOR_LEARNT_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.WIPER_VOL_LVL != Rx_buffer.mbfm10_100.WIPER_VOL_LVL))
     {
         ILSet_WIPER_VOL_LVL_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.CHARGE_FLAP_STS != Rx_buffer.mbfm10_100.CHARGE_FLAP_STS))
     {
         ILSet_CHARGE_FLAP_STS_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_AMB_LIGHT != Rx_buffer.mbfm10_100.STS_AMB_LIGHT))
     {
         ILSet_STS_AMB_LIGHT_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.FR_SEAT_HEAT_VENT_LEVEL_MBFM != Rx_buffer.mbfm10_100.FR_SEAT_HEAT_VENT_LEVEL_MBFM))
     {
         ILSet_FR_SEAT_HEAT_VENT_LEVEL_MBFM_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.FL_SEAT_HEAT_VENT_LEVEL_MBFM != Rx_buffer.mbfm10_100.FL_SEAT_HEAT_VENT_LEVEL_MBFM))
     {
         ILSet_FL_SEAT_HEAT_VENT_LEVEL_MBFM_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.ECU_DEFECT != Rx_buffer.mbfm10_100.ECU_DEFECT))
     {
         ILSet_ECU_DEFECT_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.TIRE_FILL_LOCATION != Rx_buffer.mbfm10_100.TIRE_FILL_LOCATION))
     {
         ILSet_TIRE_FILL_LOCATION_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_FRNT_WIPER != Rx_buffer.mbfm10_100.STS_FRNT_WIPER))
     {
         ILSet_STS_FRNT_WIPER_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_WIPER_SWT != Rx_buffer.mbfm10_100.STS_WIPER_SWT))
     {
         ILSet_STS_WIPER_SWT_DataChanged();
     }

     if((MBFM10_100.mbfm10_100.STS_REAR_WIPER_SWT != Rx_buffer.mbfm10_100.STS_REAR_WIPER_SWT))
     {
         ILSet_STS_REAR_WIPER_SWT_DataChanged();
     }

   }
}

void MBFM14_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM14_100.mbfm14_100.RLS_IR_BRIGHTNESS != Rx_buffer.mbfm14_100.RLS_IR_BRIGHTNESS))
     {
         ILSet_RLS_IR_BRIGHTNESS_DataChanged();
     }

     if((MBFM14_100.mbfm14_100.RLS_SOLAR_LEFT != Rx_buffer.mbfm14_100.RLS_SOLAR_LEFT))
     {
         ILSet_RLS_SOLAR_LEFT_DataChanged();
     }

     if((MBFM14_100.mbfm14_100.RLS_SOLAR_RIGHT != Rx_buffer.mbfm14_100.RLS_SOLAR_RIGHT))
     {
         ILSet_RLS_SOLAR_RIGHT_DataChanged();
     }

     if((MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_0 != Rx_buffer.mbfm14_100.RLS_FW_BRIGHTNESS_0) || 
       (MBFM14_100.mbfm14_100.RLS_FW_BRIGHTNESS_1 != Rx_buffer.mbfm14_100.RLS_FW_BRIGHTNESS_1))
     {
         ILSet_RLS_FW_BRIGHTNESS_DataChanged();
     }

     if((MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_0 != Rx_buffer.mbfm14_100.RLS_AMB_BRIGHTNESS_0) || 
       (MBFM14_100.mbfm14_100.RLS_AMB_BRIGHTNESS_1 != Rx_buffer.mbfm14_100.RLS_AMB_BRIGHTNESS_1))
     {
         ILSet_RLS_AMB_BRIGHTNESS_DataChanged();
     }

     if((MBFM14_100.mbfm14_100.RLS_WINDOW_CLOSE_REQ != Rx_buffer.mbfm14_100.RLS_WINDOW_CLOSE_REQ))
     {
         ILSet_RLS_WINDOW_CLOSE_REQ_DataChanged();
     }

   }
}

void MBFM15_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM15_10.mbfm15_10.STS_ELOCKER_ALERT != Rx_buffer.mbfm15_10.STS_ELOCKER_ALERT))
     {
         ILSet_STS_ELOCKER_ALERT_DataChanged();
     }

     if((MBFM15_10.mbfm15_10.STS_ELOCKER_ACTIVATION_LED != Rx_buffer.mbfm15_10.STS_ELOCKER_ACTIVATION_LED))
     {
         ILSet_STS_ELOCKER_ACTIVATION_LED_DataChanged();
     }

     if((MBFM15_10.mbfm15_10.STS_ELOCKER_MALFUNCTION_LED != Rx_buffer.mbfm15_10.STS_ELOCKER_MALFUNCTION_LED))
     {
         ILSet_STS_ELOCKER_MALFUNCTION_LED_DataChanged();
     }

   }
}

void MBFM16_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM16_200.mbfm16_200.IBS_SOC_MBFM != Rx_buffer.mbfm16_200.IBS_SOC_MBFM))
     {
         ILSet_IBS_SOC_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.IBS_SOH_MBFM != Rx_buffer.mbfm16_200.IBS_SOH_MBFM))
     {
         ILSet_IBS_SOH_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.IBS_SOF_MBFM != Rx_buffer.mbfm16_200.IBS_SOF_MBFM))
     {
         ILSet_IBS_SOF_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.ALTERNATOR_MODE_MBFM != Rx_buffer.mbfm16_200.ALTERNATOR_MODE_MBFM))
     {
         ILSet_ALTERNATOR_MODE_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.BATT_CHARGE_LAMP_INDC_MBFM != Rx_buffer.mbfm16_200.BATT_CHARGE_LAMP_INDC_MBFM))
     {
         ILSet_BATT_CHARGE_LAMP_INDC_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.STS_ESS_DEACTIVATION_MBFM != Rx_buffer.mbfm16_200.STS_ESS_DEACTIVATION_MBFM))
     {
         ILSet_STS_ESS_DEACTIVATION_MBFM_DataChanged();
     }

     if((MBFM16_200.mbfm16_200.BATT_RESET_FLG_MBFM != Rx_buffer.mbfm16_200.BATT_RESET_FLG_MBFM))
     {
         ILSet_BATT_RESET_FLG_MBFM_DataChanged();
     }

   }
}

void MBFM17_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_0 != Rx_buffer.mbfm17_200.IBS_CURRENT_MBFM_0) || 
       (MBFM17_200.mbfm17_200.IBS_CURRENT_MBFM_1 != Rx_buffer.mbfm17_200.IBS_CURRENT_MBFM_1))
     {
         ILSet_IBS_CURRENT_MBFM_DataChanged();
     }

     if((MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_0 != Rx_buffer.mbfm17_200.IBS_BATT_VOLT_MBFM_0) || 
       (MBFM17_200.mbfm17_200.IBS_BATT_VOLT_MBFM_1 != Rx_buffer.mbfm17_200.IBS_BATT_VOLT_MBFM_1))
     {
         ILSet_IBS_BATT_VOLT_MBFM_DataChanged();
     }

     if((MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_0 != Rx_buffer.mbfm17_200.IBS_BATT_TEMP_MBFM_0) || 
       (MBFM17_200.mbfm17_200.IBS_BATT_TEMP_MBFM_1 != Rx_buffer.mbfm17_200.IBS_BATT_TEMP_MBFM_1))
     {
         ILSet_IBS_BATT_TEMP_MBFM_DataChanged();
     }

   }
}

void MBFM1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM1_100.mbfm1_100.INDC_FRNT_FOG != Rx_buffer.mbfm1_100.INDC_FRNT_FOG))
     {
         ILSet_INDC_FRNT_FOG_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.INDC_REAR_FOG != Rx_buffer.mbfm1_100.INDC_REAR_FOG))
     {
         ILSet_INDC_REAR_FOG_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.INDC_PARK_BRK != Rx_buffer.mbfm1_100.INDC_PARK_BRK))
     {
         ILSet_INDC_PARK_BRK_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_PARKLAMP != Rx_buffer.mbfm1_100.STS_PARKLAMP))
     {
         ILSet_STS_PARKLAMP_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.INDC_TURN_FLSHR != Rx_buffer.mbfm1_100.INDC_TURN_FLSHR))
     {
         ILSet_INDC_TURN_FLSHR_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_IGN != Rx_buffer.mbfm1_100.STS_IGN))
     {
         ILSet_STS_IGN_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.KEY_IN_REMINDER != Rx_buffer.mbfm1_100.KEY_IN_REMINDER))
     {
         ILSet_KEY_IN_REMINDER_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.PARK_LAMP_ON_REMINDER != Rx_buffer.mbfm1_100.PARK_LAMP_ON_REMINDER))
     {
         ILSet_PARK_LAMP_ON_REMINDER_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_BRAKE_FLUID_LVL != Rx_buffer.mbfm1_100.STS_BRAKE_FLUID_LVL))
     {
         ILSet_STS_BRAKE_FLUID_LVL_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.ENG_OFF_TIME_0 != Rx_buffer.mbfm1_100.ENG_OFF_TIME_0) || 
       (MBFM1_100.mbfm1_100.ENG_OFF_TIME_1 != Rx_buffer.mbfm1_100.ENG_OFF_TIME_1))
     {
         ILSet_ENG_OFF_TIME_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.SECURITY_LED_MBFM != Rx_buffer.mbfm1_100.SECURITY_LED_MBFM))
     {
         ILSet_SECURITY_LED_MBFM_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_DOOR != Rx_buffer.mbfm1_100.STS_DOOR))
     {
         ILSet_STS_DOOR_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_RKE_BATT != Rx_buffer.mbfm1_100.STS_RKE_BATT))
     {
         ILSet_STS_RKE_BATT_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_TRAILER != Rx_buffer.mbfm1_100.STS_TRAILER))
     {
         ILSet_STS_TRAILER_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_HIGH_BEAM != Rx_buffer.mbfm1_100.STS_HIGH_BEAM))
     {
         ILSet_STS_HIGH_BEAM_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_REAR_DEFOG_LOAD != Rx_buffer.mbfm1_100.STS_REAR_DEFOG_LOAD))
     {
         ILSet_STS_REAR_DEFOG_LOAD_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_SEAT_BLT_DRV_MBFM != Rx_buffer.mbfm1_100.STS_SEAT_BLT_DRV_MBFM))
     {
         ILSet_STS_SEAT_BLT_DRV_MBFM_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_LOW_BEAM != Rx_buffer.mbfm1_100.STS_LOW_BEAM))
     {
         ILSet_STS_LOW_BEAM_DataChanged();
     }

     if((MBFM1_100.mbfm1_100.STS_RKE != Rx_buffer.mbfm1_100.STS_RKE))
     {
         ILSet_STS_RKE_DataChanged();
     }

   }
}

void MBFM5_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM5_100.mbfm5_100.TPMS_ID_NOT_LEARNT != Rx_buffer.mbfm5_100.TPMS_ID_NOT_LEARNT))
     {
         ILSet_TPMS_ID_NOT_LEARNT_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.TPMS_SIGNAL_MISSING != Rx_buffer.mbfm5_100.TPMS_SIGNAL_MISSING))
     {
         ILSet_TPMS_SIGNAL_MISSING_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.TPMS_PROG_MODE != Rx_buffer.mbfm5_100.TPMS_PROG_MODE))
     {
         ILSet_TPMS_PROG_MODE_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.HIGH_TYRE_TEMPERATURE != Rx_buffer.mbfm5_100.HIGH_TYRE_TEMPERATURE))
     {
         ILSet_HIGH_TYRE_TEMPERATURE_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.LOW_TYRE_PRESSURE != Rx_buffer.mbfm5_100.LOW_TYRE_PRESSURE))
     {
         ILSet_LOW_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.SPARE_TYRE_SWAP != Rx_buffer.mbfm5_100.SPARE_TYRE_SWAP))
     {
         ILSet_SPARE_TYRE_SWAP_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.HIGH_TYRE_PRESSURE != Rx_buffer.mbfm5_100.HIGH_TYRE_PRESSURE))
     {
         ILSet_HIGH_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.TPMS_LEAKAGE_ALERT != Rx_buffer.mbfm5_100.TPMS_LEAKAGE_ALERT))
     {
         ILSet_TPMS_LEAKAGE_ALERT_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.STS_DOOR_LATCH != Rx_buffer.mbfm5_100.STS_DOOR_LATCH))
     {
         ILSet_STS_DOOR_LATCH_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.TPMS_SYSTEM_FAULT != Rx_buffer.mbfm5_100.TPMS_SYSTEM_FAULT))
     {
         ILSet_TPMS_SYSTEM_FAULT_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.REQ_TFA_PATTERN != Rx_buffer.mbfm5_100.REQ_TFA_PATTERN))
     {
         ILSet_REQ_TFA_PATTERN_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.STS_TPMS_LED != Rx_buffer.mbfm5_100.STS_TPMS_LED))
     {
         ILSet_STS_TPMS_LED_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.VEH_THEFT_STS != Rx_buffer.mbfm5_100.VEH_THEFT_STS))
     {
         ILSet_VEH_THEFT_STS_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.STS_DRL != Rx_buffer.mbfm5_100.STS_DRL))
     {
         ILSet_STS_DRL_DataChanged();
     }

     if((MBFM5_100.mbfm5_100.REQ_TFA_DISPLAY != Rx_buffer.mbfm5_100.REQ_TFA_DISPLAY))
     {
         ILSet_REQ_TFA_DISPLAY_DataChanged();
     }

   }
}

void MBFM6_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM6_100.mbfm6_100.FL_TYRE_PRESSURE != Rx_buffer.mbfm6_100.FL_TYRE_PRESSURE))
     {
         ILSet_FL_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.FR_TYRE_PRESSURE != Rx_buffer.mbfm6_100.FR_TYRE_PRESSURE))
     {
         ILSet_FR_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.RL_TYRE_PRESSURE != Rx_buffer.mbfm6_100.RL_TYRE_PRESSURE))
     {
         ILSet_RL_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.RR_TYRE_PRESSURE != Rx_buffer.mbfm6_100.RR_TYRE_PRESSURE))
     {
         ILSet_RR_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.FL_TYRE_TEMP != Rx_buffer.mbfm6_100.FL_TYRE_TEMP))
     {
         ILSet_FL_TYRE_TEMP_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.FR_TYRE_TEMP != Rx_buffer.mbfm6_100.FR_TYRE_TEMP))
     {
         ILSet_FR_TYRE_TEMP_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.RL_TYRE_TEMP != Rx_buffer.mbfm6_100.RL_TYRE_TEMP))
     {
         ILSet_RL_TYRE_TEMP_DataChanged();
     }

     if((MBFM6_100.mbfm6_100.RR_TYRE_TEMP != Rx_buffer.mbfm6_100.RR_TYRE_TEMP))
     {
         ILSet_RR_TYRE_TEMP_DataChanged();
     }

   }
}

void MBFM7_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM7_100.mbfm7_100.AUTO_LIGHT != Rx_buffer.mbfm7_100.AUTO_LIGHT))
     {
         ILSet_AUTO_LIGHT_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.AUTO_RAIN != Rx_buffer.mbfm7_100.AUTO_RAIN))
     {
         ILSet_AUTO_RAIN_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.SPARE_TYRE_PRESSURE != Rx_buffer.mbfm7_100.SPARE_TYRE_PRESSURE))
     {
         ILSet_SPARE_TYRE_PRESSURE_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.BATT_VOLT != Rx_buffer.mbfm7_100.BATT_VOLT))
     {
         ILSet_BATT_VOLT_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.SPARE_TYRE_TEMP != Rx_buffer.mbfm7_100.SPARE_TYRE_TEMP))
     {
         ILSet_SPARE_TYRE_TEMP_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.SUNROOF_REMINDER != Rx_buffer.mbfm7_100.SUNROOF_REMINDER))
     {
         ILSet_SUNROOF_REMINDER_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.BRAKE_LAMP_FAULT != Rx_buffer.mbfm7_100.BRAKE_LAMP_FAULT))
     {
         ILSet_BRAKE_LAMP_FAULT_DataChanged();
     }

     if((MBFM7_100.mbfm7_100.HAND_BRAKE_REMINDER != Rx_buffer.mbfm7_100.HAND_BRAKE_REMINDER))
     {
         ILSet_HAND_BRAKE_REMINDER_DataChanged();
     }

   }
}

void MBFM9_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM9_500.mbfm9_500.STS_PWM_POS != Rx_buffer.mbfm9_500.STS_PWM_POS))
     {
         ILSet_STS_PWM_POS_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.CABIN_HVAC_REQ_MBFM != Rx_buffer.mbfm9_500.CABIN_HVAC_REQ_MBFM))
     {
         ILSet_CABIN_HVAC_REQ_MBFM_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.HEAD_LAMP_SW_STS != Rx_buffer.mbfm9_500.HEAD_LAMP_SW_STS))
     {
         ILSet_HEAD_LAMP_SW_STS_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.STS_LAMP_FAILURE_1 != Rx_buffer.mbfm9_500.STS_LAMP_FAILURE_1))
     {
         ILSet_STS_LAMP_FAILURE_1_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.STS_LAMP_FAILURE_2 != Rx_buffer.mbfm9_500.STS_LAMP_FAILURE_2))
     {
         ILSet_STS_LAMP_FAILURE_2_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.STS_SRF_POS != Rx_buffer.mbfm9_500.STS_SRF_POS))
     {
         ILSet_STS_SRF_POS_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.PSGR_REAR_SEAT_BELT != Rx_buffer.mbfm9_500.PSGR_REAR_SEAT_BELT))
     {
         ILSet_PSGR_REAR_SEAT_BELT_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.GP_CLOSE_REQ_RAIN != Rx_buffer.mbfm9_500.GP_CLOSE_REQ_RAIN))
     {
         ILSet_GP_CLOSE_REQ_RAIN_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.GP_CLOSE_REQ_AC != Rx_buffer.mbfm9_500.GP_CLOSE_REQ_AC))
     {
         ILSet_GP_CLOSE_REQ_AC_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.STS_EHORN_FAIL != Rx_buffer.mbfm9_500.STS_EHORN_FAIL))
     {
         ILSet_STS_EHORN_FAIL_DataChanged();
     }

     if((MBFM9_500.mbfm9_500.STS_VACATION_MODE != Rx_buffer.mbfm9_500.STS_VACATION_MODE))
     {
         ILSet_STS_VACATION_MODE_DataChanged();
     }

   }
}

void MBFM_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM_NSM.mbfm_nsm.RESERVED_MBFM_0 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_0) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_1 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_1) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_2 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_2) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_3 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_3) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_4 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_4) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_5 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_5) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_6 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_6) || 
       (MBFM_NSM.mbfm_nsm.RESERVED_MBFM_7 != Rx_buffer.mbfm_nsm.RESERVED_MBFM_7))
     {
         ILSet_RESERVED_MBFM_DataChanged();
     }

   }
}

void MBFM_PAS1_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MBFM_PAS1_50.mbfm_pas1_50.FPAS_ERROR != Rx_buffer.mbfm_pas1_50.FPAS_ERROR))
     {
         ILSet_FPAS_ERROR_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.FPAS_ACTIVE_STS != Rx_buffer.mbfm_pas1_50.FPAS_ACTIVE_STS))
     {
         ILSet_FPAS_ACTIVE_STS_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.FPAS_SWT_STS != Rx_buffer.mbfm_pas1_50.FPAS_SWT_STS))
     {
         ILSet_FPAS_SWT_STS_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_FL != Rx_buffer.mbfm_pas1_50.BAR_ZONE_FL))
     {
         ILSet_BAR_ZONE_FL_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_FR != Rx_buffer.mbfm_pas1_50.BAR_ZONE_FR))
     {
         ILSet_BAR_ZONE_FR_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_FLC != Rx_buffer.mbfm_pas1_50.BAR_ZONE_FLC))
     {
         ILSet_BAR_ZONE_FLC_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_FRC != Rx_buffer.mbfm_pas1_50.BAR_ZONE_FRC))
     {
         ILSet_BAR_ZONE_FRC_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.FPAS_DISP_DIST != Rx_buffer.mbfm_pas1_50.FPAS_DISP_DIST))
     {
         ILSet_FPAS_DISP_DIST_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.RPAS_ERROR != Rx_buffer.mbfm_pas1_50.RPAS_ERROR))
     {
         ILSet_RPAS_ERROR_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.RPAS_ACTIVE_STS != Rx_buffer.mbfm_pas1_50.RPAS_ACTIVE_STS))
     {
         ILSet_RPAS_ACTIVE_STS_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_RL != Rx_buffer.mbfm_pas1_50.BAR_ZONE_RL))
     {
         ILSet_BAR_ZONE_RL_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_RR != Rx_buffer.mbfm_pas1_50.BAR_ZONE_RR))
     {
         ILSet_BAR_ZONE_RR_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_RLC != Rx_buffer.mbfm_pas1_50.BAR_ZONE_RLC))
     {
         ILSet_BAR_ZONE_RLC_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.BAR_ZONE_RRC != Rx_buffer.mbfm_pas1_50.BAR_ZONE_RRC))
     {
         ILSet_BAR_ZONE_RRC_DataChanged();
     }

     if((MBFM_PAS1_50.mbfm_pas1_50.RPAS_DISP_DIST != Rx_buffer.mbfm_pas1_50.RPAS_DISP_DIST))
     {
         ILSet_RPAS_DISP_DIST_DataChanged();
     }

   }
}

void MCU1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_0 != Rx_buffer.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_0) || 
       (MCU1_100.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_1 != Rx_buffer.mcu1_100.MCU_REGENTORQUEAVAIL_QUASI_1))
     {
         ILSet_MCU_REGENTORQUEAVAIL_QUASI_DataChanged();
     }

     if((MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_0 != Rx_buffer.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_0) || 
       (MCU1_100.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_1 != Rx_buffer.mcu1_100.MCU_TRACTIONTORQUEAVAIL_QUASI_1))
     {
         ILSet_MCU_TRACTIONTORQUEAVAIL_QUASI_DataChanged();
     }

     if((MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_0 != Rx_buffer.mcu1_100.MCU_HIGHPOWERVOLTAGE_0) || 
       (MCU1_100.mcu1_100.MCU_HIGHPOWERVOLTAGE_1 != Rx_buffer.mcu1_100.MCU_HIGHPOWERVOLTAGE_1))
     {
         ILSet_MCU_HIGHPOWERVOLTAGE_DataChanged();
     }

     if((MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_0 != Rx_buffer.mcu1_100.MCU_HIGHPOWERCURRENT_0) || 
       (MCU1_100.mcu1_100.MCU_HIGHPOWERCURRENT_1 != Rx_buffer.mcu1_100.MCU_HIGHPOWERCURRENT_1))
     {
         ILSet_MCU_HIGHPOWERCURRENT_DataChanged();
     }

   }
}

void MCU2_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_0 != Rx_buffer.mcu2_10.MCU_MOTORTORQUEESTIMATED_0) || 
       (MCU2_10.mcu2_10.MCU_MOTORTORQUEESTIMATED_1 != Rx_buffer.mcu2_10.MCU_MOTORTORQUEESTIMATED_1))
     {
         ILSet_MCU_MOTORTORQUEESTIMATED_DataChanged();
     }

     if((MCU2_10.mcu2_10.MCU_MOTORSPEED_0 != Rx_buffer.mcu2_10.MCU_MOTORSPEED_0) || 
       (MCU2_10.mcu2_10.MCU_MOTORSPEED_1 != Rx_buffer.mcu2_10.MCU_MOTORSPEED_1))
     {
         ILSet_MCU_MOTORSPEED_DataChanged();
     }

     if((MCU2_10.mcu2_10.MCU118_COUNTER != Rx_buffer.mcu2_10.MCU118_COUNTER))
     {
         ILSet_MCU118_COUNTER_DataChanged();
     }

     if((MCU2_10.mcu2_10.MCU118_CHECKSUM != Rx_buffer.mcu2_10.MCU118_CHECKSUM))
     {
         ILSet_MCU118_CHECKSUM_DataChanged();
     }

   }
}

void MCU3_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MCU3_10.mcu3_10.MCU_COMMANDMODE != Rx_buffer.mcu3_10.MCU_COMMANDMODE))
     {
         ILSet_MCU_COMMANDMODE_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_ACTV_DISCHARGE_FAIL != Rx_buffer.mcu3_10.MCU_ACTV_DISCHARGE_FAIL))
     {
         ILSet_MCU_ACTV_DISCHARGE_FAIL_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_ACTV_DISCHARGE_STS != Rx_buffer.mcu3_10.MCU_ACTV_DISCHARGE_STS))
     {
         ILSet_MCU_ACTV_DISCHARGE_STS_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_STATE != Rx_buffer.mcu3_10.MCU_STATE))
     {
         ILSet_MCU_STATE_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_OPERATIONALMODE != Rx_buffer.mcu3_10.MCU_OPERATIONALMODE))
     {
         ILSet_MCU_OPERATIONALMODE_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_ACTIVEDAMPING != Rx_buffer.mcu3_10.MCU_ACTIVEDAMPING))
     {
         ILSet_MCU_ACTIVEDAMPING_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU_ERRORLEVEL != Rx_buffer.mcu3_10.MCU_ERRORLEVEL))
     {
         ILSet_MCU_ERRORLEVEL_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU11B_COUNTER != Rx_buffer.mcu3_10.MCU11B_COUNTER))
     {
         ILSet_MCU11B_COUNTER_DataChanged();
     }

     if((MCU3_10.mcu3_10.MCU11B_CHECKSUM != Rx_buffer.mcu3_10.MCU11B_CHECKSUM))
     {
         ILSet_MCU11B_CHECKSUM_DataChanged();
     }

   }
}

void MCU5_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MCU5_100.mcu5_100.MCU_INVERTER_COOLINGFLOWREQ != Rx_buffer.mcu5_100.MCU_INVERTER_COOLINGFLOWREQ))
     {
         ILSet_MCU_INVERTER_COOLINGFLOWREQ_DataChanged();
     }

     if((MCU5_100.mcu5_100.MCU_TPI != Rx_buffer.mcu5_100.MCU_TPI))
     {
         ILSet_MCU_TPI_DataChanged();
     }

     if((MCU5_100.mcu5_100.MCU_INVERTER_TEMP_INDICATOR != Rx_buffer.mcu5_100.MCU_INVERTER_TEMP_INDICATOR))
     {
         ILSet_MCU_INVERTER_TEMP_INDICATOR_DataChanged();
     }

     if((MCU5_100.mcu5_100.MCU_MOTOR_TEMP_INDICATOR != Rx_buffer.mcu5_100.MCU_MOTOR_TEMP_INDICATOR))
     {
         ILSet_MCU_MOTOR_TEMP_INDICATOR_DataChanged();
     }

     if((MCU5_100.mcu5_100.MCU_MOTORCOOLINGFLOWREQ != Rx_buffer.mcu5_100.MCU_MOTORCOOLINGFLOWREQ))
     {
         ILSet_MCU_MOTORCOOLINGFLOWREQ_DataChanged();
     }

   }
}

void MCU_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((MCU_STS_500.mcu_sts_500.MCU_STS_IGN != Rx_buffer.mcu_sts_500.MCU_STS_IGN))
     {
         ILSet_MCU_STS_IGN_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_COMFLT_SGN_CONTFAIL != Rx_buffer.mcu_sts_500.MCU_COMFLT_SGN_CONTFAIL))
     {
         ILSet_MCU_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_COMFLT_MSGTOUT_STS != Rx_buffer.mcu_sts_500.MCU_COMFLT_MSGTOUT_STS))
     {
         ILSet_MCU_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_COMFLT_NODEABS_STS != Rx_buffer.mcu_sts_500.MCU_COMFLT_NODEABS_STS))
     {
         ILSet_MCU_COMFLT_NODEABS_STS_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_UV_STS != Rx_buffer.mcu_sts_500.MCU_UV_STS))
     {
         ILSet_MCU_UV_STS_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_OV_STS != Rx_buffer.mcu_sts_500.MCU_OV_STS))
     {
         ILSet_MCU_OV_STS_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_AUX_BATT_VOLT != Rx_buffer.mcu_sts_500.MCU_AUX_BATT_VOLT))
     {
         ILSet_MCU_AUX_BATT_VOLT_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_SW_VERSION != Rx_buffer.mcu_sts_500.MCU_SW_VERSION))
     {
         ILSet_MCU_SW_VERSION_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_NM_ACTIVE_STS != Rx_buffer.mcu_sts_500.MCU_NM_ACTIVE_STS))
     {
         ILSet_MCU_NM_ACTIVE_STS_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_COMFLT_MSG_CONTFAIL != Rx_buffer.mcu_sts_500.MCU_COMFLT_MSG_CONTFAIL))
     {
         ILSet_MCU_COMFLT_MSG_CONTFAIL_DataChanged();
     }

     if((MCU_STS_500.mcu_sts_500.MCU_SW_VERSION_INTERNAL != Rx_buffer.mcu_sts_500.MCU_SW_VERSION_INTERNAL))
     {
         ILSet_MCU_SW_VERSION_INTERNAL_DataChanged();
     }

   }
}

void OBC1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_0 != Rx_buffer.obc1_100.OBC_LV_PWRSUPPLY_0) || 
       (OBC1_100.obc1_100.OBC_LV_PWRSUPPLY_1 != Rx_buffer.obc1_100.OBC_LV_PWRSUPPLY_1))
     {
         ILSet_OBC_LV_PWRSUPPLY_DataChanged();
     }

     if((OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_0 != Rx_buffer.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_0) || 
       (OBC1_100.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_1 != Rx_buffer.obc1_100.OBC_PRIMARYSIDE_TEMPERATURE_1))
     {
         ILSet_OBC_PRIMARYSIDE_TEMPERATURE_DataChanged();
     }

     if((OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_0 != Rx_buffer.obc1_100.OBC_TRANSFORMER_TEMPERATURE_0) || 
       (OBC1_100.obc1_100.OBC_TRANSFORMER_TEMPERATURE_1 != Rx_buffer.obc1_100.OBC_TRANSFORMER_TEMPERATURE_1))
     {
         ILSet_OBC_TRANSFORMER_TEMPERATURE_DataChanged();
     }

     if((OBC1_100.obc1_100.OBC_COOLINGREQUEST_0 != Rx_buffer.obc1_100.OBC_COOLINGREQUEST_0) || 
       (OBC1_100.obc1_100.OBC_COOLINGREQUEST_1 != Rx_buffer.obc1_100.OBC_COOLINGREQUEST_1))
     {
         ILSet_OBC_COOLINGREQUEST_DataChanged();
     }

     if((OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_0 != Rx_buffer.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_0) || 
       (OBC1_100.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_1 != Rx_buffer.obc1_100.OBC_SECONDARYSIDE_TEMPERATURE_1))
     {
         ILSet_OBC_SECONDARYSIDE_TEMPERATURE_DataChanged();
     }

   }
}

void OBC2_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC2_100.obc2_100.OBC_ACDETECTSTA != Rx_buffer.obc2_100.OBC_ACDETECTSTA))
     {
         ILSet_OBC_ACDETECTSTA_DataChanged();
     }

     if((OBC2_100.obc2_100.OBC_OPERATINGMODE != Rx_buffer.obc2_100.OBC_OPERATINGMODE))
     {
         ILSet_OBC_OPERATINGMODE_DataChanged();
     }

     if((OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_0 != Rx_buffer.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_0) || 
       (OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_1 != Rx_buffer.obc2_100.OBC_INDUCTOR_CURRENT_L1_RMS_1))
     {
         ILSet_OBC_INDUCTOR_CURRENT_L1_RMS_DataChanged();
     }

     if((OBC2_100.obc2_100.OBC_POWERDERATINGSTA != Rx_buffer.obc2_100.OBC_POWERDERATINGSTA))
     {
         ILSet_OBC_POWERDERATINGSTA_DataChanged();
     }

     if((OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_0 != Rx_buffer.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_0) || 
       (OBC2_100.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_1 != Rx_buffer.obc2_100.OBC_INDUCTOR_CURRENT_L2_RMS_1))
     {
         ILSet_OBC_INDUCTOR_CURRENT_L2_RMS_DataChanged();
     }

   }
}

void OBC3_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_0 != Rx_buffer.obc3_100.OBC_DCCURRENTCAPABLE_0) || 
       (OBC3_100.obc3_100.OBC_DCCURRENTCAPABLE_1 != Rx_buffer.obc3_100.OBC_DCCURRENTCAPABLE_1))
     {
         ILSet_OBC_DCCURRENTCAPABLE_DataChanged();
     }

     if((OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_0 != Rx_buffer.obc3_100.OBC_DCVOLTAGECAPABLE_0) || 
       (OBC3_100.obc3_100.OBC_DCVOLTAGECAPABLE_1 != Rx_buffer.obc3_100.OBC_DCVOLTAGECAPABLE_1))
     {
         ILSet_OBC_DCVOLTAGECAPABLE_DataChanged();
     }

     if((OBC3_100.obc3_100.OBC_PFC_VOLTAGE_0 != Rx_buffer.obc3_100.OBC_PFC_VOLTAGE_0) || 
       (OBC3_100.obc3_100.OBC_PFC_VOLTAGE_1 != Rx_buffer.obc3_100.OBC_PFC_VOLTAGE_1))
     {
         ILSet_OBC_PFC_VOLTAGE_DataChanged();
     }

     if((OBC3_100.obc3_100.OBC_LINE_FREQUENCY_0 != Rx_buffer.obc3_100.OBC_LINE_FREQUENCY_0) || 
       (OBC3_100.obc3_100.OBC_LINE_FREQUENCY_1 != Rx_buffer.obc3_100.OBC_LINE_FREQUENCY_1))
     {
         ILSet_OBC_LINE_FREQUENCY_DataChanged();
     }

   }
}

void OBC4_30_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_0 != Rx_buffer.obc4_30.OBC_ACINPUTCURRENTRMS_0) || 
       (OBC4_30.obc4_30.OBC_ACINPUTCURRENTRMS_1 != Rx_buffer.obc4_30.OBC_ACINPUTCURRENTRMS_1))
     {
         ILSet_OBC_ACINPUTCURRENTRMS_DataChanged();
     }

     if((OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_0 != Rx_buffer.obc4_30.OBC_ACINPUTVOLTAGERMS_0) || 
       (OBC4_30.obc4_30.OBC_ACINPUTVOLTAGERMS_1 != Rx_buffer.obc4_30.OBC_ACINPUTVOLTAGERMS_1))
     {
         ILSet_OBC_ACINPUTVOLTAGERMS_DataChanged();
     }

     if((OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_0 != Rx_buffer.obc4_30.OBC_DCOUTPUTCURRENT_0) || 
       (OBC4_30.obc4_30.OBC_DCOUTPUTCURRENT_1 != Rx_buffer.obc4_30.OBC_DCOUTPUTCURRENT_1))
     {
         ILSet_OBC_DCOUTPUTCURRENT_DataChanged();
     }

     if((OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_0 != Rx_buffer.obc4_30.OBC_DCOUTPUTVOLTAGE_0) || 
       (OBC4_30.obc4_30.OBC_DCOUTPUTVOLTAGE_1 != Rx_buffer.obc4_30.OBC_DCOUTPUTVOLTAGE_1))
     {
         ILSet_OBC_DCOUTPUTVOLTAGE_DataChanged();
     }

   }
}

void OBC6_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC6_100.obc6_100.OBC_IP_DERATE != Rx_buffer.obc6_100.OBC_IP_DERATE))
     {
         ILSet_OBC_IP_DERATE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_IP_OVER_CURR != Rx_buffer.obc6_100.OBC_IP_OVER_CURR))
     {
         ILSet_OBC_IP_OVER_CURR_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_IP_OVER_VOLT != Rx_buffer.obc6_100.OBC_IP_OVER_VOLT))
     {
         ILSet_OBC_IP_OVER_VOLT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_IP_UNDER_VOLT != Rx_buffer.obc6_100.OBC_IP_UNDER_VOLT))
     {
         ILSet_OBC_IP_UNDER_VOLT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LLC_OVER_TEMP != Rx_buffer.obc6_100.OBC_LLC_OVER_TEMP))
     {
         ILSet_OBC_LLC_OVER_TEMP_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LV_OVER_VOLT != Rx_buffer.obc6_100.OBC_LV_OVER_VOLT))
     {
         ILSet_OBC_LV_OVER_VOLT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LV_UNDER_VOLT != Rx_buffer.obc6_100.OBC_LV_UNDER_VOLT))
     {
         ILSet_OBC_LV_UNDER_VOLT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_OP_OC != Rx_buffer.obc6_100.OBC_OP_OC))
     {
         ILSet_OBC_OP_OC_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_OP_OV != Rx_buffer.obc6_100.OBC_OP_OV))
     {
         ILSet_OBC_OP_OV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_OP_UV != Rx_buffer.obc6_100.OBC_OP_UV))
     {
         ILSet_OBC_OP_UV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFC_OVER_TEMP != Rx_buffer.obc6_100.OBC_PFC_OVER_TEMP))
     {
         ILSet_OBC_PFC_OVER_TEMP_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFC_UV != Rx_buffer.obc6_100.OBC_PFC_UV))
     {
         ILSet_OBC_PFC_UV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFV_OV != Rx_buffer.obc6_100.OBC_PFV_OV))
     {
         ILSet_OBC_PFV_OV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PRE_CHARGE_FAULT != Rx_buffer.obc6_100.OBC_PRE_CHARGE_FAULT))
     {
         ILSet_OBC_PRE_CHARGE_FAULT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_TEMP_DERATE != Rx_buffer.obc6_100.OBC_TEMP_DERATE))
     {
         ILSet_OBC_TEMP_DERATE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_CAN_BUS_OFF != Rx_buffer.obc6_100.OBC_CAN_BUS_OFF))
     {
         ILSet_OBC_CAN_BUS_OFF_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LINE_OC_SW != Rx_buffer.obc6_100.OBC_LINE_OC_SW))
     {
         ILSet_OBC_LINE_OC_SW_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFC_OC_HW_FLAG != Rx_buffer.obc6_100.OBC_PFC_OC_HW_FLAG))
     {
         ILSet_OBC_PFC_OC_HW_FLAG_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LLC_OC_HW_FLAG != Rx_buffer.obc6_100.OBC_LLC_OC_HW_FLAG))
     {
         ILSet_OBC_LLC_OC_HW_FLAG_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_EEPROM_FAIL != Rx_buffer.obc6_100.OBC_EEPROM_FAIL))
     {
         ILSet_OBC_EEPROM_FAIL_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_EMI_IP_OV != Rx_buffer.obc6_100.OBC_EMI_IP_OV))
     {
         ILSet_OBC_EMI_IP_OV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_EMI_IP_UV != Rx_buffer.obc6_100.OBC_EMI_IP_UV))
     {
         ILSet_OBC_EMI_IP_UV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_IPROG_OUT_OF_RANGE != Rx_buffer.obc6_100.OBC_IPROG_OUT_OF_RANGE))
     {
         ILSet_OBC_IPROG_OUT_OF_RANGE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_HIGH_TEMP != Rx_buffer.obc6_100.OBC_HIGH_TEMP))
     {
         ILSet_OBC_HIGH_TEMP_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_INTERNAL_FAIL != Rx_buffer.obc6_100.OBC_INTERNAL_FAIL))
     {
         ILSet_OBC_INTERNAL_FAIL_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_OVER_TEMP != Rx_buffer.obc6_100.OBC_OVER_TEMP))
     {
         ILSet_OBC_OVER_TEMP_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_TEMP_SENSOR_FAIL != Rx_buffer.obc6_100.OBC_TEMP_SENSOR_FAIL))
     {
         ILSet_OBC_TEMP_SENSOR_FAIL_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_VPROG_OUT_OF_RANGE != Rx_buffer.obc6_100.OBC_VPROG_OUT_OF_RANGE))
     {
         ILSet_OBC_VPROG_OUT_OF_RANGE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_STATE != Rx_buffer.obc6_100.OBC_STATE))
     {
         ILSet_OBC_STATE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_BURST_MODE_STS != Rx_buffer.obc6_100.OBC_BURST_MODE_STS))
     {
         ILSet_OBC_BURST_MODE_STS_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_CC_CV_STS != Rx_buffer.obc6_100.OBC_CC_CV_STS))
     {
         ILSet_OBC_CC_CV_STS_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PLL_TIMELOCK_STS != Rx_buffer.obc6_100.OBC_PLL_TIMELOCK_STS))
     {
         ILSet_OBC_PLL_TIMELOCK_STS_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_HVDC_HW_OV != Rx_buffer.obc6_100.OBC_HVDC_HW_OV))
     {
         ILSet_OBC_HVDC_HW_OV_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_HVDC_HW_OC != Rx_buffer.obc6_100.OBC_HVDC_HW_OC))
     {
         ILSet_OBC_HVDC_HW_OC_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_CPDUTY_OUT_OF_RANGE != Rx_buffer.obc6_100.OBC_CPDUTY_OUT_OF_RANGE))
     {
         ILSet_OBC_CPDUTY_OUT_OF_RANGE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_INDUCTR_CURRENT_L1_OC != Rx_buffer.obc6_100.OBC_INDUCTR_CURRENT_L1_OC))
     {
         ILSet_OBC_INDUCTR_CURRENT_L1_OC_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_INDUCTR_CURRENT_L2_OC != Rx_buffer.obc6_100.OBC_INDUCTR_CURRENT_L2_OC))
     {
         ILSet_OBC_INDUCTR_CURRENT_L2_OC_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LLC_CONTROL_INPUT != Rx_buffer.obc6_100.OBC_LLC_CONTROL_INPUT))
     {
         ILSet_OBC_LLC_CONTROL_INPUT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_CPVOL_OUT_OF_RANGE != Rx_buffer.obc6_100.OBC_CPVOL_OUT_OF_RANGE))
     {
         ILSet_OBC_CPVOL_OUT_OF_RANGE_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_LOW_TEMP_SHUTDOWN != Rx_buffer.obc6_100.OBC_LOW_TEMP_SHUTDOWN))
     {
         ILSet_OBC_LOW_TEMP_SHUTDOWN_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFC_VOLT_CNTRL_IP != Rx_buffer.obc6_100.OBC_PFC_VOLT_CNTRL_IP))
     {
         ILSet_OBC_PFC_VOLT_CNTRL_IP_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PFC_BUS_FAULT_CNT != Rx_buffer.obc6_100.OBC_PFC_BUS_FAULT_CNT))
     {
         ILSet_OBC_PFC_BUS_FAULT_CNT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_PRECHARGE_FAULT_CNT != Rx_buffer.obc6_100.OBC_PRECHARGE_FAULT_CNT))
     {
         ILSet_OBC_PRECHARGE_FAULT_CNT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_ECU_RESET_FAULT != Rx_buffer.obc6_100.OBC_ECU_RESET_FAULT))
     {
         ILSet_OBC_ECU_RESET_FAULT_DataChanged();
     }

     if((OBC6_100.obc6_100.OBC_VIN_MISMATCH_FAULT != Rx_buffer.obc6_100.OBC_VIN_MISMATCH_FAULT))
     {
         ILSet_OBC_VIN_MISMATCH_FAULT_DataChanged();
     }

   }
}

void OBC_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((OBC_STS_500.obc_sts_500.OBC_STS_IGN_NM != Rx_buffer.obc_sts_500.OBC_STS_IGN_NM))
     {
         ILSet_OBC_STS_IGN_NM_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_VARIANT_CODE_ERR_STS != Rx_buffer.obc_sts_500.OBC_VARIANT_CODE_ERR_STS))
     {
         ILSet_OBC_VARIANT_CODE_ERR_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_COMFLT_SGN_CONTFAIL != Rx_buffer.obc_sts_500.OBC_COMFLT_SGN_CONTFAIL))
     {
         ILSet_OBC_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_FEATURE_CODE_ERR_STS != Rx_buffer.obc_sts_500.OBC_FEATURE_CODE_ERR_STS))
     {
         ILSet_OBC_FEATURE_CODE_ERR_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_COMFLT_MSGTOUT_STS != Rx_buffer.obc_sts_500.OBC_COMFLT_MSGTOUT_STS))
     {
         ILSet_OBC_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_COMFLT_NODEABS_STS != Rx_buffer.obc_sts_500.OBC_COMFLT_NODEABS_STS))
     {
         ILSet_OBC_COMFLT_NODEABS_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_UV_STS != Rx_buffer.obc_sts_500.OBC_UV_STS))
     {
         ILSet_OBC_UV_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_OV_STS != Rx_buffer.obc_sts_500.OBC_OV_STS))
     {
         ILSet_OBC_OV_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_AUX_BATT_VOLT != Rx_buffer.obc_sts_500.OBC_AUX_BATT_VOLT))
     {
         ILSet_OBC_AUX_BATT_VOLT_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_SW_VERSION != Rx_buffer.obc_sts_500.OBC_SW_VERSION))
     {
         ILSet_OBC_SW_VERSION_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_NM_ACTIVE_STS != Rx_buffer.obc_sts_500.OBC_NM_ACTIVE_STS))
     {
         ILSet_OBC_NM_ACTIVE_STS_DataChanged();
     }

     if((OBC_STS_500.obc_sts_500.OBC_COMFLT_MSG_CONTFAIL != Rx_buffer.obc_sts_500.OBC_COMFLT_MSG_CONTFAIL))
     {
         ILSet_OBC_COMFLT_MSG_CONTFAIL_DataChanged();
     }

   }
}

void PKE1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE1_100.pke1_100.KEYFOB_INSIDE_STATUS != Rx_buffer.pke1_100.KEYFOB_INSIDE_STATUS))
     {
         ILSet_KEYFOB_INSIDE_STATUS_DataChanged();
     }

     if((PKE1_100.pke1_100.LAST_KEYFOB_NUM != Rx_buffer.pke1_100.LAST_KEYFOB_NUM))
     {
         ILSet_LAST_KEYFOB_NUM_DataChanged();
     }

   }
}

void PKE2_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE2_200.pke2_200.EMRGNCY_CRANK_WRN != Rx_buffer.pke2_200.EMRGNCY_CRANK_WRN))
     {
         ILSet_EMRGNCY_CRANK_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.KEY_NOT_VEH_WRN != Rx_buffer.pke2_200.KEY_NOT_VEH_WRN))
     {
         ILSet_KEY_NOT_VEH_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.FOB_AUTH_FAIL_WRN != Rx_buffer.pke2_200.FOB_AUTH_FAIL_WRN))
     {
         ILSet_FOB_AUTH_FAIL_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.KEY_FOB_INSD_WRN != Rx_buffer.pke2_200.KEY_FOB_INSD_WRN))
     {
         ILSet_KEY_FOB_INSD_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.CAR_START_WARNING != Rx_buffer.pke2_200.CAR_START_WARNING))
     {
         ILSet_CAR_START_WARNING_DataChanged();
     }

     if((PKE2_200.pke2_200.FOB_BATT_DISCHG_WRN != Rx_buffer.pke2_200.FOB_BATT_DISCHG_WRN))
     {
         ILSet_FOB_BATT_DISCHG_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.SSB_FAIL_WRN != Rx_buffer.pke2_200.SSB_FAIL_WRN))
     {
         ILSet_SSB_FAIL_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.PKE_SHIFT_TO_PARK != Rx_buffer.pke2_200.PKE_SHIFT_TO_PARK))
     {
         ILSet_PKE_SHIFT_TO_PARK_DataChanged();
     }

     if((PKE2_200.pke2_200.TERMINAL_NOT_OFF_WRN_CMD != Rx_buffer.pke2_200.TERMINAL_NOT_OFF_WRN_CMD))
     {
         ILSet_TERMINAL_NOT_OFF_WRN_CMD_DataChanged();
     }

     if((PKE2_200.pke2_200.DOOR_LOCK_WRN != Rx_buffer.pke2_200.DOOR_LOCK_WRN))
     {
         ILSet_DOOR_LOCK_WRN_DataChanged();
     }

     if((PKE2_200.pke2_200.PKE_PN_OFF_WARNING != Rx_buffer.pke2_200.PKE_PN_OFF_WARNING))
     {
         ILSet_PKE_PN_OFF_WARNING_DataChanged();
     }

     if((PKE2_200.pke2_200.REMOTE_ENGINE_START_WARNING != Rx_buffer.pke2_200.REMOTE_ENGINE_START_WARNING))
     {
         ILSet_REMOTE_ENGINE_START_WARNING_DataChanged();
     }

     if((PKE2_200.pke2_200.STS_CAPASENSOR != Rx_buffer.pke2_200.STS_CAPASENSOR))
     {
         ILSet_STS_CAPASENSOR_DataChanged();
     }

     if((PKE2_200.pke2_200.REMOTE_START_SOURCE != Rx_buffer.pke2_200.REMOTE_START_SOURCE))
     {
         ILSet_REMOTE_START_SOURCE_DataChanged();
     }

     if((PKE2_200.pke2_200.REMOTE_START_FAILURE_CODE != Rx_buffer.pke2_200.REMOTE_START_FAILURE_CODE))
     {
         ILSet_REMOTE_START_FAILURE_CODE_DataChanged();
     }

   }
}

void PKE_ICU2_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE_ICU2_100.pke_icu2_100.STS_SECURITY_KEY != Rx_buffer.pke_icu2_100.STS_SECURITY_KEY))
     {
         ILSet_STS_SECURITY_KEY_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.REMOTE_ENGINE_STATE != Rx_buffer.pke_icu2_100.REMOTE_ENGINE_STATE))
     {
         ILSet_REMOTE_ENGINE_STATE_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.REMOTE_START_TIME_EXTENSION != Rx_buffer.pke_icu2_100.REMOTE_START_TIME_EXTENSION))
     {
         ILSet_REMOTE_START_TIME_EXTENSION_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.P_IMMTRG_STATE != Rx_buffer.pke_icu2_100.P_IMMTRG_STATE))
     {
         ILSet_P_IMMTRG_STATE_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.RES_FAILURE_MCM != Rx_buffer.pke_icu2_100.RES_FAILURE_MCM))
     {
         ILSet_RES_FAILURE_MCM_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.STS_RES_MCM != Rx_buffer.pke_icu2_100.STS_RES_MCM))
     {
         ILSet_STS_RES_MCM_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.PKE_ICU2_MSG_CNT != Rx_buffer.pke_icu2_100.PKE_ICU2_MSG_CNT))
     {
         ILSet_PKE_ICU2_MSG_CNT_DataChanged();
     }

     if((PKE_ICU2_100.pke_icu2_100.PKE_ICU2_CRC != Rx_buffer.pke_icu2_100.PKE_ICU2_CRC))
     {
         ILSet_PKE_ICU2_CRC_DataChanged();
     }

   }
}

void PKE_ICU_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_0 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_0) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_1 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_1) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_2 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_2) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_3 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_3) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_4 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_4) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_5 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_5) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_6 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_6) || 
       (PKE_ICU_NSM.pke_icu_nsm.RESERVED_PKE_7 != Rx_buffer.pke_icu_nsm.RESERVED_PKE_7))
     {
         ILSet_RESERVED_PKE_DataChanged();
     }

   }
}

void PKE_MCM_SP_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_0 != Rx_buffer.pke_mcm_sp.IMMOVAL5_0) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_1 != Rx_buffer.pke_mcm_sp.IMMOVAL5_1) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_2 != Rx_buffer.pke_mcm_sp.IMMOVAL5_2) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_3 != Rx_buffer.pke_mcm_sp.IMMOVAL5_3) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_4 != Rx_buffer.pke_mcm_sp.IMMOVAL5_4) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_5 != Rx_buffer.pke_mcm_sp.IMMOVAL5_5) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_6 != Rx_buffer.pke_mcm_sp.IMMOVAL5_6) || 
       (PKE_MCM_SP.pke_mcm_sp.IMMOVAL5_7 != Rx_buffer.pke_mcm_sp.IMMOVAL5_7))
     {
         ILSet_IMMOVAL5_DataChanged();
     }

   }
}

void PKE_TEST5_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((PKE_TEST5_100.pke_test5_100.SIG2_MATCH_STS != Rx_buffer.pke_test5_100.SIG2_MATCH_STS))
     {
         ILSet_SIG2_MATCH_STS_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.SIG1_MATCH != Rx_buffer.pke_test5_100.SIG1_MATCH))
     {
         ILSet_SIG1_MATCH_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.REMOTE_VEH_IMMO_STS != Rx_buffer.pke_test5_100.REMOTE_VEH_IMMO_STS))
     {
         ILSet_REMOTE_VEH_IMMO_STS_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.REMOTE_ENG_START_STATE != Rx_buffer.pke_test5_100.REMOTE_ENG_START_STATE))
     {
         ILSet_REMOTE_ENG_START_STATE_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.MCMTRG_RECEIVE_STS != Rx_buffer.pke_test5_100.MCMTRG_RECEIVE_STS))
     {
         ILSet_MCMTRG_RECEIVE_STS_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.PKE_PACK != Rx_buffer.pke_test5_100.PKE_PACK))
     {
         ILSet_PKE_PACK_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.PKE_NACK != Rx_buffer.pke_test5_100.PKE_NACK))
     {
         ILSet_PKE_NACK_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.RES_EXTENSION_COUNTER != Rx_buffer.pke_test5_100.RES_EXTENSION_COUNTER))
     {
         ILSet_RES_EXTENSION_COUNTER_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.PKE_CHALLENGE_STS != Rx_buffer.pke_test5_100.PKE_CHALLENGE_STS))
     {
         ILSet_PKE_CHALLENGE_STS_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.NUM_PKE_CHALLENGES != Rx_buffer.pke_test5_100.NUM_PKE_CHALLENGES))
     {
         ILSet_NUM_PKE_CHALLENGES_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.MCM_NACK != Rx_buffer.pke_test5_100.MCM_NACK))
     {
         ILSet_MCM_NACK_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.MCM_PACK != Rx_buffer.pke_test5_100.MCM_PACK))
     {
         ILSet_MCM_PACK_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.RESPONSE_STS != Rx_buffer.pke_test5_100.RESPONSE_STS))
     {
         ILSet_RESPONSE_STS_DataChanged();
     }

     if((PKE_TEST5_100.pke_test5_100.PREVIOUS_CYL_AUTH_STS != Rx_buffer.pke_test5_100.PREVIOUS_CYL_AUTH_STS))
     {
         ILSet_PREVIOUS_CYL_AUTH_STS_DataChanged();
     }

   }
}

void SAS1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SAS1_10.sas1_10.ABSOLUTE_ANGLE_0 != Rx_buffer.sas1_10.ABSOLUTE_ANGLE_0) || 
       (SAS1_10.sas1_10.ABSOLUTE_ANGLE_1 != Rx_buffer.sas1_10.ABSOLUTE_ANGLE_1))
     {
         ILSet_ABSOLUTE_ANGLE_DataChanged();
     }

     if((SAS1_10.sas1_10.ANGLE_SPD != Rx_buffer.sas1_10.ANGLE_SPD))
     {
         ILSet_ANGLE_SPD_DataChanged();
     }

     if((SAS1_10.sas1_10.STS_SAS_FAILURE != Rx_buffer.sas1_10.STS_SAS_FAILURE))
     {
         ILSet_STS_SAS_FAILURE_DataChanged();
     }

     if((SAS1_10.sas1_10.STS_SAS_CALIB != Rx_buffer.sas1_10.STS_SAS_CALIB))
     {
         ILSet_STS_SAS_CALIB_DataChanged();
     }

     if((SAS1_10.sas1_10.STS_SAS_TRIM != Rx_buffer.sas1_10.STS_SAS_TRIM))
     {
         ILSet_STS_SAS_TRIM_DataChanged();
     }

     if((SAS1_10.sas1_10.STS_SAS_INTERNAL != Rx_buffer.sas1_10.STS_SAS_INTERNAL))
     {
         ILSet_STS_SAS_INTERNAL_DataChanged();
     }

     if((SAS1_10.sas1_10.SAS_MSG_CNT != Rx_buffer.sas1_10.SAS_MSG_CNT))
     {
         ILSet_SAS_MSG_CNT_DataChanged();
     }

     if((SAS1_10.sas1_10.SAS_CRC != Rx_buffer.sas1_10.SAS_CRC))
     {
         ILSet_SAS_CRC_DataChanged();
     }

   }
}

void SBRM1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SBRM1_100.sbrm1_100.PSGR_REAR_SEAT_BELT_SBRM != Rx_buffer.sbrm1_100.PSGR_REAR_SEAT_BELT_SBRM))
     {
         ILSet_PSGR_REAR_SEAT_BELT_SBRM_DataChanged();
     }

   }
}

void SBW1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SBW1_10.sbw1_10.SBW_LEVER != Rx_buffer.sbw1_10.SBW_LEVER))
     {
         ILSet_SBW_LEVER_DataChanged();
     }

     if((SBW1_10.sbw1_10.SBW_FAULT != Rx_buffer.sbw1_10.SBW_FAULT))
     {
         ILSet_SBW_FAULT_DataChanged();
     }

     if((SBW1_10.sbw1_10.SBW_WARN != Rx_buffer.sbw1_10.SBW_WARN))
     {
         ILSet_SBW_WARN_DataChanged();
     }

     if((SBW1_10.sbw1_10.SBW1_MSG_COUNT != Rx_buffer.sbw1_10.SBW1_MSG_COUNT))
     {
         ILSet_SBW1_MSG_COUNT_DataChanged();
     }

     if((SBW1_10.sbw1_10.SBW1_CRC != Rx_buffer.sbw1_10.SBW1_CRC))
     {
         ILSet_SBW1_CRC_DataChanged();
     }

   }
}

void SCM1_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SCM1_500.scm1_500.SCM_MEMORY_MODE != Rx_buffer.scm1_500.SCM_MEMORY_MODE))
     {
         ILSet_SCM_MEMORY_MODE_DataChanged();
     }

     if((SCM1_500.scm1_500.SEAT_POSITION_FEEDBACK != Rx_buffer.scm1_500.SEAT_POSITION_FEEDBACK))
     {
         ILSet_SEAT_POSITION_FEEDBACK_DataChanged();
     }

     if((SCM1_500.scm1_500.SCM_MEMORY_STS != Rx_buffer.scm1_500.SCM_MEMORY_STS))
     {
         ILSet_SCM_MEMORY_STS_DataChanged();
     }

     if((SCM1_500.scm1_500.HEATER_TEMP != Rx_buffer.scm1_500.HEATER_TEMP))
     {
         ILSet_HEATER_TEMP_DataChanged();
     }

     if((SCM1_500.scm1_500.STS_HEATER != Rx_buffer.scm1_500.STS_HEATER))
     {
         ILSet_STS_HEATER_DataChanged();
     }

     if((SCM1_500.scm1_500.SEAT_HEAT_VENT_LEVEL_SCM != Rx_buffer.scm1_500.SEAT_HEAT_VENT_LEVEL_SCM))
     {
         ILSet_SEAT_HEAT_VENT_LEVEL_SCM_DataChanged();
     }

     if((SCM1_500.scm1_500.POWER_SEAT_MEMORY_RECALL != Rx_buffer.scm1_500.POWER_SEAT_MEMORY_RECALL))
     {
         ILSet_POWER_SEAT_MEMORY_RECALL_DataChanged();
     }

     if((SCM1_500.scm1_500.POWER_SEAT_MEMORY_STORE != Rx_buffer.scm1_500.POWER_SEAT_MEMORY_STORE))
     {
         ILSet_POWER_SEAT_MEMORY_STORE_DataChanged();
     }

   }
}

void SRS1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SRS1_20.srs1_20.INDC_SRS != Rx_buffer.srs1_20.INDC_SRS))
     {
         ILSet_INDC_SRS_DataChanged();
     }

     if((SRS1_20.srs1_20.DOOR_UNLOCK != Rx_buffer.srs1_20.DOOR_UNLOCK))
     {
         ILSet_DOOR_UNLOCK_DataChanged();
     }

     if((SRS1_20.srs1_20.STS_CRASH != Rx_buffer.srs1_20.STS_CRASH))
     {
         ILSet_STS_CRASH_DataChanged();
     }

     if((SRS1_20.srs1_20.INDC_PADL != Rx_buffer.srs1_20.INDC_PADL))
     {
         ILSet_INDC_PADL_DataChanged();
     }

     if((SRS1_20.srs1_20.SRS_RESERVE1 != Rx_buffer.srs1_20.SRS_RESERVE1))
     {
         ILSet_SRS_RESERVE1_DataChanged();
     }

     if((SRS1_20.srs1_20.EVEN_PARITY_BIT != Rx_buffer.srs1_20.EVEN_PARITY_BIT))
     {
         ILSet_EVEN_PARITY_BIT_DataChanged();
     }

     if((SRS1_20.srs1_20.STS_SEAT_BLT_DRV != Rx_buffer.srs1_20.STS_SEAT_BLT_DRV))
     {
         ILSet_STS_SEAT_BLT_DRV_DataChanged();
     }

     if((SRS1_20.srs1_20.STS_SEAT_BLT_PSGR != Rx_buffer.srs1_20.STS_SEAT_BLT_PSGR))
     {
         ILSet_STS_SEAT_BLT_PSGR_DataChanged();
     }

     if((SRS1_20.srs1_20.STS_CRASH_OUTPUT != Rx_buffer.srs1_20.STS_CRASH_OUTPUT))
     {
         ILSet_STS_CRASH_OUTPUT_DataChanged();
     }

     if((SRS1_20.srs1_20.SRS_MSG_CNT != Rx_buffer.srs1_20.SRS_MSG_CNT))
     {
         ILSet_SRS_MSG_CNT_DataChanged();
     }

     if((SRS1_20.srs1_20.SRS_CRC != Rx_buffer.srs1_20.SRS_CRC))
     {
         ILSet_SRS_CRC_DataChanged();
     }

   }
}

void SVS1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SVS1_10.svs1_10.SVS_GUIDED_VOICE_REQ != Rx_buffer.svs1_10.SVS_GUIDED_VOICE_REQ))
     {
         ILSet_SVS_GUIDED_VOICE_REQ_DataChanged();
     }

     if((SVS1_10.svs1_10.SVS_INFO != Rx_buffer.svs1_10.SVS_INFO))
     {
         ILSet_SVS_INFO_DataChanged();
     }

     if((SVS1_10.svs1_10.SVS_VIEW_REQUEST_IS != Rx_buffer.svs1_10.SVS_VIEW_REQUEST_IS))
     {
         ILSet_SVS_VIEW_REQUEST_IS_DataChanged();
     }

     if((SVS1_10.svs1_10.SVS_VIEW_REQUEST_IC != Rx_buffer.svs1_10.SVS_VIEW_REQUEST_IC))
     {
         ILSet_SVS_VIEW_REQUEST_IC_DataChanged();
     }

   }
}

void SYNC_MSG_SP_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_0 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_0) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_1 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_1) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_2 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_2) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_3 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_3) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_4 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_4) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_5 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_5) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_6 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_6) || 
       (SYNC_MSG_SP.sync_msg_sp.RESERVED_EMS_SP_7 != Rx_buffer.sync_msg_sp.RESERVED_EMS_SP_7))
     {
         ILSet_RESERVED_EMS_SP_DataChanged();
     }

   }
}

void TC1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TC1_20.tc1_20.TC1_MSG_CNT != Rx_buffer.tc1_20.TC1_MSG_CNT))
     {
         ILSet_TC1_MSG_CNT_DataChanged();
     }

     if((TC1_20.tc1_20.INDC_TC_ALERT != Rx_buffer.tc1_20.INDC_TC_ALERT))
     {
         ILSet_INDC_TC_ALERT_DataChanged();
     }

     if((TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_0 != Rx_buffer.tc1_20.CUR_CARD_SHAFT_TRQ_0) || 
       (TC1_20.tc1_20.CUR_CARD_SHAFT_TRQ_1 != Rx_buffer.tc1_20.CUR_CARD_SHAFT_TRQ_1))
     {
         ILSet_CUR_CARD_SHAFT_TRQ_DataChanged();
     }

     if((TC1_20.tc1_20.TRANSFER_MODE_TC != Rx_buffer.tc1_20.TRANSFER_MODE_TC))
     {
         ILSet_TRANSFER_MODE_TC_DataChanged();
     }

     if((TC1_20.tc1_20.INDC_TC_MALF != Rx_buffer.tc1_20.INDC_TC_MALF))
     {
         ILSet_INDC_TC_MALF_DataChanged();
     }

     if((TC1_20.tc1_20.TC1_CRC != Rx_buffer.tc1_20.TC1_CRC))
     {
         ILSet_TC1_CRC_DataChanged();
     }

   }
}

void TCU5_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TCU5_10.tcu5_10.GEAR_ACTUAL != Rx_buffer.tcu5_10.GEAR_ACTUAL))
     {
         ILSet_GEAR_ACTUAL_DataChanged();
     }

     if((TCU5_10.tcu5_10.GEAR_TARGET != Rx_buffer.tcu5_10.GEAR_TARGET))
     {
         ILSet_GEAR_TARGET_DataChanged();
     }

     if((TCU5_10.tcu5_10.SHIFTING != Rx_buffer.tcu5_10.SHIFTING))
     {
         ILSet_SHIFTING_DataChanged();
     }

   }
}

void TCU6_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TCU6_20.tcu6_20.TRANS_MIL_LAMP != Rx_buffer.tcu6_20.TRANS_MIL_LAMP))
     {
         ILSet_TRANS_MIL_LAMP_DataChanged();
     }

     if((TCU6_20.tcu6_20.TGS_LEVER != Rx_buffer.tcu6_20.TGS_LEVER))
     {
         ILSet_TGS_LEVER_DataChanged();
     }

     if((TCU6_20.tcu6_20.TGS_MODE != Rx_buffer.tcu6_20.TGS_MODE))
     {
         ILSet_TGS_MODE_DataChanged();
     }

     if((TCU6_20.tcu6_20.INDC_AT_MALFUNC != Rx_buffer.tcu6_20.INDC_AT_MALFUNC))
     {
         ILSet_INDC_AT_MALFUNC_DataChanged();
     }

     if((TCU6_20.tcu6_20.TCU6_MSG_COUNT != Rx_buffer.tcu6_20.TCU6_MSG_COUNT))
     {
         ILSet_TCU6_MSG_COUNT_DataChanged();
     }

     if((TCU6_20.tcu6_20.TCU6_CRC != Rx_buffer.tcu6_20.TCU6_CRC))
     {
         ILSet_TCU6_CRC_DataChanged();
     }

   }
}

void TC_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TC_NSM.tc_nsm.RESERVED_TC_0 != Rx_buffer.tc_nsm.RESERVED_TC_0) || 
       (TC_NSM.tc_nsm.RESERVED_TC_1 != Rx_buffer.tc_nsm.RESERVED_TC_1) || 
       (TC_NSM.tc_nsm.RESERVED_TC_2 != Rx_buffer.tc_nsm.RESERVED_TC_2) || 
       (TC_NSM.tc_nsm.RESERVED_TC_3 != Rx_buffer.tc_nsm.RESERVED_TC_3) || 
       (TC_NSM.tc_nsm.RESERVED_TC_4 != Rx_buffer.tc_nsm.RESERVED_TC_4) || 
       (TC_NSM.tc_nsm.RESERVED_TC_5 != Rx_buffer.tc_nsm.RESERVED_TC_5) || 
       (TC_NSM.tc_nsm.RESERVED_TC_6 != Rx_buffer.tc_nsm.RESERVED_TC_6) || 
       (TC_NSM.tc_nsm.RESERVED_TC_7 != Rx_buffer.tc_nsm.RESERVED_TC_7))
     {
         ILSet_RESERVED_TC_DataChanged();
     }

   }
}

void TPMS1_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TPMS1_100.tpms1_100.TPMS_ID_NOT_LEARNT_TPMS != Rx_buffer.tpms1_100.TPMS_ID_NOT_LEARNT_TPMS))
     {
         ILSet_TPMS_ID_NOT_LEARNT_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.TPMS_SIGNAL_MISSING_TPMS != Rx_buffer.tpms1_100.TPMS_SIGNAL_MISSING_TPMS))
     {
         ILSet_TPMS_SIGNAL_MISSING_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.TPMS_PROGRAM_MODE != Rx_buffer.tpms1_100.TPMS_PROGRAM_MODE))
     {
         ILSet_TPMS_PROGRAM_MODE_DataChanged();
     }

     if((TPMS1_100.tpms1_100.HIGH_TYRE_TEMPERATURE_TPMS != Rx_buffer.tpms1_100.HIGH_TYRE_TEMPERATURE_TPMS))
     {
         ILSet_HIGH_TYRE_TEMPERATURE_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.TPMS_MALFUNCTION != Rx_buffer.tpms1_100.TPMS_MALFUNCTION))
     {
         ILSet_TPMS_MALFUNCTION_DataChanged();
     }

     if((TPMS1_100.tpms1_100.LOW_TYRE_PRESSURE_TPMS != Rx_buffer.tpms1_100.LOW_TYRE_PRESSURE_TPMS))
     {
         ILSet_LOW_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.SPARE_TYRE_SWAP_TPMS != Rx_buffer.tpms1_100.SPARE_TYRE_SWAP_TPMS))
     {
         ILSet_SPARE_TYRE_SWAP_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.HIGH_TYRE_PRESSURE_TPMS != Rx_buffer.tpms1_100.HIGH_TYRE_PRESSURE_TPMS))
     {
         ILSet_HIGH_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.TPMS_LEAKAGE_ALERT_TPMS != Rx_buffer.tpms1_100.TPMS_LEAKAGE_ALERT_TPMS))
     {
         ILSet_TPMS_LEAKAGE_ALERT_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.TPMS_SYSTEM_FAULT_TPMS != Rx_buffer.tpms1_100.TPMS_SYSTEM_FAULT_TPMS))
     {
         ILSet_TPMS_SYSTEM_FAULT_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.STS_TPMS_LED_TPMS != Rx_buffer.tpms1_100.STS_TPMS_LED_TPMS))
     {
         ILSet_STS_TPMS_LED_TPMS_DataChanged();
     }

     if((TPMS1_100.tpms1_100.REQ_TFA_DISPLAY_TPMS != Rx_buffer.tpms1_100.REQ_TFA_DISPLAY_TPMS))
     {
         ILSet_REQ_TFA_DISPLAY_TPMS_DataChanged();
     }

   }
}

void TPMS2_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TPMS2_100.tpms2_100.FL_TYRE_PRESSURE_TPMS != Rx_buffer.tpms2_100.FL_TYRE_PRESSURE_TPMS))
     {
         ILSet_FL_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.FR_TYRE_PRESSURE_TPMS != Rx_buffer.tpms2_100.FR_TYRE_PRESSURE_TPMS))
     {
         ILSet_FR_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.RL_TYRE_PRESSURE_TPMS != Rx_buffer.tpms2_100.RL_TYRE_PRESSURE_TPMS))
     {
         ILSet_RL_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.RR_TYRE_PRESSURE_TPMS != Rx_buffer.tpms2_100.RR_TYRE_PRESSURE_TPMS))
     {
         ILSet_RR_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.FL_TYRE_TEMP_TPMS != Rx_buffer.tpms2_100.FL_TYRE_TEMP_TPMS))
     {
         ILSet_FL_TYRE_TEMP_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.FR_TYRE_TEMP_TPMS != Rx_buffer.tpms2_100.FR_TYRE_TEMP_TPMS))
     {
         ILSet_FR_TYRE_TEMP_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.RL_TYRE_TEMP_TPMS != Rx_buffer.tpms2_100.RL_TYRE_TEMP_TPMS))
     {
         ILSet_RL_TYRE_TEMP_TPMS_DataChanged();
     }

     if((TPMS2_100.tpms2_100.RR_TYRE_TEMP_TPMS != Rx_buffer.tpms2_100.RR_TYRE_TEMP_TPMS))
     {
         ILSet_RR_TYRE_TEMP_TPMS_DataChanged();
     }

   }
}

void TPMS3_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((TPMS3_100.tpms3_100.TYRE_POSITION_AUTOLOCATED != Rx_buffer.tpms3_100.TYRE_POSITION_AUTOLOCATED))
     {
         ILSet_TYRE_POSITION_AUTOLOCATED_DataChanged();
     }

     if((TPMS3_100.tpms3_100.FILLING_FL != Rx_buffer.tpms3_100.FILLING_FL))
     {
         ILSet_FILLING_FL_DataChanged();
     }

     if((TPMS3_100.tpms3_100.FILLING_FR != Rx_buffer.tpms3_100.FILLING_FR))
     {
         ILSet_FILLING_FR_DataChanged();
     }

     if((TPMS3_100.tpms3_100.FILLING_RL != Rx_buffer.tpms3_100.FILLING_RL))
     {
         ILSet_FILLING_RL_DataChanged();
     }

     if((TPMS3_100.tpms3_100.FILLING_RR != Rx_buffer.tpms3_100.FILLING_RR))
     {
         ILSet_FILLING_RR_DataChanged();
     }

     if((TPMS3_100.tpms3_100.SPARE_TYRE_TEMP_TPMS != Rx_buffer.tpms3_100.SPARE_TYRE_TEMP_TPMS))
     {
         ILSet_SPARE_TYRE_TEMP_TPMS_DataChanged();
     }

     if((TPMS3_100.tpms3_100.SPARE_TYRE_PRESSURE_TPMS != Rx_buffer.tpms3_100.SPARE_TYRE_PRESSURE_TPMS))
     {
         ILSet_SPARE_TYRE_PRESSURE_TPMS_DataChanged();
     }

     if((TPMS3_100.tpms3_100.FILLING_SPARE_TYRE != Rx_buffer.tpms3_100.FILLING_SPARE_TYRE))
     {
         ILSet_FILLING_SPARE_TYRE_DataChanged();
     }

   }
}

void VCU10_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU10_100.vcu10_100.GEAR_ACTUAL_VCU != Rx_buffer.vcu10_100.GEAR_ACTUAL_VCU))
     {
         ILSet_GEAR_ACTUAL_VCU_DataChanged();
     }

     if((VCU10_100.vcu10_100.PRESS_BRAKE != Rx_buffer.vcu10_100.PRESS_BRAKE))
     {
         ILSet_PRESS_BRAKE_DataChanged();
     }

     if((VCU10_100.vcu10_100.INDC_DRIVE_ENABLE != Rx_buffer.vcu10_100.INDC_DRIVE_ENABLE))
     {
         ILSet_INDC_DRIVE_ENABLE_DataChanged();
     }

     if((VCU10_100.vcu10_100.STS_REGEN_CUTOFF_TT != Rx_buffer.vcu10_100.STS_REGEN_CUTOFF_TT))
     {
         ILSet_STS_REGEN_CUTOFF_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.DRIVE_EFFICIENCY != Rx_buffer.vcu10_100.DRIVE_EFFICIENCY))
     {
         ILSet_DRIVE_EFFICIENCY_DataChanged();
     }

     if((VCU10_100.vcu10_100.STATE_OF_CHARGE != Rx_buffer.vcu10_100.STATE_OF_CHARGE))
     {
         ILSet_STATE_OF_CHARGE_DataChanged();
     }

     if((VCU10_100.vcu10_100.EV_READY_TT != Rx_buffer.vcu10_100.EV_READY_TT))
     {
         ILSet_EV_READY_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.REDUCE_POWER_MODE_TT != Rx_buffer.vcu10_100.REDUCE_POWER_MODE_TT))
     {
         ILSet_REDUCE_POWER_MODE_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.TIME_TO_CHARGE_VCU != Rx_buffer.vcu10_100.TIME_TO_CHARGE_VCU))
     {
         ILSet_TIME_TO_CHARGE_VCU_DataChanged();
     }

     if((VCU10_100.vcu10_100.ALERT_MSGS != Rx_buffer.vcu10_100.ALERT_MSGS))
     {
         ILSet_ALERT_MSGS_DataChanged();
     }

     if((VCU10_100.vcu10_100.STS_CHARGE_LIGHT_TT != Rx_buffer.vcu10_100.STS_CHARGE_LIGHT_TT))
     {
         ILSet_STS_CHARGE_LIGHT_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.STS_EVWARNING_TT != Rx_buffer.vcu10_100.STS_EVWARNING_TT))
     {
         ILSet_STS_EVWARNING_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.STS_HV_BATT_TT != Rx_buffer.vcu10_100.STS_HV_BATT_TT))
     {
         ILSet_STS_HV_BATT_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.STS_SERVICE_LIGHT_TT != Rx_buffer.vcu10_100.STS_SERVICE_LIGHT_TT))
     {
         ILSet_STS_SERVICE_LIGHT_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.HIGH_TEMP_LIGHT_OP != Rx_buffer.vcu10_100.HIGH_TEMP_LIGHT_OP))
     {
         ILSet_HIGH_TEMP_LIGHT_OP_DataChanged();
     }

     if((VCU10_100.vcu10_100.LOW_AUX_BATT_TT != Rx_buffer.vcu10_100.LOW_AUX_BATT_TT))
     {
         ILSet_LOW_AUX_BATT_TT_DataChanged();
     }

     if((VCU10_100.vcu10_100.AEE_RESET_REQ_FB != Rx_buffer.vcu10_100.AEE_RESET_REQ_FB))
     {
         ILSet_AEE_RESET_REQ_FB_DataChanged();
     }

     if((VCU10_100.vcu10_100.REGEN_LEVELS != Rx_buffer.vcu10_100.REGEN_LEVELS))
     {
         ILSet_REGEN_LEVELS_DataChanged();
     }

   }
}

void VCU11_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU11_100.vcu11_100.VCU_CHARINLETTEMPPOS != Rx_buffer.vcu11_100.VCU_CHARINLETTEMPPOS))
     {
         ILSet_VCU_CHARINLETTEMPPOS_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_CHARPLUGATLOCKSWINDSTS != Rx_buffer.vcu11_100.VCU_CHARPLUGATLOCKSWINDSTS))
     {
         ILSet_VCU_CHARPLUGATLOCKSWINDSTS_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_CHARPLUGLOCKCTRLSTS != Rx_buffer.vcu11_100.VCU_CHARPLUGLOCKCTRLSTS))
     {
         ILSet_VCU_CHARPLUGLOCKCTRLSTS_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_CHARPLUGLOCKFBSTS != Rx_buffer.vcu11_100.VCU_CHARPLUGLOCKFBSTS))
     {
         ILSet_VCU_CHARPLUGLOCKFBSTS_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_COOLFANSPDCTRL != Rx_buffer.vcu11_100.VCU_COOLFANSPDCTRL))
     {
         ILSet_VCU_COOLFANSPDCTRL_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_PUMPSPDCTRL != Rx_buffer.vcu11_100.VCU_PUMPSPDCTRL))
     {
         ILSet_VCU_PUMPSPDCTRL_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_PUMPSPDFB != Rx_buffer.vcu11_100.VCU_PUMPSPDFB))
     {
         ILSet_VCU_PUMPSPDFB_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_CHARINLETTEMPNEG != Rx_buffer.vcu11_100.VCU_CHARINLETTEMPNEG))
     {
         ILSet_VCU_CHARINLETTEMPNEG_DataChanged();
     }

     if((VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_0 != Rx_buffer.vcu11_100.VCU_VALEVSEUMAXLIM_0) || 
       (VCU11_100.vcu11_100.VCU_VALEVSEUMAXLIM_1 != Rx_buffer.vcu11_100.VCU_VALEVSEUMAXLIM_1))
     {
         ILSet_VCU_VALEVSEUMAXLIM_DataChanged();
     }

   }
}

void VCU11_50_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_0 != Rx_buffer.vcu11_50.ACT_REGEN_TORQUE_APPLIED_0) || 
       (VCU11_50.vcu11_50.ACT_REGEN_TORQUE_APPLIED_1 != Rx_buffer.vcu11_50.ACT_REGEN_TORQUE_APPLIED_1))
     {
         ILSet_ACT_REGEN_TORQUE_APPLIED_DataChanged();
     }

     if((VCU11_50.vcu11_50.RECUP_CTRL_STATE != Rx_buffer.vcu11_50.RECUP_CTRL_STATE))
     {
         ILSet_RECUP_CTRL_STATE_DataChanged();
     }

     if((VCU11_50.vcu11_50.STS_REGEN != Rx_buffer.vcu11_50.STS_REGEN))
     {
         ILSet_STS_REGEN_DataChanged();
     }

     if((VCU11_50.vcu11_50.MOTOR_PWR_0 != Rx_buffer.vcu11_50.MOTOR_PWR_0) || 
       (VCU11_50.vcu11_50.MOTOR_PWR_1 != Rx_buffer.vcu11_50.MOTOR_PWR_1))
     {
         ILSet_MOTOR_PWR_DataChanged();
     }

     if((VCU11_50.vcu11_50.BRAKE_PEDAL_VALUE != Rx_buffer.vcu11_50.BRAKE_PEDAL_VALUE))
     {
         ILSet_BRAKE_PEDAL_VALUE_DataChanged();
     }

     if((VCU11_50.vcu11_50.ENERGY_EFFICIENCY != Rx_buffer.vcu11_50.ENERGY_EFFICIENCY))
     {
         ILSet_ENERGY_EFFICIENCY_DataChanged();
     }

     if((VCU11_50.vcu11_50.POWER_REGEN_METER != Rx_buffer.vcu11_50.POWER_REGEN_METER))
     {
         ILSet_POWER_REGEN_METER_DataChanged();
     }

     if((VCU11_50.vcu11_50.REQUEST_RESPONSE_REVIVE != Rx_buffer.vcu11_50.REQUEST_RESPONSE_REVIVE))
     {
         ILSet_REQUEST_RESPONSE_REVIVE_DataChanged();
     }

   }
}

void VCU12_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU12_100.vcu12_100.VCU_CHARINDBLCTRLSTS != Rx_buffer.vcu12_100.VCU_CHARINDBLCTRLSTS))
     {
         ILSet_VCU_CHARINDBLCTRLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_CHARINDGRCTRLSTS != Rx_buffer.vcu12_100.VCU_CHARINDGRCTRLSTS))
     {
         ILSet_VCU_CHARINDGRCTRLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_QKCHARNEGRLYCTRLSTS != Rx_buffer.vcu12_100.VCU_QKCHARNEGRLYCTRLSTS))
     {
         ILSet_VCU_QKCHARNEGRLYCTRLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_CHARINDREDCTRLSTS != Rx_buffer.vcu12_100.VCU_CHARINDREDCTRLSTS))
     {
         ILSet_VCU_CHARINDREDCTRLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_QKCHARNEGRLYFBLSTS != Rx_buffer.vcu12_100.VCU_QKCHARNEGRLYFBLSTS))
     {
         ILSet_VCU_QKCHARNEGRLYFBLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_QKCHARPOSRLYCTRLSTS != Rx_buffer.vcu12_100.VCU_QKCHARPOSRLYCTRLSTS))
     {
         ILSet_VCU_QKCHARPOSRLYCTRLSTS_DataChanged();
     }

     if((VCU12_100.vcu12_100.VCU_QKCHARPOSRLYFBLSTS != Rx_buffer.vcu12_100.VCU_QKCHARPOSRLYFBLSTS))
     {
         ILSet_VCU_QKCHARPOSRLYFBLSTS_DataChanged();
     }

   }
}

void VCU13_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU13_100.vcu13_100.VCU_MAX_CPU_LOAD != Rx_buffer.vcu13_100.VCU_MAX_CPU_LOAD))
     {
         ILSet_VCU_MAX_CPU_LOAD_DataChanged();
     }

     if((VCU13_100.vcu13_100.VCU_AVG_CPU_LOAD != Rx_buffer.vcu13_100.VCU_AVG_CPU_LOAD))
     {
         ILSet_VCU_AVG_CPU_LOAD_DataChanged();
     }

     if((VCU13_100.vcu13_100.VCU_PUMPRLYCTRLSTS != Rx_buffer.vcu13_100.VCU_PUMPRLYCTRLSTS))
     {
         ILSet_VCU_PUMPRLYCTRLSTS_DataChanged();
     }

     if((VCU13_100.vcu13_100.VCU_SBWS_BU_RAWVAL != Rx_buffer.vcu13_100.VCU_SBWS_BU_RAWVAL))
     {
         ILSet_VCU_SBWS_BU_RAWVAL_DataChanged();
     }

     if((VCU13_100.vcu13_100.VCU_SBWS_BUFB_RAWVAL != Rx_buffer.vcu13_100.VCU_SBWS_BUFB_RAWVAL))
     {
         ILSet_VCU_SBWS_BUFB_RAWVAL_DataChanged();
     }

     if((VCU13_100.vcu13_100.VCU_DCCHARGINGSEQUENCE != Rx_buffer.vcu13_100.VCU_DCCHARGINGSEQUENCE))
     {
         ILSet_VCU_DCCHARGINGSEQUENCE_DataChanged();
     }

   }
}

void VCU14_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_0 != Rx_buffer.vcu14_20.VCU_VALEVSEUMINLIM_0) || 
       (VCU14_20.vcu14_20.VCU_VALEVSEUMINLIM_1 != Rx_buffer.vcu14_20.VCU_VALEVSEUMINLIM_1))
     {
         ILSet_VCU_VALEVSEUMINLIM_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_ACCEP1_VOLTAGE != Rx_buffer.vcu14_20.VCU_ACCEP1_VOLTAGE))
     {
         ILSet_VCU_ACCEP1_VOLTAGE_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_ACCEP2_VOLTAGE != Rx_buffer.vcu14_20.VCU_ACCEP2_VOLTAGE))
     {
         ILSet_VCU_ACCEP2_VOLTAGE_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_BRAKE1_VOLTAGE != Rx_buffer.vcu14_20.VCU_BRAKE1_VOLTAGE))
     {
         ILSet_VCU_BRAKE1_VOLTAGE_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_BRAKE2_VOLTAGE != Rx_buffer.vcu14_20.VCU_BRAKE2_VOLTAGE))
     {
         ILSet_VCU_BRAKE2_VOLTAGE_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_LV_BATTERY_VOLTAGE != Rx_buffer.vcu14_20.VCU_LV_BATTERY_VOLTAGE))
     {
         ILSet_VCU_LV_BATTERY_VOLTAGE_DataChanged();
     }

     if((VCU14_20.vcu14_20.VCU_STSISLNEVSE != Rx_buffer.vcu14_20.VCU_STSISLNEVSE))
     {
         ILSet_VCU_STSISLNEVSE_DataChanged();
     }

   }
}

void VCU15_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU15_100.vcu15_100.VCU_ECONSPERKM_0 != Rx_buffer.vcu15_100.VCU_ECONSPERKM_0) || 
       (VCU15_100.vcu15_100.VCU_ECONSPERKM_1 != Rx_buffer.vcu15_100.VCU_ECONSPERKM_1))
     {
         ILSet_VCU_ECONSPERKM_DataChanged();
     }

     if((VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_0 != Rx_buffer.vcu15_100.VCU_HVACCPOWERCONSUMPTION_0) || 
       (VCU15_100.vcu15_100.VCU_HVACCPOWERCONSUMPTION_1 != Rx_buffer.vcu15_100.VCU_HVACCPOWERCONSUMPTION_1))
     {
         ILSet_VCU_HVACCPOWERCONSUMPTION_DataChanged();
     }

     if((VCU15_100.vcu15_100.VCU_TORQUECOASTING_0 != Rx_buffer.vcu15_100.VCU_TORQUECOASTING_0) || 
       (VCU15_100.vcu15_100.VCU_TORQUECOASTING_1 != Rx_buffer.vcu15_100.VCU_TORQUECOASTING_1))
     {
         ILSet_VCU_TORQUECOASTING_DataChanged();
     }

     if((VCU15_100.vcu15_100.VCU_STCOASTING != Rx_buffer.vcu15_100.VCU_STCOASTING))
     {
         ILSet_VCU_STCOASTING_DataChanged();
     }

     if((VCU15_100.vcu15_100.VCU_STCREEP != Rx_buffer.vcu15_100.VCU_STCREEP))
     {
         ILSet_VCU_STCREEP_DataChanged();
     }

     if((VCU15_100.vcu15_100.VCU_SWITCHS2 != Rx_buffer.vcu15_100.VCU_SWITCHS2))
     {
         ILSet_VCU_SWITCHS2_DataChanged();
     }

   }
}

void VCU16_1000_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_0 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE1_0) || 
       (VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE1_1 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE1_1))
     {
         ILSet_VCU_ECONSDISTSAMPLE1_DataChanged();
     }

     if((VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_0 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE2_0) || 
       (VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE2_1 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE2_1))
     {
         ILSet_VCU_ECONSDISTSAMPLE2_DataChanged();
     }

     if((VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_0 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE3_0) || 
       (VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE3_1 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE3_1))
     {
         ILSet_VCU_ECONSDISTSAMPLE3_DataChanged();
     }

     if((VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_0 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE4_0) || 
       (VCU16_1000.vcu16_1000.VCU_ECONSDISTSAMPLE4_1 != Rx_buffer.vcu16_1000.VCU_ECONSDISTSAMPLE4_1))
     {
         ILSet_VCU_ECONSDISTSAMPLE4_DataChanged();
     }

   }
}

void VCU16_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU16_500.vcu16_500.VESS_DISABLE != Rx_buffer.vcu16_500.VESS_DISABLE))
     {
         ILSet_VESS_DISABLE_DataChanged();
     }

     if((VCU16_500.vcu16_500.VEHICLE_MODE != Rx_buffer.vcu16_500.VEHICLE_MODE))
     {
         ILSet_VEHICLE_MODE_DataChanged();
     }

     if((VCU16_500.vcu16_500.DTE_0 != Rx_buffer.vcu16_500.DTE_0) || 
       (VCU16_500.vcu16_500.DTE_1 != Rx_buffer.vcu16_500.DTE_1))
     {
         ILSet_DTE_DataChanged();
     }

     if((VCU16_500.vcu16_500.AVAIL_PWR_COMPRESSOR != Rx_buffer.vcu16_500.AVAIL_PWR_COMPRESSOR))
     {
         ILSet_AVAIL_PWR_COMPRESSOR_DataChanged();
     }

     if((VCU16_500.vcu16_500.AVAIL_PWR_CABIN_HEATER != Rx_buffer.vcu16_500.AVAIL_PWR_CABIN_HEATER))
     {
         ILSet_AVAIL_PWR_CABIN_HEATER_DataChanged();
     }

   }
}

void VCU17_200_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_0 != Rx_buffer.vcu17_200.BATT_COMPRES_SPD_REQ_0) || 
       (VCU17_200.vcu17_200.BATT_COMPRES_SPD_REQ_1 != Rx_buffer.vcu17_200.BATT_COMPRES_SPD_REQ_1))
     {
         ILSet_BATT_COMPRES_SPD_REQ_DataChanged();
     }

     if((VCU17_200.vcu17_200.BATT_COOLING_REQ != Rx_buffer.vcu17_200.BATT_COOLING_REQ))
     {
         ILSet_BATT_COOLING_REQ_DataChanged();
     }

     if((VCU17_200.vcu17_200.CRITICAL_HV_LOAD_CUTOFF != Rx_buffer.vcu17_200.CRITICAL_HV_LOAD_CUTOFF))
     {
         ILSet_CRITICAL_HV_LOAD_CUTOFF_DataChanged();
     }

     if((VCU17_200.vcu17_200.NONCRITICAL_HV_LOAD_CUTOFF != Rx_buffer.vcu17_200.NONCRITICAL_HV_LOAD_CUTOFF))
     {
         ILSet_NONCRITICAL_HV_LOAD_CUTOFF_DataChanged();
     }

     if((VCU17_200.vcu17_200.CRITICAL_LV_LOAD_CUTOFF != Rx_buffer.vcu17_200.CRITICAL_LV_LOAD_CUTOFF))
     {
         ILSet_CRITICAL_LV_LOAD_CUTOFF_DataChanged();
     }

     if((VCU17_200.vcu17_200.NONCRITICAL_LV_LOAD_CUTOFF != Rx_buffer.vcu17_200.NONCRITICAL_LV_LOAD_CUTOFF))
     {
         ILSet_NONCRITICAL_LV_LOAD_CUTOFF_DataChanged();
     }

     if((VCU17_200.vcu17_200.STS_EPT_RADIATORFAN != Rx_buffer.vcu17_200.STS_EPT_RADIATORFAN))
     {
         ILSet_STS_EPT_RADIATORFAN_DataChanged();
     }

     if((VCU17_200.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_0 != Rx_buffer.vcu17_200.EPT_RADIATORFAN_SPEED_REQ_0))
     {
         ILSet_EPT_RADIATORFAN_SPEED_REQ_DataChanged();
     }

     if((VCU17_200.vcu17_200.REMOTE_HV_CONNECT_FB != Rx_buffer.vcu17_200.REMOTE_HV_CONNECT_FB))
     {
         ILSet_REMOTE_HV_CONNECT_FB_DataChanged();
     }

     if((VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_0 != Rx_buffer.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_0) || 
       (VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_1 != Rx_buffer.vcu17_200.BATTERY_INLET_COOLANT_TEMP_REQ_1))
     {
         ILSet_BATTERY_INLET_COOLANT_TEMP_REQ_DataChanged();
     }

     if((VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_0 != Rx_buffer.vcu17_200.BATTERY_INLET_COOLANT_TEMP_0) || 
       (VCU17_200.vcu17_200.BATTERY_INLET_COOLANT_TEMP_1 != Rx_buffer.vcu17_200.BATTERY_INLET_COOLANT_TEMP_1))
     {
         ILSet_BATTERY_INLET_COOLANT_TEMP_DataChanged();
     }

     if((VCU17_200.vcu17_200.LIMIT_POWER_CCM != Rx_buffer.vcu17_200.LIMIT_POWER_CCM))
     {
         ILSet_LIMIT_POWER_CCM_DataChanged();
     }

   }
}

void VCU18_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU18_10.vcu18_10.VCU_CHARCP_RAWVAL != Rx_buffer.vcu18_10.VCU_CHARCP_RAWVAL))
     {
         ILSet_VCU_CHARCP_RAWVAL_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_CHARPD_RAWVAL != Rx_buffer.vcu18_10.VCU_CHARPD_RAWVAL))
     {
         ILSet_VCU_CHARPD_RAWVAL_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_EVCSI_STATE != Rx_buffer.vcu18_10.VCU_EVCSI_STATE))
     {
         ILSet_VCU_EVCSI_STATE_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_WAKEUP_REASON_INTERNAL != Rx_buffer.vcu18_10.VCU_WAKEUP_REASON_INTERNAL))
     {
         ILSet_VCU_WAKEUP_REASON_INTERNAL_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_BMS_ASW_SLEEPREQUEST != Rx_buffer.vcu18_10.VCU_BMS_ASW_SLEEPREQUEST))
     {
         ILSet_VCU_BMS_ASW_SLEEPREQUEST_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_NOSM_STATE_0 != Rx_buffer.vcu18_10.VCU_NOSM_STATE_0) || 
       (VCU18_10.vcu18_10.VCU_NOSM_STATE_1 != Rx_buffer.vcu18_10.VCU_NOSM_STATE_1))
     {
         ILSet_VCU_NOSM_STATE_DataChanged();
     }

     if((VCU18_10.vcu18_10.VCU_SMOBC_STATE_0 != Rx_buffer.vcu18_10.VCU_SMOBC_STATE_0) || 
       (VCU18_10.vcu18_10.VCU_SMOBC_STATE_1 != Rx_buffer.vcu18_10.VCU_SMOBC_STATE_1))
     {
         ILSet_VCU_SMOBC_STATE_DataChanged();
     }

   }
}

void VCU1_20_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU1_20.vcu1_20.VCU_MAINCONTACTORCONTROL != Rx_buffer.vcu1_20.VCU_MAINCONTACTORCONTROL))
     {
         ILSet_VCU_MAINCONTACTORCONTROL_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU_CMDENABLELDC != Rx_buffer.vcu1_20.VCU_CMDENABLELDC))
     {
         ILSet_VCU_CMDENABLELDC_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU_STSCODEVSE != Rx_buffer.vcu1_20.VCU_STSCODEVSE))
     {
         ILSet_VCU_STSCODEVSE_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU_CMDTARGETVOLTLDC != Rx_buffer.vcu1_20.VCU_CMDTARGETVOLTLDC))
     {
         ILSet_VCU_CMDTARGETVOLTLDC_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_0 != Rx_buffer.vcu1_20.VCU_MAXCHARGECURRENT_0) || 
       (VCU1_20.vcu1_20.VCU_MAXCHARGECURRENT_1 != Rx_buffer.vcu1_20.VCU_MAXCHARGECURRENT_1))
     {
         ILSet_VCU_MAXCHARGECURRENT_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_0 != Rx_buffer.vcu1_20.VCU_MAXDISCHARGECURRENT_0) || 
       (VCU1_20.vcu1_20.VCU_MAXDISCHARGECURRENT_1 != Rx_buffer.vcu1_20.VCU_MAXDISCHARGECURRENT_1))
     {
         ILSet_VCU_MAXDISCHARGECURRENT_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU337_COUNTER != Rx_buffer.vcu1_20.VCU337_COUNTER))
     {
         ILSet_VCU337_COUNTER_DataChanged();
     }

     if((VCU1_20.vcu1_20.VCU337_CRC != Rx_buffer.vcu1_20.VCU337_CRC))
     {
         ILSet_VCU337_CRC_DataChanged();
     }

   }
}

void VCU2_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_0 != Rx_buffer.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_0) || 
       (VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_1 != Rx_buffer.vcu2_100.VCU_CMDACCHARGETARGETCURRENT_1))
     {
         ILSet_VCU_CMDACCHARGETARGETCURRENT_DataChanged();
     }

     if((VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_0 != Rx_buffer.vcu2_100.VCU_CMDACCHARGETARGETVOLT_0) || 
       (VCU2_100.vcu2_100.VCU_CMDACCHARGETARGETVOLT_1 != Rx_buffer.vcu2_100.VCU_CMDACCHARGETARGETVOLT_1))
     {
         ILSet_VCU_CMDACCHARGETARGETVOLT_DataChanged();
     }

     if((VCU2_100.vcu2_100.VCU_ACCHARGINGREADY != Rx_buffer.vcu2_100.VCU_ACCHARGINGREADY))
     {
         ILSet_VCU_ACCHARGINGREADY_DataChanged();
     }

     if((VCU2_100.vcu2_100.VCU_CMDENABLEOBC != Rx_buffer.vcu2_100.VCU_CMDENABLEOBC))
     {
         ILSet_VCU_CMDENABLEOBC_DataChanged();
     }

     if((VCU2_100.vcu2_100.VCU338_COUNTER != Rx_buffer.vcu2_100.VCU338_COUNTER))
     {
         ILSet_VCU338_COUNTER_DataChanged();
     }

     if((VCU2_100.vcu2_100.VCU338_CRC != Rx_buffer.vcu2_100.VCU338_CRC))
     {
         ILSet_VCU338_CRC_DataChanged();
     }

   }
}

void VCU3_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU3_100.vcu3_100.VCU_EVREADY != Rx_buffer.vcu3_100.VCU_EVREADY))
     {
         ILSet_VCU_EVREADY_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU_STS_IGN != Rx_buffer.vcu3_100.VCU_STS_IGN))
     {
         ILSet_VCU_STS_IGN_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU_EPTCOOLANTFLOW != Rx_buffer.vcu3_100.VCU_EPTCOOLANTFLOW))
     {
         ILSet_VCU_EPTCOOLANTFLOW_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU_AUX_BATTERY_VOLT != Rx_buffer.vcu3_100.VCU_AUX_BATTERY_VOLT))
     {
         ILSet_VCU_AUX_BATTERY_VOLT_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU_EPTCOOLANTTEMP != Rx_buffer.vcu3_100.VCU_EPTCOOLANTTEMP))
     {
         ILSet_VCU_EPTCOOLANTTEMP_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_0 != Rx_buffer.vcu3_100.VCU_VEHICLE_SPEED_0) || 
       (VCU3_100.vcu3_100.VCU_VEHICLE_SPEED_1 != Rx_buffer.vcu3_100.VCU_VEHICLE_SPEED_1))
     {
         ILSet_VCU_VEHICLE_SPEED_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU336_COUNTER != Rx_buffer.vcu3_100.VCU336_COUNTER))
     {
         ILSet_VCU336_COUNTER_DataChanged();
     }

     if((VCU3_100.vcu3_100.VCU336_CRC != Rx_buffer.vcu3_100.VCU336_CRC))
     {
         ILSet_VCU336_CRC_DataChanged();
     }

   }
}

void VCU4_20_EV_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU4_20_EV.vcu4_20_ev.VCU_ECOMP_HVIL_STATUS != Rx_buffer.vcu4_20_ev.VCU_ECOMP_HVIL_STATUS))
     {
         ILSet_VCU_ECOMP_HVIL_STATUS_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_SRSCRASHSTA != Rx_buffer.vcu4_20_ev.VCU_SRSCRASHSTA))
     {
         ILSet_VCU_SRSCRASHSTA_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_TRANSPMOTORPARKREQ != Rx_buffer.vcu4_20_ev.VCU_TRANSPMOTORPARKREQ))
     {
         ILSet_VCU_TRANSPMOTORPARKREQ_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_CHARGE_DISCHARGE_TRANS != Rx_buffer.vcu4_20_ev.VCU_CHARGE_DISCHARGE_TRANS))
     {
         ILSet_VCU_CHARGE_DISCHARGE_TRANS_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_MSGSTS != Rx_buffer.vcu4_20_ev.VCU_MSGSTS))
     {
         ILSet_VCU_MSGSTS_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_RESPCOD != Rx_buffer.vcu4_20_ev.VCU_RESPCOD))
     {
         ILSet_VCU_RESPCOD_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_STMACERR != Rx_buffer.vcu4_20_ev.VCU_STMACERR))
     {
         ILSet_VCU_STMACERR_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_0 != Rx_buffer.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_0) || 
       (VCU4_20_EV.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_1 != Rx_buffer.vcu4_20_ev.VCU_EXMEDI_IDXDCCHRGNERR_1))
     {
         ILSet_VCU_EXMEDI_IDXDCCHRGNERR_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU241_COUNTER != Rx_buffer.vcu4_20_ev.VCU241_COUNTER))
     {
         ILSet_VCU241_COUNTER_DataChanged();
     }

     if((VCU4_20_EV.vcu4_20_ev.VCU241_CHECKSUM != Rx_buffer.vcu4_20_ev.VCU241_CHECKSUM))
     {
         ILSet_VCU241_CHECKSUM_DataChanged();
     }

   }
}

void VCU5_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_0 != Rx_buffer.vcu5_100.VCU_HVACCOOLINGPOWER_0) || 
       (VCU5_100.vcu5_100.VCU_HVACCOOLINGPOWER_1 != Rx_buffer.vcu5_100.VCU_HVACCOOLINGPOWER_1))
     {
         ILSet_VCU_HVACCOOLINGPOWER_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_HVACCOOLINGSTA != Rx_buffer.vcu5_100.VCU_HVACCOOLINGSTA))
     {
         ILSet_VCU_HVACCOOLINGSTA_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_ACTIVEDAMPINGDISABLECOMMAND != Rx_buffer.vcu5_100.VCU_ACTIVEDAMPINGDISABLECOMMAND))
     {
         ILSet_VCU_ACTIVEDAMPINGDISABLECOMMAND_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_HVACHEATINGSTA != Rx_buffer.vcu5_100.VCU_HVACHEATINGSTA))
     {
         ILSet_VCU_HVACHEATINGSTA_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_DISP_AMBT_TEMP_FATC != Rx_buffer.vcu5_100.VCU_DISP_AMBT_TEMP_FATC))
     {
         ILSet_VCU_DISP_AMBT_TEMP_FATC_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_CHARGINGPLUGSTA != Rx_buffer.vcu5_100.VCU_CHARGINGPLUGSTA))
     {
         ILSet_VCU_CHARGINGPLUGSTA_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_HVCONNECT_STA != Rx_buffer.vcu5_100.VCU_HVCONNECT_STA))
     {
         ILSet_VCU_HVCONNECT_STA_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_0 != Rx_buffer.vcu5_100.VCU_VALEVSEIMAXLIM_0) || 
       (VCU5_100.vcu5_100.VCU_VALEVSEIMAXLIM_1 != Rx_buffer.vcu5_100.VCU_VALEVSEIMAXLIM_1))
     {
         ILSet_VCU_VALEVSEIMAXLIM_DataChanged();
     }

     if((VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_0 != Rx_buffer.vcu5_100.VCU_VALEVSEIMINLIM_0) || 
       (VCU5_100.vcu5_100.VCU_VALEVSEIMINLIM_1 != Rx_buffer.vcu5_100.VCU_VALEVSEIMINLIM_1))
     {
         ILSet_VCU_VALEVSEIMINLIM_DataChanged();
     }

   }
}

void VCU5_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_0 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_0) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_1 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_1) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_2 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_2) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_3 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_3) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_4 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_4) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_5 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_5) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_6 != Rx_buffer.vcu5_500.vin_index_data.vin_index_1.VIN_DATA_1_6))
     {
         ILSet_VIN_DATA_1_DataChanged();
     }

     if((VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_0 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_0) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_1 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_1) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_2 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_2) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_3 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_3) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_4 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_4) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_5 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_5) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_6 != Rx_buffer.vcu5_500.vin_index_data.vin_index_0.VIN_DATA_0_6))
     {
         ILSet_VIN_DATA_0_DataChanged();
     }

     if((VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_0 != Rx_buffer.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_0) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_1 != Rx_buffer.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_1) || 
       (VCU5_500.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_2 != Rx_buffer.vcu5_500.vin_index_data.vin_index_2.VIN_DATA_2_2))
     {
         ILSet_VIN_DATA_2_DataChanged();
     }

     if((VCU5_500.vcu5_500.VIN_INDEX != Rx_buffer.vcu5_500.VIN_INDEX))
     {
         ILSet_VIN_INDEX_DataChanged();
     }

   }
}

void VCU7_100_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU7_100.vcu7_100.VCU_CMDACCP != Rx_buffer.vcu7_100.VCU_CMDACCP))
     {
         ILSet_VCU_CMDACCP_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_HVDISCONNECT_REASONS != Rx_buffer.vcu7_100.VCU_HVDISCONNECT_REASONS))
     {
         ILSet_VCU_HVDISCONNECT_REASONS_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_VEHCHARGEMODESTA != Rx_buffer.vcu7_100.VCU_VEHCHARGEMODESTA))
     {
         ILSet_VCU_VEHCHARGEMODESTA_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_GEAR_ACTUAL != Rx_buffer.vcu7_100.VCU_GEAR_ACTUAL))
     {
         ILSet_VCU_GEAR_ACTUAL_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_CMDACPWM != Rx_buffer.vcu7_100.VCU_CMDACPWM))
     {
         ILSet_VCU_CMDACPWM_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_PP_CURRENTLIMIT != Rx_buffer.vcu7_100.VCU_PP_CURRENTLIMIT))
     {
         ILSet_VCU_PP_CURRENTLIMIT_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_VALEVSEPRESI_0 != Rx_buffer.vcu7_100.VCU_VALEVSEPRESI_0) || 
       (VCU7_100.vcu7_100.VCU_VALEVSEPRESI_1 != Rx_buffer.vcu7_100.VCU_VALEVSEPRESI_1))
     {
         ILSet_VCU_VALEVSEPRESI_DataChanged();
     }

     if((VCU7_100.vcu7_100.VCU_VALEVSEPRESU_0 != Rx_buffer.vcu7_100.VCU_VALEVSEPRESU_0) || 
       (VCU7_100.vcu7_100.VCU_VALEVSEPRESU_1 != Rx_buffer.vcu7_100.VCU_VALEVSEPRESU_1))
     {
         ILSet_VCU_VALEVSEPRESU_DataChanged();
     }

   }
}

void VCU8_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU8_10.vcu8_10.VCU_ACTV_DISCHARGE_REQ != Rx_buffer.vcu8_10.VCU_ACTV_DISCHARGE_REQ))
     {
         ILSet_VCU_ACTV_DISCHARGE_REQ_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_ISOLT_MTR_STP_REQ != Rx_buffer.vcu8_10.VCU_ISOLT_MTR_STP_REQ))
     {
         ILSet_VCU_ISOLT_MTR_STP_REQ_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_COMMANDMODE != Rx_buffer.vcu8_10.VCU_COMMANDMODE))
     {
         ILSet_VCU_COMMANDMODE_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_OPERATIONALMODECMD != Rx_buffer.vcu8_10.VCU_OPERATIONALMODECMD))
     {
         ILSet_VCU_OPERATIONALMODECMD_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_OPERATIONREQ != Rx_buffer.vcu8_10.VCU_OPERATIONREQ))
     {
         ILSet_VCU_OPERATIONREQ_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_VEHICLESTATE != Rx_buffer.vcu8_10.VCU_VEHICLESTATE))
     {
         ILSet_VCU_VEHICLESTATE_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_ERRSTACK != Rx_buffer.vcu8_10.VCU_ERRSTACK))
     {
         ILSet_VCU_ERRSTACK_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_MSGST != Rx_buffer.vcu8_10.VCU_MSGST))
     {
         ILSet_VCU_MSGST_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU_TORQUECOMMAND_0 != Rx_buffer.vcu8_10.VCU_TORQUECOMMAND_0) || 
       (VCU8_10.vcu8_10.VCU_TORQUECOMMAND_1 != Rx_buffer.vcu8_10.VCU_TORQUECOMMAND_1))
     {
         ILSet_VCU_TORQUECOMMAND_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU112_COUNTER != Rx_buffer.vcu8_10.VCU112_COUNTER))
     {
         ILSet_VCU112_COUNTER_DataChanged();
     }

     if((VCU8_10.vcu8_10.VCU112_CHECKSUM != Rx_buffer.vcu8_10.VCU112_CHECKSUM))
     {
         ILSet_VCU112_CHECKSUM_DataChanged();
     }

   }
}

void VCU_FC1_10_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_0 != Rx_buffer.vcu_fc1_10.VCU_ISETPOINTCHRGN_0) || 
       (VCU_FC1_10.vcu_fc1_10.VCU_ISETPOINTCHRGN_1 != Rx_buffer.vcu_fc1_10.VCU_ISETPOINTCHRGN_1))
     {
         ILSet_VCU_ISETPOINTCHRGN_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_0 != Rx_buffer.vcu_fc1_10.VCU_USETPOINTCHRGN_0) || 
       (VCU_FC1_10.vcu_fc1_10.VCU_USETPOINTCHRGN_1 != Rx_buffer.vcu_fc1_10.VCU_USETPOINTCHRGN_1))
     {
         ILSet_VCU_USETPOINTCHRGN_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_STMACSTS != Rx_buffer.vcu_fc1_10.VCU_STMACSTS))
     {
         ILSet_VCU_STMACSTS_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_ERREVEH != Rx_buffer.vcu_fc1_10.VCU_ERREVEH))
     {
         ILSet_VCU_ERREVEH_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_STSCOMASSCN != Rx_buffer.vcu_fc1_10.VCU_STSCOMASSCN))
     {
         ILSet_VCU_STSCOMASSCN_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_STSVEHRDY != Rx_buffer.vcu_fc1_10.VCU_STSVEHRDY))
     {
         ILSet_VCU_STSVEHRDY_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_MSGRXCYCLC != Rx_buffer.vcu_fc1_10.VCU_MSGRXCYCLC))
     {
         ILSet_VCU_MSGRXCYCLC_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_TRIGMSGTXCYCLC != Rx_buffer.vcu_fc1_10.VCU_TRIGMSGTXCYCLC))
     {
         ILSet_VCU_TRIGMSGTXCYCLC_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_EXMEDI_ERRSTSEMPOWDCRIT != Rx_buffer.vcu_fc1_10.VCU_EXMEDI_ERRSTSEMPOWDCRIT))
     {
         ILSet_VCU_EXMEDI_ERRSTSEMPOWDCRIT_DataChanged();
     }

     if((VCU_FC1_10.vcu_fc1_10.VCU_EXMEDI_ERRSTSEMPOWDNONECRIT != Rx_buffer.vcu_fc1_10.VCU_EXMEDI_ERRSTSEMPOWDNONECRIT))
     {
         ILSet_VCU_EXMEDI_ERRSTSEMPOWDNONECRIT_DataChanged();
     }

   }
}

void VCU_STS_500_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((VCU_STS_500.vcu_sts_500.VCU_STS_IGN_NM != Rx_buffer.vcu_sts_500.VCU_STS_IGN_NM))
     {
         ILSet_VCU_STS_IGN_NM_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_VARIANT_CODE_ERR_STS != Rx_buffer.vcu_sts_500.VCU_VARIANT_CODE_ERR_STS))
     {
         ILSet_VCU_VARIANT_CODE_ERR_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_COMFLT_SGN_CONTFAIL != Rx_buffer.vcu_sts_500.VCU_COMFLT_SGN_CONTFAIL))
     {
         ILSet_VCU_COMFLT_SGN_CONTFAIL_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_FEATURE_CODE_ERR_STS != Rx_buffer.vcu_sts_500.VCU_FEATURE_CODE_ERR_STS))
     {
         ILSet_VCU_FEATURE_CODE_ERR_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_COMFLT_MSGTOUT_STS != Rx_buffer.vcu_sts_500.VCU_COMFLT_MSGTOUT_STS))
     {
         ILSet_VCU_COMFLT_MSGTOUT_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_COMFLT_NODEABS_STS != Rx_buffer.vcu_sts_500.VCU_COMFLT_NODEABS_STS))
     {
         ILSet_VCU_COMFLT_NODEABS_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_UV_STS != Rx_buffer.vcu_sts_500.VCU_UV_STS))
     {
         ILSet_VCU_UV_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_OV_STS != Rx_buffer.vcu_sts_500.VCU_OV_STS))
     {
         ILSet_VCU_OV_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_AUX_BATT_VOLT != Rx_buffer.vcu_sts_500.VCU_AUX_BATT_VOLT))
     {
         ILSet_VCU_AUX_BATT_VOLT_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_NM_ACTIVE_STS != Rx_buffer.vcu_sts_500.VCU_NM_ACTIVE_STS))
     {
         ILSet_VCU_NM_ACTIVE_STS_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_COMFLT_MSG_CONTFAIL != Rx_buffer.vcu_sts_500.VCU_COMFLT_MSG_CONTFAIL))
     {
         ILSet_VCU_COMFLT_MSG_CONTFAIL_DataChanged();
     }

     if((VCU_STS_500.vcu_sts_500.VCU_SW_VERSION != Rx_buffer.vcu_sts_500.VCU_SW_VERSION))
     {
         ILSet_VCU_SW_VERSION_DataChanged();
     }

   }
}

void WLC3_2000_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((WLC3_2000.wlc3_2000.TIME_TO_CHARGE != Rx_buffer.wlc3_2000.TIME_TO_CHARGE))
     {
         ILSet_TIME_TO_CHARGE_DataChanged();
     }

     if((WLC3_2000.wlc3_2000.FOD_ALERT != Rx_buffer.wlc3_2000.FOD_ALERT))
     {
         ILSet_FOD_ALERT_DataChanged();
     }

   }
}

void WLC_NSM_PreCopy (void)
{
   if (0 == (il_status & (CAN_UINT8) IL_STATUS_SUSPEND))
   {
     if((WLC_NSM.wlc_nsm.RESERVED_WLC_0 != Rx_buffer.wlc_nsm.RESERVED_WLC_0) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_1 != Rx_buffer.wlc_nsm.RESERVED_WLC_1) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_2 != Rx_buffer.wlc_nsm.RESERVED_WLC_2) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_3 != Rx_buffer.wlc_nsm.RESERVED_WLC_3) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_4 != Rx_buffer.wlc_nsm.RESERVED_WLC_4) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_5 != Rx_buffer.wlc_nsm.RESERVED_WLC_5) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_6 != Rx_buffer.wlc_nsm.RESERVED_WLC_6) || 
       (WLC_NSM.wlc_nsm.RESERVED_WLC_7 != Rx_buffer.wlc_nsm.RESERVED_WLC_7))
     {
         ILSet_RESERVED_WLC_DataChanged();
     }

   }
}

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
Date			    : 2024-02-16 15:47
By			        : VENKI
Traceability		: S220&S237_IVN_Communication_Matrix_SMART_CORE_Rev36144_080224_Edited.dbc
Change Description	: Tool Generated code
*****************************************************************************/
