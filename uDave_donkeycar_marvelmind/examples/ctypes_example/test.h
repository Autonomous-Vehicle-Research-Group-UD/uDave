#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "called.h"

//////////////////////////////////////////////////////////////////////////////
// Init
//////////////////////////////////////////////////////////////////////////////
bool initHedge (char * ttyFileName, struct MarvelmindHedge * hedge);

//////////////////////////////////////////////////////////////////////////////
bool getHedgePositionByAddr (struct MarvelmindHedge * hedge, struct PositionValue * position, uint8_t address);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeStationaryBeaconsPositions (struct MarvelmindHedge * hedge, struct StationaryBeaconsPositions * positions);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawDistances (struct MarvelmindHedge * hedge, struct RawDistances* rawDistances);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawIMU (struct MarvelmindHedge * hedge, struct RawIMUValue* rawIMU);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeFusionIMU (struct MarvelmindHedge * hedge, struct FusionIMUValue * fusionIMU);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeTelemetry (struct MarvelmindHedge * hedge, struct TelemetryData * telemetry);
//////////////////////////////////////////////////////////////////////////////
bool getHedgeQuality (struct MarvelmindHedge * hedge, struct QualityData * quality);
//////////////////////////////////////////////////////////////////////////////
bool pointerTest (int * a, int * b);
//////////////////////////////////////////////////////////////////////////////
int callTest (int a);
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
// Exit
//////////////////////////////////////////////////////////////////////////////
bool stopHedge (struct MarvelmindHedge * hedge);

