#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "marvelmind.h"

// Init
void * initHedge (char * ttyFileName);

// Data providers
bool getHedgePosition (void * hedge, struct PositionValue * position);
bool getHedgeStationaryBeaconsPositions (void * hedge, struct StationaryBeaconsPositions * positions);
bool getHedgeRawDistances (void * hedge, struct RawDistances* rawDistances);
bool getHedgeRawIMU (void * hedge, struct RawIMUValue* rawIMU);
bool getHedgeFusionIMU (void * hedge, struct FusionIMUValue * fusionIMU);
bool getHedgeTelemetry (void * hedge, struct TelemetryData * telemetry);
bool getHedgeQuality (void * hedge, struct QualityData * quality);

// Exit
bool stopHedge (void * hedge);
