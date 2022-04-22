#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#include "marvelmind.h"
#include "Read_to_py_void_global.h"

//////////////////////////////////////////////////////////////////////////////
// Init
//////////////////////////////////////////////////////////////////////////////
bool initHedge (char * ttyFileName)
{
    GLOBAL_HEDGE = createMarvelmindHedge();
    if (GLOBAL_HEDGE==NULL)
    {
        puts ("Error: Unable to create MarvelmindHedge");
        return false;
    }
    GLOBAL_HEDGE->ttyFileName=ttyFileName;
    GLOBAL_HEDGE->verbose=true; // show errors and warnings
    startMarvelmindHedge (GLOBAL_HEDGE);
    
    return true;
}

//////////////////////////////////////////////////////////////////////////////
// Get position coordinates
// hedge:      MarvelmindHedge structure
// position:   pointer to PositionValue for write coordinates
// returncode: true if position is valid
//////////////////////////////////////////////////////////////////////////////
bool getHedgePosition (struct PositionValue * position)
{
    return getPositionFromMarvelmindHedge(GLOBAL_HEDGE, position);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeStationaryBeaconsPositions (struct StationaryBeaconsPositions * positions)
{
    return getStationaryBeaconsPositionsFromMarvelmindHedge (GLOBAL_HEDGE, positions);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawDistances (struct RawDistances* rawDistances)
{
    return getRawDistancesFromMarvelmindHedge (GLOBAL_HEDGE, rawDistances);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawIMU (struct RawIMUValue* rawIMU)
{
    return getRawIMUFromMarvelmindHedge (GLOBAL_HEDGE, rawIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeFusionIMU (struct FusionIMUValue * fusionIMU)
{
    return getFusionIMUFromMarvelmindHedge (GLOBAL_HEDGE, fusionIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeTelemetry (struct TelemetryData * telemetry)
{
    return getTelemetryFromMarvelmindHedge (GLOBAL_HEDGE, telemetry);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeQuality (struct QualityData * quality)
{
    return getQualityFromMarvelmindHedge (GLOBAL_HEDGE, quality);
};

//////////////////////////////////////////////////////////////////////////////
// Exit
//////////////////////////////////////////////////////////////////////////////
bool stopHedge (){
    stopMarvelmindHedge (GLOBAL_HEDGE);
    destroyMarvelmindHedge (GLOBAL_HEDGE);
    return true;
}

