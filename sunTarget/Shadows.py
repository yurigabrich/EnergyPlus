'''
Copyright (C) 2018 - 2019
Yuri Bastos Gabrich <yuribgabrich[at]gmail.com>

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

SPDX-License-Identifier: BSD-3-Clause
For more information check at: https://spdx.org/licenses/BSD-3-Clause.html
'''

# The Python version considers only the functions related to surface objects.
# ------------------------------------------
# SURFACE = WALL, ROOF, floor, or a ceiling
# SUBSURFACE = window, door, or glassdoor
# A BACK SURFACE – an inside surface – is one that may be partially sunlit/receive solar transmission for interior solar distribution.
# ------------------------------------------

import math
import pandas as pd
from collections import namedtuple
from enum import Enum

class ExternalFunctions:
	'''
	Definition of a variety of additional functions from another packages.
	Only those useful for the following computations was copied to here.
    Nontheless, some are particularly defined inside other 'class' statement.
	'''

	# DataGlobals.cc
    BeginSimFlag = False        # True until any actual simulation (full or sizing) has begun, False after first time step
    NumOfZones = 0              # Total number of Zones for simulation
    KickOffSimulation = False   # Kick off simulation -- meaning run each environment for 1 or 2 time steps.
    KickOffSizing = False       # Kick off sizing -- meaning run each environment for 1 or 2 time steps.
    WarmupFlag = False          # True during the warmup portion of a simulation
    BeginDayFlag = False        # True at the start of each day, False after first time step in day
    DoingSizing = False         # TRUE when "sizing" is being performed (some error messages won't be displayed)
    DoWeathSim = False          # User input in SimulationControl object
    DoDesDaySim = False         # User input in SimulationControl object
    KindOfSim = 0               # See parameters. (ksDesignDay, ksRunPeriodDesign, ksRunPeriodWeather)
    ksRunPeriodWeather = 3      # one of the parameters for KindOfSim
    HourOfDay = 0               # Counter for hours in a simulation day
    TimeStep = 0                # Counter for time steps (fractional hours)

    # DataStringGlobals::outputShdFileName
	outputShdFileName = 'eplusout.shd'     # file to save the simulations result

	# DataShadowingCombinations.hh
    ShadowingCombinations_ = namedtuple('ShadowingCombinations_', ['UseThisSurf', 'NumGenSurf', 'GenSurf', 'NumBackSurf', 'BackSurf', 'NumSubSurf', 'SubSurf'])
    ShadowingCombinations = ShadowingCombinations_(UseThisSurf=False, NumGenSurf=0, GenSurf=pd.Series(), NumBackSurf=0, BackSurf=pd.Series(), NumSubSurf=0, SubSurf=pd.Series())
    '''
        // Members
        bool UseThisSurf;     // True when this surface should be used in calculations
        int NumGenSurf;       // Number of General surfaces for this surf
        GenSurf = pd.Series()  // Array of General Surface Numbers
        int NumBackSurf;      // Number of Back (Interior) surfaces for this surf
        BackSurf = pd.Series() // Array of Back (Interior) surface numbers
        int NumSubSurf;       // Number of SubSurfaces for this surf
        SubSurf = pd.Series() // Array of SubSurface surface Numbers

        // Default Constructor
        ShadowingCombinations() : UseThisSurf(false), NumGenSurf(0), NumBackSurf(0), NumSubSurf(0)
        {
        }
    '''

    # DataShadowingCombinations.cc
	ShadowComb = pd.Series()

	# DataHeatBalance.hh
    ZoneListData_ = namedtuple('ZoneListData', ['Name', 'NumOfZones', 'MaxZoneNameLength', 'Zone'])
    ZoneListData = ZoneListData_(Name="", NumOfZones=0, MaxZoneNameLength=0, Zone=pd.Series())
    '''
        // Members
        std::string Name;                         // Zone List name
        int NumOfZones;                           // Number of zones in the list
        std::string::size_type MaxZoneNameLength; // Max Name length of zones in the list
        Zone = pd.Series()                        // Pointers to zones in the list

        // Default Constructor
        ZoneListData() : NumOfZones(0), MaxZoneNameLength(0u)
        {
        }
    '''

    ConstructionData_ = namedtuple('ConstructionData', ['Name', 'TotLayers', 'TotSolidLayers', 'TotGlassLayers', 'LayerPoint', 'IsUsed', 'IsUsedCTF',
                                   'InsideAbsorpVis', 'OutsideAbsorpVis', 'InsideAbsorpSolar', 'OutsideAbsorpSolar', 'InsideAbsorpThermal', 'OutsideAbsorpThermal',
                                   'OutsideRoughness', 'DayltPropPtr', 'W5FrameDivider', 'CTFCross', 'CTFFlux', 'CTFInside', 'CTFOutside', 'CTFSourceIn',
                                   'CTFSourceOut', 'CTFTimeStep', 'CTFSourceOut', 'CTFSourceIn', 'CTFTSourceQ', 'CTFTUserOut', 'CTFTUserIn', 'CTFTUserSource',
                                   'NumHistories', 'NumCTFTerms', 'UValue', 'SolutionDimensions', 'SourceAfterLayer', 'TempAfterLayer', 'ThicknessPerpend',
                                   'AbsDiffIn', 'AbsDiffOut', 'AbsDiff', 'BlAbsDiff', 'BlAbsDiffGnd', 'BlAbsDiffSky', 'AbsDiffBack', 'BlAbsDiffBack', 'AbsDiffShade',
                                   'AbsDiffBlind', 'AbsDiffBlindGnd', 'AbsDiffBlindSky', 'AbsDiffBackShade', 'AbsDiffBackBlind', 'ShadeAbsorpThermal', 'AbsBeamCoef',
                                   'AbsBeamBackCoef', 'AbsBeamShadeCoef', 'TransDiff', 'BlTransDiff', 'BlTransDiffGnd', 'BlTransDiffSky', 'TransDiffVis',
                                   'BlTransDiffVis', 'ReflectSolDiffBack', 'BlReflectSolDiffBack', 'ReflectSolDiffFront', 'BlReflectSolDiffFront', 'ReflectVisDiffBack',
                                   'BlReflectVisDiffBack', 'ReflectVisDiffFront', 'BlReflectVisDiffFront', 'TransSolBeamCoef', 'TransVisBeamCoef', 'ReflSolBeamFrontCoef',
                                   'ReflSolBeamBackCoef', 'tBareSolCoef', 'tBareVisCoef', 'rfBareSolCoef', 'rfBareVisCoef', 'rbBareSolCoef', 'rbBareVisCoef',
                                   'afBareSolCoef', 'abBareSolCoef', 'tBareSolDiff', 'tBareVisDiff', 'rfBareSolDiff', 'rfBareVisDiff', 'rbBareSolDiff', 'rbBareVisDiff',
                                   'afBareSolDiff', 'abBareSolDiff', 'FromWindow5DataFile', 'W5FileMullionWidth', 'W5FileMullionOrientation', 'W5FileGlazingSysWidth',
                                   'W5FileGlazingSysHeight', 'SummerSHGC', 'VisTransNorm', 'SolTransNorm', 'SourceSinkPresent', 'TypeIsWindow', 'WindowTypeBSDF',
                                   'TypeIsEcoRoof', 'TypeIsIRT', 'TypeIsCfactorWall', 'TypeIsFfactorFloor', 'TCFlag', 'TCMasterConst', 'TCLayerID', 'TCGlassID',
                                   'CFactor', 'Height', 'FFactor', 'Area', 'PerimeterExposed', 'ReverseConstructionNumLayersWarning', 'ReverseConstructionLayersOrderWarning'])
    ConstructionData = ConstructionData_(Name=?, TotLayers=0, TotSolidLayers=0, TotGlassLayers=0, LayerPoint=(MaxLayersInConstruct, 0), IsUsed=False, IsUsedCTF=False,
                                         InsideAbsorpVis=0.0, OutsideAbsorpVis=0.0, InsideAbsorpSolar=0.0, OutsideAbsorpSolar=0.0, InsideAbsorpThermal=0.0,
                                         OutsideAbsorpThermal=0.0, OutsideRoughness=0, DayltPropPtr=0, W5FrameDivider=0, CTFCross=({0, MaxCTFTerms - 1}, 0.0),
                                         CTFFlux=(MaxCTFTerms - 1, 0.0), CTFInside=({0, MaxCTFTerms - 1}, 0.0), CTFOutside=({0, MaxCTFTerms - 1}, 0.0),
                                         CTFSourceIn=({0, MaxCTFTerms - 1}, 0.0), CTFSourceOut=({0, MaxCTFTerms - 1}, 0.0), CTFTimeStep=?, CTFSourceOut=({0, MaxCTFTerms - 1}, 0.0),
                                         CTFSourceIn=({0, MaxCTFTerms - 1}, 0.0), CTFTSourceQ=?, CTFTUserOut=?, CTFTUserIn=?, CTFTUserSource=?, NumHistories=0, NumCTFTerms=0,
                                         UValue=0.0, SolutionDimensions=0, SourceAfterLayer=0, TempAfterLayer=0, ThicknessPerpend=0, AbsDiffIn=0.0, AbsDiffOut=0.0,
                                         AbsDiff=(MaxSolidWinLayers, 0.0), BlAbsDiff=(MaxSlatAngs, MaxSolidWinLayers, 0.0), BlAbsDiffGnd=(MaxSlatAngs, MaxSolidWinLayers, 0.0),
                                         BlAbsDiffSky=(MaxSlatAngs, MaxSolidWinLayers, 0.0), AbsDiffBack=(MaxSolidWinLayers, 0.0), BlAbsDiffBack=(MaxSlatAngs, MaxSolidWinLayers, 0.0),
                                         AbsDiffShade=0.0, AbsDiffBlind=(MaxSlatAngs, 0.0), AbsDiffBlindGnd=(MaxSlatAngs, 0.0), AbsDiffBlindSky=(MaxSlatAngs, 0.0), AbsDiffBackShade=0.0,
                                         AbsDiffBackBlind=(MaxSlatAngs, 0.0), ShadeAbsorpThermal=0.0, AbsBeamCoef=(6, MaxSolidWinLayers, 0.0), AbsBeamBackCoef=(6, MaxSolidWinLayers, 0.0),
                                         AbsBeamShadeCoef=(6, 0.0), TransDiff=0.0, BlTransDiff=(MaxSlatAngs, 0.0), BlTransDiffGnd=(MaxSlatAngs, 0.0), BlTransDiffSky=(MaxSlatAngs, 0.0),
                                         TransDiffVis=0.0, BlTransDiffVis=(MaxSlatAngs, 0.0), ReflectSolDiffBack=0.0, BlReflectSolDiffBack=(MaxSlatAngs, 0.0), ReflectSolDiffFront=0.0,
                                         BlReflectSolDiffFront=(MaxSlatAngs, 0.0), ReflectVisDiffBack=0.0, BlReflectVisDiffBack=(MaxSlatAngs, 0.0), ReflectVisDiffFront=0.0,
                                         BlReflectVisDiffFront=(MaxSlatAngs, 0.0), TransSolBeamCoef=(6, 0.0), TransVisBeamCoef=(6, 0.0), ReflSolBeamFrontCoef=(6, 0.0),
                                         ReflSolBeamBackCoef=(6, 0.0), tBareSolCoef=(6, 5, 0.0), tBareVisCoef=(6, 5, 0.0), rfBareSolCoef=(6, 5, 0.0), rfBareVisCoef=(6, 5, 0.0),
                                         rbBareSolCoef=(6, 5, 0.0), rbBareVisCoef=(6, 5, 0.0), afBareSolCoef=(6, 5, 0.0), abBareSolCoef=(6, 5, 0.0), tBareSolDiff=(5, 0.0),
                                         tBareVisDiff=(5, 0.0), rfBareSolDiff=(5, 0.0), rfBareVisDiff=(5, 0.0), rbBareSolDiff=(5, 0.0), rbBareVisDiff=(5, 0.0), afBareSolDiff=(5, 0.0),
                                         abBareSolDiff=(5, 0.0), FromWindow5DataFile=False, W5FileMullionWidth=0.0, W5FileMullionOrientation=0, W5FileGlazingSysWidth=0.0,
                                         W5FileGlazingSysHeight=0.0, SummerSHGC=0.0, VisTransNorm=0.0, SolTransNorm=0.0, SourceSinkPresent=False, TypeIsWindow=False, WindowTypeBSDF=False,
                                         TypeIsEcoRoof=False, TypeIsIRT=False, TypeIsCfactorWall=False, TypeIsFfactorFloor=False, TCFlag=0, TCMasterConst=0, TCLayerID=0, TCGlassID=0,
                                         CFactor=0.0, Height=0.0, FFactor=0.0, Area=0.0, PerimeterExposed=0.0, ReverseConstructionNumLayersWarning=False, ReverseConstructionLayersOrderWarning=False)
    '''
        // Members
        std::string Name; // Name of construction
        int TotLayers;    // Total number of layers for the construction; for windows
                          //  this is the total of the glass, gas and shade layers
        int TotSolidLayers;     // Total number of solid (glass or shade) layers (windows only)
        int TotGlassLayers;     // Total number of glass layers (windows only)
        Array1D_int LayerPoint; // Pointer array which refers back to
                                // the Material structure; LayerPoint(i)=j->Material(j)%Name,etc
        bool IsUsed;                // Marked true when the construction is used
        bool IsUsedCTF;             // Mark true when the construction is used for a surface with CTF calculations
        Real64 InsideAbsorpVis;     // Inside Layer visible absorptance of an opaque surface; not used for windows.
        Real64 OutsideAbsorpVis;    // Outside Layer visible absorptance of an opaque surface; not used for windows.
        Real64 InsideAbsorpSolar;   // Inside Layer solar absorptance of an opaque surface; not used for windows.
        Real64 OutsideAbsorpSolar;  // Outside Layer solar absorptance of an opaque surface; not used for windows.
        Real64 InsideAbsorpThermal; // Inside Layer Thermal absorptance for opaque surfaces or windows;
                                    // for windows, applies to innermost glass layer
        Real64 OutsideAbsorpThermal; // Outside Layer Thermal absorptance
        int OutsideRoughness;        // Outside Surface roughness index (6=very smooth, 5=smooth,
                                     // 4=medium smooth, 3=medium rough, 2=rough, 1=very rough)
        int DayltPropPtr;   // Pointer to Daylight Construction Properties
        int W5FrameDivider; // FrameDivider number for window construction from Window5 data file;
                            //  zero is construction not from Window5 file or Window5 construction has no frame.
                            // Conductive properties for the construction
        Array1D<Real64> CTFCross;     // Cross or Y terms of the CTF equation
        Array1D<Real64> CTFFlux;      // Flux history terms of the CTF equation
        Array1D<Real64> CTFInside;    // Inside or Z terms of the CTF equation
        Array1D<Real64> CTFOutside;   // Outside or X terms of the CTF equation
        Array1D<Real64> CTFSourceIn;  // Heat source/sink inside terms of CTF equation
        Array1D<Real64> CTFSourceOut; // Heat source/sink outside terms of CTF equation
        Real64 CTFTimeStep;           // Time increment for stable simulation of construct (could be greater than TimeStep)
                                      // The next three series of terms are used to calculate the temperature at the location of a source/sink
                                      // in the QTF formulation.  This calculation is necessary to allow the proper simulation of a
                                      // radiant system.
        Array1D<Real64> CTFTSourceOut; // Outside terms of the CTF equation for interior temp
                                       // calc@source location
        Array1D<Real64> CTFTSourceIn; // Inside terms of the CTF equation for interior temp
                                      // calc@source location
        Array1D<Real64> CTFTSourceQ; // Source/sink terms of the CTF equation for interior temp
                                     // calc@source location
                                     // The next three series of terms are used to calculate the temperature at a location specified by the user.
                                     // This location must be between two layers and is intended to allow the user to evaluate whether or not
                                     // condensation is a possibility between material layers.
        Array1D<Real64> CTFTUserOut; // Outside terms of the CTF equation for interior temp
                                     // calc@user location
        Array1D<Real64> CTFTUserIn; // Inside terms of the CTF equation for interior temp
                                    // calc@user location
        Array1D<Real64> CTFTUserSource; // Source/sink terms of the CTF equation for interior temp
                                        // calc@user location
        int NumHistories; // CTFTimeStep/TimeStepZone or the number of temp/flux history series
                          // for the construction
        int NumCTFTerms;        // Number of CTF terms for this construction (not including terms at current time)
        Real64 UValue;          // Overall heat transfer coefficient for the construction
        int SolutionDimensions; // Number of dimensions in the solution (1 for normal constructions,
                                // 1 or 2 for constructions with sources or sinks)-->may allow 3-D later?
        int SourceAfterLayer;    // Source/sink is present after this layer in the construction
        int TempAfterLayer;      // User is requesting a temperature calculation after this layer in the construction
        Real64 ThicknessPerpend; // Thickness between planes of symmetry in the direction
                                 // perpendicular to the main direction of heat transfer
                                 // (same as half the distance between tubes)
                                 // Moisture Transfer Functions term belong here as well
                                 // BLAST detailed solar model parameters
        Real64 AbsDiffIn;  // Inner absorptance coefficient for diffuse radiation
        Real64 AbsDiffOut; // Outer absorptance coefficient for diffuse radiation
                           // Variables for window constructions
        Array1D<Real64> AbsDiff; // Diffuse solar absorptance for each glass layer,
                                 // bare glass or shade on
        Array2D<Real64> BlAbsDiff; // Diffuse solar absorptance for each glass layer vs.
                                   // slat angle, blind on
        Array2D<Real64> BlAbsDiffGnd; // Diffuse ground solar absorptance for each glass layer
                                      // vs. slat angle, blind on
        Array2D<Real64> BlAbsDiffSky; // Diffuse sky solar absorptance for each glass layer
                                      // vs. slat angle, blind on
        Array1D<Real64> AbsDiffBack;   // Diffuse back solar absorptance for each glass layer
        Array2D<Real64> BlAbsDiffBack; // Diffuse back solar absorptance for each glass layer,
                                       //  vs. slat angle, blind on
        Real64 AbsDiffShade;              // Diffuse solar absorptance for shade
        Array1D<Real64> AbsDiffBlind;     // Diffuse solar absorptance for blind, vs. slat angle
        Array1D<Real64> AbsDiffBlindGnd;  // Diffuse ground solar absorptance for blind, vs. slat angle
        Array1D<Real64> AbsDiffBlindSky;  // Diffuse sky solar absorptance for blind, vs. slat angle
        Real64 AbsDiffBackShade;          // Diffuse back solar absorptance for shade
        Array1D<Real64> AbsDiffBackBlind; // Diffuse back solar absorptance for blind, vs. slat angle
        Real64 ShadeAbsorpThermal;        // Diffuse back thermal absorptance of shade
        Array2D<Real64> AbsBeamCoef;      // Coefficients of incidence-angle polynomial for solar
                                          // absorptance for each solid glazing layer
        Array2D<Real64> AbsBeamBackCoef;  // As for AbsBeamCoef but for back-incident solar
        Array1D<Real64> AbsBeamShadeCoef; // Coefficients of incidence-angle polynomial for solar
                                          // absorptance of shade
        Real64 TransDiff;                      // Diffuse solar transmittance, bare glass or shade on
        Array1D<Real64> BlTransDiff;           // Diffuse solar transmittance, blind present, vs. slat angle
        Array1D<Real64> BlTransDiffGnd;        // Ground diffuse solar transmittance, blind present, vs. slat angle
        Array1D<Real64> BlTransDiffSky;        // Sky diffuse solar transmittance, blind present, vs. slat angle
        Real64 TransDiffVis;                   // Diffuse visible transmittance, bare glass or shade on
        Array1D<Real64> BlTransDiffVis;        // Diffuse visible transmittance, blind present, vs. slat angle
        Real64 ReflectSolDiffBack;             // Diffuse back solar reflectance, bare glass or shade on
        Array1D<Real64> BlReflectSolDiffBack;  // Diffuse back solar reflectance, blind present, vs. slat angle
        Real64 ReflectSolDiffFront;            // Diffuse front solar reflectance, bare glass or shade on
        Array1D<Real64> BlReflectSolDiffFront; // Diffuse front solar reflectance, blind present, vs. slat angle
        Real64 ReflectVisDiffBack;             // Diffuse back visible reflectance, bare glass or shade on
        Array1D<Real64> BlReflectVisDiffBack;  // Diffuse back visible reflectance, blind present, vs. slat angle
        Real64 ReflectVisDiffFront;            // Diffuse front visible reflectance, bare glass or shade on
        Array1D<Real64> BlReflectVisDiffFront; // Diffuse front visible reflectance, blind present, vs. slat angle
        Array1D<Real64> TransSolBeamCoef;      // Coeffs of incidence-angle polynomial for beam sol trans,
                                               // bare glass or shade on
        Array1D<Real64> TransVisBeamCoef; // Coeffs of incidence-angle polynomial for beam vis trans,
                                          // bare glass or shade on
        Array1D<Real64> ReflSolBeamFrontCoef; // Coeffs of incidence-angle polynomial for beam sol front refl,
                                              // bare glass or shade on
        Array1D<Real64> ReflSolBeamBackCoef; // Like ReflSolBeamFrontCoef, but for back-incident beam solar
        Array2D<Real64> tBareSolCoef;        // Isolated glass solar transmittance coeffs of inc. angle polynomial
        Array2D<Real64> tBareVisCoef;        // Isolated glass visible transmittance coeffs of inc. angle polynomial
        Array2D<Real64> rfBareSolCoef;       // Isolated glass front solar reflectance coeffs of inc. angle polynomial
        Array2D<Real64> rfBareVisCoef;       // Isolated glass front visible reflectance coeffs of inc. angle polynomial
        Array2D<Real64> rbBareSolCoef;       // Isolated glass back solar reflectance coeffs of inc. angle polynomial
        Array2D<Real64> rbBareVisCoef;       // Isolated glass back visible reflectance coeffs of inc. angle polynomial
        Array2D<Real64> afBareSolCoef;       // Isolated glass front solar absorptance coeffs of inc. angle polynomial
        Array2D<Real64> abBareSolCoef;       // Isolated glass back solar absorptance coeffs of inc. angle polynomial
        Array1D<Real64> tBareSolDiff;        // Isolated glass diffuse solar transmittance
        Array1D<Real64> tBareVisDiff;        // Isolated glass diffuse visible transmittance
        Array1D<Real64> rfBareSolDiff;       // Isolated glass diffuse solar front reflectance
        Array1D<Real64> rfBareVisDiff;       // Isolated glass diffuse visible front reflectance
        Array1D<Real64> rbBareSolDiff;       // Isolated glass diffuse solar back reflectance
        Array1D<Real64> rbBareVisDiff;       // Isolated glass diffuse visible back reflectance
        Array1D<Real64> afBareSolDiff;       // Isolated glass diffuse solar front absorptance
        Array1D<Real64> abBareSolDiff;       // Isolated glass diffuse solar back absorptance
        bool FromWindow5DataFile;            // True if this is a window construction extracted from the Window5 data file
        Real64 W5FileMullionWidth;           // Width of mullion for construction from Window5 data file (m)
        int W5FileMullionOrientation;        // Orientation of mullion, if present, for Window5 data file construction,
        Real64 W5FileGlazingSysWidth;        // Glass width for construction from Window5 data file (m)
        Real64 W5FileGlazingSysHeight;       // Glass height for construction form Window5 data file (m)
        Real64 SummerSHGC;                   // Calculated ASHRAE SHGC for summer conditions
        Real64 VisTransNorm;                 // The normal visible transmittance
        Real64 SolTransNorm;                 // the normal solar transmittance
        bool SourceSinkPresent;              // .TRUE. if there is a source/sink within this construction
        bool TypeIsWindow;                   // True if a window construction, false otherwise
        bool WindowTypeBSDF;                 // True for complex window, false otherwise
        bool TypeIsEcoRoof;                  // -- true for construction with ecoRoof outside, the flag
                                             //-- is turned on when the outside layer is of type EcoRoof
        bool TypeIsIRT;          // -- true for construction with IRT material
        bool TypeIsCfactorWall;  // -- true for construction with Construction:CfactorUndergroundWall
        bool TypeIsFfactorFloor; // -- true for construction with Construction:FfactorGroundFloor
        
        // Added TH 12/22/2008 for thermochromic windows
        int TCFlag; // 0: this construction is not a thermochromic window construction
                    // 1: it is a TC window construction
        int TCLayer;       // Reference to the TC glazing material layer in the Material array
        int TCMasterConst; // The master TC construction referenced by its slave constructions
        int TCLayerID;     // Which material layer is the TC glazing, counting all material layers.
        int TCGlassID;     // Which glass layer is the TC glazing, counting from glass layers only.
        
        // For CFactor underground walls
        Real64 CFactor;
        Real64 Height;
        
        // For FFactor slabs-on-grade or underground floors
        Real64 FFactor;
        Real64 Area;
        Real64 PerimeterExposed;
        bool ReverseConstructionNumLayersWarning;
        bool ReverseConstructionLayersOrderWarning;

        // Default Constructor
        ConstructionData()
            : TotLayers(0), TotSolidLayers(0), TotGlassLayers(0), LayerPoint(MaxLayersInConstruct, 0), IsUsed(false), IsUsedCTF(false),
              InsideAbsorpVis(0.0), OutsideAbsorpVis(0.0), InsideAbsorpSolar(0.0), OutsideAbsorpSolar(0.0), InsideAbsorpThermal(0.0),
              OutsideAbsorpThermal(0.0), OutsideRoughness(0), DayltPropPtr(0), W5FrameDivider(0), CTFCross({0, MaxCTFTerms - 1}, 0.0),
              CTFFlux(MaxCTFTerms - 1, 0.0), CTFInside({0, MaxCTFTerms - 1}, 0.0), CTFOutside({0, MaxCTFTerms - 1}, 0.0),
              CTFSourceIn({0, MaxCTFTerms - 1}, 0.0), CTFSourceOut({0, MaxCTFTerms - 1}, 0.0), CTFTSourceOut({0, MaxCTFTerms - 1}, 0.0),
              CTFTSourceIn({0, MaxCTFTerms - 1}, 0.0), CTFTSourceQ({0, MaxCTFTerms - 1}, 0.0), CTFTUserOut({0, MaxCTFTerms - 1}, 0.0),
              CTFTUserIn({0, MaxCTFTerms - 1}, 0.0), CTFTUserSource({0, MaxCTFTerms - 1}, 0.0), NumHistories(0), NumCTFTerms(0), UValue(0.0),
              SolutionDimensions(0), SourceAfterLayer(0), TempAfterLayer(0), ThicknessPerpend(0.0), AbsDiffIn(0.0), AbsDiffOut(0.0),
              AbsDiff(MaxSolidWinLayers, 0.0), BlAbsDiff(MaxSlatAngs, MaxSolidWinLayers, 0.0), BlAbsDiffGnd(MaxSlatAngs, MaxSolidWinLayers, 0.0),
              BlAbsDiffSky(MaxSlatAngs, MaxSolidWinLayers, 0.0), AbsDiffBack(MaxSolidWinLayers, 0.0),
              BlAbsDiffBack(MaxSlatAngs, MaxSolidWinLayers, 0.0), AbsDiffShade(0.0), AbsDiffBlind(MaxSlatAngs, 0.0),
              AbsDiffBlindGnd(MaxSlatAngs, 0.0), AbsDiffBlindSky(MaxSlatAngs, 0.0), AbsDiffBackShade(0.0), AbsDiffBackBlind(MaxSlatAngs, 0.0),
              ShadeAbsorpThermal(0.0), AbsBeamCoef(6, MaxSolidWinLayers, 0.0), AbsBeamBackCoef(6, MaxSolidWinLayers, 0.0), AbsBeamShadeCoef(6, 0.0),
              TransDiff(0.0), BlTransDiff(MaxSlatAngs, 0.0), BlTransDiffGnd(MaxSlatAngs, 0.0), BlTransDiffSky(MaxSlatAngs, 0.0), TransDiffVis(0.0),
              BlTransDiffVis(MaxSlatAngs, 0.0), ReflectSolDiffBack(0.0), BlReflectSolDiffBack(MaxSlatAngs, 0.0), ReflectSolDiffFront(0.0),
              BlReflectSolDiffFront(MaxSlatAngs, 0.0), ReflectVisDiffBack(0.0), BlReflectVisDiffBack(MaxSlatAngs, 0.0), ReflectVisDiffFront(0.0),
              BlReflectVisDiffFront(MaxSlatAngs, 0.0), TransSolBeamCoef(6, 0.0), TransVisBeamCoef(6, 0.0), ReflSolBeamFrontCoef(6, 0.0),
              ReflSolBeamBackCoef(6, 0.0), tBareSolCoef(6, 5, 0.0), tBareVisCoef(6, 5, 0.0), rfBareSolCoef(6, 5, 0.0), rfBareVisCoef(6, 5, 0.0),
              rbBareSolCoef(6, 5, 0.0), rbBareVisCoef(6, 5, 0.0), afBareSolCoef(6, 5, 0.0), abBareSolCoef(6, 5, 0.0), tBareSolDiff(5, 0.0),
              tBareVisDiff(5, 0.0), rfBareSolDiff(5, 0.0), rfBareVisDiff(5, 0.0), rbBareSolDiff(5, 0.0), rbBareVisDiff(5, 0.0), afBareSolDiff(5, 0.0),
              abBareSolDiff(5, 0.0), FromWindow5DataFile(false), W5FileMullionWidth(0.0), W5FileMullionOrientation(0), W5FileGlazingSysWidth(0.0),
              W5FileGlazingSysHeight(0.0), SummerSHGC(0.0), VisTransNorm(0.0), SolTransNorm(0.0), SourceSinkPresent(false), TypeIsWindow(false),
              WindowTypeBSDF(false), TypeIsEcoRoof(false), TypeIsIRT(false), TypeIsCfactorWall(false), TypeIsFfactorFloor(false), TCFlag(0),
              TCLayer(0), TCMasterConst(0), TCLayerID(0), TCGlassID(0), CFactor(0.0), Height(0.0), FFactor(0.0), Area(0.0), PerimeterExposed(0.0),
              ReverseConstructionNumLayersWarning(false), ReverseConstructionLayersOrderWarning(false), WindowTypeEQL(false), EQLConsPtr(0),
              AbsDiffFrontEQL(CFSMAXNL, 0.0), AbsDiffBackEQL(CFSMAXNL, 0.0), TransDiffFrontEQL(0.0), TransDiffBackEQL(0.0)
        {
        }
    '''

    # DataHeatBalance.cc
	ZoneList = pd.Series()
    Construct = ConstructionData
    AnisoSkyMult = pd.Series()              # Multiplier on exterior-surface sky view factor to
                                            # account for anisotropy of sky radiance; = 1.0 for
                                            # for isotropic sky
    curDifShdgRatioIsoSky = pd.Series()     # Diffuse shading ratio (WithShdgIsoSky/WoShdgIsoSky)
    DifShdgRatioHoriz = pd.Series()         # Horizon shading ratio (WithShdgHoriz/WoShdgHoriz)
    DifShdgRatioHorizHRTS = pd.DataFrame()  # Horizon shading ratio (WithShdgHoriz/WoShdgHoriz)
    DifShdgRatioIsoSky = pd.Series()        # Diffuse shading ratio (WithShdgIsoSky/WoShdgIsoSky)
    MultCircumSolar = pd.Series()           # Contribution to eff sky view factor from circumsolar brightening
    MultHorizonZenith = pd.Series()         # Contribution to eff sky view factor from horizon or zenith brightening
    MultIsoSky = pd.Series()                # Contribution to eff sky view factor from isotropic sky
    SunlitFrac = pd.DataFrame()             # TimeStep fraction of heat transfer surface that is sunlit

	# DataSurfaces.hh
    Vertices = pd.Series()
    Plane = pd.DataFrame() # Vector4<Real64> ?

    SurfaceData_ = namedtuple('SurfaceData', ['Name', 'Construction', 'EMSConstructionOverrideON', 'EMSConstructionOverrideValue',
                                                'ConstructionStoredInputValue', 'Class', 'Shape', 'Sides', 'Area', 'GrossArea',
                                                'NetAreaShadowCalc', 'Perimeter', 'Azimuth', 'Height', 'Reveal', 'Tilt', 'Width',
                                                'HeatTransSurf', 'OutsideHeatSourceTermSchedule', 'InsideHeatSourceTermSchedule',
                                                'HeatTransferAlgorithm', 'BaseSurfName', 'BaseSurf', 'NumSubSurfaces', 'ZoneName',
                                                'Zone', 'ExtBoundCondName', 'LowTempErrCount', 'HighTempErrCount', 'ExtSolar',
                                                'ExtWind', 'IntConvCoeff', 'EMSOverrideIntConvCoef', 'EMSValueForIntConvCoef',
                                                'ExtConvCoeff', 'EMSOverrideExtConvCoef', 'EMSValueForExtConvCoef', 'ViewFactorGround',
                                                'ViewFactorSky', 'ViewFactorGroundIR', 'ViewFactorSkyIR', 'OSCPtr', 'OSCMPtr',
                                                'SchedShadowSurfIndex', 'ShadowSurfSchedVaries', 'ShadowingSurf', 'IsTransparent',
                                                'SchedMinValue', 'ShadowSurfDiffuseSolRefl', 'ShadowSurfDiffuseVisRefl',
                                                'ShadowSurfGlazingFrac', 'ShadowSurfGlazingConstruct', 'ShadowSurfPossibleObstruction',
                                                'ShadowSurfPossibleReflector', 'ShadowSurfRecSurfNum', 'MaterialMovInsulExt',
                                                'MaterialMovInsulInt', 'SchedMovInsulExt', 'SchedMovInsulInt', 'MovInsulIntPresent',
                                                'MovInsulIntPresentPrevTS', 'NewVertex', 'Vertex', 'Centroid', 'lcsx', 'lcsy', 'lcsz',
                                                'NewellAreaVector', 'NewellSurfaceNormalVector', 'OutNormVec', 'SinAzim', 'CosAzim',
                                                'SinTilt', 'CosTilt', 'IsConvex', 'IsDegenerate', 'shapeCat', 'plane', 'surface2d',
                                                '...Window Parameters...',
                                                'Shelf', 'TAirRef', 'OutDryBulbTemp', 'OutDryBulbTempEMSOverrideOn',
                                                'OutDryBulbTempEMSOverrideValue', 'OutWetBulbTemp', 'OutWetBulbTempEMSOverrideOn',
                                                'OutWetBulbTempEMSOverrideValue', 'WindSpeed', 'WindSpeedEMSOverrideOn',
                                                'WindSpeedEMSOverrideValue', 'WindDir', 'WindDirEMSOverrideOn', 'WindDirEMSOverrideValue',
                                                'SchedExternalShadingFrac', 'ExternalShadingSchInd', 'HasSurroundingSurfProperties',
                                                'SurroundingSurfacesNum', 'HasLinkedOutAirNode', 'LinkedOutAirNode', 'UNomWOFilm',
                                                'UNomFilm', 'ExtEcoRoof', 'ExtCavityPresent', 'ExtCavNum', 'IsPV', 'IsICS', 'IsPool',
                                                'ICSPtr', 'MirroredSurf', 'IntConvClassification', 'IntConvHcModelEq', 'IntConvHcUserCurveIndex',
                                                'OutConvClassification', 'OutConvHfModelEq', 'OutConvHfUserCurveIndex', 'OutConvHnModelEq',
                                                'OutConvHnUserCurveIndex', 'OutConvFaceArea', 'OutConvFacePerimeter', 'OutConvFaceHeight',
                                                'IntConvZoneWallHeight', 'IntConvZonePerimLength', 'IntConvZoneHorizHydrDiam',
                                                'IntConvWindowWallRatio', 'IntConvWindowLocation', 'IntConvSurfGetsRadiantHeat',
                                                'IntConvSurfHasActiveInIt', 'PartOfVentSlabOrRadiantSurface', 'GenericContam',
                                                'DisabledShadowingZoneList'])
    SurfaceData = SurfaceData_(Name=?, Construction=0, EMSConstructionOverrideON=False, EMSConstructionOverrideValue=0,
                                ConstructionStoredInputValue=0, Class=0, Shape=?SurfaceShape::None, Sides=0, Area=0.0,
                                GrossArea=0.0, NetAreaShadowCalc=0.0, Perimeter=0.0, Azimuth=0.0, Height=0.0, Reveal=0.0,
                                Tilt=0.0, Width=0.0, HeatTransSurf=False, OutsideHeatSourceTermSchedule=0, InsideHeatSourceTermSchedule=0,
                                HeatTransferAlgorithm=?HeatTransferModel_NotSet, BaseSurfName=?, BaseSurf=0, NumSubSurfaces=0, ZoneName=?,
                                Zone=0, ExtBoundCondName=?, ExtBoundCond=0, LowTempErrCount=0, HighTempErrCount=0, ExtSolar=False, ExtWind=False,
                                IntConvCoeff=0, EMSOverrideIntConvCoef=False, EMSValueForIntConvCoef=0.0, ExtConvCoeff=0, EMSOverrideExtConvCoef=False,
                                EMSValueForExtConvCoef=0.0, ViewFactorGround=0.0, ViewFactorSky=0.0, ViewFactorGroundIR=0.0, ViewFactorSkyIR=0.0,
                                OSCPtr=0, OSCMPtr=0, SchedShadowSurfIndex=0, ShadowSurfSchedVaries=False, ShadowingSurf=False, IsTransparent=False,
                                SchedMinValue=0.0, ShadowSurfDiffuseSolRefl=0.0, ShadowSurfDiffuseVisRefl=0.0, ShadowSurfGlazingFrac=0.0,
                                ShadowSurfGlazingConstruct=0, ShadowSurfPossibleObstruction=True, ShadowSurfPossibleReflector=False, ShadowSurfRecSurfNum=0,
                                MaterialMovInsulExt=0, MaterialMovInsulInt=0, SchedMovInsulExt=0, SchedMovInsulInt=0, MovInsulIntPresent=False,
                                MovInsulIntPresentPrevTS=False, NewVertex=?, Vertex=?, Centroid=(0.0, 0.0, 0.0), lcsx=(0.0, 0.0, 0.0), lcsy=(0.0, 0.0, 0.0),
                                lcsz=(0.0, 0.0, 0.0), NewellAreaVector=(0.0, 0.0, 0.0), NewellSurfaceNormalVector=(0.0, 0.0, 0.0), OutNormVec=(3, 0.0),
                                SinAzim=0.0, CosAzim=0.0, SinTilt=0.0, CosTilt=0.0, IsConvex=True, IsDegenerate=False, shapeCat=?ShapeCat::Unknown,
                                plane=(0.0, 0.0, 0.0, 0.0), surface2d=?,
                                ...Window Parameters...=,
                                Shelf=0, TAirRef=?ZoneMeanAirTemp, OutDryBulbTemp=0.0, OutDryBulbTempEMSOverrideOn=False, OutDryBulbTempEMSOverrideValue=0.0,
                                OutWetBulbTemp=0.0, OutWetBulbTempEMSOverrideOn=False, OutWetBulbTempEMSOverrideValue=0.0, WindSpeed=0.0,
                                WindSpeedEMSOverrideOn=False, WindSpeedEMSOverrideValue=0.0, WindDir=0.0, WindDirEMSOverrideOn=False, WindDirEMSOverrideValue=0.0,
                                SchedExternalShadingFrac=False, ExternalShadingSchInd=0, HasSurroundingSurfProperties=False, SurroundingSurfacesNum=0,
                                HasLinkedOutAirNode=False, LinkedOutAirNode=0, UNomWOFilm="-              ", UNomFilm="-              ", ExtEcoRoof=False,
                                ExtCavityPresent=False, ExtCavNum=0, IsPV=False, IsICS=False, IsPool=False, ICSPtr=0, MirroredSurf=False, IntConvClassification=0,
                                IntConvHcModelEq=0, IntConvHcUserCurveIndex=0, OutConvClassification=0, OutConvHfModelEq=0, OutConvHfUserCurveIndex=0,
                                OutConvHnModelEq=0, OutConvHnUserCurveIndex=0, OutConvFaceArea=0.0, OutConvFacePerimeter=0.0, OutConvFaceHeight=0.0,
                                IntConvZoneWallHeight=0.0, IntConvZonePerimLength=0.0, IntConvZoneHorizHydrDiam=0.0, IntConvWindowWallRatio=0.0,
                                IntConvWindowLocation=?InConvWinLoc_NotSet, IntConvSurfGetsRadiantHeat=False, IntConvSurfHasActiveInIt=False,
                                PartOfVentSlabOrRadiantSurface=False, GenericContam=0.0, DisabledShadowingZoneList=?)
    '''
        // Types
        using Vertices = pd.Series();
        using Plane = Vector4<Real64>;

        // Members
        std::string Name;                 // User supplied name of the surface (must be unique)
        int Construction;                 // Pointer to the construction in the Construct derived type
        bool EMSConstructionOverrideON;   // if true, EMS is calling to override the construction value
        int EMSConstructionOverrideValue; // pointer value to use for Construction when overridden
        int ConstructionStoredInputValue; // holds the original value for Construction per surface input
        int Class;
        
        // Geometry related parameters
        SurfaceShape Shape; // Surface shape (Triangle=1,Quadrilateral=2,Rectangle=3,
                            // Rectangular Window/Door=4,Rectangular Overhang=5,
                            // Rectangular Left Fin=6,Rectangular Right Fin=7,
                            // Triangular Window=8)
        int Sides;                // Number of side/vertices for this surface (based on Shape)
        Real64 Area;              // Surface area of the surface (less any subsurfaces) {m2}
        Real64 GrossArea;         // Surface area of the surface (including subsurfaces) {m2}
        Real64 NetAreaShadowCalc; // Area of a wall/floor/ceiling less subsurfaces assuming
                                  //  all windows, if present, have unity multiplier.
                                  // Wall/floor/ceiling/roof areas that include windows include
                                  //  frame (unity) areas.
                                  // Areas of Windows including divider (unity) area.
                                  // These areas are used in shadowing / sunlit area calculations.
        Real64 Perimeter; // Perimeter length of the surface {m}
        Real64 Azimuth;   // Direction the surface outward normal faces (degrees) or FACING
        Real64 Height;    // Height of the surface (m)
        Real64 Reveal;    // Depth of the window reveal (m) if this surface is a window
        Real64 Tilt;      // Angle (deg) between the ground outward normal and the surface outward normal
        Real64 Width;     // Width of the surface (m)
        
        // Boundary conditions and interconnections
        bool HeatTransSurf;                // True if surface is a heat transfer surface,
        int OutsideHeatSourceTermSchedule; // Pointer to the schedule of additional source of heat flux rate applied to the outside surface
        int InsideHeatSourceTermSchedule;  // Pointer to the schedule of additional source of heat flux rate applied to the inside surface
                                           // False if a (detached) shadowing (sub)surface
        int HeatTransferAlgorithm; // used for surface-specific heat transfer algorithm.
        std::string BaseSurfName;  // Name of BaseSurf
        int BaseSurf;              // "Base surface" for this surface.  Applies mainly to subsurfaces
                                   // in which case it points back to the base surface number.
                                   // Equals 0 for detached shading.
                                   // BaseSurf equals surface number for all other surfaces.
        int NumSubSurfaces;   // Number of subsurfaces this surface has (doors/windows)
        std::string ZoneName; // User supplied name of the Zone
        int Zone;             // Interior environment or zone the surface is a part of
                              // Note that though attached shading surfaces are part of a zone, this
                              // value is 0 there to facilitate using them as detached surfaces (more
                              // accurate shading.
        std::string ExtBoundCondName; // Name for the Outside Environment Object
        int ExtBoundCond;             // For an "interzone" surface, this is the adjacent surface number.
                                      // for an internal/adiabatic surface this is the current surface number.
                                      // Otherwise, 0=external environment, -1=ground,
                                      // -2=other side coefficients (OSC--won't always use CTFs)
                                      // -3=other side conditions model
                                      // During input, interim values of UnreconciledZoneSurface ("Surface") and
                                      // UnenteredAdjacentZoneSurface ("Zone") are used until reconciled.
        int LowTempErrCount;
        int HighTempErrCount;
        bool ExtSolar; // True if the "outside" of the surface is exposed to solar
        bool ExtWind;  // True if the "outside" of the surface is exposed to wind
        
        // Heat transfer coefficients
        int IntConvCoeff; // Interior Convection Coefficient pointer (different data structure)
                          // when being overridden
        bool EMSOverrideIntConvCoef;   // if true, EMS is calling to override interior convection coefficeint
        Real64 EMSValueForIntConvCoef; // Value EMS is calling to use for interior convection coefficient [W/m2-K]
        int ExtConvCoeff;              // Exterior Convection Coefficient pointer (different data structure)
                                       // when being overridden
        bool EMSOverrideExtConvCoef;   // if true, EMS is calling to override exterior convection coefficeint
        Real64 EMSValueForExtConvCoef; // Value EMS is calling to use for exterior convection coefficient [W/m2-K]
        Real64 ViewFactorGround;       // View factor to the ground from the exterior of the surface for diffuse solar radiation
        Real64 ViewFactorSky;          // View factor to the sky from the exterior of the surface for diffuse solar radiation
        Real64 ViewFactorGroundIR;     // View factor to the ground and shadowing surfaces from the exterior of the surface for IR radiation
        Real64 ViewFactorSkyIR;        // View factor to the sky from the exterior of the surface for IR radiation
        
        // Special/optional other side coefficients (OSC)
        int OSCPtr;  // Pointer to OSC data structure
        int OSCMPtr; // "Pointer" to OSCM data structure (other side conditions from a model)

        // Optional parameters specific to shadowing surfaces and subsurfaces (detached shading, overhangs, wings, etc.)
        int SchedShadowSurfIndex;   // Schedule for a shadowing (sub)surface
        bool ShadowSurfSchedVaries; // true if the scheduling (transmittance) on a shading surface varies.
        bool ShadowingSurf;         // True if a surface is a shadowing surface
        bool IsTransparent;         // True if the schedule values are always 1.0 (or the minimum is 1.0)
        Real64 SchedMinValue;       // Schedule minimum value.
        
        // Optional parameters specific to solar reflection from surfaces
        Real64 ShadowSurfDiffuseSolRefl;    // Diffuse solar reflectance of opaque portion
        Real64 ShadowSurfDiffuseVisRefl;    // Diffuse visible reflectance of opaque portion
        Real64 ShadowSurfGlazingFrac;       // Glazing fraction
        int ShadowSurfGlazingConstruct;     // Glazing construction number
        bool ShadowSurfPossibleObstruction; // True if a surface can be an exterior obstruction
        bool ShadowSurfPossibleReflector;   // True if a surface can be an exterior reflector, not used!
        int ShadowSurfRecSurfNum;           // Receiving surface number

        // Optional movable insulation parameters
        int MaterialMovInsulExt;       // Pointer to the material used for exterior movable insulation
        int MaterialMovInsulInt;       // Pointer to the material used for interior movable insulation
        int SchedMovInsulExt;          // Schedule for exterior movable insulation
        int SchedMovInsulInt;          // Schedule for interior movable insulation
        bool MovInsulIntPresent;       // True when movable insulation is present
        bool MovInsulIntPresentPrevTS; // True when movable insulation was present during the previous time step
        
        // Vertices
        NewVertex = pd.Series()
        Vertices Vertex; // Surface Vertices are represented by Number of Sides and Vector (type)
        Vector Centroid; // computed centroid (also known as center of mass or surface balance point)
        Vector lcsx;
        Vector lcsy;
        Vector lcsz;
        Vector NewellAreaVector;
        Vector NewellSurfaceNormalVector; // same as OutNormVec in vector notation
        OutNormVec = pd.Series()          // Direction cosines (outward normal vector) for surface
        Real64 SinAzim;                   // Sine of surface azimuth angle
        Real64 CosAzim;                   // Cosine of surface azimuth angle
        Real64 SinTilt;                   // Sine of surface tilt angle
        Real64 CosTilt;                   // Cosine of surface tilt angle
        bool IsConvex;                    // true if the surface is convex.
        bool IsDegenerate;                // true if the surface is degenerate.
        
        // Precomputed parameters for PierceSurface performance
        ShapeCat shapeCat;   // Shape category
        Plane plane;         // Plane
        Surface2D surface2d; // 2D projected surface for efficient intersection testing
        
        // Window Parameters (when surface is Window)
        int WindowShadingControlPtr; // Pointer to shading control (windows only)
        bool HasShadeControl;           // True if the surface is listed in a WindowShadingControl object
        int ShadedConstruction;         // Shaded construction (windows only)
        int StormWinConstruction;       // Construction with storm window (windows only)
        int StormWinShadedConstruction; // Shaded construction with storm window (windows only)
        int FrameDivider;               // Pointer to frame and divider information (windows only)
        Real64 Multiplier;              // Multiplies glazed area, frame area and divider area (windows only)
        
        // Daylighting pointers
        int Shelf;   // Pointer to daylighting shelf
        int TAirRef; // Flag for reference air temperature
                     // ZoneMeanAirTemp   = 1 = mean air temperature or MAT => for mixing air model with all convection algos
                     // except inlet-dependent algo
                     // AdjacentAirTemp   = 2 = adjacent air temperature or TempEffBulkAir => for nodal or zonal air model
                     // with all convection algos except inlet-dependent algo
                     // ZoneSupplyAirTemp = 3 = supply air temperature => for mixing air model with inlet-dependent algo
                     // Default value is 'ZoneMeanAirTemp' and value for each particular surface will be changed only if
                     // the inlet-dependent convection algorithm and/or nodal and zonal air models are used.
        Real64 OutDryBulbTemp;                 // Surface outside dry bulb air temperature, for surface heat balance (C)
        bool OutDryBulbTempEMSOverrideOn;      // if true, EMS is calling to override the surface's outdoor air temp
        Real64 OutDryBulbTempEMSOverrideValue; // value to use for EMS override of outdoor air drybulb temp (C)
        Real64 OutWetBulbTemp;                 // Surface outside wet bulb air temperature, for surface heat balance (C)
        bool OutWetBulbTempEMSOverrideOn;      // if true, EMS is calling to override the surface's outdoor wetbulb
        Real64 OutWetBulbTempEMSOverrideValue; // value to use for EMS override of outdoor air wetbulb temp (C)
        Real64 WindSpeed;                      // Surface outside wind speed, for surface heat balance (m/s)
        bool WindSpeedEMSOverrideOn;
        Real64 WindSpeedEMSOverrideValue;

        // XL added 7/19/2017
        Real64 WindDir;                 // Surface outside wind direction, for surface heat balance and ventilation(degree)
        bool WindDirEMSOverrideOn;      // if true, EMS is calling to override the surface's outside wind direction
        Real64 WindDirEMSOverrideValue; // value to use for EMS override of the surface's outside wind speed

        // XL added 7/25/2017
        bool SchedExternalShadingFrac;     // true if the external shading is scheduled or calculated externally to be imported
        int ExternalShadingSchInd;         // Schedule for a the external shading
        bool HasSurroundingSurfProperties; // true if surrounding surfaces properties are listed for an external surface
        int SurroundingSurfacesNum;        // Index of a surrounding surfaces list (defined in SurfaceProperties::SurroundingSurfaces)
        bool HasLinkedOutAirNode;          // true if an OutdoorAir::Node is linked to the surface
        int LinkedOutAirNode;              // Index of the an OutdoorAir:Node

        std::string UNomWOFilm; // Nominal U Value without films stored as string
        std::string UNomFilm;   // Nominal U Value with films stored as string
        bool ExtEcoRoof;        // True if the top outside construction material is of type Eco Roof
        bool ExtCavityPresent;  // true if there is an exterior vented cavity on surface
        int ExtCavNum;          // index for this surface in ExtVentedCavity structure (if any)
        bool IsPV;              // true if this is a photovoltaic surface (dxf output)
        bool IsICS;             // true if this is an ICS collector
        bool IsPool;            // true if this is a pool
        int ICSPtr;             // Index to ICS collector
        
        // TH added 3/26/2010
        bool MirroredSurf; // True if it is a mirrored surface

        // additional attributes for convection correlations
        int IntConvClassification;       // current classification for inside face air flow regime and surface orientation
        int IntConvHcModelEq;            // current convection model for inside face
        int IntConvHcUserCurveIndex;     // current index to user convection model if used
        int OutConvClassification;       // current classification for outside face wind regime and convection orientation
        int OutConvHfModelEq;            // current convection model for forced convection at outside face
        int OutConvHfUserCurveIndex;     // current index to user forced convection model if used
        int OutConvHnModelEq;            // current Convection model for natural convection at outside face
        int OutConvHnUserCurveIndex;     // current index to user natural convection model if used
        Real64 OutConvFaceArea;          // area of larger building envelope facade that surface is a part of
        Real64 OutConvFacePerimeter;     // perimeter of larger building envelope facade that surface is a part of
        Real64 OutConvFaceHeight;        // height of larger building envelope facade that surface is a part of
        Real64 IntConvZoneWallHeight;    // [m] height of larger inside building wall element that surface is a part of
        Real64 IntConvZonePerimLength;   // [m] length of perimeter zone's exterior wall
        Real64 IntConvZoneHorizHydrDiam; // [m] hydraulic diameter, usually 4 times the zone floor area div by perimeter
        Real64 IntConvWindowWallRatio;   // [-] area of windows over area of exterior wall for zone
        int IntConvWindowLocation;       // relative location of window in zone for interior Hc models
        bool IntConvSurfGetsRadiantHeat;
        bool IntConvSurfHasActiveInIt;
        bool PartOfVentSlabOrRadiantSurface; // surface cannot be part of both a radiant surface & ventilated slab group
        
        // LG added 1/6/12
        Real64 GenericContam; // [ppm] Surface generic contaminant as a storage term for

        std::vector<int> DisabledShadowingZoneList; // Array of all disabled shadowing zone number to the current surface
                                                    // the surface diffusion model

        // Default Constructor
        SurfaceData()
            : Construction(0), EMSConstructionOverrideON(false), EMSConstructionOverrideValue(0), ConstructionStoredInputValue(0), Class(0),
              Shape(SurfaceShape::None), Sides(0), Area(0.0), GrossArea(0.0), NetAreaShadowCalc(0.0), Perimeter(0.0), Azimuth(0.0), Height(0.0),
              Reveal(0.0), Tilt(0.0), Width(0.0), HeatTransSurf(false), OutsideHeatSourceTermSchedule(0), InsideHeatSourceTermSchedule(0),
              HeatTransferAlgorithm(HeatTransferModel_NotSet), BaseSurf(0), NumSubSurfaces(0), Zone(0), ExtBoundCond(0), LowTempErrCount(0),
              HighTempErrCount(0), ExtSolar(false), ExtWind(false), IntConvCoeff(0), EMSOverrideIntConvCoef(false), EMSValueForIntConvCoef(0.0),
              ExtConvCoeff(0), EMSOverrideExtConvCoef(false), EMSValueForExtConvCoef(0.0), ViewFactorGround(0.0), ViewFactorSky(0.0),
              ViewFactorGroundIR(0.0), ViewFactorSkyIR(0.0), OSCPtr(0), OSCMPtr(0), SchedShadowSurfIndex(0), ShadowSurfSchedVaries(false),
              ShadowingSurf(false), IsTransparent(false), SchedMinValue(0.0), ShadowSurfDiffuseSolRefl(0.0), ShadowSurfDiffuseVisRefl(0.0),
              ShadowSurfGlazingFrac(0.0), ShadowSurfGlazingConstruct(0), ShadowSurfPossibleObstruction(true), ShadowSurfPossibleReflector(false),
              ShadowSurfRecSurfNum(0), MaterialMovInsulExt(0), MaterialMovInsulInt(0), SchedMovInsulExt(0), SchedMovInsulInt(0),
              MovInsulIntPresent(false), MovInsulIntPresentPrevTS(false), Centroid(0.0, 0.0, 0.0), lcsx(0.0, 0.0, 0.0), lcsy(0.0, 0.0, 0.0),
              lcsz(0.0, 0.0, 0.0), NewellAreaVector(0.0, 0.0, 0.0), NewellSurfaceNormalVector(0.0, 0.0, 0.0), OutNormVec(3, 0.0), SinAzim(0.0),
              CosAzim(0.0), SinTilt(0.0), CosTilt(0.0), IsConvex(true), IsDegenerate(false), shapeCat(ShapeCat::Unknown), plane(0.0, 0.0, 0.0, 0.0),
              
              WindowShadingControlPtr(0), HasShadeControl(false), ShadedConstruction(0), StormWinConstruction(0), StormWinShadedConstruction(0), FrameDivider(0),
              Multiplier(1.0),

              Shelf(0), TAirRef(ZoneMeanAirTemp), OutDryBulbTemp(0.0), OutDryBulbTempEMSOverrideOn(false),
              OutDryBulbTempEMSOverrideValue(0.0), OutWetBulbTemp(0.0), OutWetBulbTempEMSOverrideOn(false), OutWetBulbTempEMSOverrideValue(0.0),
              WindSpeed(0.0), WindSpeedEMSOverrideOn(false), WindSpeedEMSOverrideValue(0.0), WindDir(0.0), WindDirEMSOverrideOn(false),
              WindDirEMSOverrideValue(0.0), SchedExternalShadingFrac(false), ExternalShadingSchInd(0), HasSurroundingSurfProperties(false),
              SurroundingSurfacesNum(0), HasLinkedOutAirNode(false), LinkedOutAirNode(0), UNomWOFilm("-              "), UNomFilm("-              "),
              ExtEcoRoof(false), ExtCavityPresent(false), ExtCavNum(0), IsPV(false), IsICS(false), IsPool(false), ICSPtr(0), MirroredSurf(false),
              IntConvClassification(0), IntConvHcModelEq(0), IntConvHcUserCurveIndex(0), OutConvClassification(0), OutConvHfModelEq(0),
              OutConvHfUserCurveIndex(0), OutConvHnModelEq(0), OutConvHnUserCurveIndex(0),
              OutConvFaceArea(0.0), OutConvFacePerimeter(0.0), OutConvFaceHeight(0.0), IntConvZoneWallHeight(0.0), IntConvZonePerimLength(0.0),
              IntConvZoneHorizHydrDiam(0.0), IntConvWindowWallRatio(0.0), IntConvWindowLocation(InConvWinLoc_NotSet),
              IntConvSurfGetsRadiantHeat(false), IntConvSurfHasActiveInIt(false), PartOfVentSlabOrRadiantSurface(false), GenericContam(0.0)
    '''

    # DataSurfaces.cc
	Surface = pd.Series()
	SurfaceWindow = pd.Series() # PROVAVELMENTE NÃO SERÁ NECESSÁRIO
	NumOfZoneLists = 0
    ?pd.DataFrame() SUNCOSHR(24, 3, 0.0); # Hourly values of SUNCOS (solar direction cosines) # Autodesk:Init Zero-initialization added to avoid use uninitialized
    # três colunas ou linhas?

    # DataSystemVariables.cc
    DisableGroupSelfShading = False          # when True, defined shadowing surfaces group is ignored when calculating sunlit fraction
    DetailedSkyDiffuseAlgorithm = False      # use detailed diffuse shading algorithm for sky (shading transmittance varies)
    DetailedSolarTimestepIntegration = False # when true, use detailed timestep integration for all solar,shading, etc.

    # OutputProcessor::Unit --> I don't how it works...?
    class Unit(Enum):
        # enum.auto()
        kg_s,
        C,
        kgWater_kgDryAir,
        ppm,
        Pa,
        m3_s,
        None,
        min,
        W,
        J,
        m3,
        kg,
        ach,
        W_W,
        lux,
        lum_W,
        hr,
        cd_m2,
        J_kgWater,
        m_s,
        W_m2,
        m,
        Ah,
        A,
        V,
        deltaC,
        kmol_s,
        rev_min,
        Btu_h_W,
        W_m2K,
        J_kg,
        kg_kg,
        Perc,
        deg,
        s,
        kg_m3,
        kg_m2s,
        J_kgK,
        L,
        K_m,
        m2,
        W_m2C,
        rad,
        J_m2,
        clo,
        W_K,
        kgWater_s,
        unknown,
        customEMS,

	# DataIPShortCuts.cc
	cAlphaFieldNames = pd.Series()
    cNumericFieldNames = pd.Series()
    lNumericFieldBlanks = pd.Series()
    lAlphaFieldBlanks = pd.Series()

    # DataEnvironment.cc
    SunIsUpValue = 0.00001                  # if Cos Zenith Angle of the sun is >= this value, the sun is "up"

    # DataGlobals.cc
    PiOvr2 = math.pi / 2.0                  # Pi/2

    # DataDaylighting.hh::ZoneDaylightCalc
    ZoneDaylightCalc_ = namedtuple('ZoneDaylightCalc', ['Name', 'ZoneName', 'DaylightMethod', 'AvailSchedNum', 'TotalDaylRefPoints',
                                    'DaylRefPtNum', 'DaylRefPtAbsCoord', 'DaylRefPtInBounds', 'FracZoneDaylit', 'IllumSetPoint',
                                    'LightControlType', 'glareRefPtNumber', 'ViewAzimuthForGlare', 'MaxGlareallowed', 'MinPowerFraction',
                                    'MinLightFraction', 'LightControlSteps', 'LightControlProbability', 'TotalExtWindows', 'AveVisDiffReflect',
                                    'DElightGriddingResolution', 'RefPtPowerReductionFactor', 'ZonePowerReductionFactor', 'DaylIllumAtRefPt',
                                    'GlareIndexAtRefPt', 'AdjIntWinZoneNums', 'NumOfIntWinAdjZones', 'NumOfIntWinAdjZoneExtWins',
                                    'IntWinAdjZoneExtWin', 'NumOfDayltgExtWins', 'DayltgExtWinSurfNums', 'ShadeDeployOrderExtWins',
                                    'MapShdOrdToLoopNum', 'MinIntWinSolidAng', 'TotInsSurfArea', 'FloorVisRefl', 'InterReflIllFrIntWins',
                                    'BacLum', 'SolidAngAtRefPt', 'SolidAngAtRefPtWtd', 'IllumFromWinAtRefPt', 'BackLumFromWinAtRefPt',
                                    'SourceLumFromWinAtRefPt', 'DaylIllFacSky', 'DaylSourceFacSky', 'DaylBackFacSky', 'DaylIllFacSun',
                                    'DaylIllFacSunDisk', 'DaylSourceFacSun', 'DaylSourceFacSunDisk', 'DaylBackFacSun', 'DaylBackFacSunDisk',
                                    'TimeExceedingGlareIndexSPAtRefPt', 'TimeExceedingDaylightIlluminanceSPAtRefPt', 'AdjZoneHasDayltgCtrl',
                                    'MapCount', 'ZoneToMap'])
    ZoneDaylightCalc = ZoneDaylightCalc_(DaylightMethod=0, AvailSchedNum=0, TotalDaylRefPoints=0, LightControlType=1, ViewAzimuthForGlare=0.0,
                                         MaxGlareallowed=0, MinPowerFraction=0.0, MinLightFraction=0.0, LightControlSteps=0, LightControlProbability=0.0,
                                         TotalExtWindows=0, AveVisDiffReflect=0.0, ZonePowerReductionFactor=1.0, NumOfIntWinAdjZones=0, NumOfIntWinAdjZoneExtWins=0,
                                         NumOfDayltgExtWins=0, MinIntWinSolidAng=0.0, TotInsSurfArea=0.0, FloorVisRefl=0.0, InterReflIllFrIntWins=0.0,
                                         AdjZoneHasDayltgCtrl=False, MapCount=0)
    '''
        // Members
        std::string Name;                  // Name of the daylighting:controls object
        std::string ZoneName;              // name of the zone where the daylighting:controls object is located
        int DaylightMethod;                // Type of Daylighting (1=SplitFlux, 2=DElight)
        int AvailSchedNum;                 // pointer to availability schedule if present
        int TotalDaylRefPoints;            // Number of daylighting reference points in a zone (0,1 or 2)
        DaylRefPtNum = pd.Series()         // Reference number to DaylRefPt array that stores Daylighting:ReferencePoint
        DaylRefPtAbsCoord = pd.DataFrame() // =0.0 ! X,Y,Z coordinates of all daylighting reference points
                                           // in absolute coordinate system (m)
                                           // Points 1 and 2 are the control reference points
        DaylRefPtInBounds = pd.Series()    // True when coordinates are in bounds of zone coordinates
        FracZoneDaylit = pd.Series()       // =0.0  ! Fraction of zone controlled by each reference point
        IllumSetPoint = pd.Series()        // =0.0  ! Illuminance setpoint at each reference point (lux)
        int LightControlType;              // Lighting control type (same for all reference points)
                                           // (1=continuous, 2=stepped, 3=continuous/off)
        int glareRefPtNumber;                      // from field: Glare Calculation Daylighting Reference Point Name
        Real64 ViewAzimuthForGlare;                // View direction relative to window for glare calculation (deg)
        int MaxGlareallowed;                       // Maximum allowable discomfort glare index
        Real64 MinPowerFraction;                   // Minimum fraction of power input that continuous dimming system can dim down to
        Real64 MinLightFraction;                   // Minimum fraction of light output that continuous dimming system can dim down to
        int LightControlSteps;                     // Number of levels (excluding zero) of stepped control system
        Real64 LightControlProbability;            // For manual control of stepped systems, probability that lighting will
        int TotalExtWindows;                       // Total number of exterior windows in the zone
        Real64 AveVisDiffReflect;                  // Area-weighted average inside surface visible reflectance of zone
        Real64 DElightGriddingResolution;          // Field: Delight Gridding Resolution
        RefPtPowerReductionFactor = pd.Series()    // =1.0  ! Electric power reduction factor at reference points
                                                   // due to daylighting
        Real64 ZonePowerReductionFactor;           // Electric power reduction factor for entire zone due to daylighting
        DaylIllumAtRefPt = pd.Series()             // =0.0 ! Daylight illuminance at reference points (lux)
        GlareIndexAtRefPt = pd.Series()            // =0.0 ! Glare index at reference points
        AdjIntWinZoneNums = pd.Series()            // List of zone numbers of adjacent zones that have exterior windows and
                                                   // share one or more interior windows with target zone
        int NumOfIntWinAdjZones; // Number of adjacent zones that have exterior windows and share one or
                                 // more interior windows with target zone
        int NumOfIntWinAdjZoneExtWins;      // number of exterior windows associated with zone via interior windows
        IntWinAdjZoneExtWin = pd.Series()   // nested structure | info about exterior window associated with zone via interior window
        int NumOfDayltgExtWins;             // Number of associated exterior windows providing daylight to this zone
        DayltgExtWinSurfNums = pd.Series()  // List of surface numbers of zone's exterior windows or
                                            // exterior windows in adjacent zones sharing interior windows with the zone
        std::vector<std::vector<int>> ShadeDeployOrderExtWins; // describes how the fenestration surfaces should deploy the shades. 
                                                               // It is a list of lists. Each sublist is a group of fenestration surfaces that should be deployed together. Many times the 
                                                               // sublists a just a single index to a fenestration surface if they are deployed one at a time.
        MapShdOrdToLoopNum = pd.Series()  // list that maps back the original loop order when using ShadeDeployOrderExtWins for shade deployment
        Real64 MinIntWinSolidAng;     // Minimum solid angle subtended by an interior window in a zone
        Real64 TotInsSurfArea;        // Total inside surface area of a daylit zone (m2)
        Real64 FloorVisRefl;          // Area-weighted visible reflectance of floor of a daylit zone
        Real64 InterReflIllFrIntWins; // Inter-reflected illuminance due to beam and diffuse solar passing
                                      //  through a zone's interior windows (lux)
        BacLum = pd.Series()                  // =0.0 ! Background luminance at each reference point (cd/m2)
        SolidAngAtRefPt = pd.DataFrame()         // (MaxRefPoints,50)
        SolidAngAtRefPtWtd = pd.DataFrame()      // (MaxRefPoints,50)
        IllumFromWinAtRefPt = pd.DataFrame()     // (MaxRefPoints,2,50)
        BackLumFromWinAtRefPt = pd.DataFrame()   // (MaxRefPoints,2,50)
        SourceLumFromWinAtRefPt = pd.DataFrame() // (MaxRefPoints,2,50)
        
        // Allocatable daylight factor arrays
        // Arguments for Dayl---Sky are:
        //  1: Daylit window number (1 to NumOfDayltgExtWins)
        //  2: Reference point number (1 to MaxRefPoints)
        //  3: Sky type (1 to 4; 1 = clear, 2 = clear turbid, 3 = intermediate, 4 = overcast
        //  4: Shading index (1 to MaxSlatAngs+1; 1 = bare window; 2 = with shade, or, if blinds
        //                                        2 = first slat position, 3 = second position, ..., MaxSlatAngs+1 = last position)
        //  5: Sun position index (1 to 24)
        DaylIllFacSky = pd.DataFrame()
        DaylSourceFacSky = pd.DataFrame()
        DaylBackFacSky = pd.DataFrame()
        
        // Arguments for Dayl---Sun are:
        //  1: Daylit window number (1 to NumOfDayltgExtWins)
        //  2: Reference point number (1 to MaxRefPoints)
        //  3: Shading index (1 to MaxShadeIndex; 1 = no shade; 2 = with shade, or, if blinds
        //                                        2 = first slat position, 3 = second position, ..., MaxSlatAngs+1 = last position)
        //  4: Sun position index (1 to 24)
        DaylIllFacSun = pd.DataFrame()
        DaylIllFacSunDisk = pd.DataFrame()
        DaylSourceFacSun = pd.DataFrame()
        DaylSourceFacSunDisk = pd.DataFrame()
        DaylBackFacSun = pd.DataFrame()
        DaylBackFacSunDisk = pd.DataFrame()
        
        // Time exceeding maximum allowable discomfort glare index at reference points (hours)
        TimeExceedingGlareIndexSPAtRefPt = pd.Series()
        
        // Time exceeding daylight illuminance setpoint at reference points (hours)
        TimeExceedingDaylightIlluminanceSPAtRefPt = pd.Series()
        
        // True if at least one adjacent zone, sharing one or more interior windows, has daylighting control
        bool AdjZoneHasDayltgCtrl;
        int MapCount;           // Number of maps assigned to Zone
        ZoneToMap = pd.Series() // Pointers to maps allocated to Zone

        // Default Constructor
        ZoneDaylightCalc()
            : DaylightMethod(0), AvailSchedNum(0), TotalDaylRefPoints(0), LightControlType(1), ViewAzimuthForGlare(0.0), MaxGlareallowed(0),
              MinPowerFraction(0.0), MinLightFraction(0.0), LightControlSteps(0), LightControlProbability(0.0), TotalExtWindows(0),
              AveVisDiffReflect(0.0), ZonePowerReductionFactor(1.0), NumOfIntWinAdjZones(0), NumOfIntWinAdjZoneExtWins(0), NumOfDayltgExtWins(0),
              MinIntWinSolidAng(0.0), TotInsSurfArea(0.0), FloorVisRefl(0.0), InterReflIllFrIntWins(0.0), AdjZoneHasDayltgCtrl(false), MapCount(0)
        {
        }
    '''

    # DataDaylighting.cc
    ZoneDaylight = pd.Series()

    # General::RoundSigDigits
    def RoundSigDigits(RealValue, SigDigits):
    	'''
        FUNCTION INFORMATION:
              AUTHOR         Linda K. Lawrie
              DATE WRITTEN   March 2002
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS FUNCTION:
        This function accepts a number as parameter as well as the number of
        significant digits after the decimal point to report and returns a string
        that is appropriate.

        # INPUTS:
        #		Real64 const RealValue
        # 		int const SigDigits
		'''
        # USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY : IEEE_IS_NAN ! Use IEEE_IS_NAN when GFortran supports it

        # FUNCTION PARAMETER DEFINITIONS:
        DigitChar = "01234567890"
        NAN_string = "NAN"
        ZEROOOO = "0.000000000000000000000000000"
        ?static gio::Fmt fmtLD("*");

        # FUNCTION LOCAL VARIABLE DECLARATIONS:

        if (np.isnan(RealValue)):
        	return NAN_string

        String = "" # Working string
        if (RealValue != 0.0):
            ?gio::write(String, fmtLD) << RealValue;
        else:
            String = ZEROOOO

        # EString --> E string retained from original string
        try:
            EPos = String.index("E") # Position of E in original string format xxEyy
            EString = String.substr(EPos)
            String.erase(EPos)
        except ValueError:
            continue # ? --> Isso que o 'if' está fazendo?
        # if (EPos != std::string::npos): # npos = non-position = not found
        #     EString = String.substr(EPos)
        #     String.erase(EPos)

        DotPos = String.index(".") # Position of decimal point in original string
        assert(DotPos != std::string::npos);
        assert(DotPos > 0); # Or SPos will not be valid

        # (if, else, then) statement ?
        char TestChar(DotPos + SigDigits + 1 < String.length() ? String[DotPos + SigDigits + 1] : ' '); # Test character (digit) for rounding, if position in digit string >= 5 (digit is 5 or greater) then will round

        TPos = DigitChar.index(TestChar) # Position of Testchar in Digit string

        # SPos --> Actual string position being replaced
        if (SigDigits == 0):
            SPos = DotPos - 1
        else:
            SPos = DotPos + SigDigits

        if ((TPos != std::string::npos) && (TPos >= 5)):    # Must round to next Digit
            char const Char2Rep = String[SPos];             # Character (digit) to be replaced
            NPos = DigitChar.index(Char2Rep)                # Position of "next" char in Digit String
            
            assert(NPos != std::string::npos);
            String[SPos] = DigitChar[NPos + 1]
            
            while (NPos == 9):                              # Must change other char too
                if (SigDigits == 1):
                    assert(SPos >= 2u);
                    TestChar = String[SPos - 2]
                    
                    if (TestChar == '.'):
                        assert(SPos >= 3u);
                        TestChar = String[SPos - 3]
                        SPos =- 2
                    
                    if (TestChar == ' '):
                        TestChar = '0'                      # all 999s
                    elif (TestChar == '-'):                 # Autodesk Added to fix bug for values like -9.9999
                        assert(SPos >= 3u);
                        String[SPos - 3] = TestChar         # Shift sign left to avoid overwriting it
                        TestChar = '0'                      # all 999s
                    
                    TPos1 = DigitChar.index(TestChar)
                    assert(TPos1 != std::string::npos);
                    assert(SPos >= 2u);
                    String[SPos - 2] = DigitChar[TPos1 + 1]
                else:
                    assert(SPos >= 1u);
                    TestChar = String[SPos - 1]
                    if (TestChar == '.'):
                        assert(SPos >= 2u);
                        TestChar = String[SPos - 2]
                        SPos =- 1
                    
                    if (TestChar == ' '):
                        TestChar = '0'                      # all 999s
                    elif (TestChar == '-'):                 # Autodesk Added to fix bug for values like -9.9999
                        assert(SPos >= 2u);
                        String[SPos - 2] = TestChar         # Shift sign left to avoid overwriting it
                        TestChar = '0'                      # all 999s
                    
                    TPos1 = DigitChar.index(TestChar)
                    assert(TPos1 != std::string::npos);
                    assert(SPos >= 1u);
                    String[SPos - 1] = DigitChar[TPos1 + 1]
                
                SPos =- 1
                NPos = TPos1

        # IncludeDot --> True when decimal point output
        if (SigDigits > 0 || EString != ""):
            IncludeDot = True
        else:
            IncludeDot = False
        
        if (IncludeDot):
            String.erase(min(DotPos + SigDigits + 1, len(String)))
            String =+ EString
        else:
            String.erase(DotPos)
        

        return stripped(String)

    # General::POLYF --> ? REVER COMPORTAMENTO DO 'A'
    # ACHO Q ESSA FUNÇÃO NÃO SERÁ USADA PARA A SOMBRA!
    def POLYF(X, A):
    '''
        FUNCTION INFORMATION:
                AUTHOR         Fred Winkelmann
                DATE WRITTEN   February 1999
                DATE MODIFIED  October 1999, FW: change to 6th order polynomial over
                               entire incidence angle range

        PURPOSE OF THIS FUNCTION:
                Evaluates glazing beam transmittance or absorptance of the form
                A(1)*X + A(2)*X^2 + A(3)*X^3 + A(4)*X^4 + A(5)*X^5 + A(6)*X^6
                where X is the cosine of the angle of incidence (0.0 to 1.0)

        INPUTS:
                Real64 const X,         # Cosine of angle of incidence
                Array1A<Real64> const A # Polynomial coefficients
    '''
        # Argument array dimensioning
        A.dim(6);

        if (X < 0.0 || X > 1.0):
            POLYF = 0.0
        else:
            POLYF = X * ( A(1) + X * ( A(2) + X * ( A(3) + X * ( A(4) + X * ( A(5) + X * A(6) )))))
        
        return POLYF

    # DaylightingManager.cc
    ?pd.Series() PHSUNHR(24, 0.0);  	# Hourly values of PHSUN
    ?pd.Series() SPHSUNHR(24, 0.0); 	# Hourly values of the sine of PHSUN
    ?pd.Series() CPHSUNHR(24, 0.0); 	# Hourly values of the cosine of PHSUN
    ?pd.Series() THSUNHR(24, 0.0);  	# Hourly values of THSUN
    ?pd.DataFrame() GILSK(24, 4, 0.0); 	# Horizontal illuminance from sky, by sky type, for each hour of the day
    ?pd.Series() GILSU(24, 0.0);    	# Horizontal illuminance from sun for each hour of the day
    TotWindowsWithDayl = 0				# Total number of exterior windows in all daylit zones
    CheckTDDZone = pd.Series()
    TDDTransVisBeam = pd.DataFrame()
    TDDFluxInc = pd.DataFrame()
    TDDFluxTrans = pd.DataFrame()
    FirstTimeDaylFacCalc = True

    # DaylightingDevices.cc
    NumOfTDDPipes = 0                   # Number of TDD pipes in the input file

    # DataDaylightingDevices.cc
    TDDPipe = pd.Series()

    # DaylightingDevices::CalcTDDTransSolAniso
    def CalcTDDTransSolAniso(PipeNum, COSI):
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Peter Graham Ellis
              DATE WRITTEN   July 2003
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Calculates the transmittance of the anisotropic sky.

        METHODOLOGY EMPLOYED:
        Similar to the Trans = FluxTrans/FluxInc integrations above, the anisotropic sky can be decomposed
        and have a different transmittance applied to each component.
          FluxInc = IsoSkyRad + CircumSolarRad + HorizonRad
          FluxTrans = T1*IsoSkyRad + T2*CircumSolarRad + T3*HorizonRad
        It turns out that FluxTrans/FluxInc is equivalent to AnisoSkyTDDMult/AnisoSkyMult.
        AnisoSkyMult has been conveniently calculated already in AnisoSkyViewFactors in SolarShading.cc.
        AnisoSkyMult = MultIsoSky*DifShdgRatioIsoSky + MultCircumSolar*SunlitFrac + MultHorizonZenith*DifShdgRatioHoriz
        In this routine a similar AnisoSkyTDDMult is calculated that applies the appropriate transmittance to each
        of the components above.  The result is Trans = AnisoSkyTDDMult/AnisoSkyMult.
        Shading and orientation are already taken care of by DifShdgRatioIsoSky and DifShdgRatioHoriz.

        REFERENCES:
        See AnisoSkyViewFactors in SolarShading.cc.

        INPUTS:
            int const PipeNum, # TDD pipe object number
            Real64 const COSI  # Cosine of the incident angle
        '''

        # FUNCTION LOCAL VARIABLE DECLARATIONS:
        DomeSurf = 0          # TDD:DOME surface number
        IsoSkyRad = 0.0       # Isotropic sky radiation component
        CircumSolarRad = 0.0  # Circumsolar sky radiation component
        HorizonRad = 0.0      # Horizon sky radiation component
        AnisoSkyTDDMult = 0.0 # Anisotropic sky multiplier for TDD

        # FLOW:
        DomeSurf = TDDPipe(PipeNum).Dome;

        if (!DetailedSkyDiffuseAlgorithm || !ShadingTransmittanceVaries || SolarDistribution == MinimalShadowing):
            IsoSkyRad = MultIsoSky(DomeSurf) * DifShdgRatioIsoSky(DomeSurf)
            HorizonRad = MultHorizonZenith(DomeSurf) * DifShdgRatioHoriz(DomeSurf)
        else:
            IsoSkyRad = MultIsoSky(DomeSurf) * curDifShdgRatioIsoSky(DomeSurf)
            HorizonRad = MultHorizonZenith(DomeSurf) * DifShdgRatioHorizHRTS(TimeStep, HourOfDay, DomeSurf)
        
        CircumSolarRad = MultCircumSolar(DomeSurf) * SunlitFrac(TimeStep, HourOfDay, DomeSurf)

        AnisoSkyTDDMult = TDDPipe(PipeNum).TransSolIso * IsoSkyRad + TransTDD(PipeNum, COSI, SolarBeam) * CircumSolarRad + TDDPipe(PipeNum).TransSolHorizon * HorizonRad

        if (AnisoSkyMult(DomeSurf) > 0.0):
            CalcTDDTransSolAniso = AnisoSkyTDDMult / AnisoSkyMult(DomeSurf)
        else:
            CalcTDDTransSolAniso = 0.0

        return CalcTDDTransSolAniso

    # DaylightingDevices::InterpolatePipeTransBeam
    def InterpolatePipeTransBeam(COSI, transBeam):
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Peter Graham Ellis
              DATE WRITTEN   July 2003
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Interpolates the beam transmittance vs. cosine angle table.

        METHODOLOGY EMPLOYED: na
        REFERENCES: na

        INPUTS:
            Real64 const COSI,              # Cosine of the incident angle
            Array1A<Real64> const transBeam # Table of beam transmittance vs. cosine angle
        '''

        # Using/Aliasing
        # using FluidProperties::FindArrayIndex; # USEd code could be copied here to eliminate dependence on FluidProperties

        # Argument array dimensioning
        transBeam.dim(NumOfAngles);

        # FUNCTION LOCAL VARIABLE DECLARATIONS:
        Lo = 0
        Hi = 0
        m = 0.0
        b = 0.0

        # FLOW:
        InterpolatePipeTransBeam = 0.0

        # Linearly interpolate transBeam/COSAngle table to get value at current cosine of the angle
        Lo = FindArrayIndex(COSI, COSAngle)
        Hi = Lo + 1

        if (Lo > 0 && Hi <= NumOfAngles):
            m = (transBeam(Hi) - transBeam(Lo)) / (COSAngle(Hi) - COSAngle(Lo))
            b = transBeam(Lo) - m * COSAngle(Lo)

            InterpolatePipeTransBeam = m * COSI + b
        else:
            InterpolatePipeTransBeam = 0.0
        
        return InterpolatePipeTransBeam

    # DaylightingDevices::FindTDDPipe
    def FindTDDPipe(WinNum):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Peter Graham Ellis
              DATE WRITTEN   May 2003
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Given the TDD:DOME or TDD:DIFFUSER object number, returns TDD pipe number.

        METHODOLOGY EMPLOYED:
        Similar to UtilityRoutines::FindItemInList( defined in InputProcessor.

        INPUT:
        	int const WinNum
    	'''
        # Using/Aliasing
        # using DataSurfaces::Surface;

        # FLOW:
        FindTDDPipe = 0

        if (NumOfTDDPipes <= 0):
            ShowFatalError("FindTDDPipe: Surface = {}, TDD:Dome object does not reference a valid Diffuser object....needs DaylightingDevice:Tubular of same name as Surface.".format(Surface(WinNum).Name))

        for PipeNum in range(1, NumOfTDDPipes+1):
            if ((WinNum == TDDPipe(PipeNum).Dome) || (WinNum == TDDPipe(PipeNum).Diffuser)):
                FindTDDPipe = PipeNum
                break

        return FindTDDPipe

    # DaylightingDevices::TransTDD
    def TransTDD(PipeNum, COSI, RadiationType):
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Peter Graham Ellis
              DATE WRITTEN   May 2003
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Calculates the total transmittance of the TDD for specified radiation type.

        METHODOLOGY EMPLOYED:
        The transmittances for each component (i.e. TDD:DIFFUSER, TDD:DOME, and pipe) are calculated.
        All transmittances are multiplied to get the total for the TDD:
          TransTDD = transDome * transPipe * transDiff
        Transmittance of beam radiation is calculated by interpolating the values in a
        table created during initialization.  The table values are from Swift and Smith's
        numerical integral for collimated beam radiation.
        Transmittances of isotropic and anisotropic diffuse radiation are more complicated and call
        other subroutines in this module.
        All light reaching the TDD:DIFFUSER is assumed to be diffuse.
        NOTE: Dome transmittance could be improved by taking into account curvature of the dome.

        REFERENCES:
        Swift, P. D., and Smith, G. B.  "Cylindrical Mirror Light Pipes",
          Solar Energy Materials and Solar Cells 36 (1995), pp. 159-168.

        INPUTS:
        		int const PipeNum,      # TDD pipe object number
                Real64 const COSI,      # Cosine of the incident angle
                int const RadiationType # Radiation type flag
        '''
        # Using/Aliasing
        # using General::POLYF;

        # FUNCTION LOCAL VARIABLE DECLARATIONS:
        constDome = 0	# Construction object number for TDD:DOME
        constDiff = 0	# Construction object number for TDD:DIFFUSER
        transDome = 0.0
        transPipe = 0.0
        transDiff = 0.0

        # FLOW:
        TransTDD = 0.0	# returned value, it's not a recursive function

        # Get constructions of each TDD component
        constDome = Surface(TDDPipe(PipeNum).Dome).Construction
        constDiff = Surface(TDDPipe(PipeNum).Diffuser).Construction

        # Get the transmittance of each component and of total TDD
        SELECT_CASE_var = RadiationType

        if (SELECT_CASE_var == VisibleBeam):
            transDome = POLYF(COSI, Construct(constDome).TransVisBeamCoef)
            transPipe = InterpolatePipeTransBeam(COSI, TDDPipe(PipeNum).PipeTransVisBeam)
            transDiff = Construct(constDiff).TransDiffVis # May want to change to POLYF also!

            TransTDD = transDome * transPipe * transDiff

        elif (SELECT_CASE_var == SolarBeam):
            transDome = POLYF(COSI, Construct(constDome).TransSolBeamCoef)
            transPipe = InterpolatePipeTransBeam(COSI, TDDPipe(PipeNum).PipeTransSolBeam)
            transDiff = Construct(constDiff).TransDiff # May want to change to POLYF also!

            TransTDD = transDome * transPipe * transDiff

        elif (SELECT_CASE_var == SolarAniso):
            TransTDD = CalcTDDTransSolAniso(PipeNum, COSI)

        elif (SELECT_CASE_var == SolarIso):
            TransTDD = TDDPipe(PipeNum).TransSolIso

        return TransTDD

    # DaylightingManager::CheckTDDsAndLightShelvesInDaylitZones
    def CheckTDDsAndLightShelvesInDaylitZones():
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Brent Griffith
              DATE WRITTEN   Dec 2007
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine checks daylighting input for TDDs and light shelfs
         which need to be checked after daylighting input has been read in (CR 7145)
         (eventually this should be changed once/if implementations change to decouple from daylighting calcs so that
         these devices can be used in models without daylighting controls
        CR 7145 was for TDDs, but also implenting check for light shelves, the other "daylighting device"

        METHODOLOGY EMPLOYED:
        loop thru daylighting devices and check that their zones have daylight controls
        '''

        # Using/Aliasing
        using DataDaylighting::NoDaylighting;
        using DataDaylighting::ZoneDaylight;
        using DataHeatBalance::Zone;
        using namespace DataDaylightingDevices;
        using General::RoundSigDigits;

        # SUBROUTINE PARAMETER DEFINITIONS:
        static gio::Fmt fmtA("(A)");

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        PipeNum = 0  # TDD pipe object number
        ShelfNum = 0 # light shelf object number
        SurfNum = 0  # daylight device surface number
        # bool ErrorsFound;
        ErrorsFound = False

        if (CheckTDDs_firstTime):
            CheckTDDZone.dimension(NumOfZones, true);
            CheckTDDs_firstTime = False

        for PipeNum in range(1, NumOfTDDPipes+1):
            SurfNum = TDDPipe(PipeNum).Diffuser
            
            if (SurfNum > 0):
                if (ZoneDaylight(Surface(SurfNum).Zone).DaylightMethod == NoDaylighting):
                    ShowSevereError("DaylightingDevice:Tubular = " + TDDPipe(PipeNum).Name + ":  is not connected to a Zone that has Daylighting.  ");
                    ShowContinueError("Add Daylighting:Controls to Zone named:  " + Zone(Surface(SurfNum).Zone).Name);
                    ShowContinueError("A sufficient control is provided on the .dbg file.");
                    ErrorsFound = True
                    
                    if (CheckTDDZone(Surface(SurfNum).Zone)):
                        gio::write(OutputFileDebug, fmtA) << " ! Following control is to allow tubular reporting in this Zone";
                        gio::write(OutputFileDebug, fmtA) << "Daylighting:Controls,  !- this control controls 0% of zone.";
                        gio::write(OutputFileDebug, fmtA) << "   " + Zone(Surface(SurfNum).Zone).Name + ",  !- Zone Name";
                        gio::write(OutputFileDebug, fmtA) << "     1,   !- Total Daylighting Reference Points";
                        
                        if (DaylRefWorldCoordSystem):
                            # world coordinates, use zone origin for ref pt
                            gio::write(OutputFileDebug, fmtA) << "   " + RoundSigDigits(Zone(Surface(SurfNum).Zone).OriginX, 2) +
                                                                     ",   !- X-Coordinate of First Reference Point {m}";
                            gio::write(OutputFileDebug, fmtA) << "   " + RoundSigDigits(Zone(Surface(SurfNum).Zone).OriginY, 2) +
                                                                     ",   !- Y-Coordinate of First Reference Point {m}";
                            gio::write(OutputFileDebug, fmtA) << "   " + RoundSigDigits(Zone(Surface(SurfNum).Zone).OriginZ, 2) +
                                                                     ",   !- Z-Coordinate of First Reference Point {m}";
                        else:
                            # relative coordinates, use 0,0,0 for ref pt
                            gio::write(OutputFileDebug, fmtA) << "   0.0,   !- X-Coordinate of First Reference Point {m}";
                            gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Y-Coordinate of First Reference Point {m}";
                            gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Z-Coordinate of First Reference Point {m}";
                        
                        gio::write(OutputFileDebug, fmtA) << "      ,   !- X-Coordinate of Second Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "      ,   !- Y-Coordinate of Second Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "      ,   !- Z-Coordinate of Second Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Fraction of Zone Controlled by First Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Fraction of Zone Controlled by Second Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Illuminance Setpoint at First Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Illuminance Setpoint at Second Reference Point";
                        gio::write(OutputFileDebug, fmtA) << "     3,   !- Lighting Control Type";
                        gio::write(OutputFileDebug, fmtA)
                            << "   0.0,   !- Glare Calculation Azimuth Angle of View Direction Clockwise from Zone y-Axis";
                        gio::write(OutputFileDebug, fmtA) << "      ,   !- Maximum Allowable Discomfort Glare Index";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Minimum Input Power Fraction for Continuous Dimming Control";
                        gio::write(OutputFileDebug, fmtA) << "   0.0,   !- Minimum Light Output Fraction for Continuous Dimming Control";
                        gio::write(OutputFileDebug, fmtA) << "     0,   !- Number of Stepped Control Steps";
                        gio::write(OutputFileDebug, fmtA) << "   0.0;   !- Probability Lighting will be Reset When Needed in Manual Stepped Control";

                        CheckTDDZone(Surface(SurfNum).Zone) = False

            else: # SurfNum == 0
                # should not come here (would have already been caught in TDD get input), but is an error
                ShowSevereError("DaylightingDevice:Tubular = " + TDDPipe(PipeNum).Name + ":  Diffuser surface not found ");
                ErrorsFound = True

        for ShelfNum in range(1, NumOfShelf+1):
            SurfNum = Shelf(ShelfNum).Window
            
            if (SurfNum == 0):
                # should not come here (would have already been caught in shelf get input), but is an error
                ShowSevereError("DaylightingDevice:Shelf = " + Shelf(ShelfNum).Name + ":  window not found ");
                ErrorsFound = True

        if (ErrorsFound):
            ShowFatalError("CheckTDDsAndLightShelvesInDaylitZones: Errors in DAYLIGHTING input.");
        
        return None

    # DaylightingManager::AssociateWindowShadingControlWithDaylighting
    def AssociateWindowShadingControlWithDaylighting():
        '''
        no description o.O
        '''
        for iShadeCtrl in range(1, TotWinShadingControl+1):
            found = -1
            
            for jZone in range(1, NumOfZones+1):
                if (UtilityRoutines::SameString(WindowShadingControl(iShadeCtrl).DaylightingControlName, ZoneDaylight(jZone).Name)):
                    found = jZone
                    break

            if (found > 0):
                WindowShadingControl(iShadeCtrl).DaylightControlIndex = found
            else:
                ShowWarningError("AssociateWindowShadingControlWithDaylighting: Daylighting object name used in WindowShadingControl not found.");
                ShowContinueError("..The WindowShadingControl object=\"" + WindowShadingControl(iShadeCtrl).Name +
                                  "\" and referenes an object named: \"" + WindowShadingControl(iShadeCtrl).DaylightingControlName + "\"");
            
        return None
    
    # DaylightingManager::CalcMinIntWinSolidAngs --> acho q não será necessário, pois é para janela
    def CalcMinIntWinSolidAngs():
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Fred Winkelmann
              DATE WRITTEN   Feb. 2004
              MODIFIED:na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        For each Daylighting:Detailed zone finds the minimum solid angle subtended
        by interior windows through which daylight can pass from adjacent zones with
        exterior windows.

        METHODOLOGY EMPLOYED:na
        REFERENCES:na
        '''
        # Using/Aliasing
        using namespace Vectors;

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS: na
        # SUBROUTINE PARAMETER DEFINITIONS: na
        # INTERFACE BLOCK SPECIFICATIONS: na
        # DERIVED TYPE DEFINITIONS: na

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:

        ZoneNum = 0                    # Zone number
        ZoneNumAdj = 0                 # Adjacent zone number
        IWin = 0                       # Window surface number
        IL = 0                         # Reference point number
        loop = 0                       # DO loop index
        # bool is_Triangle;               # True if window is a triangle
        # bool is_Rectangle;              # True if window is a rectangle
        # bool IntWinNextToIntWinAdjZone; # True if an interior window is next to a zone with one or more exterior windows
        IntWinSolidAng = 0.0          # Approximation to solid angle subtended by an interior window from a point a distance SQRT(zone floor area) away.
        static Vector3<Real64> W1;      # Window vertices
        static Vector3<Real64> W2;
        static Vector3<Real64> W3;
        static Vector3<Real64> WC;      # Center point of window
        static Vector3<Real64> W21;     # Unit vectors from window vertex 2 to 1 and 2 to 3
        static Vector3<Real64> W23;
        HW = 0.0                      # Window height and width (m)
        WW = 0.0
        static Vector3<Real64> RREF;  # Location of a reference point in absolute coordinate system
        static Vector3<Real64> Ray;   # Unit vector along ray from reference point to window center
        static Vector3<Real64> REFWC; # Vector from reference point to center of window
        static Vector3<Real64> WNORM; # Unit vector normal to window (pointing away from room)
        DIS = 0.0                   # Distance from ref point to window center (m)
        COSB = 0.0                  # Cosine of angle between ray from ref pt to center of window and window outward normal

        # FLOW:
        for ZoneNum in range(1, NumOfZones+1):
            ZoneDaylight(ZoneNum).MinIntWinSolidAng = 2.0 * math.pi

            if (ZoneDaylight(ZoneNum).TotalDaylRefPoints == 0): continue
            if (ZoneDaylight(ZoneNum).NumOfIntWinAdjZones == 0): continue
            
            for IWin in range( Zone(ZoneNum).SurfaceFirst, Zone(ZoneNum).SurfaceLast+1 ):

                if (Surface(IWin).Class == SurfaceClass_Window && Surface(IWin).ExtBoundCond >= 1):
                    ZoneNumAdj = Surface(Surface(IWin).ExtBoundCond).Zone
                    IntWinNextToIntWinAdjZone = False
                    
                    for loop in range(1, ZoneDaylight(ZoneNum).NumOfIntWinAdjZones+1):
                        if (ZoneNumAdj == ZoneDaylight(ZoneNum).AdjIntWinZoneNums(loop)):
                            IntWinNextToIntWinAdjZone = True
                            break

                    if (IntWinNextToIntWinAdjZone):
                        for IL in range(1, ZoneDaylight(ZoneNum).TotalDaylRefPoints+1):
                            
                            # Reference point in absolute coordinate system
                            RREF = ZoneDaylight(ZoneNum).DaylRefPtAbsCoord({1, 3}, IL)
                            is_Triangle = (Surface(IWin).Sides == 3)
                            is_Rectangle = (Surface(IWin).Sides == 4)
                            
                            if (is_Rectangle):
                                # Vertices of window numbered counter-clockwise starting at upper left as viewed
                                # from inside of room. Assumes original vertices are numbered counter-clockwise from
                                # upper left as viewed from outside.
                                W3 = Surface(IWin).Vertex(2)
                                W2 = Surface(IWin).Vertex(3)
                                W1 = Surface(IWin).Vertex(4)
                            elif (is_Triangle):
                                W3 = Surface(IWin).Vertex(2)
                                W2 = Surface(IWin).Vertex(3)
                                W1 = Surface(IWin).Vertex(1)
                            
                            # Unit vectors from window vertex 2 to 1 and 2 to 3, center point of window,
                            # and vector from ref pt to center of window
                            W21 = W1 - W2
                            W23 = W3 - W2
                            HW = W21.magnitude()
                            WW = W23.magnitude()
                            
                            if (is_Rectangle):
                                WC = W2 + (W23 + W21) / 2.0
                            elif (is_Triangle):
                                WC = W2 + (W23 + W21) / 3.0
                            
                            # Vector from ref point to center of window
                            REFWC = WC - RREF
                            W21 /= HW
                            W23 /= WW
                            
                            # Unit vector normal to window (pointing away from room)
                            WNORM = Surface(IWin).OutNormVec
                            
                            # Distance from ref point to center of window
                            DIS = REFWC.magnitude()
                            
                            # Unit vector from ref point to center of window
                            Ray = REFWC / DIS
                            
                            # Cosine of angle between ray from ref pt to center of window and window outward normal
                            COSB = dot(WNORM, Ray)
                            if (COSB > 0.01765): # 0 <= B < 89 deg
                                # Above test avoids case where ref point cannot receive daylight directly from the
                                # interior window
                                IntWinSolidAng = COSB * Surface(IWin).Area / (pow_2(DIS) + 0.001)
                                ZoneDaylight(ZoneNum).MinIntWinSolidAng = min(ZoneDaylight(ZoneNum).MinIntWinSolidAng, IntWinSolidAng)
                            
                        # End of loop over reference points
            # End of loop over surfaces in zone
        # End of loop over zones

        return None

    # DaylightingManager::DayltgExtHorizIllum
    def DayltgExtHorizIllum(HISK, &HISU):
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Fred Winkelmann
              DATE WRITTEN   July 1997
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Calculates exterior daylight illuminance.

        METHODOLOGY EMPLOYED:
        Called by CalcDayltgCoefficients. Calculates illuminance
        on unobstructed horizontal surface by integrating
        over the luminance distribution of standard CIE skies.
        Calculates horizontal beam illuminance.
        REFERENCES:
        Based on DOE-2.1E subroutine DHILL.

        INPUTS:
                Array1A<Real64> HISK, # Horizontal illuminance from sky for different sky types
                Real64 &HISU          # Horizontal illuminance from sun for unit beam normal
        '''

        # Argument array dimensioning
        HISK.dim = 4

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        #  and overcast sky (lux)
        #   illuminance (lux)

        # SUBROUTINE PARAMETER DEFINITIONS:
        NTH = 18                            # Number of azimuth steps for sky integration
        NPH = 8                             # Number of altitude steps for sky integration
        DTH = (2.0 * Pi) / double(NTH)      # Sky integration azimuth stepsize (radians)
        DPH = PiOvr2 / double(NPH)          # Sky integration altitude stepsize (radians)

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        IPH = 0                            # Altitude index for sky integration
        ITH = 0                            # Azimuth index for sky integration
        PH = pd.Series(NPH*[0])     # Altitude of sky element (radians)
        TH = pd.Series(NTH*[0])     # Azimuth of sky element (radians)
        ISky = 0                           # Sky type index
        SPHCPH = pd.Series(NPH*[0]) # Sine times cosine of altitude of sky element

        # FLOW:
        # Integrate to obtain illuminance from sky.
        # The contribution in lumens/m2 from a patch of sky at altitude PH and azimuth TH
        # is L(TH,PH)*SIN(PH)*COS(PH)*DTH*DPH, where L(TH,PH) is the luminance
        # of the patch in cd/m2.
        #  Init
        if (DayltgExtHorizIllum_firstTime):
            for IPH in range(1, NPH+1):
                PH(IPH) = (IPH - 0.5) * DPH
                SPHCPH(IPH) = math.sin(PH(IPH)) * math.cos(PH(IPH)) # DA = COS(PH)*DTH*DPH
            
            for ITH in range(1, NTH+1):
                TH(ITH) = (ITH - 0.5) * DTH
            
            DayltgExtHorizIllum_firstTime = False

        HISK = 0.0 # --> definido lá em cima com dimensão 4...

        # Sky integration
        for IPH in range(1, NPH+1):
            PH_IPH = PH(IPH)
            SPHCPH_IPH = SPHCPH(IPH)

            for ITH in range(1, NTH+1):
                TH_ITH = TH(ITH)
                
                for ISky in range(1, 5):
                    HISK(ISky) += DayltgSkyLuminance(ISky, TH_ITH, PH_IPH) * SPHCPH_IPH

        for ISky in range(1, 5):
            HISK(ISky) *= DTH * DPH

        # Direct solar horizontal illum (for unit direct normal illuminance)
        HISU = SPHSUN * 1.0
    
        return None

    # DaylightingManager::CalcDayltgCoeffsRefMapPoints
    def CalcDayltgCoeffsRefMapPoints(ZoneNum):
        '''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda Lawrie
              DATE WRITTEN   October 2004
              MODIFIED       May 2006 (RR): added exterior window screens
                             April 2012 (LKL); change to allow multiple maps per zone
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        This subroutine does the daylighting coefficient calculation for the
        daylighting and illuminance map reference points.

        METHODOLOGY EMPLOYED:
        na

        REFERENCES:
        na

        INPUT:
                int const ZoneNum
        '''

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        IWin = 0        # Window counter
        PipeNum = 0     # TDD pipe object number
        loopwin = 0     # loop index for exterior windows associated with a daylit zone
        TZoneNum = 0
        MapNum = 0

        if (VeryFirstTime):
            # make sure all necessary surfaces match to pipes
            ErrorsFound = False
            for TZoneNum in range(1, NumOfZones+1):

                for loopwin in range(1, ZoneDaylight(TZoneNum).NumOfDayltgExtWins+1):
                    IWin = ZoneDaylight(TZoneNum).DayltgExtWinSurfNums(loopwin)
                    if (SurfaceWindow(IWin).OriginalClass != SurfaceClass_TDD_Diffuser):
                        continue
                    
                    # Look up the TDD:DOME object
                    PipeNum = FindTDDPipe(IWin)
                    if (PipeNum == 0):
                        ShowSevereError("GetTDDInput: Surface=" + Surface(IWin).Name +
                                        ", TDD:Dome object does not reference a valid Diffuser object.");
                        ShowContinueError("...needs DaylightingDevice:Tubular of same name as Surface.");
                        ErrorsFound = True

            if (ErrorsFound):
                ShowFatalError("Not all TubularDaylightDome objects have corresponding DaylightingDevice:Tubular objects. Program terminates.");

            VeryFirstTime = False

        # Calc for daylighting reference points
        CalcDayltgCoeffsRefPoints(ZoneNum)

        if (!DoingSizing && !KickOffSimulation):
            # Calc for illuminance map
            if (TotIllumMaps > 0):
                for MapNum in range(1, TotIllumMaps+1):
                    if (IllumMapCalc(MapNum).Zone != ZoneNum):
                        continue
                    if (WarmupFlag):
                        print("Calculating Daylighting Coefficients (Map Points), Zone = {}".format(Zone(ZoneNum).Name))
                    else:
                        print("Updating Daylighting Coefficients (Map Points), Zone = {}".format(Zone(ZoneNum).Name))
                
                CalcDayltgCoeffsMapPoints(ZoneNum)
        
        return None

    # DaylightingManager::GetDaylightingParametersInput
    def GetDaylightingParametersInput():
    	'''
    	SUBROUTINE INFORMATION:
    	    AUTHOR         Linda Lawrie
    	    DATE WRITTEN   Oct 2004
    	    MODIFIED       na
    	    RE-ENGINEERED  na

    	PURPOSE OF THIS SUBROUTINE:
    	This subroutine provides a simple structure to get all daylighting parameters.
        '''
        # Using/Aliasing
        using namespace DataIPShortCuts;

        # RJH DElight Modification Begin
        using namespace DElightManagerF; # Module for managing DElight subroutines
        # RJH DElight Modification End
        # using DataSystemVariables::GoodIOStatValue;

        # Locals
        # SUBROUTINE ARGUMENT DEFINITIONS:
        static gio::Fmt fmtA("(A)");

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        TotDaylightingControls = 0  # Total Daylighting:Controls inputs (splitflux or delight type)
        IntWin = 0                  # Interior window surface index
        # bool ErrorsFound;         # Error flag
        SurfNum = 0                 # Surface counter (loop)
        WindowShadingControlPtr = 0 # Pointer for WindowShadingControl
        ZoneNum = 0                 # Zone Number (loop counter)
        SurfNumAdj = 0              # Surface Number for adjacent surface
        ZoneNumAdj = 0              # Zone Number for adjacent zone
        # RJH DElight Modification Begin - local variable declarations
        dLatitude = 0.0             # double for argument passing
        iErrorFlag = 0              # Error Flag for warning/errors returned from DElight
        iDElightErrorFile = 0       # Unit number for reading DElight Error File
        iReadStatus = 0             # Error File Read Status
        cErrorLine = ""             # Each DElight Error line can be up to 210 characters long
        cErrorMsg = ""              # Each DElight Error Message can be up to 200 characters long
        # bool bEndofErrFile;       # End of Error File flag
        # bool bRecordsOnErrFile;   # true if there are records on the error file
        # RJH DElight Modification End - local variable declarations

        NumReports = 0
        NumNames = 0
        NumNumbers = 0
        IOStat = 0

        ErrorsFound = False
        cCurrentModuleObject = "Daylighting:Controls"
        TotDaylightingControls = inputProcessor->getNumObjectsFound(cCurrentModuleObject);

        if (TotDaylightingControls > 0):
            GetInputDayliteRefPt(ErrorsFound)
            GetDaylightingControls(TotDaylightingControls, ErrorsFound)
            GeometryTransformForDaylighting()
            GetInputIlluminanceMap(ErrorsFound)
            GetLightWellData(ErrorsFound)
            if (ErrorsFound):
            	ShowFatalError("Program terminated for above reasons, related to DAYLIGHTING")
            DayltgSetupAdjZoneListsAndPointers()

        maxNumRefPtInAnyZone = 0
        for SurfNum in range(1, TotSurfaces+1):
            if (Surface(SurfNum).Class != SurfaceClass_Window):
            	continue
            
            ZoneNum = Surface(SurfNum).Zone
            numRefPoints = ZoneDaylight(ZoneNum).TotalDaylRefPoints
            
            if (numRefPoints > maxNumRefPtInAnyZone):
                maxNumRefPtInAnyZone = numRefPoints

            if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 0):
                if (!SurfaceWindow(SurfNum).SurfDayLightInit):
                    SurfaceWindow(SurfNum).SolidAngAtRefPt.allocate(numRefPoints)
                    SurfaceWindow(SurfNum).SolidAngAtRefPt = 0.0
                    SurfaceWindow(SurfNum).SolidAngAtRefPtWtd.allocate(numRefPoints)
                    SurfaceWindow(SurfNum).SolidAngAtRefPtWtd = 0.0
                    SurfaceWindow(SurfNum).IllumFromWinAtRefPt.allocate(2, numRefPoints)
                    SurfaceWindow(SurfNum).IllumFromWinAtRefPt = 0.0
                    SurfaceWindow(SurfNum).BackLumFromWinAtRefPt.allocate(2, numRefPoints)
                    SurfaceWindow(SurfNum).BackLumFromWinAtRefPt = 0.0
                    SurfaceWindow(SurfNum).SourceLumFromWinAtRefPt.allocate(2, numRefPoints)
                    SurfaceWindow(SurfNum).SourceLumFromWinAtRefPt = 0.0
                    SurfaceWindow(SurfNum).IllumFromWinAtRefPtRep.allocate(numRefPoints)
                    SurfaceWindow(SurfNum).IllumFromWinAtRefPtRep = 0.0
                    SurfaceWindow(SurfNum).LumWinFromRefPtRep.allocate(numRefPoints)
                    SurfaceWindow(SurfNum).LumWinFromRefPtRep = 0.0
                    SurfaceWindow(SurfNum).SurfDayLightInit = True
            else:
                SurfNumAdj = Surface(SurfNum).ExtBoundCond
                if (SurfNumAdj > 0):
                    ZoneNumAdj = Surface(SurfNumAdj).Zone
                    
                    if (ZoneDaylight(ZoneNumAdj).TotalDaylRefPoints > 0):
                        if (!SurfaceWindow(SurfNum).SurfDayLightInit):
                            SurfaceWindow(SurfNum).SolidAngAtRefPt.allocate(numRefPoints)
                            SurfaceWindow(SurfNum).SolidAngAtRefPt = 0.0
                            SurfaceWindow(SurfNum).SolidAngAtRefPtWtd.allocate(numRefPoints)
                            SurfaceWindow(SurfNum).SolidAngAtRefPtWtd = 0.0
                            SurfaceWindow(SurfNum).IllumFromWinAtRefPt.allocate(2, numRefPoints)
                            SurfaceWindow(SurfNum).IllumFromWinAtRefPt = 0.0
                            SurfaceWindow(SurfNum).BackLumFromWinAtRefPt.allocate(2, numRefPoints)
                            SurfaceWindow(SurfNum).BackLumFromWinAtRefPt = 0.0
                            SurfaceWindow(SurfNum).SourceLumFromWinAtRefPt.allocate(2, numRefPoints)
                            SurfaceWindow(SurfNum).SourceLumFromWinAtRefPt = 0.0
                            SurfaceWindow(SurfNum).IllumFromWinAtRefPtRep.allocate(numRefPoints)
                            SurfaceWindow(SurfNum).IllumFromWinAtRefPtRep = 0.0
                            SurfaceWindow(SurfNum).LumWinFromRefPtRep.allocate(numRefPoints)
                            SurfaceWindow(SurfNum).LumWinFromRefPtRep = 0.0
                            SurfaceWindow(SurfNum).SurfDayLightInit = True

            if (Surface(SurfNum).ExtBoundCond == ExternalEnvironment):
                WindowShadingControlPtr = Surface(SurfNum).WindowShadingControlPtr

                if (Surface(SurfNum).HasShadeControl):
                    if (WindowShadingControl(WindowShadingControlPtr).GlareControlIsActive):
                        # Error if GlareControlIsActive but window is not in a Daylighting:Detailed zone
                        if (ZoneDaylight(Surface(SurfNum).Zone).TotalDaylRefPoints == 0):
                            ShowSevereError("Window = {} has Window Shading Control with".format(Surface(SurfNum).Name));
                            ShowContinueError("GlareControlIsActive = Yes but it is not in a Daylighting zone.");
                            ShowContinueError("Zone indicated = {}".format(Zone(ZoneNum).Name));
                            ErrorsFound = True

                        # Error if GlareControlIsActive and window is in a Daylighting:Detailed zone with
                        # an interior window adjacent to another Daylighting:Detailed zone
                        if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 0):
                            for IntWin in range(Zone(ZoneNum).SurfaceFirst, Zone(ZoneNum).SurfaceLast+1):
                            # for (IntWin = Zone(ZoneNum).SurfaceFirst; IntWin <= Zone(ZoneNum).SurfaceLast; ++IntWin) {
                                SurfNumAdj = Surface(IntWin).ExtBoundCond
                                if (Surface(IntWin).Class == SurfaceClass_Window && SurfNumAdj > 0):
                                    ZoneNumAdj = Surface(SurfNumAdj).Zone

                                    if (ZoneDaylight(ZoneNumAdj).TotalDaylRefPoints > 0):
                                        ShowSevereError("Window = {} has Window Shading Control with".format(Surface(SurfNum).Name));
                                        ShowContinueError("GlareControlIsActive = Yes and is in a Daylighting zone");
                                        ShowContinueError("that shares an interior window with another Daylighting zone");
                                        ShowContinueError("Adjacent Zone indicated = {}".format(Zone(ZoneNumAdj).Name));
                                        ErrorsFound = True

                    if (WindowShadingControl(WindowShadingControlPtr).ShadingControlType == WSCT_MeetDaylIlumSetp):
                        # Error if window has ShadingControlType = MeetDaylightingIlluminanceSetpoint &
                        # but is not in a Daylighting:Detailed zone
                        if (ZoneDaylight(Surface(SurfNum).Zone).TotalDaylRefPoints == 0):
                            ShowSevereError("Window = {} has Window Shading Control with".format(Surface(SurfNum).Name));
                            ShowContinueError("MeetDaylightingIlluminanceSetpoint but it is not in a Daylighting zone.");
                            ShowContinueError("Zone indicated = {}".format(Zone(ZoneNum).Name));
                            ErrorsFound = True
                        
                        # Error if window has ShadingControlType = MeetDaylightIlluminanceSetpoint and is in a &
                        # Daylighting:Detailed zone with an interior window adjacent to another Daylighting:Detailed zone
                        if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 0):
                            for IntWin in range(Zone(ZoneNum).SurfaceFirst, Zone(ZoneNum).SurfaceLast+1):
                            # for (IntWin = Zone(ZoneNum).SurfaceFirst; IntWin <= Zone(ZoneNum).SurfaceLast; ++IntWin) {
                                SurfNumAdj = Surface(IntWin).ExtBoundCond
                                if (Surface(IntWin).Class == SurfaceClass_Window && SurfNumAdj > 0):
                                    ZoneNumAdj = Surface(SurfNumAdj).Zone
                                    
                                    if (ZoneDaylight(ZoneNumAdj).TotalDaylRefPoints > 0):
                                        ShowSevereError("Window = {} has Window Shading Control with".format(Surface(SurfNum).Name));
                                        ShowContinueError("MeetDaylightIlluminanceSetpoint and is in a Daylighting zone");
                                        ShowContinueError("that shares an interior window with another Daylighting zone");
                                        ShowContinueError("Adjacent Zone indicated = {}".format(Zone(ZoneNumAdj).Name));
                                        ErrorsFound = True

        # RJH DElight Modification Begin - Calls to DElight preprocessing subroutines
        if (doesDayLightingUseDElight()):
            dLatitude = Latitude
            print("Calculating DElight Daylighting Factors")
            DElightInputGenerator()
            # Init Error Flag to 0 (no Warnings or Errors)
            print("ReturnFrom DElightInputGenerator")
            iErrorFlag = 0
            print("Calculating DElight DaylightCoefficients")
            GenerateDElightDaylightCoefficients(dLatitude, iErrorFlag)

            # Check Error Flag for Warnings or Errors returning from DElight
            # RJH 2008-03-07: open file for READWRITE and DELETE file after processing
            print("ReturnFrom DElight DaylightCoefficients Calc")
            if (iErrorFlag != 0):
                # Open DElight Daylight Factors Error File for reading
                iDElightErrorFile = GetNewUnitNumber()
                {
                    IOFlags flags;
                    flags.ACTION("READWRITE");
                    gio::open(iDElightErrorFile, DataStringGlobals::outputDelightDfdmpFileName, flags);
                }

                # Sequentially read lines in DElight Daylight Factors Error File
                # and process them using standard EPlus warning/error handling calls
                # Process all error/warning messages first
                # Then, if any error has occurred, ShowFatalError to terminate processing
                bEndofErrFile = False
                bRecordsOnErrFile = False
                while (!bEndofErrFile):
                    {
                        IOFlags flags;
                        gio::read(iDElightErrorFile, fmtA, flags) >> cErrorLine;
                        iReadStatus = flags.ios();
                    }
                    if (iReadStatus < GoodIOStatValue):
                        bEndofErrFile = True
                        continue
                    
                    bRecordsOnErrFile = True
                    # Is the current line a Warning message?
                    if (has_prefix(cErrorLine, "WARNING: ")):
                        cErrorMsg = cErrorLine.substr(9)
                        ShowWarningError(cErrorMsg)
                    
                    # Is the current line an Error message?
                    if (has_prefix(cErrorLine, "ERROR: ")):
                        cErrorMsg = cErrorLine.substr(7)
                        ShowSevereError(cErrorMsg)
                        iErrorFlag = 1

                # Close and Delete DElight Error File
                if (bRecordsOnErrFile):
                    {
                        IOFlags flags;
                        flags.DISPOSE("DELETE");
                        gio::close(iDElightErrorFile, flags);
                    }
                else:
                    {
                        IOFlags flags;
                        flags.DISPOSE("DELETE");
                        gio::close(iDElightErrorFile, flags);
                    }
                
                # If any DElight Error occurred then ShowFatalError to terminate
                if (iErrorFlag > 0):
                    ErrorsFound = True
                
            else:
                # Open, Close, and Delete DElight Daylight Factors Error File for reading
                iDElightErrorFile = GetNewUnitNumber()
                {
                    IOFlags flags;
                    flags.ACTION("READWRITE");
                    gio::open(iDElightErrorFile, DataStringGlobals::outputDelightDfdmpFileName, flags);
                }
                {
                    IOFlags flags;
                    flags.DISPOSE("DELETE");
                    gio::close(iDElightErrorFile, flags);
                }
        # RJH DElight Modification End - Calls to DElight preprocessing subroutines

        # TH 6/3/2010, added to report daylight factors
        cCurrentModuleObject = "Output:DaylightFactors"
        NumReports = inputProcessor->getNumObjectsFound(cCurrentModuleObject);
        if (NumReports > 0):
            inputProcessor->getObjectItem(cCurrentModuleObject,
                                          1,
                                          cAlphaArgs,
                                          NumNames,
                                          rNumericArgs,
                                          NumNumbers,
                                          IOStat,
                                          lNumericFieldBlanks,
                                          lAlphaFieldBlanks,
                                          cAlphaFieldNames,
                                          cNumericFieldNames);
            if (has_prefix(cAlphaArgs(1), "SIZINGDAYS")):
                DFSReportSizingDays = True
            elif (has_prefix(cAlphaArgs(1), "ALLSHADOWCALCULATIONDAYS")):
                DFSReportAllShadowCalculationDays = True

        if (ErrorsFound):
        	ShowFatalError("Program terminated for above reasons");

    	return None   

    # DaylightingManager::CalcDayltgCoefficients
    def CalcDayltgCoefficients():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Fred Winkelmann
              DATE WRITTEN   July 1997
              MODIFIED       FW, Jan 2002: add variable slat angle blinds
                             FW, Mar 2002: add triangular windows
                             FW, Oct 2002: remove warning on window discretization relative to
                                           reference point distance to window plane
                             FW, Jan 2003: add between-glass shades and blinds
                             FW, Apr 2003: initialize shading type to 'NOSHADE' in window loop
                             PE, May 2003: add light pipes (tubular daylighting devices)
                             FW, Jul 2003: account for possible non-zero transmittance of
                                           shading surfaces (previously all shading surfaces were
                                           assumed to be opaque)
                             PE, Aug 2003: add daylighting shelves
                             FW, Sep 2003: write the bare-window overcast sky daylight factors to the eio file
                             FW, Nov 2003: add exterior beam and sky solar diffuse reflection from obstructions;
                                           add beam solar and sky solar reflection from ground with obstructions.
                             FW, Nov 2003: change expression for NDIVX, NDIVY (no. of window elements in X,Y) to
                                           round up to nearest integer rather than down
                             FW, Nov 2003: add specular reflection of beam solar from obstructions
                             RJH, Jan 2004: add alternative daylighting analysis using DElight
                                            All modifications demarked with RJH (Rob Hitchcock)
                             FW, Feb 2004: add daylighting through interior windows
                             FW, Apr 2004: add light well efficiency that multiplies glazing transmittance
                             FW, Apr 2004: add diffusing glazing
                             RJH, Jul 2004: add error handling for warnings/errors returned from DElight
                             LKL, Oct 2004: Separate "map" and "ref" point calculations -- move some input routines to
                                            separate routines.
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Calculates daylighting factors for later use in the time-step loop.

        METHODOLOGY EMPLOYED:

        For each combination of exterior window and reference point in a zone,
        calculates daylighting factors (interior illuminance / exterior illuminance)
        and glare factors for clear and overcast skies and for windows with and
        without shading devices. These factors are calculated for each hourly
        sun position for design days and for selected days throughout the year.

        If a target zone has one or more interior windows, also calculates daylighting
        factors for the target zone that are associated with exterior windows in adjacent
        zones that share interior windows with the target zone.

        The daylight illuminance at a reference point from a window is determined
        by dividing the window into rectangular elements and calculating the illuminance
        reaching the reference point directly from each element. The illumination
        from an element can come from the sky or ground if the window is unshaded, or from
        a shading device illuminated by solar radiation. Also considered are the
        illuminance contribution from interreflection among the zone's interior surfaces
        and sunlight striking the reference point.

        In calculating sky-related interior illuminance and luminance quantities,
        the sky luminance for the different sky types are determined from distributions
        in which the zenith luminance is normalized to 1.0 cd/m2. Similarly, sun-related
        illuminance and luminance quantities are based on beam normal solar illuminance
        normalized to 1.0 lux.
        The daylight and glare factors calculated in this subroutine are used in DayltgInteriorIllum
        to get the daylight illuminance and glare at each time step.
        Based on this information and user-input lighting setpoint and type of lighting
        control system, DayltgElecLightingControl then determines how much the overhead electric lighting
        can be reduced.

        REFERENCES:
        Based on DOE-2.1E subroutine DCOF.
        '''

        # using DataSystemVariables::DetailedSolarTimestepIntegration;
        # using DaylightingDevices::FindTDDPipe;
        # using DaylightingDevices::TransTDD;
        # using General::BlindBeamBeamTrans;
        # using General::RoundSigDigits;

        # SUBROUTINE PARAMETER DEFINITIONS:
        static gio::Fmt fmtA("(A)");

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        ZoneNum = 0		# Zone number
        IHR = 0			# Hour of day counter
        IWin = 0		# Window counter
        # loop = 0		# DO loop indices
        DaylFac1 = 0.0	# sky daylight factor at ref pt 1
        DaylFac2 = 0.0	# sky daylight factor at ref pt 2

        # added for output all daylight factors
        write_stat = 0
        DFClrSky1 = 0.0
        DFClrTbSky1 = 0.0
        DFIntSky1 = 0.0
        DFOcSky1 = 0.0
        DFClrSky2 = 0.0
        DFClrTbSky2 = 0.0
        DFIntSky2 = 0.0
        DFOcSky2 = 0.0
        SlatAngle = 0.0
        ISA = 0
        ISlatAngle = 0

        CreateDFSReportFile = True
        doSkyReporting = True

        # Formats
        static gio::Fmt Format_700(
            "('! <Sky Daylight Factors>, MonthAndDay, Zone Name, Window Name, Daylight Fac: Ref Pt #1, Daylight Fac: Ref Pt #2')");

        # FLOW:
        if (CalcDayltghCoefficients_firstTime):
            GetDaylightingParametersInput()
            CheckTDDsAndLightShelvesInDaylitZones()
            AssociateWindowShadingControlWithDaylighting()
            CalcDayltghCoefficients_firstTime = False
            
            if (allocated(CheckTDDZone)):
            	CheckTDDZone.deallocate()
        # End of check if firstTime

        # Find the total number of exterior windows associated with all Daylighting:Detailed zones.
        # An exterior window is associated with such a zone if (1) it is an exterior window in the zone, or
        # (2) it is an exterior window in an adjacent zone that shares an interior window with the zone.
        # Note that exterior windows in category (2) may be counted more than once if an adjacent zone
        # is adjacent to more than one daylit zone with which the adjacent zone shares interior windows.
        # If there are no interior windows in a building, than TotWindowsWithDayl is just the total number of
        # exterior windows in Daylighting:Detailed zones. Note that it is possible for a
        # Daylighting:Detailed zone to have zero exterior windows of its own, but it may have an interior
        # through which daylight passes from adjacent zones with exterior windows.
        if (BeginSimFlag):
            TotWindowsWithDayl = 0
            for ZoneNum in range(1, NumOfZones+1):
                TotWindowsWithDayl += ZoneDaylight(ZoneNum).NumOfDayltgExtWins

        if (TotWindowsWithDayl == 0):
        	return None

        #-----------------------------------------!
        # Detailed daylighting factor calculation !
        #-----------------------------------------!
        if (!DetailedSolarTimestepIntegration && !KickOffSizing && !KickOffSimulation):
            if (WarmupFlag):
                print("Calculating Detailed Daylighting Factors, Start Date = {}".format(CurMnDy))
            else:
                print("Updating Detailed Daylighting Factors, Start Date = {}".format(CurMnDy))

        if (BeginSimFlag):

            # Find minimum solid angle subtended by an interior window in Daylighting:Detailed zones.
            # Used in calculating daylighting through interior windows.
            CalcMinIntWinSolidAngs()

            TDDTransVisBeam.allocate(24, NumOfTDDPipes)
            TDDFluxInc.allocate(24, 4, NumOfTDDPipes)
            TDDFluxTrans.allocate(24, 4, NumOfTDDPipes)

            # Warning if detailed daylighting has been requested for a zone with no associated exterior windows.
            for ZoneNum in range(1, NumOfZones+1):
                if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 0 && ZoneDaylight(ZoneNum).NumOfDayltgExtWins == 0):
                    ShowWarningError("Detailed daylighting will not be done for zone=" + Zone(ZoneNum).Name)
                    ShowContinueError("because it has no associated exterior windows.")

            # Find area and reflectance quantities used in calculating inter-reflected illuminance.
            for ZoneNum in range(1, NumOfZones+1):
                # TH 9/10/2009. Need to calculate for zones without daylighting controls (TotalDaylRefPoints = 0)
                # but with adjacent zones having daylighting controls.
                if ((ZoneDaylight(ZoneNum).TotalDaylRefPoints > 0 && ZoneDaylight(ZoneNum).NumOfDayltgExtWins > 0) || ZoneDaylight(ZoneNum).AdjZoneHasDayltgCtrl):
                    DayltgAveInteriorReflectance(ZoneNum)

        # Zero daylighting factor arrays
        if (!DetailedSolarTimestepIntegration):
            TDDTransVisBeam = 0.0
            TDDFluxInc = 0.0
            TDDFluxTrans = 0.0
        else:
            TDDTransVisBeam(HourOfDay, {1, NumOfTDDPipes}) = 0.0
            TDDFluxInc(HourOfDay, {1, 4}, {1, NumOfTDDPipes}) = 0.0
            TDDFluxTrans(HourOfDay, {1, 4}, {1, NumOfTDDPipes}) = 0.0

        if (!DetailedSolarTimestepIntegration):
            if (BeginDayFlag):
                # Calculate hourly sun angles, clear sky zenith luminance, and exterior horizontal illuminance
                PHSUN = 0.0
                SPHSUN = 0.0
                CPHSUN = 0.0
                THSUN = 0.0

                PHSUNHR = 0.0
                SPHSUNHR = 0.0
                CPHSUNHR = 0.0
                THSUNHR = 0.0
                GILSK = 0.0
                GILSU = 0.0

                for IHR in range(1, 25):
                    if (SUNCOSHR(IHR, 3) < SunIsUpValue):
                		# Skip if sun is below horizon #Autodesk SUNCOSHR was uninitialized here
                    	continue
                    
                    PHSUN = PiOvr2 - math.acos(SUNCOSHR(IHR, 3))
                    PHSUNHR(IHR) = PHSUN
                    SPHSUNHR(IHR) = math.sin(PHSUN)
                    CPHSUNHR(IHR) = math.cos(PHSUN)
                    THSUNHR(IHR) = math.atan2(SUNCOSHR(IHR, 2), SUNCOSHR(IHR, 1))
                    
                    # Get exterior horizontal illuminance from sky and sun
                    THSUN = THSUNHR(IHR)
                    SPHSUN = SPHSUNHR(IHR)
                    CPHSUN = CPHSUNHR(IHR)
                    DayltgExtHorizIllum(GILSK(IHR, 1), GILSU(IHR))
        else:
        	# timestep integrated calculations
            PHSUN = 0.0
            SPHSUN = 0.0
            CPHSUN = 0.0
            THSUN = 0.0

            PHSUNHR(HourOfDay) = 0.0
            SPHSUNHR(HourOfDay) = 0.0
            CPHSUNHR(HourOfDay) = 0.0
            THSUNHR(HourOfDay) = 0.0
            GILSK(HourOfDay, {1, 4}) = 0.0
            GILSU(HourOfDay) = 0.0
            
            if (!(SUNCOSHR(HourOfDay, 3) < SunIsUpValue)):
            	# Skip if sun is below horizon
                PHSUN = PiOvr2 - math.acos(SUNCOSHR(HourOfDay, 3))
                PHSUNHR(HourOfDay) = PHSUN
                SPHSUNHR(HourOfDay) = math.sin(PHSUN)
                CPHSUNHR(HourOfDay) = math.cos(PHSUN)
                THSUNHR(HourOfDay) = math.atan2(SUNCOSHR(HourOfDay, 2), SUNCOSHR(HourOfDay, 1))
                
                # Get exterior horizontal illuminance from sky and sun
                THSUN = THSUNHR(HourOfDay)
                SPHSUN = SPHSUNHR(HourOfDay)
                CPHSUN = CPHSUNHR(HourOfDay)
                DayltgExtHorizIllum(GILSK(HourOfDay, 1), GILSU(HourOfDay))

        #           -----------
        # ---------- ZONE LOOP ----------
        #           -----------
        for ZoneNum in range(1, NumOfZones+1):
            # Skip zones that are not Daylighting:Detailed zones.
            # TotalDaylRefPoints = 0 means zone has (1) no daylighting or (3) Daylighting:DElight
            if (ZoneDaylight(ZoneNum).TotalDaylRefPoints == 0 || ZoneDaylight(ZoneNum).DaylightMethod != SplitFluxDaylighting):
            	continue

            # Skip zones with no exterior windows in the zone or in adjacent zone with which an interior window is shared
            if (ZoneDaylight(ZoneNum).NumOfDayltgExtWins == 0):
        		continue

            CalcDayltgCoeffsRefMapPoints(ZoneNum)

        # End of zone loop, ZoneNum

        if (doSkyReporting):
            if (!KickOffSizing && !KickOffSimulation):
                if (FirstTimeDaylFacCalc && TotWindowsWithDayl > 0):
                    # Write the bare-window four sky daylight factors at noon time to the eio file; this is done only
                    # for first time that daylight factors are calculated and so is insensitive to possible variation
                    # due to change in ground reflectance from month to month, or change in storm window status.
                    gio::write(OutputFileInits, Format_700);

                    for ZoneNum in range(1, NumOfZones+1):
                        if (ZoneDaylight(ZoneNum).NumOfDayltgExtWins == 0 || ZoneDaylight(ZoneNum).DaylightMethod != SplitFluxDaylighting):
                    		continue
                        for loop in range(1, ZoneDaylight(ZoneNum).NumOfDayltgExtWins+1):
                            IWin = ZoneDaylight(ZoneNum).DayltgExtWinSurfNums(loop)
                            # For this report, do not include ext wins in zone adjacent to ZoneNum since the inter-reflected
                            # component will not be calculated for these windows until the time-step loop.
                            if (Surface(IWin).Zone == ZoneNum):
                                # clear sky
                                DaylFac1 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 1, 1, loop)
                                DaylFac2 = 0.0
                                if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 1):
                                	DaylFac2 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 1, 2, loop)

                                gio::write(OutputFileInits, fmtA) << " Clear Sky Daylight Factors," + CurMnDy + ',' + Zone(ZoneNum).Name + ',' +
                                                                         Surface(IWin).Name + ',' + RoundSigDigits(DaylFac1, 4) + ',' +
                                                                         RoundSigDigits(DaylFac2, 4);

                                # clear Turbid sky
                                DaylFac1 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 2, 1, loop)
                                DaylFac2 = 0.0
                                if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 1):
                                	DaylFac2 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 2, 2, loop)

                                gio::write(OutputFileInits, fmtA) << " Clear Turbid Sky Daylight Factors," + CurMnDy + ',' + Zone(ZoneNum).Name +
                                                                         ',' + Surface(IWin).Name + ',' + RoundSigDigits(DaylFac1, 4) + ',' +
                                                                         RoundSigDigits(DaylFac2, 4);

                                # Intermediate sky
                                DaylFac1 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 3, 1, loop)
                                DaylFac2 = 0.0
                                if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 1):
                                	DaylFac2 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 3, 2, loop)
                                
                                gio::write(OutputFileInits, fmtA) << " Intermediate Sky Daylight Factors," + CurMnDy + ',' + Zone(ZoneNum).Name +
                                                                         ',' + Surface(IWin).Name + ',' + RoundSigDigits(DaylFac1, 4) + ',' +
                                                                         RoundSigDigits(DaylFac2, 4);

                                # Overcast sky
                                DaylFac1 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 4, 1, loop)
                                DaylFac2 = 0.0
                                if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 1):
                                	DaylFac2 = ZoneDaylight(ZoneNum).DaylIllFacSky(12, 1, 4, 2, loop)

                                gio::write(OutputFileInits, fmtA) << " Overcast Sky Daylight Factors," + CurMnDy + ',' + Zone(ZoneNum).Name + ',' +
                                                                         Surface(IWin).Name + ',' + RoundSigDigits(DaylFac1, 4) + ',' +
                                                                         RoundSigDigits(DaylFac2, 4);
                    FirstTimeDaylFacCalc = False
                    doSkyReporting = False

        # TH 7/2010 report all daylight factors for the two reference points of daylight zones ...

        # Skip if no daylight windows
        if (TotWindowsWithDayl == 0): return None

        # Skip if no request of reporting
        if ((!DFSReportSizingDays) && (!DFSReportAllShadowCalculationDays)): return None

        # Skip duplicate calls
        if (KickOffSizing): return None
        if (DoingSizing): return None
        if (KickOffSimulation): return None

        if (DFSReportSizingDays):
            if (DoWeathSim && DoDesDaySim):
                if (KindOfSim == ksRunPeriodWeather): return None

        if (DFSReportAllShadowCalculationDays):
            if (KindOfSim != ksRunPeriodWeather): return None

        # open a new file eplusout.dfs for saving the daylight factors
        if (CreateDFSReportFile):
            OutputFileDFS = GetNewUnitNumber()
            {
                IOFlags flags;
                flags.ACTION("write");
                gio::open(OutputFileDFS, DataStringGlobals::outputDfsFileName, flags);
                write_stat = flags.ios();
            }
            if (write_stat != 0):
                ShowFatalError("CalcDayltgCoefficients: Could not open file {} for output (write).".format(DataStringGlobals::outputDfsFileName));
            else:
                gio::write(OutputFileDFS, fmtA) << "This file contains daylight factors for all exterior windows of daylight zones.";
                gio::write(OutputFileDFS, fmtA) << "If only one reference point the last 4 columns in the data will be zero.";
                gio::write(OutputFileDFS, fmtA) << "MonthAndDay,Zone Name,Window Name,Window State";
                gio::write(OutputFileDFS, fmtA) << "Hour,Daylight Factor for Clear Sky at Reference point 1,Daylight Factor for Clear Turbid Sky at "
                                                   "Reference point 1,Daylight Factor for Intermediate Sky at Reference point 1,Daylight Factor for "
                                                   "Overcast Sky at Reference point 1,Daylight Factor for Clear Sky at Reference point 2,Daylight "
                                                   "Factor for Clear Turbid Sky at Reference point 2,Daylight Factor for Intermediate Sky at "
                                                   "Reference point 2,Daylight Factor for Overcast Sky at Reference point 2";
            CreateDFSReportFile = False

        for ZoneNum in range(1, NumOfZones+1):
            if (ZoneDaylight(ZoneNum).NumOfDayltgExtWins == 0):
            	continue

            for loop in range(1, ZoneDaylight(ZoneNum).NumOfDayltgExtWins+1):
                IWin = ZoneDaylight(ZoneNum).DayltgExtWinSurfNums(loop)

                # For this report, do not include ext wins in zone adjacent to ZoneNum since the inter-reflected
                # component will not be calculated for these windows until the time-step loop.
                if (Surface(IWin).Zone == ZoneNum):

                    if (SurfaceWindow(IWin).MovableSlats):
                        # variable slat angle - MaxSlatangle sets
                        ISA = MaxSlatAngs + 1
                    elif (Surface(IWin).HasShadeControl):
                        # window shade or blind with fixed slat angle
                        ISA = 2
                    else:
                        # base window
                        ISA = 1

                    # loop over each slat angle
                    for ISlatAngle in range(1, ISA+1):
                        if (ISlatAngle == 1):
                            # base window without shades, screens, or blinds
                            gio::write(OutputFileDFS, fmtA) << CurMnDy + ',' + Zone(ZoneNum).Name + ',' + Surface(IWin).Name + ",Base Window";
                        elif (ISlatAngle == 2 && ISA == 2):
                            # window shade or blind with fixed slat angle
                            gio::write(OutputFileDFS, fmtA) << CurMnDy + ',' + Zone(ZoneNum).Name + ',' + Surface(IWin).Name + ", ";
                        else:
                            # blind with variable slat angle
                            SlatAngle = 180.0 / double(MaxSlatAngs - 1) * double(ISlatAngle - 2)
                            gio::write(OutputFileDFS, fmtA)
                                << CurMnDy + ',' + Zone(ZoneNum).Name + ',' + Surface(IWin).Name + ',' + RoundSigDigits(SlatAngle, 1);

                        for IHR in range(1, 25):
                            # daylight reference point 1
                            DFClrSky1 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 1, 1, loop)   # clear sky
                            DFClrTbSky1 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 2, 1, loop) # clear Turbid sky
                            DFIntSky1 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 3, 1, loop)   # Intermediate sky
                            DFOcSky1 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 4, 1, loop)    # Overcast sky

                            # daylight reference point 2
                            if (ZoneDaylight(ZoneNum).TotalDaylRefPoints > 1):
                                DFClrSky2 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 1, 2, loop)
                                DFClrTbSky2 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 2, 2, loop)
                                DFIntSky2 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 3, 2, loop)
                                DFOcSky2 = ZoneDaylight(ZoneNum).DaylIllFacSky(IHR, ISlatAngle, 4, 2, loop)
                            else:
                                DFClrSky2 = 0.0
                                DFClrTbSky2 = 0.0
                                DFIntSky2 = 0.0
                                DFOcSky2 = 0.0

                            # write daylight factors - 4 sky types for each daylight ref point
                            gio::write(OutputFileDFS, fmtA)
                                << RoundSigDigits(IHR) + ',' + RoundSigDigits(DFClrSky1, 5) + ',' + RoundSigDigits(DFClrTbSky1, 5) + ',' +
                                       RoundSigDigits(DFIntSky1, 5) + ',' + RoundSigDigits(DFOcSky1, 5) + ',' + RoundSigDigits(DFClrSky2, 5) + ',' +
                                       RoundSigDigits(DFClrTbSky2, 5) + ',' + RoundSigDigits(DFIntSky2, 5) + ',' + RoundSigDigits(DFOcSky2, 5);
                        # end hour loop
            # end exterior windows in zone loop
        # end zone loop
	    return None

    # PAREI AQUI!
	# ScheduleManager::GetScheduleIndex
    def GetScheduleIndex(&ScheduleName):
    	'''
        FUNCTION INFORMATION:
              AUTHOR         Linda K. Lawrie
              DATE WRITTEN   September 1997
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS FUNCTION:
        This function returns the internal pointer to Schedule "ScheduleName".
		'''

        # Return value
        GetScheduleIndex = 0

        # FUNCTION LOCAL VARIABLE DECLARATIONS:
        DayCtr = 0
        WeekCtr = 0

        if (!ScheduleInputProcessed):
            ProcessScheduleInput()
            ScheduleInputProcessed = True

        if (NumSchedules > 0):
            GetScheduleIndex = UtilityRoutines::FindItemInList(ScheduleName, Schedule({1, NumSchedules}))
            if (GetScheduleIndex > 0):
                if (!Schedule(GetScheduleIndex).Used):
                    Schedule(GetScheduleIndex).Used = True
                    
                    for WeekCtr in range(1, 367):
                        if (Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr) > 0):
                            WeekSchedule(Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr)).Used = True
                            
                            for DayCtr in range(1, MaxDayTypes+1):
                                DaySchedule(WeekSchedule(Schedule(GetScheduleIndex).WeekSchedulePointer(WeekCtr)).DaySchedulePointer(DayCtr)).Used = True
        else:
            GetScheduleIndex = 0

        return GetScheduleIndex

    # ScheduleManager::getNumObjectsFound
    def getNumObjectsFound(std::string const &ObjectWord):
		'''
	    FUNCTION INFORMATION:
	          AUTHOR         Linda K. Lawrie
	          DATE WRITTEN   September 1997
	          MODIFIED       Mark Adams
	          RE-ENGINEERED  na

	    PURPOSE OF THIS SUBROUTINE:
	    This function returns the number of objects (in input data file)
	    found in the current run.  If it can't find the object in list
	    of objects, a 0 will be returned.

	    METHODOLOGY EMPLOYED:
	    Look up object in list of objects.  If there, return the
	    number of objects found in the current input.  If not, return 0.
	    '''
	    auto const &find_obj = epJSON.find(ObjectWord);

	    if (find_obj == epJSON.end()):
	        auto tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(ObjectWord));
	        
	        if (tmp_umit == caseInsensitiveObjectMap.end() || epJSON.find(tmp_umit->second) == epJSON.end()):
	            return 0
	        
	        return static_cast<int>(epJSON[tmp_umit->second].size());
	    else:
	        return static_cast<int>(find_obj.value().size());

	    if (schema["properties"].find(ObjectWord) == schema["properties"].end()):
	        auto tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(ObjectWord));
	        if (tmp_umit == caseInsensitiveObjectMap.end()):
	            ShowWarningError("Requested Object not found in Definitions: {}.".format(ObjectWord))

	    return 0

	# ScheduleManager::getObjectItem
	def getObjectItem(&Object, Number, Alphas, &NumAlphas, Numbers, &NumNumbers, &Status, *args):
		# void InputProcessor::getObjectItem(std::string const &Object,
  		#                            int const Number,
		#                            Array1S_string Alphas,
		#                            int &NumAlphas,
		#                            Array1S<Real64> Numbers,
		#                            int &NumNumbers,
		#                            int &Status,
		#                            Optional<pd.Series()> NumBlank,
		#                            Optional<pd.Series()> AlphaBlank,
		#                            Optional<pd.Series()> AlphaFieldNames,
		#                            Optional<pd.Series()> NumericFieldNames)
		#							 *args = (NumBlank, AlphaBlank, AlphaFieldNames, NumericFieldNames)
		'''
	    SUBROUTINE INFORMATION:
	          AUTHOR         Linda K. Lawrie
	          DATE WRITTEN   September 1997
	          MODIFIED       na
	          RE-ENGINEERED  na

	    PURPOSE OF THIS SUBROUTINE:
	    This subroutine gets the 'number' 'object' from the IDFRecord data structure.
	    '''

	    int adjustedNumber = getJSONObjNum(Object, Number) # if incoming input is idf, then use idf object order

	    auto objectInfo = ObjectInfo()
	    objectInfo.objectType = Object
	    # auto sorted_iterators = find_iterators

	    auto find_iterators = objectCacheMap.find(Object)
	    if (find_iterators == objectCacheMap.end()):
	        auto const tmp_umit = caseInsensitiveObjectMap.find(convertToUpper(Object))
	        if (tmp_umit == caseInsensitiveObjectMap.end() || epJSON.find(tmp_umit->second) == epJSON.end()):
	            return None

	        objectInfo.objectType = tmp_umit->second
	        find_iterators = objectCacheMap.find(objectInfo.objectType)

	    NumAlphas = 0
	    NumNumbers = 0
	    Status = -1
	    auto const &is_AlphaBlank = present(AlphaBlank)
	    auto const &is_AlphaFieldNames = present(AlphaFieldNames)
	    auto const &is_NumBlank = present(NumBlank)
	    auto const &is_NumericFieldNames = present(NumericFieldNames)

	    auto const &epJSON_it = find_iterators->second.inputObjectIterators.at(adjustedNumber - 1)
	    auto const &epJSON_schema_it = find_iterators->second.schemaIterator
	    auto const &epJSON_schema_it_val = epJSON_schema_it.value()

	    # Locations in JSON schema relating to normal fields
	    auto const &schema_obj_props = epJSON_schema_it_val["patternProperties"][".*"]["properties"]

	    # Locations in JSON schema storing the positional aspects from the IDD format, legacy prefixed
	    auto const &legacy_idd = epJSON_schema_it_val["legacy_idd"]
	    auto const &legacy_idd_field_info = legacy_idd["field_info"]
	    auto const &legacy_idd_fields = legacy_idd["fields"]
	    auto const &schema_name_field = epJSON_schema_it_val.find("name")

	    auto key = legacy_idd.find("extension")
	    extension_key = ""
	    if (key != legacy_idd.end()):
	        extension_key = key.value()

	    Alphas = ""
	    Numbers = 0
	    if (is_NumBlank): NumBlank() = True
	    if (is_AlphaBlank): AlphaBlank() = True
	    if (is_AlphaFieldNames): AlphaFieldNames() = ""
	    if (is_NumericFieldNames): NumericFieldNames() = ""

	    auto const &obj = epJSON_it;
	    auto const &obj_val = obj.value();

	    objectInfo.objectName = obj.key();

	    auto const find_unused = unusedInputs.find(objectInfo);
	    if (find_unused != unusedInputs.end()):
	        unusedInputs.erase(find_unused)

	    size_t idf_max_fields = 0
	    auto found_idf_max_fields = obj_val.find("idf_max_fields");
	    if (found_idf_max_fields != obj_val.end()):
	        idf_max_fields = *found_idf_max_fields

	    size_t idf_max_extensible_fields = 0
	    auto found_idf_max_extensible_fields = obj_val.find("idf_max_extensible_fields");
	    if (found_idf_max_extensible_fields != obj_val.end()):
	        idf_max_extensible_fields = *found_idf_max_extensible_fields;

	    alpha_index = 1
	    numeric_index = 1

	    for (size_t i = 0; i < legacy_idd_fields.size(); ++i) { # q porra é essa?
	        std::string const &field = legacy_idd_fields[i];
	        auto const &field_info = legacy_idd_field_info.find(field);
	        if (field_info == legacy_idd_field_info.end()):
	            ShowFatalError("Could not find field = \"" + field + "\" in \"" + Object + "\" in epJSON Schema.");
	        
	        auto const &field_type = field_info.value().at("field_type").get<std::string>();
	        within_idf_fields = (i < idf_max_fields)
	        if (field == "name" && schema_name_field != epJSON_schema_it_val.end()):
	            auto const &name_iter = schema_name_field.value();
	            if (name_iter.find("retaincase") != name_iter.end()):
	                Alphas(alpha_index) = objectInfo.objectName
	            else:
	                Alphas(alpha_index) = UtilityRoutines::MakeUPPERCase(objectInfo.objectName);

	            if (is_AlphaBlank):
	            	AlphaBlank()(alpha_index) = objectInfo.objectName.empty()
	            
	            if (is_AlphaFieldNames):
	                AlphaFieldNames()(alpha_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();

	            NumAlphas += 1
	            alpha_index += 1
	            continue

	        auto const &schema_field_obj = schema_obj_props[field];
	        auto it = obj_val.find(field);
	        if (it != obj_val.end()):
	            auto const &field_value = it.value();
	            if (field_type == "a"):
	                # process alpha value
	                if (field_value.is_string()):
	                    auto const value = getObjectItemValue(field_value.get<std::string>(), schema_field_obj);

	                    Alphas(alpha_index) = value.first
	                    if (is_AlphaBlank):
	                    	AlphaBlank()(alpha_index) = value.second;

	                else:
	                    if (field_value.is_number_integer()):
	                        i64toa(field_value.get<std::int64_t>(), s);
	                    else:
	                        dtoa(field_value.get<double>(), s);

	                    Alphas(alpha_index) = s
	                    if (is_AlphaBlank):
	                    	AlphaBlank()(alpha_index) = False

	            elif (field_type == "n"):
	                # process numeric value
	                if (field_value.is_number()):
	                    if (field_value.is_number_integer()):
	                        Numbers(numeric_index) = field_value.get<std::int64_t>();
	                    else:
	                        Numbers(numeric_index) = field_value.get<double>();

	                    if (is_NumBlank):
	                    	NumBlank()(numeric_index) = False
	                else:
	                    is_empty = field_value.get<std::string>().empty()
	                    if (is_empty):
	                        findDefault(Numbers(numeric_index), schema_field_obj);
	                    else:
	                        Numbers(numeric_index) = -99999 # autosize and autocalculate

	                    if (is_NumBlank):
	                    	NumBlank()(numeric_index) = is_empty
	        else:
	            if (field_type == "a"):
	                if (!(within_idf_fields && findDefault(Alphas(alpha_index), schema_field_obj))):
	                    Alphas(alpha_index) = ""
	                
	                if (is_AlphaBlank):
	                	AlphaBlank()(alpha_index) = True
	            elif (field_type == "n"):
	                if (within_idf_fields):
	                    findDefault(Numbers(numeric_index), schema_field_obj);
	                else:
	                    Numbers(numeric_index) = 0
	                
	                if (is_NumBlank) NumBlank()(numeric_index) = True

	        if (field_type == "a"):
	            if (within_idf_fields):
	            	NumAlphas += 1
	            
	            if (is_AlphaFieldNames):
	                AlphaFieldNames()(alpha_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();
	            
	            alpha_index += 1
	        elif (field_type == "n"):
	            if (within_idf_fields):
	            	NumNumbers += 1
	            if (is_NumericFieldNames):
	                NumericFieldNames()(numeric_index) = (DataGlobals::isEpJSON) ? field : field_info.value().at("field_name").get<std::string>();
	            
	            numeric_index += 1

	    size_t extensible_count = 0
	    auto const &legacy_idd_extensibles_iter = legacy_idd.find("extensibles");
	    
	    if (legacy_idd_extensibles_iter != legacy_idd.end()):
	        auto const epJSON_extensions_array_itr = obj.value().find(extension_key);
	        
	        if (epJSON_extensions_array_itr != obj.value().end()):
	            auto const &legacy_idd_extensibles = legacy_idd_extensibles_iter.value();
	            auto const &epJSON_extensions_array = epJSON_extensions_array_itr.value();
	            auto const &schema_extension_fields = schema_obj_props[extension_key]["items"]["properties"];

	            for (auto it = epJSON_extensions_array.begin(); it != epJSON_extensions_array.end(); ++it) { # que porra é essa?
	                auto const &epJSON_extension_obj = it.value();

	                for (size_t i = 0; i < legacy_idd_extensibles.size(); i++, extensible_count++) { # que porra é essa?
	                    std::string const &field_name = legacy_idd_extensibles[i];
	                    auto const &epJSON_obj_field_iter = epJSON_extension_obj.find(field_name);
	                    auto const &schema_field = schema_extension_fields[field_name];

	                    auto const &field_info = legacy_idd_field_info.find(field_name);
	                    if (field_info == legacy_idd_field_info.end()):
	                        ShowFatalError("Could not find field = \"" + field_name + "\" in \"" + Object + "\" in epJSON Schema.");
	                    
	                    auto const &field_type = field_info.value().at("field_type").get<std::string>();
	                    within_idf_extensible_fields = (extensible_count < idf_max_extensible_fields)

	                    if (epJSON_obj_field_iter != epJSON_extension_obj.end()):
	                        auto const &field_value = epJSON_obj_field_iter.value();

	                        if (field_type == "a"):
	                            if (field_value.is_string()):
	                                auto const value = getObjectItemValue(field_value.get<std::string>(), schema_field);

	                                Alphas(alpha_index) = value.first;
	                                if (is_AlphaBlank):
	                                	AlphaBlank()(alpha_index) = value.second
	                            else:
	                                if (field_value.is_number_integer()):
	                                    i64toa(field_value.get<std::int64_t>(), s);
	                                else:
	                                    dtoa(field_value.get<double>(), s);
	                                
	                                Alphas(alpha_index) = s
	                                if (is_AlphaBlank):
	                                	AlphaBlank()(alpha_index) = False
	                            
	                        elif (field_type == "n"):
	                            if (field_value.is_number()):
	                                if (field_value.is_number_integer()):
	                                    Numbers(numeric_index) = field_value.get<std::int64_t>();
	                                else:
	                                    Numbers(numeric_index) = field_value.get<double>();
	                                
	                                if (is_NumBlank):
	                                	NumBlank()(numeric_index) = False
	                            
	                            else:
	                                is_empty = field_value.get<std::string>().empty()
	                                if (is_empty):
	                                    findDefault(Numbers(numeric_index), schema_field)
	                                else:
	                                    Numbers(numeric_index) = -99999 # autosize and autocalculate
	                                
	                                if (is_NumBlank):
	                                	NumBlank()(numeric_index) = is_empty
	                    else:
	                        if (field_type == "a"):
	                            if (!(within_idf_extensible_fields && findDefault(Alphas(alpha_index), schema_field))):
	                                Alphas(alpha_index) = ""
	                            
	                            if (is_AlphaBlank):
	                            	AlphaBlank()(alpha_index) = True
	                        
	                        elif (field_type == "n"):
	                            if (within_idf_extensible_fields):
	                                findDefault(Numbers(numeric_index), schema_field)
	                            else:
	                                Numbers(numeric_index) = 0
	                            
	                            if (is_NumBlank):
	                            	NumBlank()(numeric_index) = True

	                    if (field_type == "a"):
	                        if (within_idf_extensible_fields):
	                        	NumAlphas += 1
	                        if (is_AlphaFieldNames):
	                            AlphaFieldNames()(alpha_index) = (DataGlobals::isEpJSON) ? field_name : field_info.value().at("field_name").get<std::string>();
	                        
	                        alpha_index += 1
	                    
	                    elif (field_type == "n"):
	                        if (within_idf_extensible_fields):
	                        	NumNumbers += 1
	                        if (is_NumericFieldNames):
	                            NumericFieldNames()(numeric_index) = (DataGlobals::isEpJSON) ? field_name : field_info.value().at("field_name").get<std::string>();
	                        
	                        numeric_index += 1

	    Status = 1 # ?
	    return None

	# DataTimings::EP_Count_Calls --> como definir esta merda?!
	ifdef EP_Count_Calls
	    int NumShadow_Calls(0);
	    int NumShadowAtTS_Calls(0);
	    int NumClipPoly_Calls(0);
	    int NumInitSolar_Calls(0);
	    int NumAnisoSky_Calls(0);
	    int NumDetPolyOverlap_Calls(0);
	    int NumCalcPerSolBeam_Calls(0);
	    int NumDetShadowCombs_Calls(0);
	    int NumIntSolarDist_Calls(0);
	    int NumIntRadExchange_Calls(0);
	    int NumIntRadExchangeZ_Calls(0);
	    int NumIntRadExchangeMain_Calls(0);
	    int NumIntRadExchangeOSurf_Calls(0);
	    int NumIntRadExchangeISurf_Calls(0);
	    int NumMaxInsideSurfIterations(0);
	    int NumCalcScriptF_Calls(0);
	endif

	# OutputReportPredefined.cc::PreDefTableEntry
	def PreDefTableEntry(columnIndex, &objName, tableEntryInt):
		# void PreDefTableEntry(int const columnIndex, std::string const &objName, int const tableEntryInt)
	    '''
        SUBROUTINE INFORMATION:
              AUTHOR         Jason Glazer
              DATE WRITTEN   August 2006
              MODIFIED
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
          Creates an entry for predefined tables when the entry
          is a integer variable

        METHODOLOGY EMPLOYED:
          Simple assignments to public variables.
		'''
        # SUBROUTINE PARAMETER DEFINITIONS:
        static gio::Fmt fmtLD("*");

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        std::string stringEntry;

        incrementTableEntry()
        # convert the integer to a string
        gio::write(stringEntry, fmtLD) << tableEntryInt;
        tableEntry(numTableEntry).charEntry = stringEntry;
        tableEntry(numTableEntry).objectName = objName;
        tableEntry(numTableEntry).indexColumn = columnIndex;

        return None

    # WindowComplexManager::InitComplexWindows --> Será usado?
    def InitComplexWindows():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Linda Lawrie
              DATE WRITTEN   November 2012
              MODIFIED       na
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Extract simple init for Complex Windows
		'''
        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        Once = True # Flag for insuring things happen once

        # One-time initialization
        if (Once):
            Once = False
            InitBSDFWindows()
            CalcStaticProperties()

        return None

    # WindowComplexManager::UpdateComplexWindows --> Será usado?
    def UpdateComplexWindows():
    	'''
        SUBROUTINE INFORMATION:
              AUTHOR         Joe Klems
              DATE WRITTEN   August 2011
              MODIFIED       B. Griffith, Nov. 2012 revised for detailed timestep integration mode
              RE-ENGINEERED  na

        PURPOSE OF THIS SUBROUTINE:
        Performs the shading-dependent initialization of the Complex Fenestration data;
        On first call, calls the one-time initializition

        METHODOLOGY EMPLOYED:
        <description>
		'''

        # Using/Aliasing
        using DataGlobals::KickOffSimulation;
        using DataGlobals::KickOffSizing;

        # SUBROUTINE LOCAL VARIABLE DECLARATIONS:
        # LOGICAL,SAVE    ::  Once  =.TRUE.  !Flag for insuring things happen once
        NumStates = 0 # Number of states for a given complex fen
        ISurf = 0     # Index for sorting thru Surface array
        IState = 0    # Index identifying the window state for a particular window
        IWind = 0     # Index identifying a window in the WindowList

        # !One-time initialization
		# IF (Once) THEN
		#   ONCE = .FALSE.
		#   CALL InitBSDFWindows
		#   CALL CalcStaticProperties
		# ENDIF

        if (NumComplexWind == 0): return None
        if (KickOffSizing || KickOffSimulation): return None

        # Shading-dependent initialization; performed once for each shading period

        # Initialize the geometric quantities

        for IWind in range(1, NumComplexWind+1):
            ISurf = WindowList(IWind).SurfNo
            NumStates = ComplexWind(ISurf).NumStates
            for IState in range(1, NumStates+1):
                CFSShadeAndBeamInitialization(ISurf, IState)
            # State loop
        # window loop
    
    	return None

class SolarShading(ExternalFunctions):
	'''
    MODULE INFORMATION:
          AUTHOR         Rick Strand
          DATE WRITTEN   March 1997
          MODIFIED       December 1998, FCW
          MODIFIED       July 1999, Linda Lawrie, eliminate shadefl.scr,
                         do shadowing calculations during simulation
          MODIFIED       June 2001, FCW, handle window blinds
          MODIFIED       May 2004, LKL, Polygons > 4 sides (not subsurfaces)
          MODIFIED       January 2007, LKL, Taking parameters back to original integer (HC)
          MODIFIED       August 2011, JHK, Including Complex Fenestration optical calculations
          MODIFIED       November 2012, BG, Timestep solar and daylighting calculations
          RE-ENGINEERED  na

    PURPOSE OF THIS MODULE:
    The purpose of this module is to encompass the routines and data
    which are need to perform the solar calculations in EnergyPlus.
    This also requires that shading and geometry routines and data
    which are used by the solar calculations be included in this module.

    METHODOLOGY EMPLOYED:
    Many of the methods used in this module have been carried over from the
    (I)BLAST program.  As such, there is not much documentation on the
    methodology used.  The original code was written mainly by George
    Walton and requires coordinate transformations.  It calculates
    shading using an overlapping polygon approach.

    REFERENCES:
    TARP Manual, NIST Publication.
    Passive Solar Extension of the BLAST Program, CERL/UIUC Publication.

    OTHER NOTES:
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

	    NPhi = 6                           # Number of altitude angle steps for sky integration
	    NTheta = 24                        # Number of azimuth angle steps for sky integration
	    Eps = 1.e-10				       # Small number
	    DPhi = PiOvr2 / NPhi       	       # Altitude step size
	    DTheta = 2.0 * math.pi / NTheta    # Azimuth step size
	    DThetaDPhi = DTheta * DPhi 	       # Product of DTheta and DPhi
	    PhiMin = 0.5 * DPhi        	       # Minimum altitude

	    sin_Phi = []
	    cos_Phi = []
	    sin_Theta = []
	    cos_Theta = []

	    # SUBROUTINE SPECIFICATIONS FOR MODULE SolarShading

	    # Object Data ------------->  Que porra é essa?!
	    TrackTooManyFigures = pd.Series()
        TrackTooManyVertices = pd.Series()
	    TrackBaseSubSurround = pd.Series()

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


class SolarCalculations(SolarShading): # ExternalFunctions will be passed automatically?
	
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

            if (abs(Xdif) <= 1.E-15):
            	Xdif = 0.0
            if (abs(Ydif) <= 1.E-15):
            	Ydif = 0.0
            if (abs(Zdif) <= 1.E-15):
            	Zdif = 0.0

            XVT(N) = base_lcsx.x * Xdif + base_lcsx.y * Ydif + base_lcsx.z * Zdif
            YVT(N) = base_lcsy.x * Xdif + base_lcsy.y * Ydif + base_lcsy.z * Zdif
            ZVT(N) = base_lcsz.x * Xdif + base_lcsz.y * Ydif + base_lcsz.z * Zdif

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
                        if (abs(x - XTEMP(K)) > 2.0): continue
                        if (abs(y - YTEMP(K)) > 2.0): continue
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
        ?typedef pd.DataFrame()::size_type size_type
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
                                    if (abs(x - XTEMP(K)) > 2.0): continue
                                    if (abs(y - YTEMP(K)) > 2.0): continue
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
                                if (abs(x - XTEMP(K)) > 2.0): continue
                                if (abs(y - YTEMP(K)) > 2.0): continue
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
                                        if (abs(x - XTEMP(K)) > 2.0): continue
                                        if (abs(y - YTEMP(K)) > 2.0): continue
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
        SLOPE = pd.Series() # Slopes from left-most vertex to others
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

            if (abs(DELTAX) > 0.5):
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

            if (abs(HCAREA(NS3)) * HCMULT < abs(HCAREA(NS1))):
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

                if (abs(WoShdgIsoSky(SurfNum)) > Eps):
                    DifShdgRatioIsoSkyHRTS(iTimeStep, iHour, SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum))
                else:
                    DifShdgRatioIsoSkyHRTS(iTimeStep, iHour, SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum) + Eps)
                
                if (abs(WoShdgHoriz(SurfNum)) > Eps):
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
        XVT = pd.Series() # X Vertices of Shadows
        YVT = pd.Series() # Y vertices of Shadows
        ZVT = pd.Series() # Z vertices of Shadows
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

                if (abs(ZS) > 1.e-4):
                    XShadowProjection = XS / ZS
                    YShadowProjection = YS / ZS
                    if (abs(XShadowProjection) < 1.e-8): XShadowProjection = 0.0
                    if (abs(YShadowProjection) < 1.e-8): YShadowProjection = 0.0
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
        ?typedef pd.DataFrame()::size_type size_type
        GSSNR = 0             # General shadowing surface number
        MainOverlapStatus = 0 # Overlap status of the main overlap calculation not the check for
        # multiple overlaps (unless there was an error)
        XVT = pd.Series()
        YVT = pd.Series()
        ZVT = pd.Series()
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
                        auto const delX(abs(HCX[l] - HCX_N))
                        if (delX > 6):
                    		continue
                        auto const delY(abs(HCY[l] - HCY_N))
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
        # using DataSystemVariables::DetailedSolarTimestepIntegration
        # using DaylightingManager::CalcDayltgCoefficients
        # using DaylightingManager::TotWindowsWithDayl

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
        ?static pd.Series() const SineSolDeclCoef(9,
                                                     {0.00561800,
                                                      0.0657911,
                                                      -0.392779,
                                                      0.00064440,
                                                      -0.00618495,
                                                      -0.00010101,
                                                      -0.00007951,
                                                      -0.00011691,
                                                      0.00002096}) # Fitted coefficients of Fourier series | SINE OF DECLINATION | COEFFICIENTS
        ?static pd.Series() const EqOfTimeCoef(9,
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

            if (abs(WoShdgIsoSky(SurfNum)) > Eps):
                DifShdgRatioIsoSky(SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum))
            else:
                DifShdgRatioIsoSky(SurfNum) = (WithShdgIsoSky(SurfNum)) / (WoShdgIsoSky(SurfNum) + Eps)
            
            if (abs(WoShdgHoriz(SurfNum)) > Eps):
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

# end of SolarCalculations
