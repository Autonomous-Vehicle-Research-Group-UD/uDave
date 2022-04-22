#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#include "marvelmind.h"
#include "Read_to_py.h"

//////////////////////////////////////////////////////////////////////////////
// Init
//////////////////////////////////////////////////////////////////////////////
bool initHedge (char * ttyFileName, struct MarvelmindHedge * hedge)
{
    hedge = createMarvelmindHedge();
    if (hedge==NULL)
    {
        puts ("Error: Unable to create MarvelmindHedge");
        return -1;
    }
    hedge->ttyFileName=ttyFileName;
    //hedge->verbose=true; // show errors and warnings
    startMarvelmindHedge (hedge);
    
    return 0;
}

//////////////////////////////////////////////////////////////////////////////
// Get position coordinates
// hedge:      MarvelmindHedge structure
// position:   pointer to PositionValue for write coordinates
// returncode: true if position is valid
//////////////////////////////////////////////////////////////////////////////
bool getHedgePositionByAddr (struct MarvelmindHedge * hedge, struct PositionValue * position, uint8_t address)
{
    return getPositionFromMarvelmindHedgeByAddress(hedge, position, address);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeStationaryBeaconsPositions (struct MarvelmindHedge * hedge, struct StationaryBeaconsPositions * positions)
{
    return getStationaryBeaconsPositionsFromMarvelmindHedge (hedge, positions);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawDistances (struct MarvelmindHedge * hedge, struct RawDistances* rawDistances)
{
    return getRawDistancesFromMarvelmindHedge (hedge, rawDistances);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawIMU (struct MarvelmindHedge * hedge, struct RawIMUValue* rawIMU)
{
    return getRawIMUFromMarvelmindHedge (hedge, rawIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeFusionIMU (struct MarvelmindHedge * hedge, struct FusionIMUValue * fusionIMU)
{
    return getFusionIMUFromMarvelmindHedge (hedge, fusionIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeTelemetry (struct MarvelmindHedge * hedge, struct TelemetryData * telemetry)
{
    return getTelemetryFromMarvelmindHedge (hedge, telemetry);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeQuality (struct MarvelmindHedge * hedge, struct QualityData * quality)
{
    return getQualityFromMarvelmindHedge (hedge, quality);
};

//////////////////////////////////////////////////////////////////////////////
// Exit
//////////////////////////////////////////////////////////////////////////////
bool stopHedge (struct MarvelmindHedge * hedge){
    stopMarvelmindHedge (hedge);
    destroyMarvelmindHedge (hedge);
    return true;
}

