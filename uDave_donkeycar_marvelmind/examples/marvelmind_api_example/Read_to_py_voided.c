#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#include "marvelmind.h"
#include "Read_to_py_voided.h"

//////////////////////////////////////////////////////////////////////////////
// Init
//////////////////////////////////////////////////////////////////////////////
void * initHedge (char * ttyFileName)
{
    struct MarvelmindHedge* hedge = createMarvelmindHedge();
    if (hedge==NULL)
    {
        puts ("Error: Unable to create MarvelmindHedge");
        return NULL;
    }
    hedge->ttyFileName=ttyFileName;
    hedge->verbose=true; // show errors and warnings
    startMarvelmindHedge (hedge);
    
    return hedge;
}

//////////////////////////////////////////////////////////////////////////////
// Get position coordinates
// hedge:      MarvelmindHedge structure
// position:   pointer to PositionValue for write coordinates
// returncode: true if position is valid
//////////////////////////////////////////////////////////////////////////////
bool getHedgePosition (void * hedge, struct PositionValue * position)
{
    return getPositionFromMarvelmindHedge((struct MarvelmindHedge*) hedge, position);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeStationaryBeaconsPositions (void * hedge, struct StationaryBeaconsPositions * positions)
{
    return getStationaryBeaconsPositionsFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, positions);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawDistances (void * hedge, struct RawDistances* rawDistances)
{
    return getRawDistancesFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, rawDistances);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeRawIMU (void * hedge, struct RawIMUValue* rawIMU)
{
    return getRawIMUFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, rawIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeFusionIMU (void * hedge, struct FusionIMUValue * fusionIMU)
{
    return getFusionIMUFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, fusionIMU);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeTelemetry (void * hedge, struct TelemetryData * telemetry)
{
    return getTelemetryFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, telemetry);
};
//////////////////////////////////////////////////////////////////////////////
bool getHedgeQuality (void * hedge, struct QualityData * quality)
{
    return getQualityFromMarvelmindHedge ((struct MarvelmindHedge*) hedge, quality);
};

//////////////////////////////////////////////////////////////////////////////
// Exit
//////////////////////////////////////////////////////////////////////////////
bool stopHedge (void * hedge){
    stopMarvelmindHedge ((struct MarvelmindHedge *) hedge);
    destroyMarvelmindHedge ((struct MarvelmindHedge *) hedge);
    return true;
}

