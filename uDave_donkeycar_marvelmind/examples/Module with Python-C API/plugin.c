#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <semaphore.h>
#include <time.h>
#include "marvelmind.h"
#include "plugin.h"

#include <Python.h>

//////////////////////////////////////////////////////////////////////////////
// Init
static PyObject *initHedge (PyObject *self, PyObject *args)
{
    char *ttyFileName;
    
    if(!PyArg_ParseTuple(args, "s", &ttyFileName))
        return NULL;
    
    GLOBAL_HEDGE = createMarvelmindHedge();
    if (GLOBAL_HEDGE==NULL)
    {
        puts ("Error: Unable to create MarvelmindHedge");
        return Py_BuildValue("b", 0);
    }
    GLOBAL_HEDGE->ttyFileName=ttyFileName;
    GLOBAL_HEDGE->verbose=true; // show errors and warnings
    startMarvelmindHedge (GLOBAL_HEDGE);
    
    return Py_BuildValue("b", 1);
}
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
// Data returners
static PyObject *getHedgePosition (PyObject *self, PyObject *args)
{
    struct PositionValue position;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getPositionFromMarvelmindHedge(GLOBAL_HEDGE, &position);
    
    return Py_BuildValue("[iIiiidiiii]", 
        position.address, 
        position.timestamp, 
        position.x, 
        position.y, 
        position.z, 
        position.angle, 
        position.highResolution, 
        position.ready, 
        position.processed, 
        success
    );
};

//Partial data provideing
static PyObject *getHedgeStationaryBeaconsPositions (PyObject *self, PyObject *args)
{
    struct StationaryBeaconsPositions positions;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getStationaryBeaconsPositionsFromMarvelmindHedge (GLOBAL_HEDGE, &positions);
    
    //Create a pylist in C
    int numOfBeacons = (positions.numBeacons > MAX_STATIONARY_BEACONS) ? MAX_STATIONARY_BEACONS : positions.numBeacons;
    PyObject *python_ret_val = PyList_New(3 + numOfBeacons);
    
    //Before the big array
    PyList_SetItem(python_ret_val, 0, Py_BuildValue("b", positions.numBeacons));
    
    //The big array
    int i = 0;
    while(i < positions.numBeacons && i < MAX_STATIONARY_BEACONS ){
        
        //Create StationaryBeaconPosition object
        PyObject *ith_StatBeacPos = Py_BuildValue("[biiib]", 
            positions.beacons[i].address, 
            positions.beacons[i].x, 
            positions.beacons[i].y, 
            positions.beacons[i].z, 
            positions.beacons[i].highResolution
        );
        
        PyList_SetItem(python_ret_val, 1+i, ith_StatBeacPos);
        
        i++;
    }
    //After the big array
    PyList_SetItem(python_ret_val, numOfBeacons+1, Py_BuildValue("b", positions.updated));
    PyList_SetItem(python_ret_val, numOfBeacons+2, Py_BuildValue("b", success));
    
    return python_ret_val;
};

static PyObject *getHedgeRawDistances (PyObject *self, PyObject *args)
{
    struct RawDistances rawdistances;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getRawDistancesFromMarvelmindHedge(GLOBAL_HEDGE, &rawdistances);
    
    return Py_BuildValue("[b[bI][bI][bI][bI]IHb]", 
        rawdistances.address_hedge, 
        rawdistances.distances[0].address_beacon, 
        rawdistances.distances[0].distance, 
        rawdistances.distances[1].address_beacon, 
        rawdistances.distances[1].distance, 
        rawdistances.distances[2].address_beacon, 
        rawdistances.distances[2].distance, 
        rawdistances.distances[3].address_beacon, 
        rawdistances.distances[3].distance, 
        rawdistances.timestamp, 
        rawdistances.timeShift, 
        rawdistances.updated, 
        success
    );
};

static PyObject *getHedgeRawIMU (PyObject *self, PyObject *args)
{
    struct RawIMUValue rawIMU;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getRawIMUFromMarvelmindHedge(GLOBAL_HEDGE, &rawIMU);
    
    return Py_BuildValue("[hhhhhhhhhIbb]", 
        rawIMU.acc_x, 
        rawIMU.acc_y, 
        rawIMU.acc_z, 
        rawIMU.gyro_x, 
        rawIMU.gyro_y, 
        rawIMU.gyro_z, 
        rawIMU.compass_x, 
        rawIMU.compass_y, 
        rawIMU.compass_z, 
        rawIMU.timestamp, 
        rawIMU.updated, 
        success
    );
};

static PyObject *getHedgeFusionIMU (PyObject *self, PyObject *args)
{
    struct FusionIMUValue fusionIMU;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getFusionIMUFromMarvelmindHedge(GLOBAL_HEDGE, &fusionIMU);
    
    return Py_BuildValue("[iiihhhhhhhhhhIbb]", 
        fusionIMU.x, 
        fusionIMU.y, 
        fusionIMU.z, 
        fusionIMU.qw, 
        fusionIMU.qx, 
        fusionIMU.qy, 
        fusionIMU.qz,
        fusionIMU.vx, 
        fusionIMU.vy, 
        fusionIMU.vz, 
        fusionIMU.ax, 
        fusionIMU.ay, 
        fusionIMU.az, 
        fusionIMU.timestamp, 
        fusionIMU.updated, 
        success
    );
};

static PyObject *getHedgeTelemetry (PyObject *self, PyObject *args)
{
    struct TelemetryData telemetry;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getTelemetryFromMarvelmindHedge(GLOBAL_HEDGE, &telemetry);
    
    return Py_BuildValue("[Hibb]", 
        telemetry.vbat_mv, 
        telemetry.rssi_dbm, 
        telemetry.updated, 
        success
    );
};

static PyObject *getHedgeQuality (PyObject *self, PyObject *args)
{
    struct QualityData quality;
    
    if(!PyArg_ParseTuple(args, ""))
        return NULL;
    
    bool success = getQualityFromMarvelmindHedge(GLOBAL_HEDGE, &quality);
    
    return Py_BuildValue("[BBbb]", 
        quality.address, 
        quality.quality_per, 
        quality.updated, 
        success
    );
};

//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
// Exit
static PyObject *stopHedge(PyObject *self, PyObject *args){
    
    int ok = PyArg_ParseTuple(args, "");
    
    if(!ok)
        return NULL;
    
    stopMarvelmindHedge (GLOBAL_HEDGE);
    destroyMarvelmindHedge (GLOBAL_HEDGE);
    
    return Py_BuildValue("i", 1);
}
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//Py API
//Documentations
static char initHedge_document[] = "Starts the data provider service. The serial connecton will be established in the arg serial port with the hedge.";
static char getHedgePosition_document[] = "Get the Hedge's position in the service field.";
static char getHedgeStationaryBeaconsPositions_document[] = "Get the stationary Beacon's positions in the service field.";
static char getHedgeRawDistances_document[] = "Get the Hedge's distance from it's submap Beacons.";
static char getHedgeRawIMU_document[] = "Get the Hedge's raw IMU data.";
static char getHedgeFusionIMU_document[] = "Get the Hedge's position and IMU data fused.";
static char getHedgeTelemetry_document[] = "Get the service's Telemetry.";
static char getHedgeQuality_document[] = "Get the service's quality.";
static char stopHedge_document[] = "Stop the service and close it's task.";

//Function definitions the following way:
//	function_name, function, METH_VARARGS flag, function documents
static PyMethodDef functions[] = {
  {"initHedge", initHedge, METH_VARARGS, initHedge_document},
  {"getHedgePosition", getHedgePosition, METH_VARARGS, getHedgePosition_document},
  {"getHedgeStationaryBeaconsPositions", getHedgeStationaryBeaconsPositions, METH_VARARGS, getHedgeStationaryBeaconsPositions_document},
  {"getHedgeRawDistances", getHedgeRawDistances, METH_VARARGS, getHedgeRawDistances_document},
  {"getHedgeRawIMU", getHedgeRawIMU, METH_VARARGS, getHedgeRawIMU_document},
  {"getHedgeFusionIMU", getHedgeFusionIMU, METH_VARARGS, getHedgeFusionIMU_document},
  {"getHedgeTelemetry", getHedgeTelemetry, METH_VARARGS, getHedgeTelemetry_document},
  {"getHedgeQuality", getHedgeQuality, METH_VARARGS, getHedgeQuality_document},
  {"stopHedge", stopHedge, METH_VARARGS, stopHedge_document},
  {NULL, NULL, 0, NULL}
};
// initializing our module informations and settings in this structure
static struct PyModuleDef marvelmind_module = {
  PyModuleDef_HEAD_INIT, // head informations for Python C API. It is needed to be first member in this struct !!
  "marvelmind_module",  // module name
  NULL, // Global documentation
  -1,   //Not supports sub-interpreters, because it has global state.
  functions
};

// runs while initializing and calls module creation function.
PyMODINIT_FUNC PyInit_marvelmind_module(void){
  return PyModule_Create(&marvelmind_module);
}

//////////////////////////////////////////////////////////////////////////////

