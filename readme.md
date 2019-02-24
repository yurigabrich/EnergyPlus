```
Copyright (C) 2018 - 2019
Yuri Bastos Gabrich <yuribgabrich[at]gmail.com>

This fork has the intention to convert specific functions to Python in order to support the development of a paper on energy policy.
```

## License

SPDX-License-Identifier: [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html)

The files presented here follow the same license attribute as its source file.
For more informations about the original code license and copyright [check here](https://github.com/NREL/EnergyPlus#license--contributing-development-).

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
			CalcDayltgCoefficients() * local de definição
				DetailedSolarTimestepIntegration
					ZoneDaylight()
						? ZoneDaylight --> definido como Pandas Series (l.882)
				FindTDDPipe(WinNum)
					NumOfTDDPipes
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
						NumOfAngles --> ? não sei de onde vêm
						COSAngle --> ? não sei de onde vêm
						FindArrayIndex --> ? FluidProperties
					TDDPipe()
						? TDDPipe --> definido como Pandas Series (l.1060)
					CalcTDDTransSolAniso(PipeNum, COSI)
						HourOfDay
        				TimeStep
        				SolarBeam
        				AnisoSkyMult()
        					? AnisoSkyMult --> definido como Pandas Series (l.363)
				        curDifShdgRatioIsoSky()
				        	? curDifShdgRatioIsoSky --> definido como Pandas Series (l.366)
				        DifShdgRatioHoriz()
				        	? DifShdgRatioHoriz --> definido como Pandas Series (l.367)
				        DifShdgRatioHorizHRTS()
				        	? DifShdgRatioHorizHRTS --> definido como Pandas DataFrame (l.368)
				        DifShdgRatioIsoSky()
				        	? DifShdgRatioIsoSky --> definido como Pandas Series (l.369)
				        MultCircumSolar()
				        	? MultCircumSolar --> definido como Pandas Series (l.370)
				        MultHorizonZenith()
				        	? MultHorizonZenith --> definido como Pandas Series (l.371)
				        MultIsoSky()
				        	? MultIsoSky --> definido como Pandas Series (l.372)
				        SunlitFrac()
				        	? SunlitFrac --> definido como Pandas DataFrame (l.373)
				        DetailedSkyDiffuseAlgorithm
				        ShadingTransmittanceVaries --> definido em __init__ de SolarShading, mudar para External...
				        SolarDistribution --> definido em __init__ de SolarShading, mudar para External...
				        MinimalShadowing --> definido em __init__ de SolarShading, mudar para External...
				        TDDPipe()
				        	? TDDPipe --> definido como Pandas Series (l.1060)
				        TransTDD(PipeNum, COSI, RadiationType) --> recursivo ou loop infinito?
				RoundSigDigits(RealValue, SigDigits)
					TestChar --> ??? não sei como converter para Python
					stripped() --> computing performance?
				GetDaylightingParametersInput()				
				CheckTDDsAndLightShelvesInDaylitZones()
					NumOfTDDPipes
					CheckTDDZone
					TDDPipe()
						? TDDPipe --> definido como Pandas Series (l.1060)
					RoundSigDigits(RealValue, SigDigits)
						TestChar --> ??? não sei como converter para Python
						stripped() --> computing performance?
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
				TotWindowsWithDayl
				CalcDayltgCoeffsRefMapPoints(ZoneNum)
					TDDPipe()
						? TDDPipe --> definido como Pandas Series (l.1060)
					RoundSigDigits(RealValue, SigDigits)
						TestChar --> ??? não sei como converter para Python
						stripped() --> computing performance?
				FirstTimeDaylFacCalc
				? DFSReportSizingDays --> GetDaylightingParametersInput() --> it's enough?
				? DFSReportAllShadowCalculationDays --> GetDaylightingParametersInput() --> an 'else' of the above
				DoingSizing
				DoWeathSim
				DoDesDaySim
				KindOfSim
				ksRunPeriodWeather
				GetNewUnitNumber() --> ? aparece no html, mas não no arquivo... :(			
	__init__()
		outputShdFileName
		[ifdef?] EP_Count_Calls
		PiOvr2
		DetermineShadowingCombinations()
			ShadowComb
			[struct] ShadowingCombinations
			IgnoreSolarRadiation
			ExternalEnvironment
			OtherSideCondModeledExt
			[ifdef?] EP_Count_Calls --> DataTimings.cc --> já definido em External
			CHKGSS(NRS, NSS, ZMIN, &CannotShade)
			    Surface()
			    	? Surface --> definido como Pandas Series (l.679)
		AllocateModuleArrays()
			TotSurfaces
			NumOfTimeStepInHour
			MaxBkSurf
			NumOfZones
			MaxSolidWinLayers
			MaxVerticesPerSurface
			SurfaceWindow() --> DataSurfaces.cc --> é do tipo SurfaceWindowCalc() com várias características de absorsação de luz pela janela
				? SurfaceWindow --> definido como Pandas Series (l.680)
			Surface() --> DataSurfaces.cc
				? Surface --> definido como Pandas Series (l.679)
			[class] Unit --> OutputProcessor::Unit
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
			RoundSigDigits(RealValue, SigDigits)
				TestChar --> ??? não sei como converter para Python
				stripped() --> computing performance?
	SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)
		CLIP(NVT, &XVT, &YVT, &ZVT)
		CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)
		HTRANS0(NS, NumVertices)
		HTRANS1(NS, NumVertices)
		MULTOL(NNN, LOC0, NRFIGS)
			DeterminePolygonOverlap(NS1, NS2, NS3) * uso
		DeterminePolygonOverlap(NS1, NS2, NS3) * uso
	PerformSolarCalculations()
		TotWindowsWithDayl
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
		CalcDayltgCoefficients() * local de uso
			PiOvr2
		SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime)
	DeterminePolygonOverlap(NS1, NS2, NS3) * definição
		HTRANS0(NS, NumVertices)
		INCLOS(N1, N1NumVert, N2, N2NumVert, &NumVerticesOverlap, &NIN)
		INTCPT(NV1, NV2, &NV3, NS1, NS2)
		CLIPPOLY(NS1, NS2, NV1, NV2, &NV3)
			[ifdef?] EP_Count_Calls
		ORDER(NV3, NS3)
		[ifdef?] EP_Count_Calls
		RoundSigDigits(RealValue, SigDigits)
			TestChar --> ??? não sei como converter para Python
			stripped() --> computing performance?
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

[img-dependency](https://realtimeboard.com/app/board/o9J_k06IFRE=/?moveToWidget=3074457346456838114)

> ref: [Open-source tool to visualize C/C++ header file dependencies?](https://stackoverflow.com/questions/1190597/open-source-tool-to-visualize-c-c-header-file-dependencies)
