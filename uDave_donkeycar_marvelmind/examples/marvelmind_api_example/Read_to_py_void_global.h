#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "marvelmind.h"

static struct MarvelmindHedge* GLOBAL_HEDGE;

// Init
bool initHedge (char * ttyFileName);

// Data providers
bool getHedgePosition (struct PositionValue * position);
bool getHedgeStationaryBeaconsPositions (struct StationaryBeaconsPositions * positions);
bool getHedgeRawDistances (struct RawDistances* rawDistances);
bool getHedgeRawIMU (struct RawIMUValue* rawIMU);
bool getHedgeFusionIMU (struct FusionIMUValue * fusionIMU);
bool getHedgeTelemetry (struct TelemetryData * telemetry);
bool getHedgeQuality (struct QualityData * quality);

// Exit
bool stopHedge ();
