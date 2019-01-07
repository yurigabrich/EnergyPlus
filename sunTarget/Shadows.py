'''
Code adapted from C++ to Python, by Yuri Bastos Gabrich, in order to get some functions for
personal reasons. The copyrights is mandatory accordingly with the directives from the source
file, described below.

---------------------------------------------------------------------------------------------
// EnergyPlus, Copyright (c) 1996-2018, The Board of Trustees of the University of Illinois,
// The Regents of the University of California, through Lawrence Berkeley National Laboratory
// (subject to receipt of any required approvals from the U.S. Dept. of Energy), Oak Ridge
# national Laboratory, managed by UT-Battelle, Alliance for Sustainable Energy, LLC, and other
// contributors. All rights reserved.
//
// NOTICE: This Software was developed under funding from the U.S. Department of Energy and the
// U.S. Government consequently retains certain rights. As such, the U.S. Government has been
// granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable,
// worldwide license in the Software to reproduce, distribute copies to the public, prepare
// derivative works, and perform publicly and display publicly, and to permit others to do so.
//
// Redistribution and use in source and binary forms, with or without modification, are permitted
// provided that the following conditions are met:
//
// (1) Redistributions of source code must retain the above copyright notice, this list of
//     conditions and the following disclaimer.
//
// (2) Redistributions in binary form must reproduce the above copyright notice, this list of
//     conditions and the following disclaimer in the documentation and/or other materials
//     provided with the distribution.
//
// (3) Neither the name of the University of California, Lawrence Berkeley National Laboratory,
//     the University of Illinois, U.S. Dept. of Energy nor the names of its contributors may be
//     used to endorse or promote products derived from this software without specific prior
//     written permission.
//
// (4) Use of EnergyPlus(TM) Name. If Licensee (i) distributes the software in stand-alone form
//     without changes from the version obtained under this License, or (ii) Licensee makes a
//     reference solely to the software portion of its product, Licensee must refer to the
//     software as "EnergyPlus version X" software, where "X" is the version number Licensee
//     obtained under this License and may not use a different name for the software. Except as
//     specifically required in this Section (4), Licensee shall not use in a company name, a
//     product name, in advertising, publicity, or other promotional activities any name, trade
//     name, trademark, logo, or other designation of "EnergyPlus", "E+", "e+" or confusingly
//     similar designation, without the U.S. Department of Energy's prior written consent.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
// CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
// SERVICES LOSS OF USE, DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
'''

# The Python version considers only the functions related to surface objects.
# ------------------------------------------
# SURFACE = WALL, ROOF, floor, or a ceiling
# SUBSURFACE = window, door, or glassdoor
# A BACK SURFACE – an inside surface – is one that may be partially sunlit/receive solar transmission for interior solar distribution.
# ------------------------------------------


# C++ Headers
# include <cassert>		# defines one macro function that can be used as a standard debugging tool
# include <cmath>		# declares a set of functions to compute common mathematical operations and transformations. Python's module available by default as 'math.' or 'cmath.'
# include <memory>		# defines general utilities to manage dynamic memory

# ObjexxFCL Headers
include <ObjexxFCL/Array.functions.hh>
include <ObjexxFCL/Fmath.hh>
include <ObjexxFCL/Vector3.hh>
include <ObjexxFCL/gio.hh>
include <ObjexxFCL/member.functions.hh>
include <ObjexxFCL/string.functions.hh>

# EnergyPlus Headers
include <DataDaylighting.hh>
# include <DataEnvironment.hh>
include <DataErrorTracking.hh>
# include <DataGlobals.hh>
include <DataHeatBalFanSys.hh>
include <DataHeatBalance.hh>
include <DataIPShortCuts.hh>
# include <DataPrecisionGlobals.hh>
include <DataReportingFlags.hh>
include <DataShadowingCombinations.hh>
include <DataStringGlobals.hh>
include <DataSurfaces.hh>
include <DataSystemVariables.hh>
include <DataTimings.hh>
include <DataWindowEquivalentLayer.hh>
include <DaylightingManager.hh>
# include <General.hh>
include <InputProcessing/InputProcessor.hh> # REVIEW with CAUTION!
include <OutputProcessor.hh>
include <OutputReportPredefined.hh>
include <ScheduleManager.hh>
include <SolarReflectionManager.hh>
# include <SolarShading.hh>					# WHY THE HEADER OF THE CURRENT FILE MUST BE ADDED?
# include <UtilityRoutines.hh>
include <Vectors.hh>
include <WindowComplexManager.hh>
include <WindowEquivalentLayer.hh>
include <WindowManager.hh>

class ExternalFunctions:
	'''
	Definition of a variety of additional functions from another packages.
	Only those useful for the following computations was copied to here.
	'''

	# DataHeatBalance.cc
	Array1D<ZoneListData> ZoneList;

	# DataSurfaces.cc
	Array1D<SurfaceData> Surface;
	Array1D<SurfaceWindowCalc> SurfaceWindow;
	NumOfZoneLists = 0

	# DataSurfaces.hh
	SchedExternalShadingFrac = False  # True if the external shading is scheduled or calculated externally to be imported
    ExternalShadingSchInd = 0         # Schedule for a the external shading

    # DataSystemVariables.cc
    DisableGroupSelfShading = False   # when True, defined shadowing surfaces group is ignored when calculating sunlit fraction

	# DataI
	Array1D_string cAlphaFieldNames;
    Array1D_string cNumericFieldNames;
    Array1D_bool lNumericFieldBlanks;
    Array1D_bool lAlphaFieldBlanks;

	# using ScheduleManager::GetScheduleIndex
    def GetScheduleIndex():
        int GetScheduleIndex(std::string const &ScheduleName)
        {
    
            // FUNCTION INFORMATION:
            //       AUTHOR         Linda K. Lawrie
            //       DATE WRITTEN   September 1997
            //       MODIFIED       na
            //       RE-ENGINEERED  na
    
            // PURPOSE OF THIS FUNCTION:
            // This function returns the internal pointer to Schedule "ScheduleName".
    
            // Return value
            int GetScheduleIndex;
    
            // FUNCTION LOCAL VARIABLE DECLARATIONS:
            int DayCtr;
            int WeekCtr;
    
            if (!ScheduleInputProcessed) {
                ProcessScheduleInput();
                ScheduleInputProcessed = true;
            }
    
            if (NumSchedules > 0) {
                GetScheduleIndex = UtilityRoutines::FindItemInList(ScheduleName, Schedule({1, NumSchedules}));
                if (GetScheduleIndex > 0) {
                    if (!Schedule(GetScheduleIndex).Used) {
                        Schedule(GetScheduleIndex).Used = true;
                        for (WeekCtr = 1; WeekCtr <= 366; ++WeekCtr) {
                            if (Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr) > 0) {
                                WeekSchedule(Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr)).Used = true;
                                for (DayCtr = 1; DayCtr <= MaxDayTypes; ++DayCtr) {
                                    DaySchedule(WeekSchedule(Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr)).DaySchedulePointer(DayCtr)).Used =
                                        true;
                                }
                            }
                        }
                    }
                }
            } else {
                GetScheduleIndex = 0;
            }
    
            return GetScheduleIndex;
        }

    def getNumObjectsFound():
	    int InputProcessor::getNumObjectsFound(std::string const &ObjectWord)
		{

		    // FUNCTION INFORMATION:
		    //       AUTHOR         Linda K. Lawrie
		    //       DATE WRITTEN   September 1997
		    //       MODIFIED       Mark Adams
		    //       RE-ENGINEERED  na

		    // PURPOSE OF THIS SUBROUTINE:
		    // This function returns the number of objects (in input data file)
		    // found in the current run.  If it can't find the object in list
		    // of objects, a 0 will be returned.

		    // METHODOLOGY EMPLOYED:
		    // Look up object in list of objects.  If there, return the
		    // number of objects found in the current input.  If not, return 0.

		    auto const &find_obj = epJSON.find(ObjectWord);

		    if (find_obj == epJSON.end()) {
		        auto tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(ObjectWord));
		        if (tmp_umit == caseInsensitiveObjectMap.end() || epJSON.find(tmp_umit->second) == epJSON.end()) {
		            return 0;
		        }
		        return static_cast<int>(epJSON[tmp_umit->second].size());
		    } else {
		        return static_cast<int>(find_obj.value().size());
		    }

		    if (schema["properties"].find(ObjectWord) == schema["properties"].end()) {
		        auto tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(ObjectWord));
		        if (tmp_umit == caseInsensitiveObjectMap.end()) {
		            ShowWarningError("Requested Object not found in Definitions: " + ObjectWord);
		        }
		    }
		    return 0;
		}

	def getObjectItem():
		void InputProcessor::getObjectItem(std::string const &Object,
                                   int const Number,
                                   Array1S_string Alphas,
                                   int &NumAlphas,
                                   Array1S<Real64> Numbers,
                                   int &NumNumbers,
                                   int &Status,
                                   Optional<Array1D_bool> NumBlank,
                                   Optional<Array1D_bool> AlphaBlank,
                                   Optional<Array1D_string> AlphaFieldNames,
                                   Optional<Array1D_string> NumericFieldNames)
		{
		    // SUBROUTINE INFORMATION:
		    //       AUTHOR         Linda K. Lawrie
		    //       DATE WRITTEN   September 1997
		    //       MODIFIED       na
		    //       RE-ENGINEERED  na

		    // PURPOSE OF THIS SUBROUTINE:
		    // This subroutine gets the 'number' 'object' from the IDFRecord data structure.

		    int adjustedNumber = getJSONObjNum(Object, Number); // if incoming input is idf, then use idf object order

		    auto objectInfo = ObjectInfo();
		    objectInfo.objectType = Object;
		    // auto sorted_iterators = find_iterators;

		    auto find_iterators = objectCacheMap.find(Object);
		    if (find_iterators == objectCacheMap.end()) {
		        auto const tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(Object));
		        if (tmp_umit == caseInsensitiveObjectMap.end() || epJSON.find(tmp_umit->second) == epJSON.end()) {
		            return;
		        }
		        objectInfo.objectType = tmp_umit->second;
		        find_iterators = objectCacheMap.find(objectInfo.objectType);
		    }

		    NumAlphas = 0;
		    NumNumbers = 0;
		    Status = -1;
		    auto const &is_AlphaBlank = present(AlphaBlank);
		    auto const &is_AlphaFieldNames = present(AlphaFieldNames);
		    auto const &is_NumBlank = present(NumBlank);
		    auto const &is_NumericFieldNames = present(NumericFieldNames);

		    auto const &epJSON_it = find_iterators->second.inputObjectIterators.at(adjustedNumber - 1);
		    auto const &epJSON_schema_it = find_iterators->second.schemaIterator;
		    auto const &epJSON_schema_it_val = epJSON_schema_it.value();

		    // Locations in JSON schema relating to normal fields
		    auto const &schema_obj_props = epJSON_schema_it_val["patternProperties"][".*"]["properties"];

		    // Locations in JSON schema storing the positional aspects from the IDD format, legacy prefixed
		    auto const &legacy_idd = epJSON_schema_it_val["legacy_idd"];
		    auto const &legacy_idd_field_info = legacy_idd["field_info"];
		    auto const &legacy_idd_fields = legacy_idd["fields"];
		    auto const &schema_name_field = epJSON_schema_it_val.find("name");

		    auto key = legacy_idd.find("extension");
		    std::string extension_key;
		    if (key != legacy_idd.end()) {
		        extension_key = key.value();
		    }

		    Alphas = "";
		    Numbers = 0;
		    if (is_NumBlank) {
		        NumBlank() = true;
		    }
		    if (is_AlphaBlank) {
		        AlphaBlank() = true;
		    }
		    if (is_AlphaFieldNames) {
		        AlphaFieldNames() = "";
		    }
		    if (is_NumericFieldNames) {
		        NumericFieldNames() = "";
		    }

		    auto const &obj = epJSON_it;
		    auto const &obj_val = obj.value();

		    objectInfo.objectName = obj.key();

		    auto const find_unused = unusedInputs.find(objectInfo);
		    if (find_unused != unusedInputs.end()) {
		        unusedInputs.erase(find_unused);
		    }

		    size_t idf_max_fields = 0;
		    auto found_idf_max_fields = obj_val.find("idf_max_fields");
		    if (found_idf_max_fields != obj_val.end()) {
		        idf_max_fields = *found_idf_max_fields;
		    }

		    size_t idf_max_extensible_fields = 0;
		    auto found_idf_max_extensible_fields = obj_val.find("idf_max_extensible_fields");
		    if (found_idf_max_extensible_fields != obj_val.end()) {
		        idf_max_extensible_fields = *found_idf_max_extensible_fields;
		    }

		    int alpha_index = 1;
		    int numeric_index = 1;

		    for (size_t i = 0; i < legacy_idd_fields.size(); ++i) {
		        std::string const &field = legacy_idd_fields[i];
		        auto const &field_info = legacy_idd_field_info.find(field);
		        if (field_info == legacy_idd_field_info.end()) {
		            ShowFatalError("Could not find field = \"" + field + "\" in \"" + Object + "\" in epJSON Schema.");
		        }
		        auto const &field_type = field_info.value().at("field_type").get<std::string>();
		        bool within_idf_fields = (i < idf_max_fields);
		        if (field == "name" && schema_name_field != epJSON_schema_it_val.end()) {
		            auto const &name_iter = schema_name_field.value();
		            if (name_iter.find("retaincase") != name_iter.end()) {
		                Alphas(alpha_index) = objectInfo.objectName;
		            } else {
		                Alphas(alpha_index) = UtilityRoutines::MakeUPPERCase(objectInfo.objectName);
		            }
		            if (is_AlphaBlank) AlphaBlank()(alpha_index) = objectInfo.objectName.empty();
		            if (is_AlphaFieldNames) {
		                AlphaFieldNames()(alpha_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();
		            }
		            NumAlphas++;
		            alpha_index++;
		            continue;
		        }

		        auto const &schema_field_obj = schema_obj_props[field];
		        auto it = obj_val.find(field);
		        if (it != obj_val.end()) {
		            auto const &field_value = it.value();
		            if (field_type == "a") {
		                // process alpha value
		                if (field_value.is_string()) {
		                    auto const value = getObjectItemValue(field_value.get<std::string>(), schema_field_obj);

		                    Alphas(alpha_index) = value.first;
		                    if (is_AlphaBlank) AlphaBlank()(alpha_index) = value.second;

		                } else {
		                    if (field_value.is_number_integer()) {
		                        i64toa(field_value.get<std::int64_t>(), s);
		                    } else {
		                        dtoa(field_value.get<double>(), s);
		                    }
		                    Alphas(alpha_index) = s;
		                    if (is_AlphaBlank) AlphaBlank()(alpha_index) = false;
		                }
		            } else if (field_type == "n") {
		                // process numeric value
		                if (field_value.is_number()) {
		                    if (field_value.is_number_integer()) {
		                        Numbers(numeric_index) = field_value.get<std::int64_t>();
		                    } else {
		                        Numbers(numeric_index) = field_value.get<double>();
		                    }
		                    if (is_NumBlank) NumBlank()(numeric_index) = false;
		                } else {
		                    bool is_empty = field_value.get<std::string>().empty();
		                    if (is_empty) {
		                        findDefault(Numbers(numeric_index), schema_field_obj);
		                    } else {
		                        Numbers(numeric_index) = -99999; // autosize and autocalculate
		                    }
		                    if (is_NumBlank) NumBlank()(numeric_index) = is_empty;
		                }
		            }
		        } else {
		            if (field_type == "a") {
		                if (!(within_idf_fields && findDefault(Alphas(alpha_index), schema_field_obj))) {
		                    Alphas(alpha_index) = "";
		                }
		                if (is_AlphaBlank) AlphaBlank()(alpha_index) = true;
		            } else if (field_type == "n") {
		                if (within_idf_fields) {
		                    findDefault(Numbers(numeric_index), schema_field_obj);
		                } else {
		                    Numbers(numeric_index) = 0;
		                }
		                if (is_NumBlank) NumBlank()(numeric_index) = true;
		            }
		        }
		        if (field_type == "a") {
		            if (within_idf_fields) NumAlphas++;
		            if (is_AlphaFieldNames) {
		                AlphaFieldNames()(alpha_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();
		            }
		            alpha_index++;
		        } else if (field_type == "n") {
		            if (within_idf_fields) NumNumbers++;
		            if (is_NumericFieldNames) {
		                NumericFieldNames()(numeric_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();
		            }
		            numeric_index++;
		        }
		    }

		    size_t extensible_count = 0;
		    auto const &legacy_idd_extensibles_iter = legacy_idd.find("extensibles");
		    if (legacy_idd_extensibles_iter != legacy_idd.end()) {
		        auto const epJSON_extensions_array_itr = obj.value().find(extension_key);
		        if (epJSON_extensions_array_itr != obj.value().end()) {
		            auto const &legacy_idd_extensibles = legacy_idd_extensibles_iter.value();
		            auto const &epJSON_extensions_array = epJSON_extensions_array_itr.value();
		            auto const &schema_extension_fields = schema_obj_props[extension_key]["items"]["properties"];

		            for (auto it = epJSON_extensions_array.begin(); it != epJSON_extensions_array.end(); ++it) {
		                auto const &epJSON_extension_obj = it.value();

		                for (size_t i = 0; i < legacy_idd_extensibles.size(); i++, extensible_count++) {
		                    std::string const &field_name = legacy_idd_extensibles[i];
		                    auto const &epJSON_obj_field_iter = epJSON_extension_obj.find(field_name);
		                    auto const &schema_field = schema_extension_fields[field_name];

		                    auto const &field_info = legacy_idd_field_info.find(field_name);
		                    if (field_info == legacy_idd_field_info.end()) {
		                        ShowFatalError("Could not find field = \"" + field_name + "\" in \"" + Object + "\" in epJSON Schema.");
		                    }
		                    auto const &field_type = field_info.value().at("field_type").get<std::string>();
		                    bool within_idf_extensible_fields = (extensible_count < idf_max_extensible_fields);

		                    if (epJSON_obj_field_iter != epJSON_extension_obj.end()) {
		                        auto const &field_value = epJSON_obj_field_iter.value();

		                        if (field_type == "a") {
		                            if (field_value.is_string()) {
		                                auto const value = getObjectItemValue(field_value.get<std::string>(), schema_field);

		                                Alphas(alpha_index) = value.first;
		                                if (is_AlphaBlank) AlphaBlank()(alpha_index) = value.second;
		                            } else {
		                                if (field_value.is_number_integer()) {
		                                    i64toa(field_value.get<std::int64_t>(), s);
		                                } else {
		                                    dtoa(field_value.get<double>(), s);
		                                }
		                                Alphas(alpha_index) = s;
		                                if (is_AlphaBlank) AlphaBlank()(alpha_index) = false;
		                            }
		                        } else if (field_type == "n") {
		                            if (field_value.is_number()) {
		                                if (field_value.is_number_integer()) {
		                                    Numbers(numeric_index) = field_value.get<std::int64_t>();
		                                } else {
		                                    Numbers(numeric_index) = field_value.get<double>();
		                                }
		                                if (is_NumBlank) NumBlank()(numeric_index) = false;
		                            } else {
		                                bool is_empty = field_value.get<std::string>().empty();
		                                if (is_empty) {
		                                    findDefault(Numbers(numeric_index), schema_field);
		                                } else {
		                                    Numbers(numeric_index) = -99999; // autosize and autocalculate
		                                }
		                                if (is_NumBlank) NumBlank()(numeric_index) = is_empty;
		                            }
		                        }
		                    } else {

		                        if (field_type == "a") {
		                            if (!(within_idf_extensible_fields && findDefault(Alphas(alpha_index), schema_field))) {
		                                Alphas(alpha_index) = "";
		                            }
		                            if (is_AlphaBlank) AlphaBlank()(alpha_index) = true;
		                        } else if (field_type == "n") {
		                            if (within_idf_extensible_fields) {
		                                findDefault(Numbers(numeric_index), schema_field);
		                            } else {
		                                Numbers(numeric_index) = 0;
		                            }
		                            if (is_NumBlank) NumBlank()(numeric_index) = true;
		                        }
		                    }

		                    if (field_type == "a") {
		                        if (within_idf_extensible_fields) NumAlphas++;
		                        if (is_AlphaFieldNames) {
		                            AlphaFieldNames()(alpha_index) =
		                                (DataGlobals::isEpJSON) ? field_name : field_info.value().at("field_name").get<std::string>();
		                        }
		                        alpha_index++;
		                    } else if (field_type == "n") {
		                        if (within_idf_extensible_fields) NumNumbers++;
		                        if (is_NumericFieldNames) {
		                            NumericFieldNames()(numeric_index) =
		                                (DataGlobals::isEpJSON) ? field_name : field_info.value().at("field_name").get<std::string>();
		                        }
		                        numeric_index++;
		                    }
		                }
		            }
		        }
		    }

		    Status = 1;
		}

	


	return None

class SolarShading(ExternalFunctions):
	'''
    // MODULE INFORMATION:
    //       AUTHOR         Rick Strand
    //       DATE WRITTEN   March 1997
    //       MODIFIED       December 1998, FCW
    //       MODIFIED       July 1999, Linda Lawrie, eliminate shadefl.scr,
    //                      do shadowing calculations during simulation
    //       MODIFIED       June 2001, FCW, handle window blinds
    //       MODIFIED       May 2004, LKL, Polygons > 4 sides (not subsurfaces)
    //       MODIFIED       January 2007, LKL, Taking parameters back to original integer (HC)
    //       MODIFIED       August 2011, JHK, Including Complex Fenestration optical calculations
    //       MODIFIED       November 2012, BG, Timestep solar and daylighting calculations
    //       RE-ENGINEERED  na

    // PURPOSE OF THIS MODULE:
    // The purpose of this module is to encompass the routines and data
    // which are need to perform the solar calculations in EnergyPlus.
    // This also requires that shading and geometry routines and data
    // which are used by the solar calculations be included in this module.

    // METHODOLOGY EMPLOYED:
    // Many of the methods used in this module have been carried over from the
    // (I)BLAST program.  As such, there is not much documentation on the
    // methodology used.  The original code was written mainly by George
    // Walton and requires coordinate transformations.  It calculates
    // shading using an overlapping polygon approach.

    // REFERENCES:
    // TARP Manual, NIST Publication.
    // Passive Solar Extension of the BLAST Program, CERL/UIUC Publication.

    // OTHER NOTES:
    # na
	'''

	def __init__(self):
		'''
		Define the variables to be used throughout the routine.

		SHOULD specify all the input data too!
		'''
	    # Using/Aliasing
	    using namespace DataPrecisionGlobals
	   # using namespace DataGlobals
	    NumOfTimeStepInHour = 0                 # Number of time steps in each hour of the simulation
        NumOfZones = 0                          # Total number of Zones for simulation
	   # using namespace DataEnvironment
	    IgnoreSolarRadiation = False            # TRUE if all solar radiation is to be ignored
	   # using namespace DataHeatBalance
	    SolarDistribution = 0                   # Solar Distribution Algorithm
	    MinimalShadowing = -1                   # all incoming solar hits floor, no exterior shadowing except reveals
	    MaxSolidWinLayers = 0                   # Maximum number of solid layers in a window construction
	                                            # ** has to be big enough to hold no matter what window model
	                                            #    each window model should validate layers individually
	   # using namespace DataSurfaces
	    ShadingTransmittanceVaries = False      # overall, shading transmittance varies for the building
	    TotSurfaces = 0                         # Total number of surfaces (walls, floors, roofs, windows,
	                                            # shading surfaces, etc.--everything)
	    MaxVerticesPerSurface = 4               # Maximum number of vertices allowed for a single surface
	                                            # (default -- can go higher)
	    ExternalEnvironment = 0                 # Parameters to indicate exterior boundary conditions for use with
	    OtherSideCondModeledExt = -4            # the Surface derived type.
	                                            # Note:  Positive values correspond to an interzone adjacent surface
	   # using DataBSDFWindow::MaxBkSurf
	    MaxBkSurf = 20                          # was 20    Maximum number of back surfaces in solar overlap &
	                                            # interior solar distribution
	    using namespace DataVectorTypes
	    using namespace FenestrationCommon
	    using namespace SingleLayerOptics

	    # Data
	    # MODULE PARAMETER DEFINITIONS:
	    # General Parameters...
	    SmallIncrement = 1.0e-10 # Small increment added for shading/sunlit area calculations.
	    HCMULT = 100000.0        # Multiplier used to change meters to .01 millimeters for homogeneous coordinates.
	    
	    # Homogeneous Coordinates are represented in integers (64 bit). This changes the surface coordinates from meters
	    # to .01 millimeters -- making that the resolution for shadowing, polygon clipping, etc.
	    sqHCMULT = (HCMULT * HCMULT)			# Square of HCMult used in Homogeneous coordinates
	    sqHCMULT_fac = 0.5 / sqHCMULT			# ( 0.5 / sqHCMULT ) factor --> half of inverse square of HCMult used in Homogeneous coordinates
	    # kHCMULT= 1.0 / (HCMULT * HCMULT)		# not used below

	    # Parameters for use with the variable OverlapStatus...
	    NoOverlap = 1
	    FirstSurfWithinSecond = 2
	    SecondSurfWithinFirst = 3
	    PartialOverlap = 4
	    TooManyVertices = 5
	    TooManyFigures = 6
	    cOverLapStatus = ["No-Overlap", "1st-Surf-within-2nd", "2nd-Surf-within-1st", "Partial-Overlap", "Too-Many-Vertices", "Too-Many-Figures"]

	    # MODULE VARIABLE DECLARATIONS:
	    MaxHCV = 15					# Maximum number of HC vertices
	    							# (needs to be based on maxnumvertices)
	    MaxHCS = 15000				# 200! Maximum number of HC surfaces (was 56)
	    							# Following are initially set in AllocateModuleArrays
	    MAXHCArrayBounds = 0    	# Bounds based on Max Number of Vertices in surfaces
	    MAXHCArrayIncrement = 0 	# Increment based on Max Number of Vertices in surfaces
	    
	    # The following variable should be re-engineered to lower in module hierarchy but need more analysis
	    NVS = 0 					# Number of vertices of the shadow/clipped surface
	    NumVertInShadowOrClippedSurface = 0
	    CurrentSurfaceBeingShadowed = 0
	    CurrentShadowingSurface = 0
	    OverlapStatus = 0			# Results of overlap calculation:
	    							# 1=No overlap
	    							# 2=NS1 completely within NS2
									# 3=NS2 completely within NS1
									# 4=Partial overlap

	    CTHETA = []        			# Cosine of angle of incidence of sun's rays on surface NS
	    FBKSHC = 0                  # HC location of first back surface
	    FGSSHC = 0                  # HC location of first general shadowing surface
	    FINSHC = 0                  # HC location of first back surface overlap
	    FRVLHC = 0                  # HC location of first reveal surface
	    FSBSHC = 0                  # HC location of first subsurface
	    LOCHCA = 0		            # Location of highest data in the HC arrays
	    NBKSHC = 0                  # Number of back surfaces in the HC arrays
	    NGSSHC = 0                  # Number of general shadowing surfaces in the HC arrays
	    NINSHC = 0                  # Number of back surface overlaps in the HC arrays
	    NRVLHC = 0                  # Number of reveal surfaces in HC array
	    NSBSHC = 0                  # Number of subsurfaces in the HC arrays
	    bool CalcSkyDifShading      # True when sky diffuse solar shading is
	    ShadowingCalcFrequency = 0	# Frequency for Shadowing Calculations
	    ShadowingDaysLeft = 0		# Days left in current shadowing period
	    debugging = False
	    namespace {
	        # These were static variables within different functions. They were pulled out into the namespace
	        # to facilitate easier unit testing of those functions.
	        # These are purposefully not in the header file as an extern variable. No one outside of this should
	        # use these. They are cleared by clear_state() for use by unit tests, but normal simulations should be unaffected.
	        # This is purposefully in an anonymous namespace so nothing outside this implementation file can use it.
	        MustAllocSolarShading = True
	        GetInputFlag = True
	        firstTime = True
	    }

	    std::ofstream shd_stream # Shading file stream
	    HCNS = []         			# Surface number of back surface HC figures
	    HCNV = []         			# Number of vertices of each HC figure
	    HCA = [[]]     				# 'A' homogeneous coordinates of sides
	    HCB = [[]]     				# 'B' homogeneous coordinates of sides
	    HCC = [[]]      			# 'C' homogeneous coordinates of sides
	    HCX = [[]]      			# 'X' homogeneous coordinates of vertices of figure.
	    HCY = [[]]      			# 'Y' homogeneous coordinates of vertices of figure.
	    WindowRevealStatus = [[[]]]
	    HCAREA = []					# Area of each HC figure.  Sign Convention:  Base Surface
							    	# - Positive, Shadow - Negative, Overlap between two shadows
							    	# - positive, etc., so that sum of HC areas=base sunlit area
	    HCT = []   	 				# Transmittance of each HC figure
	    ISABSF = []  				# For simple interior solar distribution (in which all beam
									# radiation entering zone is assumed to strike the floor),
	    							# fraction of beam radiation absorbed by each floor surface
	    SAREA = []  				# Sunlit area of heat transfer surface HTS
	    
	    # Excludes multiplier for windows
	    # Shadowing combinations data structure...See ShadowingCombinations type
	    NumTooManyFigures = 0
	    NumTooManyVertices = 0
	    NumBaseSubSurround = 0
	    SUNCOS = [3] 				# Direction cosines of solar position
	    XShadowProjection = 0.0 	# X projection of a shadow (formerly called C)
	    YShadowProjection = 0.0 	# Y projection of a shadow (formerly called S)
	    XTEMP = []    				# Temporary 'X' values for HC vertices of the overlap
	    XVC = []      				# X-vertices of the clipped figure
	    XVS = []      				# X-vertices of the shadow
	    YTEMP = []    				# Temporary 'Y' values for HC vertices of the overlap
	    YVC = []      				# Y-vertices of the clipped figure
	    YVS = []      				# Y-vertices of the shadow
	    ZVC = []      				# Z-vertices of the clipped figure
	    
	    # Used in Sutherland Hodman poly clipping
	    ATEMP = []					# Temporary 'A' values for HC vertices of the overlap
	    BTEMP = [] 					# Temporary 'B' values for HC vertices of the overlap
	    CTEMP = [] 					# Temporary 'C' values for HC vertices of the overlap
	    XTEMP1 = []					# Temporary 'X' values for HC vertices of the overlap
	    YTEMP1 = []					# Temporary 'Y' values for HC vertices of the overlap
	    maxNumberOfFigures = 0

	    NPhi = 6                    # Number of altitude angle steps for sky integration
	    NTheta = 24                 # Number of azimuth angle steps for sky integration
	    Eps = 1.e-10				# Small number
	    DPhi = PiOvr2 / NPhi       	# Altitude step size
	    DTheta = 2.0 * Pi / NTheta 	# Azimuth step size
	    DThetaDPhi = DTheta * DPhi 	# Product of DTheta and DPhi
	    PhiMin = 0.5 * DPhi        	# Minimum altitude

	    sin_Phi = []
	    cos_Phi = []
	    sin_Theta = []
	    cos_Theta = []

	    # SUBROUTINE SPECIFICATIONS FOR MODULE SolarShading

	    # Object Data ------------->  Que porra é essa?!
	    Array1D<SurfaceErrorTracking> TrackTooManyFigures
	    Array1D<SurfaceErrorTracking> TrackTooManyVertices
	    Array1D<SurfaceErrorTracking> TrackBaseSubSurround

	    static gio::Fmt fmtLD("*")

    #--------------------
    # MODULE SUBROUTINES:
	#--------------------

    # Functions
    def clear_state():
    	'''
		Reset some initial variables to the values defined when the 'class' was initialized.
    	'''
        MaxHCV = 15
        MaxHCS = 1500
        MAXHCArrayBounds = 0
        MAXHCArrayIncrement = 0
        NVS = 0
        NumVertInShadowOrClippedSurface = 0
        CurrentSurfaceBeingShadowed = 0
        CurrentShadowingSurface = 0
        OverlapStatus = 0
        CTHETA.deallocate() # ---------------> ??????????
        FBKSHC = 0
        FGSSHC = 0
        FINSHC = 0
        FRVLHC = 0
        FSBSHC = 0
        LOCHCA = 0
        NBKSHC = 0
        NGSSHC = 0
        NINSHC = 0
        NRVLHC = 0
        NSBSHC = 0
        CalcSkyDifShading = False
        ShadowingCalcFrequency = 0 # Frequency for Shadowing Calculations
        ShadowingDaysLeft = 0      # Days left in current shadowing period
        debugging = False
        MustAllocSolarShading = True
        GetInputFlag = True
        firstTime = True
        HCNS.deallocate()
        HCNV.deallocate()
        HCA.deallocate()
        HCB.deallocate()
        HCC.deallocate()
        HCX.deallocate()
        HCY.deallocate()
        WindowRevealStatus.deallocate()
        HCAREA.deallocate()
        HCT.deallocate()
        ISABSF.deallocate()
        SAREA.deallocate()
        NumTooManyFigures = 0
        NumTooManyVertices = 0
        NumBaseSubSurround = 0
        XShadowProjection = 0.0
        YShadowProjection = 0.0
        XTEMP.deallocate()
        XVC.deallocate()
        XVS.deallocate()
        YTEMP.deallocate()
        YVC.deallocate()
        YVS.deallocate()
        ZVC.deallocate()
        ATEMP.deallocate()
        BTEMP.deallocate()
        CTEMP.deallocate()
        XTEMP1.deallocate()
        YTEMP1.deallocate()
        maxNumberOfFigures = 0
        TrackTooManyFigures.deallocate()
        TrackTooManyVertices.deallocate()
        TrackBaseSubSurround.deallocate()
        DBZoneIntWin.deallocate()
        ISABSF.deallocate()
    	
    	return None

# end of SolarShading


class SolarCalculations(SolarShading):
	
	def __init__(self):
		'''
	    SUBROUTINE INFORMATION:
	          AUTHOR         George Walton
	          DATE WRITTEN   September 1977
	          MODIFIED       na
	          RE-ENGINEERED  Mar97, RKS, Initial EnergyPlus Version

	    PURPOSE OF THIS SUBROUTINE:
	    This routine controls the computation of the solar flux multipliers.

	    METHODOLOGY EMPLOYED:
	    All shadowing calculations have been grouped under this routine to
	    allow segmentation separating it from the hourly loads calculation.

	    REFERENCES:
	    na
	    '''

	    # FLOW:
		#ifdef EP_Count_Calls # COMO FAZER ESTA MERDA EM PYTHON? --> Conditional inclusions: http://www.cplusplus.com/doc/tutorial/preprocessor/
	    ++NumInitSolar_Calls
		#endif

	    if (BeginSimFlag): # onde essa variável foi declarada?
	        try:
	        	shd_stream.open(DataStringGlobals::outputShdFileName) # --> "eplusout.shd" Pq preciso abrir este arquivo?
	    															  # Será que é o arquivo que salvará os resultados?
	        except OSError:
	            print("SolarCalculations: Could not open file {} for output (write).".format(DataStringGlobals::outputShdFileName))
	        else: # 'else' do 'except'? Não deveria estar junto ao 'try'?!
	            if (GetInputFlag):
	                GetShadowingInput()	# internal function
	                GetInputFlag = False
	                MaxHCV = (((max(15, MaxVerticesPerSurface) + 16) / 16) * 16) - 1 # Assure MaxHCV+1 is multiple of 16 for 128 B alignment
	                assert((MaxHCV + 1) % 16 == 0)

	            if (firstTime): print("Allocate Solar Module Arrays")
	            AllocateModuleArrays()	# internal function

	            # if (SolarDistribution != FullInteriorExterior):
	            #     if (firstTime): print("Computing Interior Solar Absorption Factors")
	            #     ComputeIntSolarAbsorpFactors()

	            if (firstTime): print("Determining Shadowing Combinations")
	            DetermineShadowingCombinations()	# internal function
	            shd_stream.close() # Done writing to shd file

	        if (CalcSolRefl): print("Initializing Solar Reflection Factors")
	        InitSolReflRecSurf()	# função não encontrada neste doc

	        if (firstTime): print("Proceeding with Initializing Solar Calculations")

	    if (BeginEnvrnFlag): # onde essa variável foi declarada?
	        CTHETA = 0.0
	        SAREA = 0.0
	        SurfSunlitArea = 0.0
	        SurfSunlitFrac = 0.0
	        SunlitFracHR = 0.0
	        SunlitFrac = 0.0
	        SunlitFracWithoutReveal = 0.0
	        BackSurfaces = 0
	        OverlapAreas = 0.0
	        CosIncAngHR = 0.0
	        CosIncAng = 0.0
	        AnisoSkyMult = 1.0 			# For isotropic sky recalculated in AnisoSkyViewFactors if anisotropic radiance
	        MultIsoSky = 0.0
	        MultCircumSolar = 0.0
	        MultHorizonZenith = 0.0
	        WinTransSolar = 0.0
	        WinBmSolar = 0.0
	        WinBmBmSolar = 0.0
	        WinBmDifSolar = 0.0

	        WinDifSolar = 0.0
	        WinDirSolTransAtIncAngle = 0.0
	        WinHeatGain = 0.0
	        WinHeatTransfer = 0.0
	        WinHeatGainRep = 0.0
	        WinHeatLossRep = 0.0
	        WinGainConvGlazToZoneRep = 0.0
	        WinGainIRGlazToZoneRep = 0.0
	        WinLossSWZoneToOutWinRep = 0.0
	        WinGainFrameDividerToZoneRep = 0.0
	        WinGainConvGlazShadGapToZoneRep = 0.0
	        WinGainConvShadeToZoneRep = 0.0
	        OtherConvGainInsideFaceToZoneRep = 0.0
	        WinGainIRShadeToZoneRep = 0.0
	        WinGapConvHtFlowRep = 0.0
	        WinShadingAbsorbedSolar = 0.0
	        WinSysSolTransmittance = 0.0
	        WinSysSolReflectance = 0.0
	        WinSysSolAbsorptance = 0.0
	        InsideGlassCondensationFlag = 0
	        InsideFrameCondensationFlag = 0
	        InsideDividerCondensationFlag = 0
	        ZoneTransSolar = 0.0
	        ZoneBmSolFrExtWinsRep = 0.0
	        ZoneBmSolFrIntWinsRep = 0.0
	        InitialZoneDifSolReflW = 0.0
	        ZoneDifSolFrExtWinsRep = 0.0
	        ZoneDifSolFrIntWinsRep = 0.0
	        ZoneWinHeatGain = 0.0
	        ZoneWinHeatGainRep = 0.0
	        ZoneWinHeatLossRep = 0.0
	        ZoneOpaqSurfInsFaceCond = 0.0
	        ZoneOpaqSurfInsFaceCondGainRep = 0.0
	        ZoneOpaqSurfInsFaceCondLossRep = 0.0
	        QRadSWOutIncident = 0.0
	        QRadSWOutIncidentBeam = 0.0
	        BmIncInsSurfIntensRep = 0.0
	        BmIncInsSurfAmountRep = 0.0
	        IntBmIncInsSurfIntensRep = 0.0
	        IntBmIncInsSurfAmountRep = 0.0
	        QRadSWOutIncidentSkyDiffuse = 0.0
	        QRadSWOutIncidentGndDiffuse = 0.0
	        QRadSWOutIncBmToDiffReflGnd = 0.0
	        QRadSWOutIncSkyDiffReflGnd = 0.0
	        QRadSWOutIncBmToBmReflObs = 0.0
	        QRadSWOutIncBmToDiffReflObs = 0.0
	        QRadSWOutIncSkyDiffReflObs = 0.0
	        CosIncidenceAngle = 0.0
	        QRadSWwinAbsTot = 0.0
	        SWwinAbsTotalReport = 0.0
	        InitialDifSolInAbsReport = 0.0
	        InitialDifSolInTransReport = 0.0
	        SWInAbsTotalReport = 0.0
	        WindowRevealStatus = 0
	        
	        # energy
	        WinTransSolarEnergy = 0.0
	        WinBmSolarEnergy = 0.0
	        WinBmBmSolarEnergy = 0.0
	        WinBmDifSolarEnergy = 0.0

	        WinDifSolarEnergy = 0.0
	        WinHeatGainRepEnergy = 0.0
	        WinHeatLossRepEnergy = 0.0
	        WinGapConvHtFlowRepEnergy = 0.0
	        WinHeatTransferRepEnergy = 0.0
	        WinShadingAbsorbedSolarEnergy = 0.0
	        ZoneTransSolarEnergy = 0.0
	        ZoneBmSolFrExtWinsRepEnergy = 0.0
	        ZoneBmSolFrIntWinsRepEnergy = 0.0
	        ZoneDifSolFrExtWinsRepEnergy = 0.0
	        ZoneDifSolFrIntWinsRepEnergy = 0.0
	        ZoneWinHeatGainRepEnergy = 0.0
	        ZoneWinHeatLossRepEnergy = 0.0
	        ZnOpqSurfInsFaceCondGnRepEnrg = 0.0
	        ZnOpqSurfInsFaceCondLsRepEnrg = 0.0
	        BmIncInsSurfAmountRepEnergy = 0.0
	        IntBmIncInsSurfAmountRepEnergy = 0.0
	        QRadSWwinAbsTotEnergy = 0.0

	    # Initialize these once
	    for IPhi in range(1, NPhi+1):
	    	# Loop over patch altitude values
	        Phi = PhiMin + (IPhi - 1) * DPhi 		# 7.5,22.5,37.5,52.5,67.5,82.5 for NPhi = 6
	        sin_Phi.append(np.sin(Phi))
	        cos_Phi.append(np.cos(Phi))

	    for ITheta in range(1, NTheta+1):
	    	# Loop over patch azimuth values
	        Theta = (ITheta - 1) * DTheta 			# 0,15,30,....,330,345 for NTheta = 24
	        sin_Theta.append(np.sin(Theta))
	        cos_Theta.append(np.cos(Theta))

	    firstTime = False
	    
	    return None

    
    def GetShadowingInput():
		'''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda K. Lawrie
              DATE WRITTEN   July 1999
              MODIFIED       B. Griffith, Nov 2012, add calculation method
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine gets the Shadowing Calculation object.
		'''
        # Using/Aliasing
        using General::RoundSigDigits
        using namespace DataIPShortCuts
        using DataSystemVariables::DetailedSkyDiffuseAlgorithm
        using DataSystemVariables::DetailedSolarTimestepIntegration
        using DataSystemVariables::DisableAllSelfShading
        using DataSystemVariables::DisableGroupSelfShading
        using DataSystemVariables::ReportExtShadingSunlitFrac
        using DataSystemVariables::SutherlandHodgman
        using DataSystemVariables::UseImportedSunlitFrac
        using DataSystemVariables::UseScheduledSunlitFrac
        # using ScheduleManager::ScheduleFileShadingProcessed
        ScheduleFileShadingProcessed = False

        # SUBROUTINE PARAMETER DEFINITIONS:
        static gio::Fmt fmtA("(A)")

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        NumItems = 0
        NumNumbers = 0
        NumAlphas = 0
        IOStat = 0
        Found = 0

        rNumericArgs({1, 4}) = 0.0 # so if nothing gotten, defaults will be maintained.
        cAlphaArgs(1) = ""
        cAlphaArgs(2) = ""
        cCurrentModuleObject = "ShadowCalculation"
        NumItems = inputProcessor->getNumObjectsFound(cCurrentModuleObject)
        NumAlphas = 0
        NumNumbers = 0
        if (NumItems > 1):
            ShowWarningError("{}: More than 1 occurrence of this object found, only first will be used.".format(cCurrentModuleObject))

        if (NumItems != 0):
            inputProcessor->getObjectItem(cCurrentModuleObject,
                                          1,
                                          cAlphaArgs,
                                          NumAlphas,
                                          rNumericArgs,
                                          NumNumbers,
                                          IOStat,
                                          lNumericFieldBlanks,
                                          lAlphaFieldBlanks,
                                          cAlphaFieldNames,
                                          cNumericFieldNames)
            ShadowingCalcFrequency = rNumericArgs(1)

        if (ShadowingCalcFrequency <= 0):
            # Set to default value
            ShadowingCalcFrequency = 20

        if (ShadowingCalcFrequency > 31):
            ShowWarningError(cCurrentModuleObject + ": suspect " + cNumericFieldNames(1))
            ShowContinueError("Value entered=[" + RoundSigDigits(rNumericArgs(1), 0) + "], Shadowing Calculations will be inaccurate.")

        if (rNumericArgs(2) > 199.0):
            MaxHCS = rNumericArgs(2)
        else:
            MaxHCS = 15000

        if (NumAlphas >= 1):
            if (UtilityRoutines::SameString(cAlphaArgs(1), "AverageOverDaysInFrequency")):
                DetailedSolarTimestepIntegration = False
                cAlphaArgs(1) = "AverageOverDaysInFrequency"
            elif (UtilityRoutines::SameString(cAlphaArgs(1), "TimestepFrequency")):
                DetailedSolarTimestepIntegration = True
                cAlphaArgs(1) = "TimestepFrequency"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(1))
                ShowContinueError("Value entered=\"" + cAlphaArgs(1) + "\", AverageOverDaysInFrequency will be used.")
                DetailedSolarTimestepIntegration = False
                cAlphaArgs(1) = "AverageOverDaysInFrequency"
        else:
            DetailedSolarTimestepIntegration = False
            cAlphaArgs(1) = "AverageOverDaysInFrequency"

        if (NumAlphas >= 2):
            if (UtilityRoutines::SameString(cAlphaArgs(2), "SutherlandHodgman")):
                SutherlandHodgman = True
                cAlphaArgs(2) = "SutherlandHodgman"
            elif (UtilityRoutines::SameString(cAlphaArgs(2), "ConvexWeilerAtherton")):
                SutherlandHodgman = False
                cAlphaArgs(2) = "ConvexWeilerAtherton"
            elif (lAlphaFieldBlanks(2)):
                if (!SutherlandHodgman): # if already set.
                    cAlphaArgs(2) = "ConvexWeilerAtherton"
                else:
                    cAlphaArgs(2) = "SutherlandHodgman"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(2))
                if (!SutherlandHodgman):
                    ShowContinueError("Value entered=\"" + cAlphaArgs(2) + "\", ConvexWeilerAtherton will be used.")
                else:
                    ShowContinueError("Value entered=\"" + cAlphaArgs(2) + "\", SutherlandHodgman will be used.")
        else:
            if (!SutherlandHodgman):
                cAlphaArgs(2) = "ConvexWeilerAtherton"
            else:
                cAlphaArgs(2) = "SutherlandHodgman"

        if (NumAlphas >= 3):
            if (UtilityRoutines::SameString(cAlphaArgs(3), "SimpleSkyDiffuseModeling")):
                DetailedSkyDiffuseAlgorithm = False
                cAlphaArgs(3) = "SimpleSkyDiffuseModeling"
            elif (UtilityRoutines::SameString(cAlphaArgs(3), "DetailedSkyDiffuseModeling")):
                DetailedSkyDiffuseAlgorithm = True
                cAlphaArgs(3) = "DetailedSkyDiffuseModeling"
            elif (lAlphaFieldBlanks(3)):
                DetailedSkyDiffuseAlgorithm = False
                cAlphaArgs(3) = "SimpleSkyDiffuseModeling"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(3))
                ShowContinueError("Value entered=\"" + cAlphaArgs(3) + "\", SimpleSkyDiffuseModeling will be used.")
        else:
            cAlphaArgs(3) = "SimpleSkyDiffuseModeling"
            DetailedSkyDiffuseAlgorithm = False

        if (NumAlphas >= 4):
            if (UtilityRoutines::SameString(cAlphaArgs(4), "ScheduledShading")):
                UseScheduledSunlitFrac = True
                cAlphaArgs(4) = "ScheduledShading"
            elif (UtilityRoutines::SameString(cAlphaArgs(4), "ImportedShading")):
                if (ScheduleFileShadingProcessed):
                    UseImportedSunlitFrac = True
                    cAlphaArgs(4) = "ImportedShading"
                else:
                    ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(4))
                    ShowContinueError("Value entered=\"" + cAlphaArgs(4) +
                                      "\" while no Schedule:File:Shading object is defined, InternalCalculation will be used.")
            elif (UtilityRoutines::SameString(cAlphaArgs(4), "InternalCalculation")):
                UseScheduledSunlitFrac = False
                UseImportedSunlitFrac = False
                cAlphaArgs(4) = "InternalCalculation"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(4))
                ShowContinueError("Value entered=\"" + cAlphaArgs(4) + "\", InternalCalculation will be used.")
        else:
            cAlphaArgs(4) = "InternalCalculation"
            UseScheduledSunlitFrac = False
            UseImportedSunlitFrac = False

        if (NumAlphas >= 5):
            if (UtilityRoutines::SameString(cAlphaArgs(5), "Yes")):
                ReportExtShadingSunlitFrac = True
                cAlphaArgs(5) = "Yes"
            elif (UtilityRoutines::SameString(cAlphaArgs(5), "No")):
                ReportExtShadingSunlitFrac = False
                cAlphaArgs(5) = "No"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(5))
                ShowContinueError("Value entered=\"" + cAlphaArgs(5) + "\", InternalCalculation will be used.")
        else:
            cAlphaArgs(5) = "No"
            ReportExtShadingSunlitFrac = False

        ExtShadingSchedNum = 0
        if (UseImportedSunlitFrac):
            # for (auto surf : Surface): # ???????
            for surf in Surface:
                ExtShadingSchedNum = ScheduleManager::GetScheduleIndex(surf.Name + "_shading")
                if (ExtShadingSchedNum):
                    surf.SchedExternalShadingFrac = True
                    surf.ExternalShadingSchInd = ExtShadingSchedNum

        DisableSelfShadingWithinGroup = False
        DisableSelfShadingBetweenGroup = False

        if (NumAlphas >= 6):
            if (UtilityRoutines::SameString(cAlphaArgs(6), "Yes")):
                DisableSelfShadingWithinGroup = True
                cAlphaArgs(6) = "Yes"
            elif (UtilityRoutines::SameString(cAlphaArgs(6), "No")):
                cAlphaArgs(6) = "No"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(6))
                ShowContinueError("Value entered=\"" + cAlphaArgs(6) + "\", all shading effects would be considered.")
        else:
            cAlphaArgs(6) = "No"

        if (NumAlphas >= 7):
            if (UtilityRoutines::SameString(cAlphaArgs(7), "Yes")):
                DisableSelfShadingBetweenGroup = True
                cAlphaArgs(7) = "Yes"
            elif (UtilityRoutines::SameString(cAlphaArgs(7), "No")):
                cAlphaArgs(7) = "No"
            else:
                ShowWarningError(cCurrentModuleObject + ": invalid " + cAlphaFieldNames(7))
                ShowContinueError("Value entered=\"" + cAlphaArgs(7) + "\", all shading effects would be considered.")
        else:
            cAlphaArgs(7) = "No"

        if (DisableSelfShadingBetweenGroup && DisableSelfShadingWithinGroup):
            DisableAllSelfShading = True
        elif (DisableSelfShadingBetweenGroup || DisableSelfShadingWithinGroup):
            DisableGroupSelfShading = True

        SurfZoneGroup = 0
        CurZoneGroup = 0
        if (DisableGroupSelfShading):
            DisableSelfShadingGroups = []
            NumOfShadingGroups = 0
            if (NumAlphas >= 8):
                # Read all shading groups
                NumOfShadingGroups = NumAlphas - 7
                DisableSelfShadingGroups.append(NumOfShadingGroups)
                for i in range(1, NumOfShadingGroups+1):
                    Found = UtilityRoutines::FindItemInList(cAlphaArgs(i + 7), ZoneList, NumOfZoneLists)
                    if (Found != 0) DisableSelfShadingGroups(i) = Found

                for SurfNum in range(1, TotSurfaces+1):
                    if (Surface(SurfNum).ExtBoundCond == 0): # Loop through all exterior surfaces
                        SurfZoneGroup = 0
                        
                        # Check the shading zone group of each exterior surface
                        for ZoneGroupLoop in range(1, NumOfShadingGroups+1):
                        	# Loop through all defined shading groups
                            CurZoneGroup = DisableSelfShadingGroups(ZoneGroupLoop)

                            for ZoneNum in range(1, ZoneList(CurZoneGroup).NumOfZones + 1):
                            	# Loop through all zones in the zone list
                                if (Surface(SurfNum).Zone == ZoneList(CurZoneGroup).Zone(ZoneNum)):
                                    SurfZoneGroup = CurZoneGroup
                                    break

                        # if a surface is not in any zone group, no self shading is disabled for this surface
                        if (SurfZoneGroup != 0):
                            # if DisableSelfShadingWithinGroup, add all zones in the same zone group to the surface's disabled zone list
                            # if DisableSelfShadingBetweenGroups, add all zones in all other zone groups to the surface's disabled zone list
                            for ZoneGroupLoop in range(1, NumOfShadingGroups+1):
                            	# Loop through all defined shading groups
                                CurZoneGroup = DisableSelfShadingGroups(ZoneGroupLoop)
                                if (SurfZoneGroup == CurZoneGroup && DisableSelfShadingWithinGroup):
                                    for ZoneNum in range(1, ZoneList(CurZoneGroup).NumOfZones + 1):
                                    	# Loop through all zones in the zone list
                                        Surface(SurfNum).DisabledShadowingZoneList.append(ZoneList(CurZoneGroup).Zone(ZoneNum))
                                
                                elif (SurfZoneGroup != CurZoneGroup && DisableSelfShadingBetweenGroup):
                                    for ZoneNum in range(1, ZoneList(CurZoneGroup).NumOfZones + 1):
                                        Surface(SurfNum).DisabledShadowingZoneList.append(ZoneList(CurZoneGroup).Zone(ZoneNum))
            else:
                ShowFatalError("No Shading groups are defined when disabling grouped self shading.")

        if (!DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing): # 'ShadingTransmittanceVaries' e 'SolarDistribution' e 'MinimalShadowing' não foram definidos
            ShowWarningError("GetShadowingInput: The shading transmittance for shading devices changes throughout the year. Choose "
                             "DetailedSkyDiffuseModeling in the " + cCurrentModuleObject + " object to remove this warning.")
            ShowContinueError("Simulation has been reset to use DetailedSkyDiffuseModeling. Simulation continues.")
            DetailedSkyDiffuseAlgorithm = True
            cAlphaArgs(2) = "DetailedSkyDiffuseModeling"
            if (ShadowingCalcFrequency > 1):
                ShowContinueError("Better accuracy may be gained by setting the " + cNumericFieldNames(1) + " to 1 in the " + cCurrentModuleObject + " object.")

        elif (DetailedSkyDiffuseAlgorithm):
            if (!ShadingTransmittanceVaries || SolarDistribution == MinimalShadowing):
                ShowWarningError("GetShadowingInput: DetailedSkyDiffuseModeling is chosen but not needed as either the shading transmittance for "
                                 "shading devices does not change throughout the year")
                ShowContinueError(" or MinimalShadowing has been chosen.")
                ShowContinueError("Simulation should be set to use SimpleSkyDiffuseModeling, but is left at Detailed for simulation.")
                ShowContinueError("Choose SimpleSkyDiffuseModeling in the " + cCurrentModuleObject + " object to reduce computation time.")

        gio::write(OutputFileInits, fmtA) << "! <Shadowing/Sun Position Calculations Annual Simulations>, Calculation Method, Value {days}, "
                                             "Allowable Number Figures in Shadow Overlap {}, Polygon Clipping Algorithm, Sky Diffuse Modeling "
                                             "Algorithm, External Shading Calculation Method, Output External Shading Calculation Results, Disable "
                                             "Self-Shading Within Shading Zone Groups, Disable Self-Shading From Shading Zone Groups to Other Zones"
        gio::write(OutputFileInits, fmtA) << "Shadowing/Sun Position Calculations Annual Simulations," + cAlphaArgs(1) + ',' +
                                                 RoundSigDigits(ShadowingCalcFrequency) + ',' + RoundSigDigits(MaxHCS) + ',' + cAlphaArgs(2) + ',' +
                                                 cAlphaArgs(3) + ',' + cAlphaArgs(4) + ',' + cAlphaArgs(5) + ',' + cAlphaArgs(6) + ',' +
                                                 cAlphaArgs(7)

    	return None

    def AllocateModuleArrays():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Rick Strand
              DATE WRITTEN   February 1998
              MODIFIED       August 2005 JG - Added output variables for energy in J
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This routine allocates all of the arrays at the module level which
        require allocation.

        METHODOLOGY EMPLOYED:
        Allocation is dependent on the user input file.

        REFERENCES:
        # na
    	'''

        ## Using/Aliasing
        using General::RoundSigDigits

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS: variáveis de loop!
        # int SurfLoop
        # int ZoneLoop
        # int I
        # int NumOfLayers

        # FLOW: --> pode virar um df!!
        CTHETA.dimension(TotSurfaces, 0.0)
        SAREA.dimension(TotSurfaces, 0.0)
        SurfSunlitArea.dimension(TotSurfaces, 0.0)
        SurfSunlitFrac.dimension(TotSurfaces, 0.0)
        SunlitFracHR.dimension(24, TotSurfaces, 0.0)
        SunlitFrac.dimension(NumOfTimeStepInHour, 24, TotSurfaces, 0.0)
        SunlitFracWithoutReveal.dimension(NumOfTimeStepInHour, 24, TotSurfaces, 0.0)
        BackSurfaces.dimension(NumOfTimeStepInHour, 24, MaxBkSurf, TotSurfaces, 0)
        OverlapAreas.dimension(NumOfTimeStepInHour, 24, MaxBkSurf, TotSurfaces, 0.0)
        CosIncAngHR.dimension(24, TotSurfaces, 0.0)
        CosIncAng.dimension(NumOfTimeStepInHour, 24, TotSurfaces, 0.0)
        AnisoSkyMult.dimension(TotSurfaces, 1.0) # For isotropic sky: recalculated in AnisoSkyViewFactors if anisotropic radiance
        MultIsoSky.dimension(TotSurfaces, 0.0)
        MultCircumSolar.dimension(TotSurfaces, 0.0)
        MultHorizonZenith.dimension(TotSurfaces, 0.0)
        WinTransSolar.dimension(TotSurfaces, 0.0)
        WinBmSolar.dimension(TotSurfaces, 0.0)
        WinBmBmSolar.dimension(TotSurfaces, 0.0)
        WinBmDifSolar.dimension(TotSurfaces, 0.0)

        WinDifSolar.dimension(TotSurfaces, 0.0)
        WinDirSolTransAtIncAngle.dimension(TotSurfaces, 0.0)
        WinHeatGain.dimension(TotSurfaces, 0.0)
        WinHeatTransfer.dimension(TotSurfaces, 0.0)
        WinHeatGainRep.dimension(TotSurfaces, 0.0)
        WinHeatLossRep.dimension(TotSurfaces, 0.0)
        WinGainConvGlazToZoneRep.dimension(TotSurfaces, 0.0)
        WinGainIRGlazToZoneRep.dimension(TotSurfaces, 0.0)
        WinLossSWZoneToOutWinRep.dimension(TotSurfaces, 0.0)
        WinGainFrameDividerToZoneRep.dimension(TotSurfaces, 0.0)
        WinGainConvGlazShadGapToZoneRep.dimension(TotSurfaces, 0.0)
        WinGainConvShadeToZoneRep.dimension(TotSurfaces, 0.0)
        OtherConvGainInsideFaceToZoneRep.dimension(TotSurfaces, 0.0)
        WinGainIRShadeToZoneRep.dimension(TotSurfaces, 0.0)
        WinGapConvHtFlowRep.dimension(TotSurfaces, 0.0)
        WinShadingAbsorbedSolar.dimension(TotSurfaces, 0.0)
        WinSysSolTransmittance.dimension(TotSurfaces, 0.0)
        WinSysSolReflectance.dimension(TotSurfaces, 0.0)
        WinSysSolAbsorptance.dimension(TotSurfaces, 0.0)
        InsideGlassCondensationFlag.dimension(TotSurfaces, 0)
        InsideFrameCondensationFlag.dimension(TotSurfaces, 0)
        InsideDividerCondensationFlag.dimension(TotSurfaces, 0)
        ZoneTransSolar.dimension(NumOfZones, 0.0)
        ZoneBmSolFrExtWinsRep.dimension(NumOfZones, 0.0)
        ZoneBmSolFrIntWinsRep.dimension(NumOfZones, 0.0)
        InitialZoneDifSolReflW.dimension(NumOfZones, 0.0)
        ZoneDifSolFrExtWinsRep.dimension(NumOfZones, 0.0)
        ZoneDifSolFrIntWinsRep.dimension(NumOfZones, 0.0)
        ZoneWinHeatGain.dimension(NumOfZones, 0.0)
        ZoneWinHeatGainRep.dimension(NumOfZones, 0.0)
        ZoneWinHeatLossRep.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfInsFaceCond.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfInsFaceCondGainRep.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfInsFaceCondLossRep.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfExtFaceCond.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfExtFaceCondGainRep.dimension(NumOfZones, 0.0)
        ZoneOpaqSurfExtFaceCondLossRep.dimension(NumOfZones, 0.0)

        QRadSWOutIncident.dimension(TotSurfaces, 0.0)
        QRadSWOutIncidentBeam.dimension(TotSurfaces, 0.0)
        BmIncInsSurfIntensRep.dimension(TotSurfaces, 0.0)
        BmIncInsSurfAmountRep.dimension(TotSurfaces, 0.0)
        IntBmIncInsSurfIntensRep.dimension(TotSurfaces, 0.0)
        IntBmIncInsSurfAmountRep.dimension(TotSurfaces, 0.0)
        QRadSWOutIncidentSkyDiffuse.dimension(TotSurfaces, 0.0)
        QRadSWOutIncidentGndDiffuse.dimension(TotSurfaces, 0.0)
        QRadSWOutIncBmToDiffReflGnd.dimension(TotSurfaces, 0.0)
        QRadSWOutIncSkyDiffReflGnd.dimension(TotSurfaces, 0.0)
        QRadSWOutIncBmToBmReflObs.dimension(TotSurfaces, 0.0)
        QRadSWOutIncBmToDiffReflObs.dimension(TotSurfaces, 0.0)
        QRadSWOutIncSkyDiffReflObs.dimension(TotSurfaces, 0.0)
        CosIncidenceAngle.dimension(TotSurfaces, 0.0)
        BSDFBeamDirectionRep.dimension(TotSurfaces, 0)
        BSDFBeamThetaRep.dimension(TotSurfaces, 0.0)
        BSDFBeamPhiRep.dimension(TotSurfaces, 0.0)
        QRadSWwinAbsTot.dimension(TotSurfaces, 0.0)

        QRadSWwinAbsLayer.dimension(MaxSolidWinLayers, TotSurfaces, 0.0)

        FenLaySurfTempFront.dimension(MaxSolidWinLayers, TotSurfaces, 0.0)
        FenLaySurfTempBack.dimension(MaxSolidWinLayers, TotSurfaces, 0.0)

        SWwinAbsTotalReport.dimension(TotSurfaces, 0.0)
        InitialDifSolInAbsReport.dimension(TotSurfaces, 0.0)
        InitialDifSolInTransReport.dimension(TotSurfaces, 0.0)
        SWInAbsTotalReport.dimension(TotSurfaces, 0.0)
        WindowRevealStatus.dimension(NumOfTimeStepInHour, 24, TotSurfaces, 0)

        # Weiler-Atherton
        MAXHCArrayBounds = 2 * (MaxVerticesPerSurface + 1)
        MAXHCArrayIncrement = MaxVerticesPerSurface + 1
        XTEMP.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        YTEMP.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        XVC.dimension(MaxVerticesPerSurface + 1, 0.0)
        XVS.dimension(MaxVerticesPerSurface + 1, 0.0)
        YVC.dimension(MaxVerticesPerSurface + 1, 0.0)
        YVS.dimension(MaxVerticesPerSurface + 1, 0.0)
        ZVC.dimension(MaxVerticesPerSurface + 1, 0.0)

        # Sutherland-Hodgman
        ATEMP.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        BTEMP.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        CTEMP.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        XTEMP1.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)
        YTEMP1.dimension(2 * (MaxVerticesPerSurface + 1), 0.0)

        # energy
        WinTransSolarEnergy.dimension(TotSurfaces, 0.0)
        WinBmSolarEnergy.dimension(TotSurfaces, 0.0)

        WinBmBmSolarEnergy.dimension(TotSurfaces, 0.0)
        WinBmDifSolarEnergy.dimension(TotSurfaces, 0.0)

        WinDifSolarEnergy.dimension(TotSurfaces, 0.0)
        WinHeatGainRepEnergy.dimension(TotSurfaces, 0.0)
        WinHeatLossRepEnergy.dimension(TotSurfaces, 0.0)
        WinGapConvHtFlowRepEnergy.dimension(TotSurfaces, 0.0)
        WinHeatTransferRepEnergy.dimension(TotSurfaces, 0.0)
        ZoneTransSolarEnergy.dimension(NumOfZones, 0.0)
        ZoneBmSolFrExtWinsRepEnergy.dimension(NumOfZones, 0.0)
        ZoneBmSolFrIntWinsRepEnergy.dimension(NumOfZones, 0.0)
        ZoneDifSolFrExtWinsRepEnergy.dimension(NumOfZones, 0.0)
        ZoneDifSolFrIntWinsRepEnergy.dimension(NumOfZones, 0.0)
        ZoneWinHeatGainRepEnergy.dimension(NumOfZones, 0.0)
        ZoneWinHeatLossRepEnergy.dimension(NumOfZones, 0.0)
        BmIncInsSurfAmountRepEnergy.dimension(TotSurfaces, 0.0)
        ZnOpqSurfInsFaceCondGnRepEnrg.dimension(NumOfZones, 0.0)
        ZnOpqSurfInsFaceCondLsRepEnrg.dimension(NumOfZones, 0.0)
        ZnOpqSurfExtFaceCondGnRepEnrg.dimension(NumOfZones, 0.0)
        ZnOpqSurfExtFaceCondLsRepEnrg.dimension(NumOfZones, 0.0)
        IntBmIncInsSurfAmountRepEnergy.dimension(TotSurfaces, 0.0)
        QRadSWwinAbsTotEnergy.dimension(TotSurfaces, 0.0)
        WinShadingAbsorbedSolarEnergy.dimension(TotSurfaces, 0.0)
        # for (auto &e : SurfaceWindow):
    	for e in SurfaceWindow:
            e.BmSolAbsdOutsReveal = 0.0
            e.BmSolRefldOutsRevealReport = 0.0
            e.BmSolAbsdInsReveal = 0.0
            e.BmSolRefldInsReveal = 0.0
            e.BmSolRefldInsRevealReport = 0.0
            e.OutsRevealDiffOntoGlazing = 0.0
            e.InsRevealDiffOntoGlazing = 0.0
            e.InsRevealDiffIntoZone = 0.0
            e.OutsRevealDiffOntoFrame = 0.0
            e.InsRevealDiffOntoFrame = 0.0

        # Added report variables for inside reveal to debug CR 7596. TH 5/26/2009
        # for (auto &e : SurfaceWindow):
        for e in SurfaceWindow:
            e.InsRevealDiffOntoGlazingReport = 0.0
            e.InsRevealDiffIntoZoneReport = 0.0
            e.InsRevealDiffOntoFrameReport = 0.0
            e.BmSolAbsdInsRevealReport = 0.0


        print("Initializing Surface (Shading) Report Variables")
        # entender por aqui:	https://bigladdersoftware.com/epx/docs/8-9/module-developer/how-do-i-output-my-variables.html
        # CurrentModuleObject='Surfaces'
        for SurfLoop in range(1, TotSurfaces+1):
            SetupOutputVariable("Surface Outside Normal Azimuth Angle",
                                OutputProcessor::Unit::deg,
                                Surface(SurfLoop).Azimuth,
                                "Zone",
                                "Average",
                                Surface(SurfLoop).Name)
            
            if (Surface(SurfLoop).ExtSolar):
                SetupOutputVariable("Surface Outside Face Sunlit Area",
                					OutputProcessor::Unit::m2,
                					SurfSunlitArea(SurfLoop),
                					"Zone",
                					"State",
                					Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Sunlit Fraction",
                                    OutputProcessor::Unit::None,
                                    SurfSunlitFrac(SurfLoop),
                                    "Zone",
                                    "State",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncident(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Beam Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncidentBeam(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Sky Diffuse Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncidentSkyDiffuse(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Ground Diffuse Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncidentGndDiffuse(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Beam Solar Incident Angle Cosine Value",
                                    OutputProcessor::Unit::None,
                                    CosIncidenceAngle(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Sky Diffuse Ground Reflected Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncSkyDiffReflGnd(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Sky Diffuse Surface Reflected Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncSkyDiffReflObs(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Beam To Beam Surface Reflected Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncBmToBmReflObs(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Beam To Diffuse Surface Reflected Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncBmToDiffReflObs(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Outside Face Incident Beam To Diffuse Ground Reflected Solar Radiation Rate per Area",
                                    OutputProcessor::Unit::W_m2,
                                    QRadSWOutIncBmToDiffReflGnd(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Anisotropic Sky Multiplier",
                                    OutputProcessor::Unit::None,
                                    AnisoSkyMult(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Window BSDF Beam Direction Number",
                                    OutputProcessor::Unit::None,
                                    BSDFBeamDirectionRep(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Window BSDF Beam Theta Angle",
                                    OutputProcessor::Unit::rad,
                                    BSDFBeamThetaRep(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)
                SetupOutputVariable("Surface Window BSDF Beam Phi Angle",
                                    OutputProcessor::Unit::rad,
                                    BSDFBeamPhiRep(SurfLoop),
                                    "Zone",
                                    "Average",
                                    Surface(SurfLoop).Name)

            if (!Surface(SurfLoop).HeatTransSurf): continue # probably will not be used

    	return None

    # MAYBE needed to get the nearby build shading
    def DetermineShadowingCombinations():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         From Legacy Code
              DATE WRITTEN
              MODIFIED       LKL March 2002 -- another missing translation from BLAST's routine
                             FCW Jan 2003 -- removed line that prevented beam solar through interior windows
              RE-ENGINEERED  Rick Strand 1998
                             Linda Lawrie Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This routine prepares a list of heat transfer surfaces and
        their possible shadowers which is used to direct the hourly
        calculation of shadows and sunlit areas.

        METHODOLOGY EMPLOYED:
        As appropriate surfaces are identified, they are placed into the
        ShadowComb data structure (module level) with the accompanying lists
        of other surface numbers.

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # Using/Aliasing
        using namespace DataErrorTracking
        using General::TrimSigDigits

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        # na

        # SUBROUTINE PARAMETER DEFINITIONS:
        static gio::Fmt fmtA("(A)")

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        GSS = []             		# List of shadowing surfaces numbers for a receiving surface
        BKS = []             		# List of back surface numbers for a receiving surface
        SBS = []             		# List of subsurfaces for a receiving surface
        MaxGSS = 50       			# Current Max for GSS array
        MaxBKS = 50       			# Current Max for BKS array
        MaxSBS = 50       			# Current Max for SBS array
        bool CannotShade            # True if subsurface cannot shade receiving surface
        bool HasWindow              # True if a window is present on receiving surface
        ZMIN = 0.0                  # Lowest point on the receiving surface
        BackSurfaceNumber = 0       # Back surface number
        HTS = 0                     # Heat transfer surface number for a receiving surface
        GRSNR = 0                   # Receiving surface number
        GSSNR = 0                   # Shadowing surface number
        SBSNR = 0                   # Subsurface number
        NBKS = 0                    # Number of back surfaces for a receiving surface
        NGSS = 0                    # Number of shadowing surfaces for a receiving surface
        NSBS = 0                    # Number of subsurfaces for a receiving surface
        bool ShadowingSurf          # True if a receiving surface is a shadowing surface
        CastingSurface = []			# [type:bool] tracking during setup of ShadowComb

        MaxDim = 0

		#ifdef EP_Count_Calls
        ++NumDetShadowCombs_Calls
		#endif

        ShadowComb.dimension(TotSurfaces, ShadowingCombinations{}) # Set all elements to default constructed state

        CastingSurface.dimension(TotSurfaces, False)

        HCA.dimension(2 * MaxHCS, MaxHCV + 1, 0)
        HCB.dimension(2 * MaxHCS, MaxHCV + 1, 0)
        HCC.dimension(2 * MaxHCS, MaxHCV + 1, 0)
        HCX.dimension(2 * MaxHCS, MaxHCV + 1, 0)
        HCY.dimension(2 * MaxHCS, MaxHCV + 1, 0)
        HCAREA.dimension(2 * MaxHCS, 0.0)
        HCNS.dimension(2 * MaxHCS, 0)
        HCNV.dimension(2 * MaxHCS, 0)
        HCT.dimension(2 * MaxHCS, 0.0)

        GSS.dimension(MaxGSS, 0)
        BKS.dimension(MaxGSS, 0)
        SBS.dimension(MaxGSS, 0)

        HTS = 0

        # Check every surface as a possible shadow receiving surface ("RS" = receiving surface).
        if (IgnoreSolarRadiation):
            return None

        for GRSNR in range(1, TotSurfaces+1): # Loop through all surfaces (looking for potential receiving surfaces)...

            ShadowingSurf = Surface(GRSNR).ShadowingSurf
            NGSS = 0
            NSBS = 0
            NBKS = 0

            if (!ShadowingSurf && !Surface(GRSNR).HeatTransSurf):
            	continue

            HTS = GRSNR

            if (!ShadowingSurf && !Surface(GRSNR).ExtSolar):
            	continue # Skip surfaces with no external solar

            if (!ShadowingSurf && Surface(GRSNR).BaseSurf != GRSNR):
            	continue # Skip subsurfaces (SBS)

            # Get the lowest point of receiving surface
            ZMIN = minval(Surface(GRSNR).Vertex, &Vector::z)

            # Check every surface as a possible shadow casting surface ("SS" = shadow sending)
            NGSS = 0
            if (SolarDistribution != MinimalShadowing): # Except when doing simplified exterior shadowing.
                for GSSNR in range(1, TotSurfaces+1): # Loop through all surfaces, looking for ones that could shade GRSNR
                    
                    if (GSSNR == GRSNR):
                    	continue # Receiving surface cannot shade itself
                    
                    if ((Surface(GSSNR).HeatTransSurf) && (Surface(GSSNR).BaseSurf == GRSNR)):
                        continue # A heat transfer subsurface of a receiving surface
                    
                    # cannot shade the receiving surface
                    if (ShadowingSurf):
                        # If receiving surf is a shadowing surface exclude matching shadow surface as sending surface
                        # IF((GSSNR == GRSNR+1 .AND. Surface(GSSNR)%Name(1:3) == 'Mir').OR. &
                        #   (GSSNR == GRSNR-1 .AND. Surface(GRSNR)%Name(1:3) == 'Mir')) CYCLE
                        if (((GSSNR == GRSNR + 1) && Surface(GSSNR).MirroredSurf) || ((GSSNR == GRSNR - 1) && Surface(GRSNR).MirroredSurf)):
                        	continue

                    if (Surface(GSSNR).BaseSurf == GRSNR): # Shadowing subsurface of receiving surface

                        NGSS += 1
                        if (NGSS > MaxGSS):
                            GSS.redimension(MaxGSS *= 2, 0)
                        
                        GSS(NGSS) = GSSNR # substitui o valor de GSS no index NGSS com GSSNR?

                    elif ((Surface(GSSNR).BaseSurf == 0) || ((Surface(GSSNR).BaseSurf == GSSNR) &&
                    		 ((Surface(GSSNR).ExtBoundCond == ExternalEnvironment) ||
                    		 Surface(GSSNR).ExtBoundCond == OtherSideCondModeledExt))): # Detached shadowing surface or | any other base surface
                                                                                        # exposed to outside environment

                        CHKGSS(GRSNR, GSSNR, ZMIN, CannotShade) # Check to see if this can shade the receiving surface
                        
						# Update the shadowing surface data if shading is possible
                        if (!CannotShade):
                            NGSS += 1
                            if (NGSS > MaxGSS):
                                GSS.redimension(MaxGSS *= 2, 0)
                            
                            GSS(NGSS) = GSSNR

                # ...end of surfaces DO loop (GSSNR)

            else: # Simplified Distribution -- still check for Shading Subsurfaces
                for GSSNR in range(1, TotSurfaces+1): # Loop through all surfaces (looking for surfaces which could shade GRSNR) ...

                    if (GSSNR == GRSNR):
                    	continue # Receiving surface cannot shade itself
                    if ((Surface(GSSNR).HeatTransSurf) && (Surface(GSSNR).BaseSurf == GRSNR)):
                        continue                           # Skip heat transfer subsurfaces of receiving surface
                    if (Surface(GSSNR).BaseSurf == GRSNR): # Shadowing subsurface of receiving surface
                        NGSS += 1
                        if (NGSS > MaxGSS):
                            GSS.redimension(MaxGSS *= 2, 0)
                        
                        GSS(NGSS) = GSSNR

            # ...end of check for simplified solar distribution

            # Check every surface as a receiving subsurface of the receiving surface
            NSBS = 0
            HasWindow = False
            # legacy: IF (OSENV(HTS) > 10) WINDOW=.True. -->Note: WINDOW was set True for roof ponds, solar walls, or other zones
            for SBSNR in range(1, TotSurfaces+1): # Loop through the surfaces yet again (looking for subsurfaces of GRSNR)...

                if (!Surface(SBSNR).HeatTransSurf):
                	continue    # Skip non heat transfer subsurfaces
                if (SBSNR == GRSNR):
                	continue                   # Surface itself cannot be its own subsurface
                if (Surface(SBSNR).BaseSurf != GRSNR):
                	continue # Ignore subsurfaces of other surfaces and other surfaces

                if (Construct(Surface(SBSNR).Construction).TransDiff > 0.0):
                	HasWindow = True # Check for window

                CHKSBS(HTS, GRSNR, SBSNR) # Check that the receiving surface completely encloses the subsurface
                # severe error if not
                NSBS += 1
                if (NSBS > MaxSBS):
                    SBS.redimension(MaxSBS *= 2, 0)
                
                SBS(NSBS) = SBSNR

            # ...end of surfaces DO loop (SBSNR)

            # Check every surface as a back surface
            NBKS = 0
            #                                        Except for simplified
            #                                        interior solar distribution,
            if ((SolarDistribution == FullInteriorExterior) && (HasWindow)): # For full interior solar distribution | and a window present on base surface (GRSNR)
                for BackSurfaceNumber in range(1, TotSurfaces+1):
                	# Loop through surfaces yet again, looking for back surfaces to GRSNR

                    if (!Surface(BackSurfaceNumber).HeatTransSurf):
                    	continue							# Skip non-heat transfer surfaces
                    if (Surface(BackSurfaceNumber).BaseSurf == GRSNR):
                    	continue							# Skip subsurfaces of this GRSNR
                    if (BackSurfaceNumber == GRSNR):
                    	continue                           # A back surface cannot be GRSNR itself
                    if (Surface(BackSurfaceNumber).Zone != Surface(GRSNR).Zone):
                    	continue							# Skip if back surface not in zone
                    if (Surface(BackSurfaceNumber).Class == SurfaceClass_IntMass):
                		continue

                    # Following line removed 1/27/03 by FCW. Was in original code that didn't do beam solar transmitted through
                    # interior windows. Was removed to allow such beam solar but then somehow was put back in.
                    # IF (Surface(BackSurfaceNumber)%BaseSurf /= BackSurfaceNumber) CYCLE ! Not for subsurfaces of Back Surface

                    CHKBKS(BackSurfaceNumber, GRSNR) # CHECK FOR CONVEX ZONE severe error if not
                    NBKS += 1
                    if (NBKS > MaxBKS):
                        BKS.redimension(MaxBKS *= 2, 0)
                    
                    BKS(NBKS) = BackSurfaceNumber

                # ...end of surfaces DO loop (BackSurfaceNumber)

            # Put this into the ShadowComb data structure
            ShadowComb(GRSNR).UseThisSurf = True
            ShadowComb(GRSNR).NumGenSurf = NGSS
            ShadowComb(GRSNR).NumBackSurf = NBKS
            ShadowComb(GRSNR).NumSubSurf = NSBS
            MaxDim = max(MaxDim, NGSS, NBKS, NSBS)

            ShadowComb(GRSNR).GenSurf.allocate({0, ShadowComb(GRSNR).NumGenSurf})
            ShadowComb(GRSNR).GenSurf(0) = 0
            if (ShadowComb(GRSNR).NumGenSurf > 0):
                ShadowComb(GRSNR).GenSurf({1, ShadowComb(GRSNR).NumGenSurf}) = GSS({1, NGSS})

            ShadowComb(GRSNR).BackSurf.allocate({0, ShadowComb(GRSNR).NumBackSurf})
            ShadowComb(GRSNR).BackSurf(0) = 0
            if (ShadowComb(GRSNR).NumBackSurf > 0):
                ShadowComb(GRSNR).BackSurf({1, ShadowComb(GRSNR).NumBackSurf}) = BKS({1, NBKS})

            ShadowComb(GRSNR).SubSurf.allocate({0, ShadowComb(GRSNR).NumSubSurf})
            ShadowComb(GRSNR).SubSurf(0) = 0
            if (ShadowComb(GRSNR).NumSubSurf > 0):
                ShadowComb(GRSNR).SubSurf({1, ShadowComb(GRSNR).NumSubSurf}) = SBS({1, NSBS})

        # ...end of surfaces (GRSNR) DO loop

        GSS.deallocate()
        SBS.deallocate()
        BKS.deallocate()

        shd_stream << "Shadowing Combinations\n"
        if (SolarDistribution == MinimalShadowing):
            shd_stream << "..Solar Distribution=Minimal Shadowing, Detached Shading will not be used in shadowing calculations\n"
        elif (SolarDistribution == FullExterior):
            if (CalcSolRefl):
                shd_stream << "..Solar Distribution=FullExteriorWithReflectionsFromExteriorSurfaces\n"
            else:
                shd_stream << "..Solar Distribution=FullExterior\n"
        elif (SolarDistribution == FullInteriorExterior):
            if (CalcSolRefl):
                shd_stream << "..Solar Distribution=FullInteriorAndExteriorWithReflectionsFromExteriorSurfaces\n"
            else:
                shd_stream << "..Solar Distribution=FullInteriorAndExterior\n"
        else:
        	# do nothing??? Vai dar erro de sintaxe!

        shd_stream << "..In the following, only the first 10 reference surfaces will be shown.\n"
        shd_stream << "..But all surfaces are used in the calculations.\n"

        for HTS in range(1, TotSurfaces+1):
            shd_stream << "==================================\n"
            if (ShadowComb(HTS).UseThisSurf):
                if (Surface(HTS).IsConvex):
                    shd_stream << "Surface=" << Surface(HTS).Name << " is used as Receiving Surface in calculations and is convex.\n"
                else:
                    shd_stream << "Surface=" << Surface(HTS).Name << " is used as Receiving Surface in calculations and is non-convex.\n"
                    if (ShadowComb(HTS).NumGenSurf > 0):
                        if (DisplayExtraWarnings):
                            raise RuntimeWarning("DetermineShadowingCombinations: Surface=\"{}\" is a receiving surface and is non-convex.".format(Surface(HTS).Name))
                            raise RuntimeError("...Shadowing values may be inaccurate. Check .shd report file for more surface shading details")
                        else:
                            TotalReceivingNonConvexSurfaces += 1
            else:
                shd_stream << "Surface=" << Surface(HTS).Name << " is not used as Receiving Surface in calculations.\n"
            
            shd_stream << "Number of general casting surfaces=" << ShadowComb(HTS).NumGenSurf << '\n'
            for NGSS in range(1, ShadowComb(HTS).NumGenSurf+1):
                if (NGSS <= 10):
                	shd_stream << "..Surface=" << Surface(ShadowComb(HTS).GenSurf(NGSS)).Name << '\n'

                CastingSurface(ShadowComb(HTS).GenSurf(NGSS)) = True

            shd_stream << "Number of back surfaces=" << ShadowComb(HTS).NumBackSurf << '\n'
            for NGSS in range(1, min(10, ShadowComb(HTS).NumBackSurf)+1):
                shd_stream << "...Surface=" << Surface(ShadowComb(HTS).BackSurf(NGSS)).Name << '\n'
            
            shd_stream << "Number of receiving sub surfaces=" << ShadowComb(HTS).NumSubSurf << '\n'
            for NGSS in range(1, min(10, ShadowComb(HTS).NumSubSurf)+1):
                shd_stream << "....Surface=" << Surface(ShadowComb(HTS).SubSurf(NGSS)).Name << '\n'

        for HTS in range(1, TotSurfaces+1):
            if (CastingSurface(HTS) && !Surface(HTS).IsConvex):
                if (DisplayExtraWarnings):
                    ShowSevereError("DetermineShadowingCombinations: Surface=\"{}\" is a casting surface and is non-convex.".format(Surface(HTS).Name))
                    raise RuntimeError("...Shadowing values may be inaccurate. Check .shd report file for more surface shading details")
                else:
                    ++TotalCastingNonConvexSurfaces

        CastingSurface.deallocate()

        if (TotalReceivingNonConvexSurfaces > 0):
            raise RuntimeWarning("DetermineShadowingCombinations: There are {} surfaces which are receiving surfaces and are non-convex.".format(TrimSigDigits(TotalReceivingNonConvexSurfaces)))
            raise RuntimeError("...Shadowing values may be inaccurate. Check .shd report file for more surface shading details")
            raise RuntimeError("...Add Output:Diagnostics,DisplayExtraWarnings to see individual warnings for each surface.")
            TotalWarningErrors += TotalReceivingNonConvexSurfaces

        if (TotalCastingNonConvexSurfaces > 0):
            ShowSevereMessage("DetermineShadowingCombinations: There are {} surfaces which are casting surfaces and are non-convex.".format(TrimSigDigits(TotalCastingNonConvexSurfaces)))
            raise RuntimeError("...Shadowing values may be inaccurate. Check .shd report file for more surface shading details")
            raise RuntimeError("...Add Output:Diagnostics,DisplayExtraWarnings to see individual severes for each surface.")
            TotalSevereErrors += TotalCastingNonConvexSurfaces

    	return None



    def CHKGSS(NRS, NSS, ZMIN, &CannotShade):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        Determines the possible shadowing combinations.  The
        routine checks detached shadowing or base heat transfer surfaces
        for the possibility that they cannot shade a given base heat transfer surface.
        - int const NRS,     # Surface number of the potential shadow receiving surface
        - int const NSS,     # Surface number of the potential shadow casting surface
        - Real64 const ZMIN, # Lowest point of the receiving surface
        - bool &CannotShade  # True if shadow casting surface cannot shade receiving surface.

        METHODOLOGY EMPLOYED:
        Shadowing is not possible if:
        1.  The lowest point of the shadow receiving surface (receiving surface)
            Is higher than the highest point of the shadow casting surface (s.s.)
        2.  The shadow casting surface Faces up (e.g. A flat roof)
        3.  The shadow casting surface Is behind the receiving surface
        4.  The receiving surface is behind the shadow casting surface

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
    	'''
        # Using/Aliasing
        using namespace Vectors

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        TolValue = 0.0003

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:

        # Object Data

        CannotShade = True

        # see if no point of shadow casting surface is above low point of receiving surface
        auto const &surface_C(Surface(NSS))
        if (surface_C.OutNormVec(3) > 0.9999):
        	# Shadow Casting Surface is horizontal and facing upward
        	return None

        auto const &vertex_C(surface_C.Vertex)
        ZMAX = vertex_C(1).z
        # for (int i = 2, e = surface_C.Sides i <= e ++i):
        e = surface_C.Sides
        for i in range(2, e+1):
            ZMAX = std::max(ZMAX, vertex_C(i).z)

        if (ZMAX <= ZMIN):
        	return None

        # SEE IF ANY VERTICES OF THE Shadow Casting Surface ARE ABOVE THE PLANE OF THE receiving surface
        auto const &surface_R(Surface(NRS))
        auto const &vertex_R(surface_R.Vertex)
        vertex_R_2 = vertex_R(2)
        Vector const AVec(vertex_R(1) - vertex_R_2) # Vector from vertex 2 to vertex 1 of receiving surface
        Vector const BVec(vertex_R(3) - vertex_R_2) # Vector from vertex 2 to vertex 3 of receiving surface

        Vector const CVec(cross(BVec, AVec)) # Vector perpendicular to surface at vertex 2

        NVSS = surface_C.Sides # Number of vertices of the shadow casting surface
        DOTP = 0.0             # Dot Product
        for I in range(1, NVSS+1):
            DOTP = dot(CVec, vertex_C(I) - vertex_R_2)
            if (DOTP > TolValue):
            	break # DOTP loop

        # SEE IF ANY VERTICES OF THE receiving surface ARE ABOVE THE PLANE OF THE S.S.
        if (DOTP > TolValue):
            vertex_C_2 = vertex_C(2)
            Vector const AVec(vertex_C(1) - vertex_C_2)
            Vector const BVec(vertex_C(3) - vertex_C_2)

            Vector const CVec(cross(BVec, AVec))

            NVRS = surface_R.Sides # Number of vertices of the receiving surface
            for I in range(1, NVRS+1):
                DOTP = dot(CVec, vertex_R(I) - vertex_C_2)
                if (DOTP > TolValue):
                    CannotShade = False
                    break # DOTP loop

    	return None

    def polygon_contains_point(nsides, polygon_3d, &point_3d, ignorex, ignorey, ignorez): # geopandas tem uma função pronta para isso!
    	'''
        Function information:
              Author         Linda Lawrie
              Date written   October 2005
              Modified       na
              Re-engineered  na

        Purpose of this function:
        Determine if a point is inside a simple 2d polygon.  For a simple polygon (one whose
        boundary never crosses itself).  The polygon does not need to be convex.
        - int const nsides,           # number of sides (vertices)
        - Array1A<Vector> polygon_3d, # points of polygon
        - Vector const &point_3d,     # point to be tested
        - bool const ignorex,
        - bool const ignorey,
        - bool const ignorez

        Methodology employed:
        <Description>

        References:
        M Shimrat, Position of Point Relative to Polygon, ACM Algorithm 112,
        Communications of the ACM, Volume 5, Number 8, page 434, August 1962.
        '''

        # USE STATEMENTS:
        # Using/Aliasing
        using namespace DataVectorTypes

        # Return value
        bool inside # Return value, True=inside, False = not inside

        # Argument array dimensioning
        polygon_3d.dim(nsides)

        # Function local variable declarations:
        int i
        int ip1

        # Object Data
        Array1D<Vector_2d> polygon(nsides)
        Vector_2d point

        inside = False
        if (ignorex):
            for (int i = 1 i <= nsides ++i):
                polygon(i).x = polygon_3d(i).y
                polygon(i).y = polygon_3d(i).z

            point.x = point_3d.y
            point.y = point_3d.z
        elif (ignorey):
            for (int i = 1 i <= nsides ++i):
                polygon(i).x = polygon_3d(i).x
                polygon(i).y = polygon_3d(i).z

            point.x = point_3d.x
            point.y = point_3d.z
        elif (ignorez):
            for (int i = 1 i <= nsides ++i):
                polygon(i).x = polygon_3d(i).x
                polygon(i).y = polygon_3d(i).y

            point.x = point_3d.x
            point.y = point_3d.y
        else: # Illegal
            assert(False)
            point.x = point.y = 0.0 # Elim possibly used uninitialized warnings

        for (i = 1 i <= nsides ++i):

            if (i < nsides):
                ip1 = i + 1
            else:
                ip1 = 1

            if ((polygon(i).y < point.y && point.y <= polygon(ip1).y) || (point.y <= polygon(i).y && polygon(ip1).y < point.y)):
                if ((point.x - polygon(i).x) - (point.y - polygon(i).y) * (polygon(ip1).x - polygon(i).x) / (polygon(ip1).y - polygon(i).y) < 0):
                    inside = !inside

        return inside # bool statement

    def CLIP(NVT, &XVT, &YVT, &ZVT):
		'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine 'clips' the shadow casting surface polygon so that
        none of it lies below the plane of the receiving surface polygon.  This
        prevents the casting of 'False' shadows.
        - int const NVT
        - Array1<Real64> &XVT
        - Array1<Real64> &YVT
        - Array1<Real64> &ZVT

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        NABOVE = 0  # Number of vertices of shadow casting surface. above the plane of receiving surface
        NEXT = 0    # First vertex above plane of receiving surface
        NON = 0     # Number of vertices of shadow casting surface. on plane of receiving surface
        XIN = 0.0   # X of entry point of shadow casting surface. into plane of receiving surface
        XOUT = 0.0  # X of exit point of shadow casting surface. from plane of receiving surface
        YIN = 0.0   # Y of entry point of shadow casting surface. into plane of receiving surface
        YOUT = 0.0  # Y of exit point of shadow casting surface. from plane of receiving surface
        #  INTEGER NVS      ! Number of vertices of the shadow/clipped surface

        # Determine if the shadow casting surface is above, below, or intersects with the plane of the receiving surface
        NumVertInShadowOrClippedSurface = NVS
        for N in range(1, NVT+1):
            ZVT_N = ZVT(N)
            if (ZVT_N > 0.0): NABOVE += 1
            if (ZVT_N == 0.0): NON += 1

        if (NABOVE + NON == NVT):
        	# Rename the unclipped shadow casting surface.
            NVS = NVT
            NumVertInShadowOrClippedSurface = NVT
            for N in range(1, NVT+1):
                XVC(N) = XVT(N)
                YVC(N) = YVT(N)
                ZVC(N) = ZVT(N)
        elif (NABOVE == 0):
        	# Totally submerged shadow casting surface.
            NVS = 0
            NumVertInShadowOrClippedSurface = 0
        else:
        	# Remove (clip) that portion of the shadow casting surface which is below the receiving surface
            NVS = NABOVE + 2
            NumVertInShadowOrClippedSurface = NABOVE + 2
            Real64 ZVT_N, ZVT_P(ZVT(1)) # ??????? ZVT_P é uma var de tipo ZVT_N ??????????
            XVT(NVT + 1) = XVT(1)
            YVT(NVT + 1) = YVT(1)
            ZVT(NVT + 1) = ZVT_P
            # for (int N = 1, P = 2 N <= NVT ++N, ++P):
            for N, P in zip(range(1, NVT+1), range(2, NVT+1)):
                ZVT_N = ZVT_P
                ZVT_P = ZVT(P)
                if (ZVT_N >= 0.0 && ZVT_P < 0.0):
                	# Line enters plane of receiving surface
                    ZVT_fac = 1.0 / (ZVT_P - ZVT_N)
                    XIN = (ZVT_P * XVT(N) - ZVT_N * XVT(P)) * ZVT_fac
                    YIN = (ZVT_P * YVT(N) - ZVT_N * YVT(P)) * ZVT_fac
                if (ZVT_N <= 0.0 && ZVT_P > 0.0):
                	# Line exits plane of receiving surface
                    NEXT = N + 1
                    ZVT_fac = 1.0 / (ZVT_P - ZVT_N)
                    XOUT = (ZVT_P * XVT(N) - ZVT_N * XVT(P)) * ZVT_fac
                    YOUT = (ZVT_P * YVT(N) - ZVT_N * YVT(P)) * ZVT_fac

            # Renumber the vertices of the clipped shadow casting surface, so they are still counter-clockwise sequential.
            XVC(1) = XOUT # ? Verify that the IN and OUT values were ever set?
            YVC(1) = YOUT
            ZVC(1) = 0.0
            XVC(NVS) = XIN
            YVC(NVS) = YIN
            ZVC(NVS) = 0.0
            for N in range(1, NABOVE):
                if (NEXT > NVT):
                	NEXT = 1
                XVC(N + 1) = XVT(NEXT)
                YVC(N + 1) = YVT(NEXT)
                ZVC(N + 1) = ZVT(NEXT)
                NEXT += 1

    	return None

    def CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT):
		'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        Transforms the general coordinates of the vertices
        of surface NS to coordinates in the plane of the receiving surface NGRS.
        See subroutine 'CalcCoordinateTransformation' SurfaceGeometry Module.					--> outro arquivo
        - int const NS,        # Surface number whose vertex coordinates are being transformed
        - int const NGRS,      # Base surface number for surface NS
        - int &NVT,            # Number of vertices for surface NS
        - Array1<Real64> &XVT, # XYZ coordinates of vertices of NS in plane of NGRS
        - Array1<Real64> &YVT,
        - Array1<Real64> &ZVT)

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        NECAP subroutine 'SHADOW'
        '''

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        Real64 Xdif # Intermediate Result
        Real64 Ydif # Intermediate Result
        Real64 Zdif # Intermediate Result

        # Tuned
        auto const &surface(Surface(NS))
        auto const &base_surface(Surface(NGRS))
        auto const &base_lcsx(base_surface.lcsx)
        auto const &base_lcsy(base_surface.lcsy)
        auto const &base_lcsz(base_surface.lcsz)
        Real64 const base_X0(X0(NGRS))
        Real64 const base_Y0(Y0(NGRS))
        Real64 const base_Z0(Z0(NGRS))

        NVT = surface.Sides

        # Perform transformation
        for N in range(1, NVT+1):
            auto const &vertex(surface.Vertex(N))

            Xdif = vertex.x - base_X0
            Ydif = vertex.y - base_Y0
            Zdif = vertex.z - base_Z0

            if (std::abs(Xdif) <= 1.E-15):
            	Xdif = 0.0
            if (std::abs(Ydif) <= 1.E-15):
            	Ydif = 0.0
            if (std::abs(Zdif) <= 1.E-15):
            	Zdif = 0.0

            XVT(N) = base_lcsx.x * Xdif + base_lcsx.y * Ydif + base_lcsx.z * Zdif
            YVT(N) = base_lcsy.x * Xdif + base_lcsy.y * Ydif + base_lcsy.z * Zdif
            ZVT(N) = base_lcsz.x * Xdif + base_lcsz.y * Ydif + base_lcsz.z * Zdif

    	return None

    def HTRANS(I, NS, NumVertices):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine sets up the homogeneous coordinates.
        This routine converts the cartesian coordinates of a surface
        or shadow polygon to homogeneous coordinates.  It also
        computes the area of the polygon.
        - int const I,          # Mode selector: 0 - Compute H.C. of sides
        - int const NS,         # Figure Number
        - int const NumVertices # Number of vertices

        METHODOLOGY EMPLOYED:
        Note: Original legacy code used integer arithmetic (tests in subroutines
        INCLOS and INTCPT are sensitive to round-off error).  However, porting to Fortran 77
        (BLAST/IBLAST) required some variables to become REAL(r64) instead.

        Notes on homogeneous coordinates:
        A point (X,Y) is represented by a 3-element vector
        (W*X,W*Y,W), where W may be any REAL(r64) number except 0.  a line
        is also represented by a 3-element vector (A,B,C).  The
        directed line (A,B,C) from point (W*X1,W*Y1,W) to point
        (V*X2,V*Y2,V) is given by (A,B,C) = (W*X1,W*Y1,W) cross
        (V*X2,V*Y2,V).  The sequence of the cross product is a
        convention to determine sign.  The condition that a point lie
        on a line is that (A,B,C) dot (W*X,W*Y,W) = 0.  'Normalize'
        the representation of a point by setting W to 1.  Then if
        (A,B,C) dot (X,Y,1) > 0.0, The point is to the left of the
        line, and if it is less than zero, the point is to the right
        of the line.  The intercept of two lines is given by
        (W*X,W*Y,W) = (A1,B1,C1) cross (A2,B2,C3).

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        W. M. Newman & R. F. Sproull, 'Principles of Interactive Computer Graphics', Appendix II, McGraw-Hill, 1973.
        'CRC Math Tables', 22 ED, 'Analytic Geometry', P.369
        '''

        # Using/Aliasing
        using General::TrimSigDigits

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        #                1 - Compute H.C. of vertices & sides

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:

        if (NS > 2 * MaxHCS):
            raise RuntimeError("Solar Shading: HTrans: Too many Figures (> {})".format(TrimSigDigits(MaxHCS)))

        HCNV(NS) = NumVertices

        # Tuned Linear indexing
        assert(equal_dimensions(HCX, HCY))
        assert(equal_dimensions(HCX, HCA))
        assert(equal_dimensions(HCX, HCB))
        assert(equal_dimensions(HCX, HCC))
        auto const l1(HCX.index(NS, 1))
        
        # Transform vertices of figure ns.
        if (I != 0):

            # See comment at top of module regarding HCMULT
            auto l(l1)
            for (int N = 1 N <= NumVertices ++N, ++l) { // [ l ] == ( NS, N )
                HCX[l] = nint64(XVS(N) * HCMULT)
                HCY[l] = nint64(YVS(N) * HCMULT)

        # Establish extra point for finding lines between points.
        auto l(HCX.index(NS, NumVertices + 1))
        Int64 HCX_m(HCX[l] = HCX[l1]) # [ l ] == ( NS, NumVertices + 1 ), [ l1 ] == ( NS, 1 )
        Int64 HCY_m(HCY[l] = HCY[l1]) # [ l ] == ( NS, NumVertices + 1 ), [ l1 ] == ( NS, 1 )

        # Determine lines between points.
        l = l1
        auto m(l1 + 1u)
        HCX_l = 0
        HCY_l = 0
        SUM = 0.0 # Sum variable
        
        # for (int N = 1 N <= NumVertices ++N, ++l, ++m):# [ l ] == ( NS, N ), [ m ] == ( NS, N + 1 )
        for N in range(1, NumVertices+1):
        	l += 1 # será q vai somar o par ordenado?
        	m += 1 # será q vai somar o par ordenado?
            HCX_l = HCX_m
            HCY_l = HCY_m
            HCX_m = HCX[m]
            HCY_m = HCY[m]
            HCA[l] = HCY_l - HCY_m
            HCB[l] = HCX_m - HCX_l
            SUM += HCC[l] = (HCY_m * HCX_l) - (HCX_m * HCY_l)

        # Compute area of polygon.
        #  SUM=0.0D0
        #  DO N = 1, NumVertices
        #    SUM = SUM + HCX(N,NS)*HCY(N+1,NS) - HCY(N,NS)*HCX(N+1,NS) ! Since HCX and HCY integerized, value of SUM should be ok
        #  END DO
        HCAREA(NS) = SUM * sqHCMULT_fac
        #  HCAREA(NS)=0.5d0*SUM*(kHCMULT)
    	
    	return None

    def HTRANS0(NS, NumVertices):
    	'''
		- int const NS,         # Figure Number
        - int const NumVertices # Number of vertices
    	'''
        # Using/Aliasing
        using General::TrimSigDigits

        # Locals

        if (NS > 2 * MaxHCS):
            raise RuntimeError("Solar Shading: HTrans0: Too many Figures (>{})".format(TrimSigDigits(MaxHCS)))

        HCNV(NS) = NumVertices

        # Tuned Linear indexing
        assert(equal_dimensions(HCX, HCY))
        assert(equal_dimensions(HCX, HCA))
        assert(equal_dimensions(HCX, HCB))
        assert(equal_dimensions(HCX, HCC))

        auto const l1(HCX.index(NS, 1))

        auto l(HCX.index(NS, NumVertices + 1))
        Int64 HCX_m(HCX[l] = HCX[l1]) # [ l1 ] == ( NS, 1 )
        Int64 HCY_m(HCY[l] = HCY[l1]) # [ l1 ] == ( NS, 1 )

        l = l1
        auto m(l1 + 1u)
        HCX_l = 0
        HCY_l = 0
        SUM = 0.0

        # for (int N = 1 N <= NumVertices ++N, ++l, ++m):# [ l ] == ( NS, N ), [ m ] == ( NS, N + 1 )
        for N in range(1, NumVertices+1):
        	l += 1 # será q vai somar o par ordenado?
        	m += 1 # será q vai somar o par ordenado?
            HCX_l = HCX_m
            HCY_l = HCY_m
            HCX_m = HCX[m]
            HCY_m = HCY[m]
            HCA[l] = HCY_l - HCY_m
            HCB[l] = HCX_m - HCX_l
            SUM += HCC[l] = (HCY_m * HCX_l) - (HCX_m * HCY_l)

        HCAREA(NS) = SUM * sqHCMULT_fac

    	return None

    def HTRANS1(NS, NumVertices):
    	'''
    	- int const NS,         # Figure Number
        - int const NumVertices # Number of vertices
    	'''
        # Using/Aliasing
        using General::TrimSigDigits

        if (NS > 2 * MaxHCS):
            raise RuntimeError("Solar Shading: HTrans1: Too many Figures (>{})".format(TrimSigDigits(MaxHCS)))

        HCNV(NS) = NumVertices

        # Tuned Linear indexing

        assert(equal_dimensions(HCX, HCY))
        assert(equal_dimensions(HCX, HCA))
        assert(equal_dimensions(HCX, HCB))
        assert(equal_dimensions(HCX, HCC))

        auto const l1(HCX.index(NS, 1))

        # only in HTRANS1
        auto l(l1)
        for N in range(1, NumVertices): # [ l ] == ( NS, N )
        	l += 1 # será q vai somar o par ordenado? Talvez precise de list comprehension: [a+1 for a in l]
            HCX[l] = nint64(XVS(N) * HCMULT)
            HCY[l] = nint64(YVS(N) * HCMULT)

        l = HCX.index(NS, NumVertices + 1)
        Int64 HCX_m(HCX[l] = HCX[l1]) # [ l1 ] == ( NS, 1 )
        Int64 HCY_m(HCY[l] = HCY[l1])

        l = l1
        auto m(l1 + 1u)
        HCX_l = 0
        HCY_l = 0
        SUM = 0.0

        # for (int N = 1 N <= NumVertices ++N, ++l, ++m):# [ l ] == ( NS, N ), [ m ] == ( NS, N + 1 )
        for N in range(1, NumVertices+1):
        	l += 1 # será q vai somar o par ordenado?
        	m += 1 # será q vai somar o par ordenado?
            HCX_l = HCX_m
            HCY_l = HCY_m
            HCX_m = HCX[m]
            HCY_m = HCY[m]
            HCA[l] = HCY_l - HCY_m
            HCB[l] = HCX_m - HCX_l
            SUM += HCC[l] = (HCY_m * HCX_l) - (HCX_m * HCY_l)

        HCAREA(NS) = SUM * sqHCMULT_fac

    	return None

    def INCLOS(N1, N1NumVert, N2, N2NumVert, &NumVerticesOverlap, &NIN):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine determines which vertices of figure N1 lie within figure N2.
        - int const N1,            # Figure number of figure 1
        - int const N1NumVert,     # Number of vertices of figure 1
        - int const N2,            # Figure number of figure 2
        - int const N2NumVert,     # Number of vertices of figure 2
        - int &NumVerticesOverlap, # Number of vertices which overlap
        - int &NIN                 # Number of vertices of figure 1 within figure 2

        METHODOLOGY EMPLOYED:
        For vertex N of figure N1 to lie within figure N2, it must be
        on or to the right of all sides of figure N2, assuming
        figure N2 is convex.

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        K = 0              # Vertex number of the overlap
        M = 0              # Side number of figure N2
        N = 0              # Vertex number of figure N1
        bool CycleMainLoop # Sets when to cycle main loop
        HFunct = 0.0

        NIN = 0

        for N in range(1, N1NumVert+1):

            CycleMainLoop = False

            # Eliminate cases where vertex N is to the left of side M.
            for M in range(1, N2NumVert):
                HFunct = HCX(N1, N) * HCA(N2, M) + HCY(N1, N) * HCB(N2, M) + HCC(N2, M)
                if (HFunct > 0.0):
                    CycleMainLoop = True # Set to cycle to the next value of N
                    break                # M DO loop

            if (CycleMainLoop): continue
            NIN += 1

            # Check for duplication of previously determined points.
            if (NumVerticesOverlap != 0):
                for K in range(1, NumVerticesOverlap+1):
                    if ((XTEMP(K) == HCX(N1, N)) && (YTEMP(K) == HCY(N1, N))):
                        CycleMainLoop = True # Set to cycle to the next value of N
                        break                # K DO loop
                if (CycleMainLoop): continue

            # Record enclosed vertices in temporary arrays.
            NumVerticesOverlap += 1
            XTEMP(NumVerticesOverlap) = HCX(N1, N)
            YTEMP(NumVerticesOverlap) = HCY(N1, N)
        
    	return None

    def INTCPT(NV1, NV2, &NV3, NS1, NS2):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine determines all intercepts between the sides of figure NS1
        and the sides of figure NS2.
        - int const NV1, # Number of vertices of figure NS1
        - int const NV2, # Number of vertices of figure NS2
        - int &NV3,      # Number of vertices of figure NS3
        - int const NS1, # Number of the figure being overlapped
        - int const NS2  # Number of the figure doing overlapping

        METHODOLOGY EMPLOYED:
        The requirements for intersection are that the end points of
        line N lie on both sides of line M and vice versa.  Also
        eliminate cases where the end point of one line lies exactly
        on the other to reduce duplication with the enclosed points.

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals

        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        W = 0.0        # Normalization factor
        XUntrunc = 0.0 # Untruncated X coordinate
        YUntrunc = 0.0 # Untruncated Y coordinate
        I1 = 0        # Intermediate result for testing intersection
        I2 = 0        # Intermediate result for testing intersection
        K = 0
        KK = 0
        M = 0 # Side number of figure NS2
        N = 0 # Side number of figure NS1

        for N in range(1, NV1):
            for M in range(1, NV2):
                
                # Eliminate cases where sides N and M do not intersect.
                I1 = HCA(NS1, N) * HCX(NS2, M) + HCB(NS1, N) * HCY(NS2, M) + HCC(NS1, N)
                I2 = HCA(NS1, N) * HCX(NS2, M + 1) + HCB(NS1, N) * HCY(NS2, M + 1) + HCC(NS1, N)
                if (I1 >= 0 && I2 >= 0): continue
                if (I1 <= 0 && I2 <= 0): continue

                I1 = HCA(NS2, M) * HCX(NS1, N) + HCB(NS2, M) * HCY(NS1, N) + HCC(NS2, M)
                I2 = HCA(NS2, M) * HCX(NS1, N + 1) + HCB(NS2, M) * HCY(NS1, N + 1) + HCC(NS2, M)
                if (I1 >= 0 && I2 >= 0): continue
                if (I1 <= 0 && I2 <= 0): continue

                # Determine the point of intersection and record in the temporary array.
                KK = NV3
                NV3 += 1
                W = HCB(NS2, M) * HCA(NS1, N) - HCA(NS2, M) * HCB(NS1, N)
                XUntrunc = (HCC(NS2, M) * HCB(NS1, N) - HCB(NS2, M) * HCC(NS1, N)) / W
                YUntrunc = (HCA(NS2, M) * HCC(NS1, N) - HCC(NS2, M) * HCA(NS1, N)) / W
                if (NV3 > isize(XTEMP)):
                    # write(outputfiledebug,*) 'nv3=',nv3,' SIZE(xtemp)=',SIZE(xtemp)
                    XTEMP.redimension(isize(XTEMP) + 10, 0.0)
                    YTEMP.redimension(isize(YTEMP) + 10, 0.0)

                XTEMP(NV3) = nint64(XUntrunc)
                YTEMP(NV3) = nint64(YUntrunc)

                # Eliminate near-duplicate points.
                if (KK != 0):
                    auto const x(XTEMP(NV3))
                    auto const y(YTEMP(NV3))
                    for K in range(1, KK):
                        if (std::abs(x - XTEMP(K)) > 2.0): continue
                        if (std::abs(y - YTEMP(K)) > 2.0): continue
                        NV3 = KK
                        break # K DO loop
        
    	return None

    def CLIPPOLY(NS1, NS2, NV1, NV2, &NV3):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Tyler Hoyt
              DATE WRITTEN   May 4, 2010
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Populate global arrays XTEMP and YTEMP with the vertices
        of the overlap between NS1 and NS2, and determine relevant
        overlap status.
        - int const NS1, # Figure number of figure 1 (The subject polygon)
		- int const NS2, # Figure number of figure 2 (The clipping polygon)
		- int const NV1, # Number of vertices of figure 1
		- int const NV2, # Number of vertices of figure 2
		- int &NV3       # Number of vertices of figure 3

        METHODOLOGY EMPLOYED:
        The Sutherland-Hodgman algorithm for polygon clipping is employed.

        METHODOLOGY EMPLOYED:

        REFERENCES:
        '''

        # Using/Aliasing
        using General::ReallocateRealArray
        using General::SafeDivide

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        typedef Array2D<Int64>::size_type size_type
        bool INTFLAG # For overlap status
        int S        # Test vertex
        int KK       # Duplicate test index
        int NVOUT    # Current output length for loops
        int NVTEMP

        Real64 W # Normalization factor
        Real64 HFunct

		#ifdef EP_Count_Calls
        ++NumClipPoly_Calls
		#endif
        # Tuned Linear indexing

        assert(equal_dimensions(HCX, HCY))
        assert(equal_dimensions(HCX, HCA))
        assert(equal_dimensions(HCX, HCB))
        assert(equal_dimensions(HCX, HCC))

        # Populate the arrays with the original polygon
        # for (size_type j = 0, l = HCX.index(NS1, 1), e = NV1 j < e ++j, ++l):
        l = HCX.index(NS1, 1)
        e = NV1
        for j in range(0, e):
            XTEMP[j] = HCX[l] # [ l ] == ( NS1, j+1 )
            YTEMP[j] = HCY[l]
            ATEMP[j] = HCA[l]
            BTEMP[j] = HCB[l]
            CTEMP[j] = HCC[l]
            l += 1			# Está no lugar certo? Ou deveria ser antes de qualquer operação?

        NVOUT = NV1 # First point-loop is the length of the subject polygon.
        INTFLAG = False
        NVTEMP = 0
        KK = 0

        auto l(HCA.index(NS2, 1))
        # Loop over edges of the clipping polygon
        # for (int E = 1 E <= NV2 ++E, ++l):
        for E in range(1, NV2+1):
            for P in range(1, NVOUT+1):
                XTEMP1(P) = XTEMP(P)
                YTEMP1(P) = YTEMP(P)

            S = NVOUT
            Real64 const HCA_E(HCA[l])
            Real64 const HCB_E(HCB[l])
            Real64 const HCC_E(HCC[l])
            Real64 XTEMP1_S(XTEMP1(S))
            Real64 YTEMP1_S(YTEMP1(S))
            for P in range(1, NVOUT+1):
                Real64 const XTEMP1_P(XTEMP1(P))
                Real64 const YTEMP1_P(YTEMP1(P))
                HFunct = XTEMP1_P * HCA_E + YTEMP1_P * HCB_E + HCC_E
                # S is constant within this block

                if (HFunct <= 0.0): # Vertex is not in the clipping plane
                    HFunct = XTEMP1_S * HCA_E + YTEMP1_S * HCB_E + HCC_E

                    if (HFunct > 0.0): # Test vertex is in the clipping plane

                        # Find/store the intersection of the clip edge and the line connecting S and P
                        KK = NVTEMP
                        NVTEMP += 1
                        Real64 const ATEMP_S(ATEMP(S))
                        Real64 const BTEMP_S(BTEMP(S))
                        Real64 const CTEMP_S(CTEMP(S))
                        W = HCB_E * ATEMP_S - HCA_E * BTEMP_S
                        
                        if (W != 0.0):
                            W_inv = (1.0 / W)
                            XTEMP(NVTEMP) = nint64((HCC_E * BTEMP_S - HCB_E * CTEMP_S) * W_inv)
                            YTEMP(NVTEMP) = nint64((HCA_E * CTEMP_S - HCC_E * ATEMP_S) * W_inv)
                        else:
                            XTEMP(NVTEMP) = SafeDivide(HCC_E * BTEMP_S - HCB_E * CTEMP_S, W)
                            YTEMP(NVTEMP) = SafeDivide(HCA_E * CTEMP_S - HCC_E * ATEMP_S, W)
                        
                        INTFLAG = True

                        if (E == NV2): # Remove near-duplicates on last edge
                            if (KK != 0):
                                auto const x(XTEMP(NVTEMP))
                                auto const y(YTEMP(NVTEMP))
                                for K in range(1, KK+1):
                                    if (std::abs(x - XTEMP(K)) > 2.0): continue
                                    if (std::abs(y - YTEMP(K)) > 2.0): continue
                                    NVTEMP = KK
                                    break # K loop

                    KK = NVTEMP
                    NVTEMP += 1
                    
                    if (NVTEMP > MAXHCArrayBounds):
                        int const NewArrayBounds(MAXHCArrayBounds + MAXHCArrayIncrement)
                        XTEMP.redimension(NewArrayBounds, 0.0)
                        YTEMP.redimension(NewArrayBounds, 0.0)
                        XTEMP1.redimension(NewArrayBounds, 0.0)
                        YTEMP1.redimension(NewArrayBounds, 0.0)
                        ATEMP.redimension(NewArrayBounds, 0.0)
                        BTEMP.redimension(NewArrayBounds, 0.0)
                        CTEMP.redimension(NewArrayBounds, 0.0)
                        MAXHCArrayBounds = NewArrayBounds

                    XTEMP(NVTEMP) = XTEMP1_P
                    YTEMP(NVTEMP) = YTEMP1_P

                    if (E == NV2): # Remove near-duplicates on last edge
                        if (KK != 0):
                            auto const x(XTEMP(NVTEMP))
                            auto const y(YTEMP(NVTEMP))
                            for K in range(1, KK+1):
                                if (std::abs(x - XTEMP(K)) > 2.0): continue
                                if (std::abs(y - YTEMP(K)) > 2.0): continue
                                NVTEMP = KK
                                break # K loop

                else:
                    HFunct = XTEMP1_S * HCA_E + YTEMP1_S * HCB_E + HCC_E
                    if (HFunct <= 0.0):
                    	# Test vertex is not in the clipping plane

                        if (NVTEMP < 2 * (MaxVerticesPerSurface + 1)):
                        # avoid assigning to element outside of XTEMP array size
                            KK = NVTEMP
                            NVTEMP += 1
                            Real64 const ATEMP_S(ATEMP(S))
                            Real64 const BTEMP_S(BTEMP(S))
                            Real64 const CTEMP_S(CTEMP(S))
                            W = HCB_E * ATEMP_S - HCA_E * BTEMP_S

                            if (W != 0.0):
                                W_inv = (1.0 / W)
                                XTEMP(NVTEMP) = nint64((HCC_E * BTEMP_S - HCB_E * CTEMP_S) * W_inv)
                                YTEMP(NVTEMP) = nint64((HCA_E * CTEMP_S - HCC_E * ATEMP_S) * W_inv)
                            else:
                                XTEMP(NVTEMP) = SafeDivide(HCC_E * BTEMP_S - HCB_E * CTEMP_S, W)
                                YTEMP(NVTEMP) = SafeDivide(HCA_E * CTEMP_S - HCC_E * ATEMP_S, W)
                            
                            INTFLAG = True

                            if (E == NV2): # Remove near-duplicates on last edge
                                if (KK != 0):
                                    auto const x(XTEMP(NVTEMP))
                                    auto const y(YTEMP(NVTEMP))
                                    for K in range(1, KK+1):
                                        if (std::abs(x - XTEMP(K)) > 2.0): continue
                                        if (std::abs(y - YTEMP(K)) > 2.0): continue
                                        NVTEMP = KK
                                        break # K loop

                S = P
                XTEMP1_S = XTEMP1_P
                YTEMP1_S = YTEMP1_P

            	l += 1			# Está no lugar certo? Ou deveria ser antes de qualquer operação?
            # end loop over points of subject polygon

            NVOUT = NVTEMP
            if (NVOUT == 0): break # Added to avoid array bounds violation of XTEMP1 and YTEMP1 and wasted looping
            NVTEMP = 0

            if (E != NV2):
                if (NVOUT > 2): # Compute HC values for edges of output polygon
                    Real64 const X_1(XTEMP(1))
                    Real64 const Y_1(YTEMP(1))
                    Real64 X_P(X_1), X_P1
                    Real64 Y_P(Y_1), Y_P1
                    
                    for P in range(1, NVOUT):
                        X_P1 = XTEMP(P + 1)
                        Y_P1 = YTEMP(P + 1)
                        ATEMP(P) = Y_P - Y_P1
                        BTEMP(P) = X_P1 - X_P
                        CTEMP(P) = X_P * Y_P1 - Y_P * X_P1
                        X_P = X_P1
                        Y_P = Y_P1
                    
                    ATEMP(NVOUT) = Y_P1 - Y_1
                    BTEMP(NVOUT) = X_1 - X_P1
                    CTEMP(NVOUT) = X_P1 * Y_1 - Y_P1 * X_1

        # end loop over edges in NS2
        NV3 = NVOUT

        if (NV3 < 3): # Determine overlap status
            OverlapStatus = NoOverlap
        elif (!INTFLAG):
            OverlapStatus = FirstSurfWithinSecond

    	return None

    def MULTOL(NNN, LOC0, NRFIGS):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine determines the overlaps of figure 'NS2' with previous figures
        'LOC0+1' through 'LOC0+NRFIGS'.  For example, if NS2 is a shadow,
        overlap with previous shadows.
        - int const NNN,   # argument
        - int const LOC0,  # Location in the homogeneous coordinate array
        - int const NRFIGS # Number of figures overlapped

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        # first figure overlapped (minus 1)

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        I = 0   # Loop Control
        NS1 = 0 # Number of the figure being overlapped
        NS2 = 0 # Number of the figure doing overlapping
        NS3 = 0 # Location to place results of overlap

        maxNumberOfFigures = max(maxNumberOfFigures, NRFIGS)

        NS2 = NNN
        for I in range(1, NRFIGS+1):
            NS1 = LOC0 + I
            NS3 = LOCHCA + 1

            DeterminePolygonOverlap(NS1, NS2, NS3) # Find overlap of figure NS2 on figure NS1.

            # Process overlap cases:
            if (OverlapStatus == NoOverlap): continue
            if ((OverlapStatus == TooManyVertices) || (OverlapStatus == TooManyFigures)): break

            LOCHCA = NS3 # Increment h.c. arrays pointer.

    	return None

    def ORDER(NV3, NS3):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine sorts the vertices found by inclosure and
        intercept in to clockwise order so that the overlap polygon
        may be used in computing subsequent overlaps.
        - int const NV3, # Number of vertices of figure NS3
        - int const NS3  # Location to place results of overlap

        METHODOLOGY EMPLOYED:
        The slopes of the lines from the left-most vertex to all
        others are found.  The slopes are sorted into descending
        sequence.  This sequence puts the vertices in clockwise order.

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        static Array1D<Real64> SLOPE # Slopes from left-most vertex to others
        Real64 DELTAX                # Difference between X coordinates of two vertices
        Real64 DELTAY                # Difference between Y coordinates of two vertices
        Real64 SAVES                 # Temporary location for exchange of variables
        Real64 SAVEX                 # Temporary location for exchange of variables
        Real64 SAVEY                 # Temporary location for exchange of variables
        Real64 XMIN                  # X coordinate of left-most vertex
        Real64 YXMIN
        I = 0   # Sort index
        IM1 = 0 # Sort control
        J = 0   # Sort index
        M = 0   # Number of slopes to be sorted
        N = 0   # Vertex number
        P = 0   # Location of first slope to be sorted
        FirstTimeFlag = True

        if (FirstTimeFlag):
            SLOPE.allocate(max(10, MaxVerticesPerSurface + 1))
            FirstTimeFlag = False

        # Determine left-most vertex.
        XMIN = XTEMP(1)
        YXMIN = YTEMP(1)
        for N in range(2, NV3+1):
            if (XTEMP(N) >= XMIN): continue # QUAL O SENTIDO DISSO?
            XMIN = XTEMP(N)
            YXMIN = YTEMP(N)

        # Determine slopes from left-most vertex to all others.
        # Identify first and second or last points as they occur.
        P = 1
        M = 0
        for N in range(1, NV3+1):
            DELTAX = XTEMP(N) - XMIN
            DELTAY = YTEMP(N) - YXMIN

            if (std::abs(DELTAX) > 0.5):
                M += 1
                SLOPE(M) = DELTAY / DELTAX
                XTEMP(M) = XTEMP(N)
                YTEMP(M) = YTEMP(N)
            elif (DELTAY > 0.5):
                P = 2
                HCX(NS3, 2) = nint64(XTEMP(N))
                HCY(NS3, 2) = nint64(YTEMP(N))
            elif (DELTAY < -0.5):
                HCX(NS3, NV3) = nint64(XTEMP(N))
                HCY(NS3, NV3) = nint64(YTEMP(N))
            else:
                HCX(NS3, 1) = nint64(XMIN)
                HCY(NS3, 1) = nint64(YXMIN)

        # Sequence the temporary arrays in order of decreasing slopes.(bubble sort)

        if (M != 1):
            for I in range(2, M+1):
                IM1 = I - 1
                for J in range(1, IM1+1):
                    if (SLOPE(I) <= SLOPE(J)): continue # QUAL O SENTIDO DISSO?
                    SAVEX = XTEMP(I)
                    SAVEY = YTEMP(I)
                    SAVES = SLOPE(I)
                    XTEMP(I) = XTEMP(J)
                    YTEMP(I) = YTEMP(J)
                    SLOPE(I) = SLOPE(J)
                    XTEMP(J) = SAVEX
                    YTEMP(J) = SAVEY
                    SLOPE(J) = SAVES

        # Place sequenced points in the homogeneous coordinate arrays.

        for N in range(1, M+1):
            HCX(NS3, N + P) = nint64(XTEMP(N))
            HCY(NS3, N + P) = nint64(YTEMP(N))
        
    	return None

    def DeterminePolygonOverlap(NS1, NS2, NS3):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine computes the possible overlap of two polygons.
        It uses homogeneous coordinate techniques to determine the overlap area
        between two convex polygons.  Results are stored in the homogeneous coordinate (HC) arrays.
        - int const NS1, # Number of the figure being overlapped
        - int const NS2, # Number of the figure doing overlapping
        - int const NS3  # Location to place results of overlap

        METHODOLOGY EMPLOYED:
        The vertices defining the overlap between fig.1 and fig.2
        consist of: the vertices of fig.1 enclosed by fig.2 (A)
        plus the vertices of fig.2 enclosed by fig.1 (B)
        plus the intercepts of fig.1 and fig.2 (C & D)

                                      +----------------------+
                                      !                      !
                                      !         FIG.2        !
                                      !                      !
                       +--------------C----------A           !
                       !              !         /            !
                       !              !        /             !
                       !              B-------D--------------+
                       !    FIG.1            /
                       !                    /
                       +-------------------+

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # Using/Aliasing
        using DataSystemVariables::SutherlandHodgman
        using General::RoundSigDigits

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        N = 0    # Loop index
        NV1 = 0  # Number of vertices of figure NS1
        NV2 = 0  # Number of vertices of figure NS2
        NV3 = 0  # Number of vertices of figure NS3 (the overlap of NS1 and NS2)
        NIN1 = 0 # Number of vertices of NS1 within NS2
        NIN2 = 0 # Number of vertices of NS2 within NS1
        TooManyFiguresMessage = False
        TooManyVerticesMessage = False

        # Check for exceeding array limits.
		#ifdef EP_Count_Calls
        ++NumDetPolyOverlap_Calls
		#endif

        if (NS3 > MaxHCS):
            OverlapStatus = TooManyFigures
            if (!TooManyFiguresMessage && !DisplayExtraWarnings):
                raise RuntimeWarning("DeterminePolygonOverlap: Too many figures [>{}] detected in an overlap calculation. Use Output:Diagnostics,DisplayExtraWarnings for more details.".format(RoundSigDigits(MaxHCS))) # round with how many decimals?
                TooManyFiguresMessage = True

            if (DisplayExtraWarnings):
                TrackTooManyFigures.redimension(++NumTooManyFigures)
                TrackTooManyFigures(NumTooManyFigures).SurfIndex1 = CurrentShadowingSurface
                TrackTooManyFigures(NumTooManyFigures).SurfIndex2 = CurrentSurfaceBeingShadowed

            return None

        OverlapStatus = PartialOverlap
        NV1 = HCNV(NS1)
        NV2 = HCNV(NS2)
        NV3 = 0

        if (!SutherlandHodgman):
            INCLOS(NS1, NV1, NS2, NV2, NV3, NIN1) # Find vertices of NS1 within NS2.

            if (NIN1 >= NV1):
                OverlapStatus = FirstSurfWithinSecond
            else:
                INCLOS(NS2, NV2, NS1, NV1, NV3, NIN2) # Find vertices of NS2 within NS1.
                if (NIN2 >= NV2):
                    OverlapStatus = SecondSurfWithinFirst
                else:
                    INTCPT(NV1, NV2, NV3, NS1, NS2) # Find intercepts of NS1 & NS2.
                    if (NV3 < 3): # Overlap must have 3 or more vertices
                        OverlapStatus = NoOverlap
                        return None

        else:
            # simple polygon clipping
            CLIPPOLY(NS1, NS2, NV1, NV2, NV3)

        if (NV3 < MaxHCV && NS3 <= MaxHCS):
            if (!SutherlandHodgman):
                ORDER(NV3, NS3) # Put vertices in clockwise order.
            else:
                assert(equal_dimensions(HCX, HCY))
                auto l(HCX.index(NS3, 1))
                # for (N = 1 N <= NV3 ++N, ++l):
                for N in range(1, NV3+1):
                    HCX[l] = nint64(XTEMP(N)) # [ l ] == ( N, NS3 )
                    HCY[l] = nint64(YTEMP(N))
                    l += 1

            HTRANS0(NS3, NV3) # Determine h.c. values of sides.
            # Skip overlaps of negligible area.

            if (std::abs(HCAREA(NS3)) * HCMULT < std::abs(HCAREA(NS1))):
                OverlapStatus = NoOverlap
            else:
                if (HCAREA(NS1) * HCAREA(NS2) > 0.0) HCAREA(NS3) = -HCAREA(NS3) # Determine sign of area of overlap
                Real64 const HCT_1(HCT(NS1))
                Real64 const HCT_2(HCT(NS2))
                Real64 HCT_3(HCT_2 * HCT_1) # Determine transmission of overlap
                if (HCT_2 >= 0.5 && HCT_1 >= 0.5):
                    if (HCT_2 != 1.0 && HCT_1 != 1.0):
                        HCT_3 = 1.0 - HCT_3
                HCT(NS3) = HCT_3

        elif (NV3 > MaxHCV):
            OverlapStatus = TooManyVertices

            if (!TooManyVerticesMessage && !DisplayExtraWarnings):
            	raise RuntimeWarning("DeterminePolygonOverlap: Too many vertices [>{}] detected in an overlap calculation. Use Output:Diagnostics,DisplayExtraWarnings for more details.".format(RoundSigDigits(MaxHCV)))
                TooManyVerticesMessage = True

            if (DisplayExtraWarnings):
                TrackTooManyVertices.redimension(++NumTooManyVertices)
                TrackTooManyVertices(NumTooManyVertices).SurfIndex1 = CurrentShadowingSurface
                TrackTooManyVertices(NumTooManyVertices).SurfIndex2 = CurrentSurfaceBeingShadowed

        elif (NS3 > MaxHCS):
            OverlapStatus = TooManyFigures

            if (!TooManyFiguresMessage && !DisplayExtraWarnings):
                raise RuntimeWarning("DeterminePolygonOverlap: Too many figures [>{}] detected in an overlap calculation. Use Output:Diagnostics,DisplayExtraWarnings for more details.".format(RoundSigDigits(MaxHCS)))
                TooManyFiguresMessage = True

            if (DisplayExtraWarnings):
                TrackTooManyFigures.redimension(++NumTooManyFigures)
                TrackTooManyFigures(NumTooManyFigures).SurfIndex1 = CurrentShadowingSurface
                TrackTooManyFigures(NumTooManyFigures).SurfIndex2 = CurrentSurfaceBeingShadowed
        
    	return None

    def CalcPerSolarBeam(AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       BG, Nov 2012 - Timestep solar.  DetailedSolarTimestepIntegration
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine manages computation of solar gain multipliers for beam radiation. These
        are calculated for a period of days depending on the input "Shadowing Calculations".
        - Real64 const AvgEqOfTime,       # Average value of Equation of Time for period
		- Real64 const AvgSinSolarDeclin, # Average value of Sine of Solar Declination for period
		- Real64 const AvgCosSolarDeclin  # Average value of Cosine of Solar Declination for period

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # Using/Aliasing
        using DataEnvironment::DayOfMonth
        using DataEnvironment::Month
        using DataGlobals::HourOfDay
        using DataGlobals::TimeStep
        using DataSystemVariables::DetailedSkyDiffuseAlgorithm
        using DataSystemVariables::DetailedSolarTimestepIntegration
        using DataSystemVariables::ReportExtShadingSunlitFrac
        using ScheduleManager::LookUpScheduleValue
        using WindowComplexManager::InitComplexWindows
        using WindowComplexManager::UpdateComplexWindows

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        iHour = 0   # Hour index number
        TS = 0      # TimeStep Loop Counter
        SurfNum = 0 # Do loop counter
        static gio::Fmt fmtA("(A)")
        static gio::Fmt ShdFracFmtName("(A, A)")
        static gio::Fmt ShdFracFmt1("(I2.2,'/',I2.2,' ',I2.2, ':',I2.2, ',')")
        static gio::Fmt ShdFracFmt2("(f6.2,',')")
        static gio::Fmt fmtN("('\n')")
        Once = True

        if (Once):
        	InitComplexWindows()
        Once = False

        if (KickOffSizing || KickOffSimulation):
        	return None # Skip solar calcs for these Initialization steps.

		#ifdef EP_Count_Calls
        ++NumCalcPerSolBeam_Calls
		#endif

        # Initialize some values for the appropriate period
        if (!DetailedSolarTimestepIntegration):
            SunlitFracHR = 0.0
            SunlitFrac = 0.0
            SunlitFracWithoutReveal = 0.0
            CTHETA = 0.0
            CosIncAngHR = 0.0
            CosIncAng = 0.0
            AOSurf = 0.0
            BackSurfaces = 0
            OverlapAreas = 0.0
            # for (auto &e : SurfaceWindow):
        	for e in SurfaceWindow:
                e.OutProjSLFracMult = 1.0
                e.InOutProjSLFracMult = 1.0
        else:
            SunlitFracHR(HourOfDay, {1, TotSurfaces}) = 0.0
            SunlitFrac(TimeStep, HourOfDay, {1, TotSurfaces}) = 0.0
            SunlitFracWithoutReveal(TimeStep, HourOfDay, {1, TotSurfaces}) = 0.0
            CTHETA({1, TotSurfaces}) = 0.0
            CosIncAngHR(HourOfDay, {1, TotSurfaces}) = 0.0
            CosIncAng(TimeStep, HourOfDay, {1, TotSurfaces}) = 0.0
            AOSurf({1, TotSurfaces}) = 0.0
            BackSurfaces(TimeStep, HourOfDay, {1, MaxBkSurf}, {1, TotSurfaces}) = 0
            OverlapAreas(TimeStep, HourOfDay, {1, MaxBkSurf}, {1, TotSurfaces}) = 0.0
            for SurfNum in range(1, TotSurfaces+1):
                SurfaceWindow(SurfNum).OutProjSLFracMult(HourOfDay) = 1.0
                SurfaceWindow(SurfNum).InOutProjSLFracMult(HourOfDay) = 1.0

        if (!DetailedSolarTimestepIntegration):
            for iHour in range(1, 25): # Do for all hours
                for TS in range(1, NumOfTimeStepInHour+1):
                    FigureSunCosines(iHour, TS, AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)
        else:
            FigureSunCosines(HourOfDay, TimeStep, AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)
        
        # Initialize/update the Complex Fenestration geometry and optical properties
        UpdateComplexWindows()
        if (!DetailedSolarTimestepIntegration):
            for iHour in range(1, 25): # Do for all hours.
                for TS in range(1, NumOfTimeStepInHour+1):
                    FigureSolarBeamAtTimestep(iHour, TS)
                	# end of TimeStep Loop
            # end of Hour Loop
        else:
            FigureSolarBeamAtTimestep(HourOfDay, TimeStep)
        
        if (ReportExtShadingSunlitFrac):
            if (KindOfSim == ksRunPeriodWeather):
                for iHour in range(1, 25): # Do for all hours.
                    for TS in range(1, NumOfTimeStepInHour+1):
                            IOFlags flags
                            flags.ADVANCE("No")
                            gio::write(OutputFileShadingFrac, ShdFracFmt1, flags)
                                << Month << DayOfMonth << iHour - 1 << (60 / NumOfTimeStepInHour) * (TS - 1)
                        for SurfNum in range(1, TotSurfaces+1):
                            {
                                IOFlags flags
                                flags.ADVANCE("No")
                                gio::write(OutputFileShadingFrac, ShdFracFmt2, flags) << SunlitFrac(TS, iHour, SurfNum)
                            }
                        {
                            IOFlags flags
                            flags.ADVANCE("No")
                            gio::write(OutputFileShadingFrac, fmtN, flags)
                        }
        
    	return None

    def FigureSunCosines(iHour, iTimeStep, EqOfTime, SinSolarDeclin, CosSolarDeclin):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         B. Griffith
              DATE WRITTEN   October 2012
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Determine solar position.  Default for sun below horizon.
        - int const iHour,
		- int const iTimeStep,
		- Real64 const EqOfTime,       # value of Equation of Time for period
		- Real64 const SinSolarDeclin, # value of Sine of Solar Declination for period
		- Real64 const CosSolarDeclin  # value of Cosine of Solar Declination for period

        METHODOLOGY EMPLOYED:
        Given hour, timestep, equation of time, solar declination sine, and solar declination cosine,
        determine sun directions for use elsewhere

        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using DataGlobals::TimeStepZone
        using DataSystemVariables::DetailedSolarTimestepIntegration

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS:
        # na

        # DERIVED TYPE DEFINITIONS:
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        CurrentTime = 0.0 # Current Time for passing to Solar Position Routine

        if (NumOfTimeStepInHour != 1):
            CurrentTime = double(iHour - 1) + double(iTimeStep) * (TimeStepZone)
        else:
            CurrentTime = double(iHour) + TS1TimeOffset
        
        SUN4(CurrentTime, EqOfTime, SinSolarDeclin, CosSolarDeclin)

        # Save hourly values for use in DaylightingManager
        if (!DetailedSolarTimestepIntegration):
            if (iTimeStep == NumOfTimeStepInHour): # poderia ser um 'AND'
            	SUNCOSHR(iHour, {1, 3}) = SUNCOS
        else:
            SUNCOSHR(iHour, {1, 3}) = SUNCOS
        
        # Save timestep values for use in WindowComplexManager
        SUNCOSTS(iTimeStep, iHour, {1, 3}) = SUNCOS
    	
    	return None

    def FigureSolarBeamAtTimestep(iHour, iTimeStep):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         B.Griffith, derived from CalcPerSolarBeam, Legacy and Lawrie.
              DATE WRITTEN   October 2012
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine computes solar gain multipliers for beam solar
        - int const iHour
        - int const iTimeStep

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using DataSystemVariables::DetailedSkyDiffuseAlgorithm
        using DataSystemVariables::DetailedSolarTimestepIntegration
        using DataSystemVariables::ReportExtShadingSunlitFrac
        using DataSystemVariables::UseScheduledSunlitFrac
        using ScheduleManager::LookUpScheduleValue

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:

        # INTERFACE BLOCK SPECIFICATIONS:
        # na

        # DERIVED TYPE DEFINITIONS:
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS
        SurfArea = 0.0        # Surface area. For walls, includes all window frame areas.
        Fac1WoShdg = 0.0      # Intermediate calculation factor, without shading
        Fac1WithShdg = 0.0    # Intermediate calculation factor, with shading
        FracIlluminated = 0.0 # Fraction of surface area illuminated by a sky patch

        # Recover the sun direction from the array stored in previous loop
        SUNCOS = SUNCOSTS(iTimeStep, iHour, {1, 3})

        CTHETA = 0.0

        if (SUNCOS(3) < SunIsUpValue):
        	return None

        for SurfNum in range(1, TotSurfaces+1):
            CTHETA(SurfNum) = SUNCOS(1) * Surface(SurfNum).OutNormVec(1) + SUNCOS(2) * Surface(SurfNum).OutNormVec(2) + SUNCOS(3) * Surface(SurfNum).OutNormVec(3)
            if (!DetailedSolarTimestepIntegration):
                if (iTimeStep == NumOfTimeStepInHour):
                	CosIncAngHR(iHour, SurfNum) = CTHETA(SurfNum)
            else:
                CosIncAngHR(iHour, SurfNum) = CTHETA(SurfNum)
            
            CosIncAng(iTimeStep, iHour, SurfNum) = CTHETA(SurfNum)

        if (UseScheduledSunlitFrac):
            for SurfNum in range(1, TotSurfaces+1):
                if (Surface(SurfNum).SchedExternalShadingFrac):
                    SunlitFrac(iTimeStep, iHour, SurfNum) = LookUpScheduleValue(Surface(SurfNum).ExternalShadingSchInd, iHour, iTimeStep)
                else:
                    SunlitFrac(iTimeStep, iHour, SurfNum) = 1.0
        else:
            SHADOW(iHour, iTimeStep) # Determine sunlit areas and solar multipliers for all surfaces.
            for SurfNum in range(1, TotSurfaces+1):
                if (Surface(SurfNum).Area >= 1.e-10):
                    SurfArea = Surface(SurfNum).NetAreaShadowCalc
                    if (!DetailedSolarTimestepIntegration):
                        if (iTimeStep == NumOfTimeStepInHour):
                        	SunlitFracHR(iHour, SurfNum) = SAREA(SurfNum) / SurfArea
                    else:
                        SunlitFracHR(iHour, SurfNum) = SAREA(SurfNum) / SurfArea
                    
                    SunlitFrac(iTimeStep, iHour, SurfNum) = SAREA(SurfNum) / SurfArea
                    if (SunlitFrac(iTimeStep, iHour, SurfNum) < 1.e-5):
                    	SunlitFrac(iTimeStep, iHour, SurfNum) = 0.0
                
                # Added check
                if (SunlitFrac(iTimeStep, iHour, SurfNum) > 1.0):
                	SunlitFrac(iTimeStep, iHour, SurfNum) = 1.0
                
        #   Note -- if not the below, values are set in SkyDifSolarShading routine (constant for simulation)
        if (DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing):
            WithShdgIsoSky = 0.
            WoShdgIsoSky = 0.
            WithShdgHoriz = 0.
            WoShdgHoriz = 0.

            for IPhi in range(0, NPhi): # Loop over patch altitude values
                SUNCOS(3) = sin_Phi[IPhi]

                for ITheta in range(0, NTheta): # Loop over patch azimuth values
                    SUNCOS(1) = cos_Phi[IPhi] * cos_Theta[ITheta]
                    SUNCOS(2) = cos_Phi[IPhi] * sin_Theta[ITheta]

                    for SurfNum in range(1, TotSurfaces+1):
                        if (!Surface(SurfNum).ShadowingSurf && !Surface(SurfNum).HeatTransSurf): continue
                        CTHETA(SurfNum) = SUNCOS(1) * Surface(SurfNum).OutNormVec(1) + SUNCOS(2) * Surface(SurfNum).OutNormVec(2) + SUNCOS(3) * Surface(SurfNum).OutNormVec(3)
                    
                    SHADOW(iHour, iTimeStep) # Determine sunlit areas and solar multipliers for all surfaces.

                    for SurfNum in range(1, TotSurfaces+1):
                        if (!Surface(SurfNum).ShadowingSurf &&
                    		(!Surface(SurfNum).HeatTransSurf || !Surface(SurfNum).ExtSolar ||
                			(Surface(SurfNum).ExtBoundCond != ExternalEnvironment && Surface(SurfNum).ExtBoundCond != OtherSideCondModeledExt))):
                    			continue

                        if (CTHETA(SurfNum) < 0.0):
                        	continue

                        Fac1WoShdg = cos_Phi[IPhi] * DThetaDPhi * CTHETA(SurfNum)
                        SurfArea = Surface(SurfNum).NetAreaShadowCalc
                        if (SurfArea > Eps):
                            FracIlluminated = SAREA(SurfNum) / SurfArea
                        else:
                            FracIlluminated = SAREA(SurfNum) / (SurfArea + Eps)
                        
                        Fac1WithShdg = Fac1WoShdg * FracIlluminated
                        WithShdgIsoSky(SurfNum) += Fac1WithShdg
                        WoShdgIsoSky(SurfNum) += Fac1WoShdg

                        # Horizon region
                        if (IPhi == 0):
                            WithShdgHoriz(SurfNum) += Fac1WithShdg
                            WoShdgHoriz(SurfNum) += Fac1WoShdg
                        
                    # end of surface loop
                # End of Theta loop
            # End of Phi loop

            for SurfNum in range(1, TotSurfaces+1):

                if (!Surface(SurfNum).ShadowingSurf &&
                	(!Surface(SurfNum).HeatTransSurf || !Surface(SurfNum).ExtSolar ||
            		(Surface(SurfNum).ExtBoundCond != ExternalEnvironment && Surface(SurfNum).ExtBoundCond != OtherSideCondModeledExt))):
                    	continue

                if (std::abs(WoShdgIsoSky(SurfNum)) > Eps):
                    DifShdgRatioIsoSkyHRTS(iTimeStep, iHour, SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum))
                else:
                    DifShdgRatioIsoSkyHRTS(iTimeStep, iHour, SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum) + Eps)
                
                if (std::abs(WoShdgHoriz(SurfNum)) > Eps):
                    DifShdgRatioHorizHRTS(iTimeStep, iHour, SurfNum) = (WithShdgHoriz(SurfNum)) / (WoShdgHoriz(SurfNum))
                else:
                    DifShdgRatioHorizHRTS(iTimeStep, iHour, SurfNum) = (WithShdgHoriz(SurfNum)) / (WoShdgHoriz(SurfNum) + Eps)

            #  ! Get IR view factors. An exterior surface can receive IR radiation from
            #  ! sky, ground or shadowing surfaces. Assume shadowing surfaces have same
            #  ! temperature as outside air (and therefore same temperature as ground),
            #  ! so that the view factor to these shadowing surfaces can be included in
            #  ! the ground view factor. Sky IR is assumed to be isotropic and shadowing
            #  ! surfaces are assumed to be opaque to IR so they totally "shade" IR from
            #  ! sky or ground.

            #  DO SurfNum = 1,TotSurfaces
            #    Surface(SurfNum)%ViewFactorSkyIR = Surface(SurfNum)%ViewFactorSkyIR * DifShdgRatioIsoSky(SurfNum,IHOUR,TS)
            #    Surface(SurfNum)%ViewFactorGroundIR = 1.0 - Surface(SurfNum)%ViewFactorSkyIR
            #  END DO

        # test for shading surfaces (DO NOT NEEDED)
        # for SurfNum in range(1, TotSurfaces+1):
            # For exterior windows with frame/divider that are partially or fully sunlit,
            # correct SunlitFrac due to shadowing of frame and divider projections onto window glass.
            # Note: if SunlitFrac = 0.0 the window is either completely shaded or the sun is in back
            # of the window in either case, frame/divider shadowing doesn't have to be done.

            # if (Surface(SurfNum).Class == SurfaceClass_Window && Surface(SurfNum).ExtBoundCond == ExternalEnvironment &&
            # 	SunlitFrac(iTimeStep, iHour, SurfNum) > 0.0 && Surface(SurfNum).FrameDivider > 0):
            #     	CalcFrameDividerShadow(SurfNum, Surface(SurfNum).FrameDivider, iHour)
        
    	return None

	

    def SHADOW(iHour, TS):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       Nov 2003, FCW: modify to do shadowing on shadowing surfaces
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine is a driving routine for calculations of shadows
        and sunlit areas used in computing the solar beam flux multipliers.
        - int const iHour, # Hour index
        - int const TS    # Time Step

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        Real64 XS # Intermediate result
        Real64 YS # Intermediate result
        Real64 ZS # Intermediate result
        N = 0     # Vertex number
        NGRS = 0  # Coordinate transformation index
        NZ = 0    # Zone Number of surface
        NVT = 0
        static Array1D<Real64> XVT # X Vertices of Shadows
        static Array1D<Real64> YVT # Y vertices of Shadows
        static Array1D<Real64> ZVT # Z vertices of Shadows
        OneTimeFlag = True
        HTS = 0         # Heat transfer surface number of the general receiving surface
        GRSNR = 0       # Surface number of general receiving surface
        NBKS = 0        # Number of back surfaces
        NGSS = 0        # Number of general shadowing surfaces
        NSBS = 0        # Number of subsurfaces (windows and doors)
        SurfArea = 0.0  # Surface area. For walls, includes all window frame areas.
        # For windows, includes divider area

        if (OneTimeFlag):
            XVT.allocate(MaxVerticesPerSurface + 1)
            YVT.allocate(MaxVerticesPerSurface + 1)
            ZVT.allocate(MaxVerticesPerSurface + 1)
            XVT = 0.0
            YVT = 0.0
            ZVT = 0.0
            OneTimeFlag = False

		#ifdef EP_Count_Calls
        if (iHour == 0):
            NumShadow_Calls += 1
        else:
            NumShadowAtTS_Calls += 1
		#endif

        SAREA = 0.0

        for GRSNR in range(1, TotSurfaces+1):

            if (!ShadowComb(GRSNR).UseThisSurf): continue

            SAREA(GRSNR) = 0.0

            NZ = Surface(GRSNR).Zone
            NGSS = ShadowComb(GRSNR).NumGenSurf
            NGSSHC = 0
            NBKS = ShadowComb(GRSNR).NumBackSurf
            NBKSHC = 0
            NSBS = ShadowComb(GRSNR).NumSubSurf
            NRVLHC = 0
            NSBSHC = 0
            LOCHCA = 1
            # Temporarily determine the old heat transfer surface number (HTS)
            HTS = GRSNR

            if (CTHETA(GRSNR) < SunIsUpValue): #.001) THEN ! Receiving surface is not in the sun
                SAREA(HTS) = 0.0
                SHDSBS(iHour, GRSNR, NBKS, NSBS, HTS, TS)
            elif ((NGSS <= 0) && (NSBS <= 0)):
            	# Simple surface--no shaders or subsurfaces
                SAREA(HTS) = Surface(GRSNR).NetAreaShadowCalc
            else:
            	# Surface in sun and either shading surfaces or subsurfaces present (or both)
                NGRS = Surface(GRSNR).BaseSurf
                if (Surface(GRSNR).ShadowingSurf):
                	NGRS = GRSNR

                # Compute the X and Y displacements of a shadow.
                XS = Surface(NGRS).lcsx.x * SUNCOS(1) + Surface(NGRS).lcsx.y * SUNCOS(2) + Surface(NGRS).lcsx.z * SUNCOS(3)
                YS = Surface(NGRS).lcsy.x * SUNCOS(1) + Surface(NGRS).lcsy.y * SUNCOS(2) + Surface(NGRS).lcsy.z * SUNCOS(3)
                ZS = Surface(NGRS).lcsz.x * SUNCOS(1) + Surface(NGRS).lcsz.y * SUNCOS(2) + Surface(NGRS).lcsz.z * SUNCOS(3)

                if (std::abs(ZS) > 1.e-4):
                    XShadowProjection = XS / ZS
                    YShadowProjection = YS / ZS
                    if (std::abs(XShadowProjection) < 1.e-8): XShadowProjection = 0.0
                    if (std::abs(YShadowProjection) < 1.e-8): YShadowProjection = 0.0
                else:
                    XShadowProjection = 0.0
                    YShadowProjection = 0.0

                CTRANS(GRSNR, NGRS, NVT, XVT, YVT, ZVT) # Transform coordinates of the receiving surface to 2-D form

                # Re-order its vertices to clockwise sequential.
                for N in range(1, NVT+1):
                    XVS(N) = XVT(NVT + 1 - N)
                    YVS(N) = YVT(NVT + 1 - N)

                HTRANS1(1, NVT) # Transform to homogeneous coordinates.

                HCAREA(1) = -HCAREA(1) # Compute (+) gross surface area.
                HCT(1) = 1.0

                SHDGSS(NGRS, iHour, TS, GRSNR, NGSS, HTS) # Determine shadowing on surface.
                if (!CalcSkyDifShading):
                    SHDBKS(NGRS, GRSNR, NBKS, HTS) # Determine possible back surfaces.

                SHDSBS(iHour, GRSNR, NBKS, NSBS, HTS, TS) # Subtract subsurf areas from total

                # Error checking:  require that 0 <= SAREA <= AREA.  + or - .01*AREA added for round-off errors
                SurfArea = Surface(GRSNR).NetAreaShadowCalc
                SAREA(HTS) = max(0.0, SAREA(HTS))

                SAREA(HTS) = min(SAREA(HTS), SurfArea)

            # ...end of surface in sun/surface with shaders and/or subsurfaces IF-THEN block

            # NOTE:
            # There used to be a call to legacy subroutine SHDCVR here when the
            # zone type was not a standard zone.

    	return None

    def SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS):
		'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine determines the shadows on a general receiving surface.
        - int const NGRS,
        - int const iHour,   # Hour Counter
        - int const TS,      # TimeStep
        - int const CurSurf, # Current Surface
        - int const NGSS,    # Number of general shadowing surfaces
        - int const HTS      # Heat transfer surface number of the general receiving surf

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
		'''
        # Using/Aliasing
        # using DataSystemVariables::DisableAllSelfShading
        DisableAllSelfShading = False                       # when true, all external shadowing surfaces is ignored
                                                            # when calculating sunlit fraction
        # using DataSystemVariables::DisableGroupSelfShading
        DisableGroupSelfShading = False                     # when true, defined shadowing surfaces group is ignored
                                                            # when calculating sunlit fraction
        using ScheduleManager::GetCurrentScheduleValue
        using ScheduleManager::GetScheduleMinValue
        using ScheduleManager::GetScheduleName
        using ScheduleManager::LookUpScheduleValue

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        typedef Array2D<Int64>::size_type size_type
        GSSNR = 0             # General shadowing surface number
        MainOverlapStatus = 0 # Overlap status of the main overlap calculation not the check for
        # multiple overlaps (unless there was an error)
        static Array1D<Real64> XVT
        static Array1D<Real64> YVT
        static Array1D<Real64> ZVT
        OneTimeFlag = True
        NS1 = 0         # Number of the figure being overlapped
        NS2 = 0         # Number of the figure doing overlapping
        NS3 = 0         # Location to place results of overlap
        SchValue = 0.0 # Value for Schedule of shading transmittence

        if (OneTimeFlag):
            XVT.dimension(MaxVerticesPerSurface + 1, 0.0)
            YVT.dimension(MaxVerticesPerSurface + 1, 0.0)
            ZVT.dimension(MaxVerticesPerSurface + 1, 0.0)
            OneTimeFlag = False

        FGSSHC = LOCHCA + 1
        MainOverlapStatus = NoOverlap # Set to ensure that the value from the last surface is not saved
        OverlapStatus = NoOverlap

        if (NGSS <= 0): # IF NO S.S., receiving surface FULLY SUNLIT.
            SAREA(HTS) = HCAREA(1) # Surface fully sunlit
        else:
            ExitLoopStatus = -1
            auto const &GenSurf(ShadowComb(CurSurf).GenSurf)
            auto const sunIsUp(SunIsUpValue)
            
            # Loop through all shadowing surfaces...
            for I in range(1, NGSS+1):
                GSSNR = GenSurf(I)

                if (CTHETA(GSSNR) > sunIsUp): #.001) CYCLE ! NO SHADOW IF GSS IN SUNLIGHT.
                	continue

                auto const &surface(Surface(GSSNR))
                bool const notHeatTransSurf(!surface.HeatTransSurf)

                #     This used to check to see if the shadowing surface was not opaque (within the scheduled dates of
                #            transmittance value.  Perhaps it ignored it if it were outside the range.  (if so, was an error)
                #     The proper action seems to be delete this statement all together, but there would also be no shading if
                #            the shading surface were transparent...
                #---former stmt      IF ((.NOT.Surface(GSSNR)%HeatTransSurf) .AND. &
                #---former stmt            GetCurrentScheduleValue(Surface(GSSNR)%SchedShadowSurfIndex,IHOUR) == 0.0) CYCLE

                if (notHeatTransSurf):
                    if (surface.IsTransparent):
                    	# No shadow if shading surface is transparent
                    	continue
                    if (surface.SchedShadowSurfIndex > 0):
                        if (LookUpScheduleValue(surface.SchedShadowSurfIndex, iHour) == 1.0):
                        	continue
                        if (!CalcSkyDifShading): # poderia ser um AND?
                            if (LookUpScheduleValue(surface.SchedShadowSurfIndex, iHour, TS) == 1.0):
                            	continue

                # Elimate shawdowing surfaces that is supposed to be disabled.
                if (DisableAllSelfShading):
                    if (surface.Zone != 0):
                        continue # Disable all shadowing surfaces in all zones. Attached shading surfaces are not part of a zone, zone value is 0.
                elif (DisableGroupSelfShading):
                    std::vector<int> DisabledZones = Surface(CurSurf).DisabledShadowingZoneList
                    isDisabledShadowSurf = False
                    # for (int i : DisabledZones):
                    for i in range(DisabledZones): # isso?
                        if (surface.Zone == i):
                            isDisabledShadowSurf = True
                            break
                    if (isDisabledShadowSurf):
                    	continue # Disable all shadowing surfaces in all disabled zones.

                #      IF ((.NOT.Surface(GSSNR)%HeatTransSurf) .AND. &
                #            GetCurrentScheduleValue(Surface(GSSNR)%SchedShadowSurfIndex) == 1.0) CYCLE

                # Transform shadow casting surface from cartesian to homogeneous coordinates according to surface type.

                if ((notHeatTransSurf) && (surface.BaseSurf != 0)):
                    # For shadowing subsurface coordinates of shadow casting surface are relative to the receiving surface
                    # project shadow to the receiving surface

                    NVS = surface.Sides
                    auto const &XV(ShadeV(GSSNR).XV)
                    auto const &YV(ShadeV(GSSNR).YV)
                    auto const &ZV(ShadeV(GSSNR).ZV)
                    for N in range(1, NVS+1):
                        XVS(N) = XV(N) - XShadowProjection * ZV(N)
                        YVS(N) = YV(N) - YShadowProjection * ZV(N)
                else:
                    # Transform coordinates of shadow casting surface from general system to the system relative to the receiving surface
                    int NVT
                    CTRANS(GSSNR, NGRS, NVT, XVT, YVT, ZVT)
                    CLIP(NVT, XVT, YVT, ZVT) # Clip portions of the shadow casting surface which are behind the receiving surface

                    if (NumVertInShadowOrClippedSurface <= 2):
                    	continue

                    # Project shadow from shadow casting surface along sun's rays to receiving surface Shadow vertices
                    # become clockwise sequential

                    for N in range(1, NumVertInShadowOrClippedSurface+1):
                        XVS(N) = XVC(N) - XShadowProjection * ZVC(N)
                        YVS(N) = YVC(N) - YShadowProjection * ZVC(N)

                # Transform to the homogeneous coordinate system.
                NS3 = LOCHCA + 1
                HTRANS1(NS3, NVS)

                # Adjust near-duplicate points.
                assert(equal_dimensions(HCX, HCY))
                assert(HCX.index(1, 1) == 0u)
                size_type j(HCX.index(NS3, 1))
                size_type NVR(HCNV(1))
                for N in range(1, NumVertInShadowOrClippedSurface+1): # Tuned Logic change: break after 1st "close" point found
                    auto const HCX_N(HCX[j])                                    # [ j ] == ( NS3, N )
                    auto const HCY_N(HCY[j])
                    j += 1 # será que é aqui ou depois do próximo loop?!
                    # for (size_type l = 0 l < NVR ++l): # [ l ] == ( 1, l+1 )
                    for l in range(l, NVR):
                        auto const delX(std::abs(HCX[l] - HCX_N))
                        if (delX > 6):
                    		continue
                        auto const delY(std::abs(HCY[l] - HCY_N))
                        if (delY > 6):
                        	continue
                        if (delX > 0):
                        	HCX[j] = HCX[l] # [ j ] == ( NS3, N )
                        if (delY > 0):
                        	HCY[j] = HCY[l]
                        break
                
                HTRANS0(NS3, NumVertInShadowOrClippedSurface)
                if (!CalcSkyDifShading):
                    if (iHour != 0):
                        SchValue = LookUpScheduleValue(surface.SchedShadowSurfIndex, iHour, TS)
                    else:
                        SchValue = surface.SchedMinValue
                else:
                    SchValue = surface.SchedMinValue

                HCT(NS3) = SchValue

                # Determine overlap of shadow with receiving surface
                CurrentShadowingSurface = I
                CurrentSurfaceBeingShadowed = GSSNR
                NS1 = 1
                NS2 = NS3
                DeterminePolygonOverlap(NS1, NS2, NS3)

                # Next statement is special to deal with transmitting shading devices
                if (OverlapStatus == FirstSurfWithinSecond && SchValue > 0.0):
                	OverlapStatus = PartialOverlap

                MainOverlapStatus = OverlapStatus
                ExitLoopStatus = MainOverlapStatus

                if (MainOverlapStatus == NoOverlap): # No overlap of general surface shadow and receiving surface
                	continue
                elif ((MainOverlapStatus == FirstSurfWithinSecond) || (MainOverlapStatus == TooManyVertices) ||
                      (MainOverlapStatus == TooManyFigures)):
                    #----------------------goto ShadowingSurfaces_exit
                elif ((MainOverlapStatus == SecondSurfWithinFirst) || (MainOverlapStatus == PartialOverlap)):
                    # Determine overlaps with previous shadows.
                    LOCHCA = NS3
                    NGSSHC = LOCHCA - FGSSHC + 1
                    if (NGSSHC > 1):
                    	MULTOL(LOCHCA, FGSSHC - 1, NGSSHC - 1) # HOYT - Remove this call
                else:
                    goto ShadowingSurfaces_exit

                ExitLoopStatus = -1

        ShadowingSurfaces_exit:

            # Compute sunlit area of surface (excluding effects of subsurfs).
            if (ExitLoopStatus == FirstSurfWithinSecond): # Surface fully shaded
                SAREA(HTS) = 0.0
                LOCHCA = FGSSHC
            elif ((ExitLoopStatus == TooManyVertices) || (ExitLoopStatus == TooManyFigures)): # Array limits exceeded, estimate
                SAREA(HTS) = 0.25 * HCAREA(1)
            else:
                # Compute the sunlit area here.
                # Call UnionShadow(FGSSHC,LOCHCA)
                NGSSHC = LOCHCA - FGSSHC + 1
                if (NGSSHC <= 0):
                    SAREA(HTS) = HCAREA(1) # Surface fully sunlit
                else:
                    Real64 A(HCAREA(1)) # Area
                    # for (int i = FGSSHC, e = FGSSHC + NGSSHC - 1 i <= e ++i):
                    e = FGSSHC + NGSSHC - 1
                    for i in range(FGSSHC, e+1):
                        A += HCAREA(i) * (1.0 - HCT(i))

                    SAREA(HTS) = A
                    if (SAREA(HTS) <= 0.0) # Surface fully shaded
                        SAREA(HTS) = 0.0
                        LOCHCA = FGSSHC

        NGSSHC = LOCHCA - FGSSHC + 1
        
    	return None

	def SurfaceScheduledSolarInc(SurfNum, ConstNum):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Simon Vidanovic
              DATE WRITTEN   June 2013
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Returns scheduled surface gain pointer for given surface-construction combination
        - int const SurfNum, # Surface number
        - int const ConstNum # Construction number
        - return int

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        # na
        '''

        # USE STATEMENTS:

        # Return value
        int SurfaceScheduledSolarInc

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:

        SurfaceScheduledSolarInc = 0

        for i in range(1, TotSurfIncSolSSG+1):
            if ((SurfIncSolSSG(i).SurfPtr == SurfNum) && (SurfIncSolSSG(i).ConstrPtr == ConstNum)):
                SurfaceScheduledSolarInc = i
                return SurfaceScheduledSolarInc

        return SurfaceScheduledSolarInc

    def PerformSolarCalculations():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda K. Lawrie
              DATE WRITTEN   July 1999
              MODIFIED       Sept 2003, FCW: add calls to CalcBeamSolDiffuseReflFactors and
                              CalcBeamSolSpecularReflFactors
                             Jan 2004, FCW: call CalcDayltgCoefficients if storm window status on
                              any window has changed
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine determines if new solar/shading calculations need
        to be performed and calls the proper routines to do the job.

        METHODOLOGY EMPLOYED:
        Users are allowed to enter a value for number of days in each period that
        will be used for calculating solar.  (Later, this could be more complicated as
        in allowing a number of days in a month or something).  Using this value or the
        default (20 days) if nothing is entered by the user, the routine will use the
        number of days left to determine if a new set of calculations should be done.
        The calculations use the average of "equation of time" and "solar declination"
        to perform the calculations.

        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using DataSystemVariables::DetailedSolarTimestepIntegration
        using DaylightingManager::CalcDayltgCoefficients
        using DaylightingManager::TotWindowsWithDayl

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        # na

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        SumDec = 0.0
        SumET = 0.0
        AvgEqOfTime = 0.0
        AvgSinSolarDeclin = 0.0
        AvgCosSolarDeclin = 0.0
        PerDayOfYear = 0
        Count = 0
        SinDec = 0.0
        EqTime = 0.0
        # not used INTEGER SurfNum

        # Calculate sky diffuse shading
        if (BeginSimFlag):
            CalcSkyDifShading = True
            SkyDifSolarShading() # Calculate factors for shading of sky diffuse solar
            CalcSkyDifShading = False

        if (BeginEnvrnFlag):
            ShadowingDaysLeft = 0

        if (ShadowingDaysLeft <= 0 || DetailedSolarTimestepIntegration):
            if (!DetailedSolarTimestepIntegration):
                #  Perform calculations.
                ShadowingDaysLeft = ShadowingCalcFrequency
                if (DayOfSim + ShadowingDaysLeft > NumOfDayInEnvrn):
                    ShadowingDaysLeft = NumOfDayInEnvrn - DayOfSim + 1

                #  Calculate average Equation of Time, Declination Angle for this period
                if (!WarmupFlag):
                    if (KindOfSim == ksRunPeriodWeather):
                        print("Updating Shadowing Calculations, Start Date = {}".format(CurMnDyYr))
                    else:
                        print("Updating Shadowing Calculations, Start Date = {}".format(CurMnDy))
                    
                    DisplayPerfSimulationFlag = True

                PerDayOfYear = DayOfYear
                SumDec = 0.0
                SumET = 0.0
                for Count in range(1, ShadowingDaysLeft+1):
                    SUN3(PerDayOfYear, SinDec, EqTime)
                    SumDec += SinDec
                    SumET += EqTime
                    PerDayOfYear += 1

                #  Compute Period Values
                AvgSinSolarDeclin = SumDec / double(ShadowingDaysLeft)
                AvgCosSolarDeclin = std::sqrt(1.0 - pow_2(AvgSinSolarDeclin))
                AvgEqOfTime = SumET / double(ShadowingDaysLeft)
            
            else:
                SUN3(DayOfYear, AvgSinSolarDeclin, AvgEqOfTime)
                AvgCosSolarDeclin = std::sqrt(1.0 - pow_2(AvgSinSolarDeclin))
                # trigger display of progress in the simulation every two weeks
                if (!WarmupFlag && BeginDayFlag && (DayOfSim % 14 == 0)):
                    DisplayPerfSimulationFlag = True

            CalcPerSolarBeam(AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)

            # Calculate factors for solar reflection
            if (CalcSolRefl):
                CalcBeamSolDiffuseReflFactors()
                CalcBeamSolSpecularReflFactors()
                if (BeginSimFlag):
                	CalcSkySolDiffuseReflFactors()

            #  Calculate daylighting coefficients
            CalcDayltgCoefficients()

        if (!WarmupFlag):
            ShadowingDaysLeft

        # Recalculate daylighting coefficients if storm window has been added
        # or removed from one or more windows at beginning of day
        if (TotWindowsWithDayl > 0 && !BeginSimFlag && !BeginEnvrnFlag && !WarmupFlag && TotStormWin > 0 && StormWinChangeThisDay):
            CalcDayltgCoefficients()
        
    	return None

	def SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Linda K. Lawrie

        PURPOSE OF THIS SUBROUTINE:
        This subroutine computes the coefficients for determining
        the solar position.
        - int const JulianDayOfYear,      # Julian Day Of Year
		- Real64 &SineOfSolarDeclination, # Sine of Solar Declination
		- Real64 &EquationOfTime          # Equation of Time (Degrees)

        METHODOLOGY EMPLOYED:
        The expressions are based on least-squares fits of data on p.316 of 'Thermal
        Environmental Engineering' by Threlkeld and on p.387 of the ASHRAE Handbook
        of Fundamentals (need date of ASHRAE HOF).

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        static Array1D<Real64> const SineSolDeclCoef(9,
                                                     {0.00561800,
                                                      0.0657911,
                                                      -0.392779,
                                                      0.00064440,
                                                      -0.00618495,
                                                      -0.00010101,
                                                      -0.00007951,
                                                      -0.00011691,
                                                      0.00002096}) # Fitted coefficients of Fourier series | SINE OF DECLINATION | COEFFICIENTS
        static Array1D<Real64> const EqOfTimeCoef(9,
                                                  {0.00021971,
                                                   -0.122649,
                                                   0.00762856,
                                                   -0.156308,
                                                   -0.0530028,
                                                   -0.00388702,
                                                   -0.00123978,
                                                   -0.00270502,
                                                   -0.00167992}) # Fitted coefficients of Fourier Series | EQUATION OF TIME | COEFFICIENTS

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        X = 0.0     # Day of Year in Radians (Computed from Input JulianDayOfYear)
        CosX = 0.0  # COS(X)
        SineX = 0.0 # SIN(X)

        X = 0.017167 * JulianDayOfYear # Convert julian date to angle X

        # Calculate sines and cosines of X
        SineX = np.sin(X)
        CosX = np.cos(X)

        SineOfSolarDeclination = SineSolDeclCoef(1) + SineSolDeclCoef(2) * SineX + SineSolDeclCoef(3) * CosX +
                                 SineSolDeclCoef(4) * (SineX * CosX * 2.0) + SineSolDeclCoef(5) * (pow_2(CosX) - pow_2(SineX)) +
                                 SineSolDeclCoef(6) * (SineX * (pow_2(CosX) - pow_2(SineX)) + CosX * (SineX * CosX * 2.0)) +
                                 SineSolDeclCoef(7) * (CosX * (pow_2(CosX) - pow_2(SineX)) - SineX * (SineX * CosX * 2.0)) +
                                 SineSolDeclCoef(8) * (2.0 * (SineX * CosX * 2.0) * (pow_2(CosX) - pow_2(SineX))) +
                                 SineSolDeclCoef(9) * (pow_2(pow_2(CosX) - pow_2(SineX)) - pow_2(SineX * CosX * 2.0))

        EquationOfTime = EqOfTimeCoef(1) + EqOfTimeCoef(2) * SineX + EqOfTimeCoef(3) * CosX + EqOfTimeCoef(4) * (SineX * CosX * 2.0) +
                         EqOfTimeCoef(5) * (pow_2(CosX) - pow_2(SineX)) +
                         EqOfTimeCoef(6) * (SineX * (pow_2(CosX) - pow_2(SineX)) + CosX * (SineX * CosX * 2.0)) +
                         EqOfTimeCoef(7) * (CosX * (pow_2(CosX) - pow_2(SineX)) - SineX * (SineX * CosX * 2.0)) +
                         EqOfTimeCoef(8) * (2.0 * (SineX * CosX * 2.0) * (pow_2(CosX) - pow_2(SineX))) +
                         EqOfTimeCoef(9) * (pow_2(pow_2(CosX) - pow_2(SineX)) - pow_2(SineX * CosX * 2.0))
    	return None

    def SUN4(CurrentTime, EqOfTime, SinSolarDeclin, CosSolarDeclin):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Legacy Code
              DATE WRITTEN
              MODIFIED       na
              RE-ENGINEERED  Lawrie, Oct 2000

        PURPOSE OF THIS SUBROUTINE:
        This subroutine computes solar direction cosines for a given hour. These
        cosines are used in the shadowing calculations.
        - Real64 const CurrentTime,    # Time to use in shadowing calculations
		- Real64 const EqOfTime,       # Equation of time for current day
		- Real64 const SinSolarDeclin, # Sine of the Solar declination (current day)
		- Real64 const CosSolarDeclin  # Cosine of the Solar declination (current day)

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        BLAST/IBLAST code, original author George Walton
        '''

        # USE STATEMENTS:
        # na

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        H = 0.0       # Hour angle (before noon = +) (in radians)
        HrAngle = 0.0 # Basic hour angle

        # Compute the hour angle
        HrAngle = (15.0 * (12.0 - (CurrentTime + EqOfTime)) + (TimeZoneMeridian - Longitude))
        H = HrAngle * DegToRadians

        # Compute the cosine of the solar zenith angle.
        SUNCOS(3) = SinSolarDeclin * SinLatitude + CosSolarDeclin * CosLatitude * np.cos(H)
        SUNCOS(2) = 0.0
        SUNCOS(1) = 0.0

        if (SUNCOS(3) < SunIsUpValue):
        	return None # Return if sun not above horizon.

        # Compute other direction cosines.
        SUNCOS(2) = SinSolarDeclin * CosLatitude - CosSolarDeclin * SinLatitude * np.cos(H)
        SUNCOS(1) = CosSolarDeclin * np.sin(H)

    	return None

	# MAYBE needed to get the nearby build shading
    def SkyDifSolarShading():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Fred Winkelmann
              DATE WRITTEN   May 1999
              MODIFIED       Sep 2000, FCW: add IR view factor calc
                             Sep 2002, FCW: correct error in expression for ground IR view factor.
                                Affects only non-vertical surfaces that are shadowed. For these surfaces
                                error caused underestimate of IR from ground and shadowing surfaces.
                             Dec 2002 LKL: Sky Radiance Distribution now only anisotropic
                             Nov 2003: FCW: modify to do sky solar shading of shadowing surfaces
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Calculates factors that account for shading of sky diffuse solar
        radiation by shadowing surfaces such as overhangs and detached shades.
        Called by PerformSolarCalculations
        For each exterior heat transfer surface calculates the following
        ratio (called DifShdgRatioIsoSky in this subroutine):
         R1 = (Diffuse solar from sky dome on surface, with shading)/
              (Diffuse solar from sky dome on surface, without shading)
        To calculate the incident diffuse radiation on a surface the sky
        hemisphere is divided into source elements ("patches"). Each patch
        is assumed to have the same radiance, i.e. the sky radiance is isotropic.
        The irradiance from each patch on a surface is calculated. Then these
        irradiances are summed to get the net irradiance on a surface, which
        the denominator of R1.
        To get the numerator of R1 the same summation is done, but for each surface
        and each patch the Shadow subroutine is called to determine how much
        radiation from a patch is blocked by shading surfaces.
        Also calculated is the following ratio (called DifShdgRatioHoriz in this routine):
         R2 = (Diffuse solar from sky horizon band on surface, with shading)/
              (Diffuse solar from sky horizon band on surface, without shading)
        For this ratio only a band of sky just above the horizon is considered.
        R1 and R2 are used in SUBROUTINE AnisoSkyViewFactors, which determines the
        sky diffuse solar irradiance on each exterior heat transfer surface each
        time step. In that routine the sky radiance distribution is a superposition
        of an isotropic distribution,
        a horizon brightening distribution and a circumsolar brightening distribution,
        where the proportion of each distribution depends
        on cloud cover, sun position and other factors. R1 multiplies the irradiance
        due to the isotropic component and R2 multiplies the irradiance due to the
        horizon brightening component.
        Calculates sky and ground IR view factors assuming sky IR is isotropic and
        shadowing surfaces are opaque to IR.
        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using DataSystemVariables::DetailedSkyDiffuseAlgorithm

        # Locals
        # SUBROUTINE PARAMETER DEFINITIONS:

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:

        SrdSurfsNum = 0       # Srd surface counter
        Fac1WoShdg = 0.0      # Intermediate calculation factor, without shading
        FracIlluminated = 0.0 # Fraction of surface area illuminated by a sky patch
        Fac1WithShdg = 0.0    # Intermediate calculation factor, with shading
        SurfArea = 0.0        # Surface area (m2)
        ShadowingSurf = 0     # True if surface is a shadowing surface
        # REAL(r64), ALLOCATABLE, DIMENSION(:) :: WithShdgIsoSky     ! Diffuse solar irradiance from isotropic
        #                                                          ! sky on surface, with shading
        # REAL(r64), ALLOCATABLE, DIMENSION(:) :: WoShdgIsoSky       ! Diffuse solar from isotropic
        #                                                           ! sky on surface, without shading
        # REAL(r64), ALLOCATABLE, DIMENSION(:) :: WithShdgHoriz      ! Diffuse solar irradiance from horizon portion of
        #                                                           ! sky on surface, with shading
        # REAL(r64), ALLOCATABLE, DIMENSION(:) :: WoShdgHoriz        ! Diffuse solar irradiance from horizon portion of
        #                                                           ! sky on surface, without shading
        # INTEGER iHour,iTS

        # FLOW:

        # Initialize Surfaces Arrays
        SAREA = 0.0
        WithShdgIsoSky.dimension(TotSurfaces, 0.0)
        WoShdgIsoSky.dimension(TotSurfaces, 0.0)
        WithShdgHoriz.dimension(TotSurfaces, 0.0)
        WoShdgHoriz.dimension(TotSurfaces, 0.0)
        DifShdgRatioIsoSky.allocate(TotSurfaces)
        DifShdgRatioHoriz.allocate(TotSurfaces)
        # initialized as no shading
        DifShdgRatioIsoSky = 1.0
        DifShdgRatioHoriz = 1.0
        if (DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing):
            curDifShdgRatioIsoSky.dimension(TotSurfaces, 1.0)
        
        # only for detailed.
        if (DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing):
            DifShdgRatioIsoSkyHRTS.allocate(NumOfTimeStepInHour, 24, TotSurfaces)
            DifShdgRatioIsoSkyHRTS = 1.0
            DifShdgRatioHorizHRTS.allocate(NumOfTimeStepInHour, 24, TotSurfaces)
            DifShdgRatioHorizHRTS = 1.0
        
        for SurfNum in range(1, TotSurfaces+1): # SurfNum <= TotSurfaces == SurfNum = TotSurfaces
            if (!Surface(SurfNum).ExtSolar):
            	continue

            # CurrentModuleObject='Surfaces'
            if (DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing):
                SetupOutputVariable("Debug Surface Solar Shading Model DifShdgRatioIsoSky",
                                    OutputProcessor::Unit::None,
                                    curDifShdgRatioIsoSky(SurfNum),
                                    "Zone",
                                    "Average",
                                    Surface(SurfNum).Name)
            else:
                SetupOutputVariable("Debug Surface Solar Shading Model DifShdgRatioIsoSky",
                                    OutputProcessor::Unit::None,
                                    DifShdgRatioIsoSky(SurfNum),
                                    "Zone",
                                    "Average",
                                    Surface(SurfNum).Name)
            
            SetupOutputVariable("Debug Surface Solar Shading Model DifShdgRatioHoriz",
                                OutputProcessor::Unit::None,
                                DifShdgRatioHoriz(SurfNum),
                                "Zone",
                                "Average",
                                Surface(SurfNum).Name)
            SetupOutputVariable("Debug Surface Solar Shading Model WithShdgIsoSky",
                                OutputProcessor::Unit::None,
                                WithShdgIsoSky(SurfNum),
                                "Zone",
                                "Average",
                                Surface(SurfNum).Name)
            SetupOutputVariable("Debug Surface Solar Shading Model WoShdgIsoSky",
                                OutputProcessor::Unit::None,
                                WoShdgIsoSky(SurfNum),
                                "Zone",
                                "Average",
                                Surface(SurfNum).Name)
        
        for IPhi in range(0, NPhi): # Loop over patch altitude values
            SUNCOS(3) = sin_Phi[IPhi]

            for ITheta in range(0, NTheta): # Loop over patch azimuth values
                SUNCOS(1) = cos_Phi[IPhi] * cos_Theta[ITheta]
                SUNCOS(2) = cos_Phi[IPhi] * sin_Theta[ITheta]

                for SurfNum in range(1, TotSurfaces+1): # Cosine of angle of incidence on surface of solar
                    # radiation from patch
                    ShadowingSurf = Surface(SurfNum).ShadowingSurf

                    if (!ShadowingSurf && !Surface(SurfNum).HeatTransSurf):
                    	continue

                    CTHETA(SurfNum) = SUNCOS(1) * Surface(SurfNum).OutNormVec(1) + SUNCOS(2) * Surface(SurfNum).OutNormVec(2) +
                                      SUNCOS(3) * Surface(SurfNum).OutNormVec(3)

                SHADOW(0, 0)

                for SurfNum in range(1, TotSurfaces+1):
                    ShadowingSurf = Surface(SurfNum).ShadowingSurf

                    if (!ShadowingSurf &&
                        (!Surface(SurfNum).HeatTransSurf || !Surface(SurfNum).ExtSolar ||
                         (Surface(SurfNum).ExtBoundCond != ExternalEnvironment && Surface(SurfNum).ExtBoundCond != OtherSideCondModeledExt))):
                        continue

                    if (CTHETA(SurfNum) < 0.0): continue

                    Fac1WoShdg = cos_Phi[IPhi] * DThetaDPhi * CTHETA(SurfNum)
                    SurfArea = Surface(SurfNum).NetAreaShadowCalc
                    if (SurfArea > Eps):
                        FracIlluminated = SAREA(SurfNum) / SurfArea
                    else:
                        FracIlluminated = SAREA(SurfNum) / (SurfArea + Eps)
                    
                    Fac1WithShdg = Fac1WoShdg * FracIlluminated
                    WithShdgIsoSky(SurfNum) += Fac1WithShdg
                    WoShdgIsoSky(SurfNum) += Fac1WoShdg

                    # Horizon region
                    if (IPhi == 0):
                        WithShdgHoriz(SurfNum) += Fac1WithShdg
                        WoShdgHoriz(SurfNum) += Fac1WoShdg
                    
                # end of surface loop
            # end of Theta loop
        # end of Phi loop

        for SurfNum in range(1, TotSurfaces+1):
            ShadowingSurf = Surface(SurfNum).ShadowingSurf

            if (!ShadowingSurf &&
                (!Surface(SurfNum).HeatTransSurf || !Surface(SurfNum).ExtSolar ||
                 (Surface(SurfNum).ExtBoundCond != ExternalEnvironment && Surface(SurfNum).ExtBoundCond != OtherSideCondModeledExt))):
                continue

            if (std::abs(WoShdgIsoSky(SurfNum)) > Eps):
                DifShdgRatioIsoSky(SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum))
            else:
                DifShdgRatioIsoSky(SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum) + Eps)
            
            if (std::abs(WoShdgHoriz(SurfNum)) > Eps):
                DifShdgRatioHoriz(SurfNum) = (WithShdgHoriz(SurfNum)) / (WoShdgHoriz(SurfNum))
            else:
                DifShdgRatioHoriz(SurfNum) = (WithShdgHoriz(SurfNum)) / (WoShdgHoriz(SurfNum) + Eps)

        # Get IR view factors. An exterior surface can receive IR radiation from
        # sky, ground or shadowing surfaces. Assume shadowing surfaces have same
        # temperature as outside air (and therefore same temperature as ground),
        # so that the view factor to these shadowing surfaces can be included in
        # the ground view factor. Sky IR is assumed to be isotropic and shadowing
        # surfaces are assumed to be opaque to IR so they totally "shade" IR from
        # sky or ground.

        for SurfNum in range(1, TotSurfaces+1):
            if (!DetailedSkyDiffuseAlgorithm || !ShadingTransmittanceVaries || SolarDistribution == MinimalShadowing):
                Surface(SurfNum).ViewFactorSkyIR *= DifShdgRatioIsoSky(SurfNum)
            else:
                Surface(SurfNum).ViewFactorSkyIR *= DifShdgRatioIsoSkyHRTS(1, 1, SurfNum)
            
            Surface(SurfNum).ViewFactorGroundIR = 1.0 - Surface(SurfNum).ViewFactorSkyIR

            if (Surface(SurfNum).HasSurroundingSurfProperties):
                SrdSurfsNum = Surface(SurfNum).SurroundingSurfacesNum
                if (SurroundingSurfsProperty(SrdSurfsNum).SkyViewFactor != -1):
                    Surface(SurfNum).ViewFactorSkyIR *= SurroundingSurfsProperty(SrdSurfsNum).SkyViewFactor
                
                if (SurroundingSurfsProperty(SrdSurfsNum).GroundViewFactor != -1):
                    Surface(SurfNum).ViewFactorGroundIR *= SurroundingSurfsProperty(SrdSurfsNum).GroundViewFactor

        #  DEALLOCATE(WithShdgIsoSky)
        #  DEALLOCATE(WoShdgIsoSky)
        #  DEALLOCATE(WithShdgHoriz)
        #  DEALLOCATE(WoShdgHoriz)

        if (DetailedSkyDiffuseAlgorithm && ShadingTransmittanceVaries && SolarDistribution != MinimalShadowing):
            for SurfNum in range(1, TotSurfaces+1):
                DifShdgRatioIsoSkyHRTS({1, NumOfTimeStepInHour}, {1, 24}, SurfNum) = DifShdgRatioIsoSky(SurfNum)
                DifShdgRatioHorizHRTS({1, NumOfTimeStepInHour}, {1, 24}, SurfNum) = DifShdgRatioHoriz(SurfNum)

    	return None

	def ReportSurfaceShading():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda Lawrie
              DATE WRITTEN   April 2000
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine uses the internal variables used in the Shading
        calculations and prepares them for reporting (at timestep level).

        METHODOLOGY EMPLOYED:
        Because all of the calculations are done on a "daily" basis in this
        module, it is difficult to formulate the values that might be useful
        for reporting.  SunlitFrac was the first of these two arrays to be
        made into "two dimensions".  It is not clear that both have to be
        two dimensions.

        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using namespace OutputReportPredefined

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        # na

        # SUBROUTINE PARAMETER DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        SurfNum = 0 # Loop Counter
        RepCol = 0  # the column of the predefined report

        for SurfNum in range(1, TotSurfaces+1):
            SurfSunlitFrac(SurfNum) = SunlitFrac(TimeStep, HourOfDay, SurfNum)
            SurfSunlitArea(SurfNum) = SunlitFrac(TimeStep, HourOfDay, SurfNum) * Surface(SurfNum).Area
        
        # added for predefined reporting
        RepCol = 0
        if (Month == 3 && DayOfMonth == 21):
            if ((HourOfDay == 9) && (TimeStep == 4)):
                RepCol = pdchSlfMar21_9
            elif ((HourOfDay == 12) && (TimeStep == 4)):
                RepCol = pdchSlfMar21_12
            elif ((HourOfDay == 15) && (TimeStep == 4)):
                RepCol = pdchSlfMar21_15
        elif (Month == 6 && DayOfMonth == 21):
            if ((HourOfDay == 9) && (TimeStep == 4)):
                RepCol = pdchSlfJun21_9
            elif ((HourOfDay == 12) && (TimeStep == 4)):
                RepCol = pdchSlfJun21_12
            elif ((HourOfDay == 15) && (TimeStep == 4)):
                RepCol = pdchSlfJun21_15
        elif (Month == 12 && DayOfMonth == 21):
            if ((HourOfDay == 9) && (TimeStep == 4)):
                RepCol = pdchSlfDec21_9
            elif ((HourOfDay == 12) && (TimeStep == 4)):
                RepCol = pdchSlfDec21_12
            elif ((HourOfDay == 15) && (TimeStep == 4)):
                RepCol = pdchSlfDec21_15
        
        if (RepCol != 0):
            for SurfNum in range(1, TotSurfaces+1):
                if (Surface(SurfNum).Class == SurfaceClass_Window):
                    PreDefTableEntry(RepCol, Surface(SurfNum).Name, SurfSunlitFrac(SurfNum))
        
    	return None

    def ReportSurfaceErrors():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda Lawrie
              DATE WRITTEN   November 2004
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine reports some recurring type errors that can get mixed up with more important
        errors in the error file.

        METHODOLOGY EMPLOYED:
        # na

        REFERENCES:
        # na
        '''

        # Using/Aliasing
        using namespace DataErrorTracking # for error tracking
        using General::RoundSigDigits

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        # na

        # SUBROUTINE PARAMETER DEFINITIONS:
        static Array1D_string const MSG(4, {"misses", "", "within", "overlaps"})

        # INTERFACE BLOCK SPECIFICATIONS
        # na

        # DERIVED TYPE DEFINITIONS
        # na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        Loop1 = 0
        Loop2 = 0
        Count = 0
        TotCount = 0
        std::string CountOut
        Array1D_bool SurfErrorReported
        Array1D_bool SurfErrorReported2

        if (NumTooManyFigures + NumTooManyVertices + NumBaseSubSurround > 0):
            print("\n===== Recurring Surface Error Summary =====")
            print("The following surface error messages occurred.\n")

            if (NumBaseSubSurround > 0):
                print("Base Surface does not surround subsurface errors occuring...")
                print("Check that the GlobalGeometryRules object is expressing the proper starting corner and direction [CounterClockwise/Clockwise]\n")

            SurfErrorReported.dimension(TotSurfaces, False)
            TotCount = 0
            for Loop1 in range(1, NumBaseSubSurround+1):
                Count = 0
                if (SurfErrorReported(TrackBaseSubSurround(Loop1).SurfIndex1)): continue
                
                for Loop2 in range(1, NumBaseSubSurround+1):
                    if (TrackBaseSubSurround(Loop1).SurfIndex1 == TrackBaseSubSurround(Loop2).SurfIndex1 &&
                        TrackBaseSubSurround(Loop1).MiscIndex == TrackBaseSubSurround(Loop2).MiscIndex):
                        Count += 1

                gio::write(CountOut, fmtLD) << Count
                TotCount += Count
                TotalWarningErrors += Count - 1
                raise RunTimeWarning("Base surface does not surround subsurface (CHKSBS), Overlap Status=" +
                                 cOverLapStatus(TrackBaseSubSurround(Loop1).MiscIndex))
                ShowContinueError("  The base surround errors occurred " + stripped(CountOut) + " times.")
                
                for (Loop2 = 1 Loop2 <= NumBaseSubSurround ++Loop2):
                    if (TrackBaseSubSurround(Loop1).SurfIndex1 == TrackBaseSubSurround(Loop2).SurfIndex1 &&
                        TrackBaseSubSurround(Loop1).MiscIndex == TrackBaseSubSurround(Loop2).MiscIndex):
                        ShowContinueError("Surface \"" + Surface(TrackBaseSubSurround(Loop1).SurfIndex1).Name + "\" " +
                                          MSG(TrackBaseSubSurround(Loop1).MiscIndex) + " SubSurface \"" +
                                          Surface(TrackBaseSubSurround(Loop2).SurfIndex2).Name + "\"")
                
                SurfErrorReported(TrackBaseSubSurround(Loop1).SurfIndex1) = True
            
            if (TotCount > 0):
                print("")
                gio::write(CountOut, fmtLD) << TotCount
                ShowContinueError("  The base surround errors occurred " + stripped(CountOut) + " times (total).")
                print("")

            SurfErrorReported2.allocate(TotSurfaces)
            SurfErrorReported = False
            TotCount = 0
            if (NumTooManyVertices > 0):
                print("Too many vertices [>=" + RoundSigDigits(MaxHCV) + "] in shadow overlap errors occurring...")
                print("These occur throughout the year and may occur several times for the same surfaces. You may be able to reduce them by "
                            "adding Output:Diagnostics,DoNotMirrorDetachedShading")

            for (Loop1 = 1 Loop1 <= NumTooManyVertices ++Loop1):
                Count = 0
                SurfErrorReported2 = False
                if (SurfErrorReported(TrackTooManyVertices(Loop1).SurfIndex1)): continue
                
                for (Loop2 = 1 Loop2 <= NumTooManyVertices ++Loop2):
                    if (TrackTooManyVertices(Loop1).SurfIndex1 == TrackTooManyVertices(Loop2).SurfIndex1):
                        ++Count
                
                gio::write(CountOut, fmtLD) << Count
                TotCount += Count
                TotalWarningErrors += Count - 1
                print("")
                raise RunTimeWarning("Too many vertices [>=" + RoundSigDigits(MaxHCV) + "] in a shadow overlap")
                ShowContinueError("Overlapping figure=" + Surface(TrackTooManyVertices(Loop1).SurfIndex1).Name + ", Surface Class=[" +
                                  cSurfaceClass(Surface(TrackTooManyVertices(Loop1).SurfIndex1).Class) + ']')
                ShowContinueError("  This error occurred " + stripped(CountOut) + " times.")
                
                for (Loop2 = 1 Loop2 <= NumTooManyVertices ++Loop2):
                    if (TrackTooManyVertices(Loop1).SurfIndex1 == TrackTooManyVertices(Loop2).SurfIndex1):
                        if (SurfErrorReported2(TrackTooManyVertices(Loop2).SurfIndex2)): continue
                        
                        ShowContinueError("Figure being Overlapped=" + Surface(TrackTooManyVertices(Loop2).SurfIndex2).Name + ", Surface Class=[" +
                                          cSurfaceClass(Surface(TrackTooManyVertices(Loop2).SurfIndex2).Class) + ']')
                        SurfErrorReported2(TrackTooManyVertices(Loop2).SurfIndex2) = True
                
                SurfErrorReported(TrackTooManyVertices(Loop1).SurfIndex1) = True
            
            if (TotCount > 0):
                print("")
                gio::write(CountOut, fmtLD) << TotCount
                ShowContinueError("  The too many vertices errors occurred " + stripped(CountOut) + " times (total).")
                print("")

            SurfErrorReported = False
            TotCount = 0
            if (NumTooManyFigures > 0):
                print("Too many figures [>=" + RoundSigDigits(MaxHCS) + "] in shadow overlap errors occurring...")
                print("These occur throughout the year and may occur several times for the same surfaces. You may be able to reduce them by "
                            "adding OutputDiagnostics,DoNotMirrorDetachedShading")
            
            for (Loop1 = 1 Loop1 <= NumTooManyFigures ++Loop1):
                Count = 0
                SurfErrorReported2 = False
                if (SurfErrorReported(TrackTooManyFigures(Loop1).SurfIndex1)): continue
                
                for (Loop2 = 1 Loop2 <= NumTooManyFigures ++Loop2):
                    if (TrackTooManyFigures(Loop1).SurfIndex1 == TrackTooManyFigures(Loop2).SurfIndex1):
                        ++Count
                
                gio::write(CountOut, fmtLD) << Count
                TotCount += Count
                TotalWarningErrors += Count - 1
                print("")
                raise RunTimeWarning("Too many figures [>={}] in a shadow overlap".format(RoundSigDigits(MaxHCS)))
                ShowContinueError("Overlapping figure={}, Surface Class=[{}]".format(Surface(TrackTooManyFigures(Loop1).SurfIndex1).Name, cSurfaceClass(Surface(TrackTooManyFigures(Loop1).SurfIndex1).Class)))
                ShowContinueError("\tThis error occurred {} times.".format(stripped(CountOut)))
                
                for Loop2 in range(1, NumTooManyFigures+1):
                    if (TrackTooManyFigures(Loop1).SurfIndex1 == TrackTooManyFigures(Loop2).SurfIndex1):
                        if (SurfErrorReported2(TrackTooManyFigures(Loop2).SurfIndex2)): continue

                        ShowContinueError("Figure being Overlapped=" + Surface(TrackTooManyFigures(Loop2).SurfIndex2).Name + ", Surface Class=[" +
                                          cSurfaceClass(Surface(TrackTooManyFigures(Loop2).SurfIndex2).Class) + ']')
                        SurfErrorReported2(TrackTooManyFigures(Loop2).SurfIndex2) = True
                
                SurfErrorReported(TrackTooManyFigures(Loop1).SurfIndex1) = True
            
            if (TotCount > 0):
                print("")
                gio::write(CountOut, fmtLD) << TotCount
                ShowContinueError("\tThe too many figures errors occurred {} times (total).".format(stripped(CountOut)))
                print("")
            
            SurfErrorReported.deallocate()
            SurfErrorReported2.deallocate()
        
    	return None

# end of SolarCalculations
