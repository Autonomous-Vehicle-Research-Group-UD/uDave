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

//Exceptions
static PyObject *HedgeCreationError = NULL;
static PyObject *NotInitialisedError = NULL;
static PyObject *HedgeTerminatedError = NULL;
static PyObject *ServiceDisabledError = NULL;

//////////////////////////////////////////////////////////////////////////////
// Init
static PyObject *initHedge (PyObject *self, PyObject *args)
{
    char *ttyFileName;
    int numOfAvgPos;
    int showVerbose;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, "sii", &ttyFileName, &numOfAvgPos, &showVerbose))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Set the Avg Pos variable.
    MAX_BUFFERED_POSITIONS = numOfAvgPos;
    
    //Create Hedge object
    GLOBAL_HEDGE = createMarvelmindHedge();
    
    //Return false if unsuccessfull
    if (GLOBAL_HEDGE==NULL)
    {
        PyErr_SetString(NotInitialisedError, "Unable to create Hedge object.");
        return (PyObject *) NULL;
    }
    
    //Set filelds if succesfull
    GLOBAL_HEDGE->ttyFileName=ttyFileName;
    GLOBAL_HEDGE->verbose=(showVerbose > 0); // show errors and warnings
    
    //Call
    startMarvelmindHedge(GLOBAL_HEDGE);
    
    //Set the initialised flag
    isInit = true;
    
    //Return if initialised
    return Py_BuildValue("b", 1);
    
}
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//Data returners

/* Documentations:
 * 	About how to raise and handle exceptions: https://docs.python.org/3/c-api/exceptions.html
 * 	Marvelmind communication interface : https://marvelmind.com/pics/marvelmind_interfaces.pdf alive in version 2021.06.04 as [2021.08.25]
 */

/* What to use for data-check:
 * 	Every non-gps data-type structure uses the updated field to check if it got data ONCE.
 * 	The gps data-type uses a ready and processed fields for being in a different state of data readiness.
 */

/* MARVELMINDHEDGE.terminationRequired is true IF:
 * 	ttyHandle is not an open port. (Connection error),
 * 	OVERLAPPED osReader event creation was unsuccesfull [#ifdef WIN32 only!] ,
 * 	not enought memory for data buffer, 
 * 	MARVELMINDHEDGE is stopped manually.
 */
 
 //TODO: Do we need initialization check every single time?

//Hedge position
static PyObject *getHedgePosition (PyObject *self, PyObject *args)
{
    struct PositionValue position;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        bool success = getPositionFromMarvelmindHedge(GLOBAL_HEDGE, &position);
        
        if(success){
            return Py_BuildValue("[iIiiidiii]", 
            	position.address, 
            	position.timestamp, 
            	position.x, 
            	position.y, 
            	position.z, 
            	position.angle, 
            	position.highResolution, 
            	position.ready, 
            	position.processed
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Hedge position data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
}

//Beacons positions
static PyObject *getHedgeStationaryBeaconsPositions (PyObject *self, PyObject *args)
{
    struct StationaryBeaconsPositions positions;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getStationaryBeaconsPositionsFromMarvelmindHedge (GLOBAL_HEDGE, &positions);
        
        if(positions.updated)
        {
            //Create a pylist in C
            int numOfBeacons = (positions.numBeacons > MAX_STATIONARY_BEACONS) ? MAX_STATIONARY_BEACONS : positions.numBeacons;
            PyObject *python_ret_val = PyList_New(1 + numOfBeacons);
            
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
            
            //Return the created list
            return python_ret_val;
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Beacon positions are unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
}

//Beacon-Hedge distances
static PyObject *getHedgeRawDistances (PyObject *self, PyObject *args)
{
    struct RawDistances rawdistances;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }

    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getRawDistancesFromMarvelmindHedge(GLOBAL_HEDGE, &rawdistances);
        
        if(rawdistances.updated){
            return Py_BuildValue("[b[bI][bI][bI][bI]IH]", 
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
                rawdistances.timeShift
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Raw distance data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
}

//Hedge IMU raw
static PyObject *getHedgeRawIMU (PyObject *self, PyObject *args)
{
    struct RawIMUValue rawIMU;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getRawIMUFromMarvelmindHedge(GLOBAL_HEDGE, &rawIMU);
        
        if(rawIMU.updated){
            return Py_BuildValue("[hhhhhhhhhI]", 
                rawIMU.acc_x, 
                rawIMU.acc_y, 
                rawIMU.acc_z, 
                rawIMU.gyro_x, 
                rawIMU.gyro_y, 
                rawIMU.gyro_z, 
                rawIMU.compass_x, 
                rawIMU.compass_y, 
                rawIMU.compass_z, 
                rawIMU.timestamp
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Raw IMU data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
}

//Hedge IMU position fused
static PyObject *getHedgeFusionIMU (PyObject *self, PyObject *args)
{
    struct FusionIMUValue fusionIMU;
    
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getFusionIMUFromMarvelmindHedge(GLOBAL_HEDGE, &fusionIMU);
        
        if(fusionIMU.updated){
            return Py_BuildValue("[iiihhhhhhhhhhI]", 
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
                fusionIMU.timestamp
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Fusion IMU data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
}

//Telemetry data
static PyObject *getHedgeTelemetry (PyObject *self, PyObject *args)
{
    struct TelemetryData telemetry;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }

    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getTelemetryFromMarvelmindHedge(GLOBAL_HEDGE, &telemetry);
        
        if(telemetry.updated){
            return Py_BuildValue("[Hi]", 
                telemetry.vbat_mv, 
                telemetry.rssi_dbm
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Telemetry data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
};

//Quality data
static PyObject *getHedgeQuality (PyObject *self, PyObject *args)
{
    struct QualityData quality;
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Return if not initialised
    if(!isInit)
    {
        PyErr_SetString(NotInitialisedError, "Module is not initialised.");
        return (PyObject *) NULL;
    }
    
    //Ask if a connection is alive
    if(!(GLOBAL_HEDGE->terminationRequired))
    {
        //Call
        getQualityFromMarvelmindHedge(GLOBAL_HEDGE, &quality);
        
        if(quality.updated){
            return Py_BuildValue("[BB]", 
            	quality.address, 
            	quality.quality_per
            );
        }
        
        //Data Unavailable Exception
        PyErr_SetString(ServiceDisabledError, "Quality data is unavailable.");
        return (PyObject *) NULL;
    }
    
    //Hedge already terminated
    PyErr_SetString(HedgeTerminatedError, "Unable to connect or not enought memory.");
    return (PyObject *) NULL;
};
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
// Exit
static PyObject *stopHedge(PyObject *self, PyObject *args){
    
    //Return if unsuccesfull call.
    if(!PyArg_ParseTuple(args, ""))
    {
        PyErr_BadArgument();
        return (PyObject *) NULL;
    }
    
    //Initialisation check
    if(isInit)
    {
        //Call
        stopMarvelmindHedge (GLOBAL_HEDGE);
        destroyMarvelmindHedge (GLOBAL_HEDGE);
        
        //Set the initialised flag
        isInit = false;
        
        return Py_BuildValue("i", 1);
    }
    
    PyErr_SetString(NotInitialisedError, "Module is not initialised.");
    return (PyObject *) NULL;
}
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//Py API
//Documentations
static char initHedge_document[] = "Starts the data provider service. The serial connecton will be established in the arg serial port with the hedge.\ninitHedge(devfile, num_of_averages)";
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
static struct PyModuleDef mm_module = {
    PyModuleDef_HEAD_INIT, // head informations for Python C API. It is needed to be first member in this struct !!
    "marvelmind_module",  // module name
    NULL, // Global documentation
    -1,   //Not supports sub-interpreters, because it has global state.
    functions
};

// runs while initializing and calls module creation function.
PyMODINIT_FUNC PyInit_mm_gps(void){
    
    //Create module
    PyObject *module = PyModule_Create(&mm_module);
    
    //Create exceptions
    HedgeCreationError = PyErr_NewException("mm_gps.HedgeCreationError", NULL, NULL);
    NotInitialisedError = PyErr_NewException("mm_gps.NotInitialisedError", NULL, NULL);
    HedgeTerminatedError = PyErr_NewException("mm_gps.HedgeTerminatedError", NULL, NULL);
    ServiceDisabledError = PyErr_NewException("mm_gps.ServiceDisabledError", NULL, NULL);
    
    //Add exception objects to module
    PyModule_AddObject(module, "HedgeCreationError", HedgeCreationError);
    PyModule_AddObject(module, "NotInitialisedError", NotInitialisedError);
    PyModule_AddObject(module, "HedgeTerminatedError", HedgeTerminatedError);
    PyModule_AddObject(module, "ServiceDisabledError", ServiceDisabledError);
    
    return module;
}

//////////////////////////////////////////////////////////////////////////////


