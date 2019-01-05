> This fork has the intention to convert specific functions to python in order to support the development of a paper on energy policy.

## Copyright

The files presented here have the same copyright attribute as the source file -- the BSD-3-like license.
For more informations [check here](https://github.com/NREL/EnergyPlus#license--contributing-development-).

## Dependecy Tree

File `Shadows.py` (functions and variables dependencies):

`[class] SolarCalculations`
	`[class] SolarShading`
		`__init__` --> comparar com 'EnergyPlus Headers'
		    ~~DataPrecisionGlobals.cc~~ (ver as casas decimais usadas na precisão para definir o msm em Python)  
		    --> DataGlobals.cc
		    --> DataEnvironment.cc
	        --> DataHeatBalance.cc
	        --> DataSurfaces.cc		
	        ~~DataShadowingCombinations.cc~~
	        ~~DaylightingManager.cc~~
	        ~~SolarReflectionManager.cc~~
	        ~~DataReportingFlags.cc~~
	        ~~DataBSDFWindow.cc~~
		
    	    --> DataVectorTypes.hh (Definição dos vetores. Procurar o equivalente em Python)
    	    ~~DataTimings.cc~~
    	    ~~WindowManager.cc~~
    	    --> ? FenestrationCommon
    	    --> ? SingleLayerOptics
		`clear_state`
	
	`__init__`
		`GetShadowingInput`
		        --> DataIPShortCuts.cc
		        --> DataSystemVariables.cc
		        --> ScheduleManager.cc
			ZoneList --> UtilityRoutines.cc
			NumOfZoneLists --> UtilityRoutines.cc
			ShadingTransmittanceVaries --> DataSurfaces.cc
			SolarDistribution --> DataHeatBalance.cc
			MinimalShadowing --> DataHeatBalance.cc
			? Surface()

		`AllocateModuleArrays`
			TotSurfaces --> DataSurfaces.cc
			NumOfTimeStepInHour --> DataGlobals.cc
			MaxBkSurf --> using DataBSDFWindow::MaxBkSurf --> DataBSDFWindow.cc
			NumOfZones --> DataGlobals.cc
			MaxSolidWinLayers --> DataHeatBalance.cc
			MaxVerticesPerSurface --> DataSurfaces.cc
			? SurfaceWindow()
			? Surface()

		`DetermineShadowingCombinations`
			IgnoreSolarRadiation --> DataEnvironment.cc
			ExternalEnvironment --> DataSurfaces.cc
			OtherSideCondModeledExt --> DataSurfaces.cc
			CHKGSS()
			    ? Surface()
	
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
			FigureSunCosines()
				SUN4()
			FigureSolarBeamAtTimestep()
				*SHADOW()
		SkyDifSolarShading()
			*SHADOW()

	*`SHADOW`
		CTRANS()
		HTRANS1()
		SHDGSS()

	**`DeterminePolygonOverlap`
		HTRANS0()
		INCLOS()
		INTCPT()
		CLIPPOLY()
		ORDER()

	SEM NENHUM VÍNCULO:
		`polygon_contains_point`
		`HTRANS`
		`SurfaceScheduledSolarInc`
		`PerformSolarCalculations`
			SUN3()
		`ReportSurfaceShading`
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
