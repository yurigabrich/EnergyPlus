> This fork has the intention to convert specific functions to python in order to support the development of a paper on energy policy.

## Copyright

The files presented here have the same copyright attribute as the source file -- the BSD-3-like license.
For more informations [check here](https://github.com/NREL/EnergyPlus#license--contributing-development-).

## Dependecy Tree

File `Shadows.py` (functions and variables dependencies):

`[class] SolarCalculations`
	`[class] SolarShading`
		`__init__`
		    ~~DataPrecisionGlobals.cc~~ (ver as casas decimais usadas na precisão para definir o msm em Python)
		    --> DataGlobals.cc
		    --> DataEnvironment.cc
	        --> DataHeatBalance.cc
	        --> DataSurfaces.cc
	        --> DataBSDFWindow.cc
    	    --> DataVectorTypes.hh (Definição dos vetores. Procurar o equivalente em Python)
    	    --> ? FenestrationCommon
    	    --> ? SingleLayerOptics
    	    EP_Count_Calls --> DataTimings.cc
		`clear_state`

		[class] ExternalFunctions
			`CalcDayltgCoefficients` --> DaylightingManager.cc
				DetailedSolarTimestepIntegration() --> DataSystemVariables.cc
					ZoneDaylight() --> DataDaylighting.cc
				FindTDDPipe --> DaylightingDevices.cc
					Surface() --> DataSurfaces.cc
					TDDPipe() --> DataDaylightingDevices.cc
				TransTDD --> DaylightingDevices.cc
					POLYF() --> General.cc
					Surface() --> DataSurfaces.cc
					Construct() --> DataHeatBalance.cc ? não está definido, só é usado...
					InterpolatePipeTransBeam() --> DaylightingDevices.cc
					TDDPipe() --> DataDaylightingDevices.cc
					CalcTDDTransSolAniso() --> DaylightingDevices.cc
				BlindBeamBeamTrans --> General.cc
					PiOvr2 --> DataGlobals.cc
				RoundSigDigits --> General.cc
					TestChar --> ??? não sei como converter para Python
					stripped() --> computing performance?
				GetDaylightingParametersInput() --> DaylightingManager.cc
				CheckTDDsAndLightShelvesInDaylitZones() --> DaylightingManager.cc
				AssociateWindowShadingControlWithDaylighting() --> DaylightingManager.cc
				CheckTDDZone --> DaylightingManager.cc
				BeginSimFlag --> DataGlobals.cc
				NumOfZones --> DataGlobals.cc
				ZoneDaylight() --> DataDaylighting.cc
				KickOffSizing --> DataGlobals.cc
				KickOffSimulation --> DataGlobals.cc
				WarmupFlag --> DataGlobals.cc
				CalcMinIntWinSolidAngs() --> DaylightingManager.cc --> acho q não será necessário, pois é para janela
				TDDTransVisBeam --> DaylightingManager.cc
				TDDFluxInc --> DaylightingManager.cc
				TDDFluxTrans --> DaylightingManager.cc
				NumOfTDDPipes --> DaylightingDevices.cc
				BeginDayFlag --> DataGlobals.cc
				SUNCOSHR() --> DataSurfaces.cc
				SunIsUpValue --> DataEnvironment.cc
				DayltgExtHorizIllum() --> DaylightingManager.cc
				PHSUNHR() --> DaylightingManager.cc
				SPHSUNHR() --> DaylightingManager.cc
				CPHSUNHR() --> DaylightingManager.cc
				THSUNHR() --> DaylightingManager.cc
				GILSK() --> DaylightingManager.cc
				GILSU() --> DaylightingManager.cc
				CalcDayltgCoeffsRefMapPoints() --> DaylightingManager.cc
				FirstTimeDaylFacCalc --> DaylightingManager.cc
				DFSReportSizingDays --> GetDaylightingParametersInput() --> it's enough?
				DFSReportAllShadowCalculationDays --> GetDaylightingParametersInput() --> an 'else' of the above
				DoingSizing --> DataGlobals.cc
				DoWeathSim --> DataGlobals.cc
				DoDesDaySim --> DataGlobals.cc
				KindOfSim --> DataGlobals.cc
				ksRunPeriodWeather --> DataGlobals.cc
				GetNewUnitNumber() --> ? aparece no html, mas não no arquivo... :(



	
	`__init__`
		`GetShadowingInput`
		        --> UtilityRoutines::SameString() --> como funciona isso?
		        --> UtilityRoutines::FindItemInList() --> como funciona isso?
		    getNumObjectsFound() --> InputProcessor.cc
		    getObjectItem() --> InputProcessor.cc
		    lNumericFieldBlanks --> DataIPShortCuts.cc
            lAlphaFieldBlanks --> DataIPShortCuts.cc
            cAlphaFieldNames --> DataIPShortCuts.cc
            cNumericFieldNames --> DataIPShortCuts.cc
            .SchedExternalShadingFrac --> .? DataSurfaces.hh (bool)
            .ExternalShadingSchInd --> .? DataSurfaces.hh (bool)
            DisableGroupSelfShading --> DataSystemVariables.cc
			ScheduleFileShadingProcessed --> ScheduleManager.cc
			ZoneList --> DataHeatBalance.cc
			NumOfZoneLists --> DataHeatBalance.cc
			ShadingTransmittanceVaries --> DataSurfaces.cc
			SolarDistribution --> DataHeatBalance.cc
			MinimalShadowing --> DataHeatBalance.cc
			Surface() --> DataSurfaces.cc

		`AllocateModuleArrays`
			TotSurfaces --> DataSurfaces.cc
			NumOfTimeStepInHour --> DataGlobals.cc
			MaxBkSurf --> DataBSDFWindow.cc
			NumOfZones --> DataGlobals.cc
			MaxSolidWinLayers --> DataHeatBalance.cc
			MaxVerticesPerSurface --> DataSurfaces.cc
			SurfaceWindow() --> DataSurfaces.cc
			Surface() --> DataSurfaces.cc
			OutputProcessor::Unit --> OutputProcessor.cc

		`DetermineShadowingCombinations`
			IgnoreSolarRadiation --> DataEnvironment.cc
			ExternalEnvironment --> DataSurfaces.cc
			OtherSideCondModeledExt --> DataSurfaces.cc
			EP_Count_Calls --> DataTimings.cc
			CHKGSS()
			    Surface() --> DataSurfaces.cc
	
	`SHDGSS`
		CLIP()
		CTRANS()
		HTRANS0()
		HTRANS1()
		MULTOL()
			**DeterminePolygonOverlap()
		**DeterminePolygonOverlap()

	`PerformSolarCalculations`
		CalcPerSolarBeam()
			EP_Count_Calls --> DataTimings.cc
			FigureSunCosines()
				SUN4()
			FigureSolarBeamAtTimestep()
				*SHADOW()
			InitComplexWindows() --> WindowComplexManager.cc
			UpdateComplexWindows() --> WindowComplexManager.cc
		SkyDifSolarShading()
			*SHADOW()
			OutputProcessor::Unit --> OutputProcessor.cc
		DetailedSolarTimestepIntegration --> DataSystemVariables.cc
		CalcDayltgCoefficients() --> DaylightingManager.cc
		TotWindowsWithDayl() --> DaylightingManager.cc

	*`SHADOW`
		CTRANS()
		HTRANS1()
		SHDGSS()
		EP_Count_Calls --> DataTimings.cc

	**`DeterminePolygonOverlap`
		HTRANS0()
		INCLOS()
		INTCPT()
		CLIPPOLY()
			EP_Count_Calls --> DataTimings.cc
		ORDER()
		EP_Count_Calls --> DataTimings.cc

	SEM NENHUM VÍNCULO:
		`polygon_contains_point`
		`HTRANS`
		`SurfaceScheduledSolarInc`
		`PerformSolarCalculations`
			SUN3()
		`ReportSurfaceShading`
			PreDefTableEntry --> OutputReportPredefined.cc
			Surface() --> DataSurfaces.cc
		`ReportSurfaceErrors`




---


### DataEnvironment.cc
[![img](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/html/DataEnvironment_8cc__incl.png)](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/EnergyPlus/DataEnvironment.cc)

### DataEnvironment.hh
[![img](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/html/DataEnvironment_8hh__incl.png)](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/EnergyPlus/DataEnvironment.hh)

### SolarShading.cc
[![img](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/html/SolarShading_8cc__incl.png)](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/EnergyPlus/SolarShading.cc)

### SolarShading.hh
[![img](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/html/SolarShading_8hh__incl.png)](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/EnergyPlus/SolarShading.hh)

[![img](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/html/SolarShading_8hh__dep__incl.png)](https://github.com/yurigabrich/EnergyPlusShadow/blob/develop/EnergyPlus/SolarShading.hh)

> ref: [Open-source tool to visualize C/C++ header file dependencies?](https://stackoverflow.com/questions/1190597/open-source-tool-to-visualize-c-c-header-file-dependencies)
