> This fork has the intention to convert specific functions to python in order to support the development of a paper on energy policy.

## Copyright

The files presented here have the same copyright attribute as the source file -- the BSD-3-like license.
For more informations [check here](https://github.com/NREL/EnergyPlus#license--contributing-development-).

## Dependecy Tree

File `Shadows.py` (functions and variables dependencies):

[class] SolarCalculations()
	[class] SolarShading)()
		__init__()
    	    ? FenestrationCommon
    	    ? SingleLayerOptics
		clear_state()
		[class] ExternalFunctions()
		    SurfaceData --> usado por `.SchedExternalShadingFrac` e `.ExternalShadingSchInd`
		    	Vertices
		    		Vertex --> falta definir, mas já está no arquivo
		    	Plane
		    		plane --> falta definir, mas já está no arquivo
			CalcDayltgCoefficients()
				DetailedSolarTimestepIntegration
					ZoneDaylight()
						? ZoneDaylight --> definido como Pandas Series (l.882)
				FindTDDPipe(WinNum)
					Surface()
						? Surface --> definido como Pandas Series (l.679)
					TDDPipe()
						? TDDPipe --> definido como Pandas Series (l.1060)
				TransTDD(PipeNum, COSI, RadiationType)
					POLYF(X, A)
					Surface()
						? Surface --> definido como Pandas Series (l.679)
					Construct()
						ConstructionData
					InterpolatePipeTransBeam(COSI, transBeam)
						FindArrayIndex --> ? FluidProperties
					TDDPipe()
						? TDDPipe --> definido como Pandas Series (l.1060)
					CalcTDDTransSolAniso(PipeNum, COSI)
						HourOfDay --> ? DataGlobals --> não foi definido ainda
        				TimeStep --> ? DataGlobals --> não foi definido ainda
        				AnisoSkyMult --> ? DataHeatBalance
				        curDifShdgRatioIsoSky --> ? DataHeatBalance
				        DifShdgRatioHoriz --> ? DataHeatBalance
				        DifShdgRatioHorizHRTS --> ? DataHeatBalance
				        DifShdgRatioIsoSky --> ? DataHeatBalance
				        MultCircumSolar --> ? DataHeatBalance
				        MultHorizonZenith --> ? DataHeatBalance
				        MultIsoSky --> ? DataHeatBalance
				        SunlitFrac --> ? DataHeatBalance
				        DetailedSkyDiffuseAlgorithm --> ? DataSystemVariables
				RoundSigDigits(RealValue, SigDigits)
					TestChar --> ??? não sei como converter para Python
					stripped() --> computing performance?
				GetDaylightingParametersInput()				
				CheckTDDsAndLightShelvesInDaylitZones()
				AssociateWindowShadingControlWithDaylighting()
				CheckTDDZone
				BeginSimFlag
				NumOfZones
				ZoneDaylight()
				KickOffSizing
				KickOffSimulation
				WarmupFlag
				CalcMinIntWinSolidAngs() --> DaylightingManager.cc --> acho q não será necessário, pois é para janela
				TDDTransVisBeam
				TDDFluxInc
				TDDFluxTrans
				NumOfTDDPipes
				BeginDayFlag
				SUNCOSHR()
				SunIsUpValue
				DayltgExtHorizIllum(HISK, &HISU)
					PiOvr2
				PHSUNHR()
				SPHSUNHR()
				CPHSUNHR()
				THSUNHR()
				GILSK()
				GILSU()
				CalcDayltgCoeffsRefMapPoints(ZoneNum)
				FirstTimeDaylFacCalc
				? DFSReportSizingDays --> GetDaylightingParametersInput() --> it's enough?
				? DFSReportAllShadowCalculationDays --> GetDaylightingParametersInput() --> an 'else' of the above
				DoingSizing
				DoWeathSim
				? DoDesDaySim --> onde foi definido?
				KindOfSim
				ksRunPeriodWeather
				GetNewUnitNumber() --> ? aparece no html, mas não no arquivo... :(			
	__init__()
		outputShdFileName
		[ifdef?] EP_Count_Calls
		PiOvr2		
	GetShadowingInput()
		GetScheduleIndex(&ScheduleName)
        ? UtilityRoutines::SameString() --> como funciona isso?
        ? UtilityRoutines::FindItemInList() --> como funciona isso?
	    getNumObjectsFound(&ObjectWord)
	    getObjectItem(&Object, Number, Alphas, &NumAlphas, Numbers, &NumNumbers, &Status, \*args)
	    lNumericFieldBlanks
        lAlphaFieldBlanks
        cAlphaFieldNames
        cNumericFieldNames
        DisableGroupSelfShading
		ScheduleFileShadingProcessed --> definido dentro de GetShadowingInput(), mudar para External...
		ZoneList
		NumOfZoneLists
		ShadingTransmittanceVaries --> definido em __init__ de SolarShading, mudar para External...
		SolarDistribution --> definido em __init__ de SolarShading, mudar para External...
		MinimalShadowing --> definido em __init__ de SolarShading, mudar para External...
		Surface()
			? Surface --> definido como Pandas Series (l.679)			
	AllocateModuleArrays()
		TotSurfaces --> definido em __init__ de SolarShading, mudar para External...
		NumOfTimeStepInHour
		MaxBkSurf
		NumOfZones
		MaxSolidWinLayers
		MaxVerticesPerSurface
		SurfaceWindow() --> DataSurfaces.cc
			? SurfaceWindow --> definido como Pandas Series (l.680)
		Surface() --> DataSurfaces.cc
			? Surface --> definido como Pandas Series (l.679)
		[class] Unit --> OutputProcessor::Unit		
	DetermineShadowingCombinations()
		ShadowComb
		[struct] ShadowingCombinations
		IgnoreSolarRadiation --> definido em __init__ de SolarShading, mudar para External...
		ExternalEnvironment --> definido em __init__ de SolarShading, mudar para External...
		OtherSideCondModeledExt --> definido em __init__ de SolarShading, mudar para External...
		[ifdef?] EP_Count_Calls --> DataTimings.cc --> já definido em External
		CHKGSS(NRS, NSS, ZMIN, &CannotShade)
		    Surface()
		    	? Surface --> definido como Pandas Series (l.679)
	SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)
		CLIP(NVT, &XVT, &YVT, &ZVT)
		CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)
		HTRANS0(NS, NumVertices)
		HTRANS1(NS, NumVertices)
		MULTOL(NNN, LOC0, NRFIGS)
			DeterminePolygonOverlap(NS1, NS2, NS3)
		DeterminePolygonOverlap(NS1, NS2, NS3)	
	PerformSolarCalculations()
		CalcPerSolarBeam(AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)
			[ifdef?] EP_Count_Calls
			FigureSunCosines(iHour, iTimeStep, EqOfTime, SinSolarDeclin, CosSolarDeclin)
				SUN4(CurrentTime, EqOfTime, SinSolarDeclin, CosSolarDeclin)
			FigureSolarBeamAtTimestep(iHour, iTimeStep)
				SHADOW(iHour, TS)
					CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)
					HTRANS1(NS, NumVertices)
					SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)
					[ifdef?] EP_Count_Calls
			InitComplexWindows()
			UpdateComplexWindows()
		SkyDifSolarShading()
			SHADOW(iHour, TS)
				CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)
				HTRANS1(NS, NumVertices)
				SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)
				[ifdef?] EP_Count_Calls
			[class] Unit --> OutputProcessor::Unit
		DetailedSolarTimestepIntegration
		CalcDayltgCoefficients()
			PiOvr2
		TotWindowsWithDayl
		SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime)
	DeterminePolygonOverlap(NS1, NS2, NS3)
		HTRANS0(NS, NumVertices)
		INCLOS(N1, N1NumVert, N2, N2NumVert, &NumVerticesOverlap, &NIN)
		INTCPT(NV1, NV2, &NV3, NS1, NS2)
		CLIPPOLY(NS1, NS2, NV1, NV2, &NV3)
			[ifdef?] EP_Count_Calls
		ORDER(NV3, NS3)
		[ifdef?] EP_Count_Calls
	SEM NENHUM VÍNCULO (pode ser excluído?):
		`polygon_contains_point` --> used for subsurfaces purposes (`CHKSBS`)
		`HTRANS` --> used for subsurfaces purposes (`CalcInteriorWinTransDifSolInitialDistribution` e `CalcComplexWindowOverlap`)
		`SurfaceScheduledSolarInc` --> used for subsurfaces purposes (`CalcInteriorSolarDistribution`)
			SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime)
		`ReportSurfaceShading` --> called by no one
			PreDefTableEntry --> OutputReportPredefined.cc
			Surface() --> DataSurfaces.cc
		`ReportSurfaceErrors` --> called by no one
		[struct] ZoneListData --> DataHeatBalance.hh ('ExternalFunctions')
		[struct] ZoneDaylightCalc --> DataDaylighting.hh ('ExternalFunctions')
		PreDefTableEntry(columnIndex, &objName, tableEntryInt) --> OutputReportPredefined.cc ('ExternalFunctions')


---

[![img](https://realtimeboard.com/app/board/o9J_k06IFRE=/?moveToWidget=3074457346456838114)

> ref: [Open-source tool to visualize C/C++ header file dependencies?](https://stackoverflow.com/questions/1190597/open-source-tool-to-visualize-c-c-header-file-dependencies)
