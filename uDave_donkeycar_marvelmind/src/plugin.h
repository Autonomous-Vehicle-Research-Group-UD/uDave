#pragma once
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include "marvelmind.h"
#define PY_SSIZE_T_CLEAN 
#include <Python.h>
static struct MarvelmindHedge* GLOBAL_HEDGE;
static bool isInit = false;

// Init
static PyObject *initHedge (PyObject *self, PyObject *args);

// Data providers
static PyObject *getHedgePosition (PyObject *self, PyObject *args);
static PyObject *getHedgeStationaryBeaconsPositions (PyObject *self, PyObject *args);
static PyObject *getHedgeRawDistances (PyObject *self, PyObject *args);
static PyObject *getHedgeRawIMU (PyObject *self, PyObject *args);
static PyObject *getHedgeFusionIMU (PyObject *self, PyObject *args);
static PyObject *getHedgeTelemetry (PyObject *self, PyObject *args);
static PyObject *getHedgeQuality (PyObject *self, PyObject *args);

// Exit
static PyObject *stopHedge(PyObject *self, PyObject *args);

PyMODINIT_FUNC PyInit_marvelmind_module(void);

