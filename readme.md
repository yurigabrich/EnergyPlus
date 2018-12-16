> This fork has the intention to convert specific functions to python in order to support the development of a paper on energy policy.

## Copyright

The files presented here have the same copyright attribute as the source file -- the BSD-3-like license.
For more informations [check here](https://github.com/NREL/EnergyPlus#license--contributing-development-).

## Dependecy Tree

`EnergyPlus()`
	`SolarShading()`
		- dependecy packages
		- `clear_state()`
		- `InitSolarCalculations()` --> acho melhor usar como uma classe
			__main__ --> define arquivo de escrita,
						 aloca espaço na memória e
						 chama as funções internas:
						 	`GetShadowingInput()`
						 	`AllocateModuleArrays()`
						 	`ComputeIntSolarAbsorpFactors()`
						 	`DetermineShadowingCombinations()`
						 	`InitSolReflRecSurf()` --> external func
			`GetShadowingInput()` [ok] --> calcula as sombras e
										   usa os seguintes pacotes:
										   General::RoundSigDigits
									       namespace DataIPShortCuts
									       DataSystemVariables::DetailedSkyDiffuseAlgorithm
									       DataSystemVariables::DetailedSolarTimestepIntegration
									       DataSystemVariables::DisableAllSelfShading
									       DataSystemVariables::DisableGroupSelfShading
									       DataSystemVariables::ReportExtShadingSunlitFrac
									       DataSystemVariables::SutherlandHodgman
									       DataSystemVariables::UseImportedSunlitFrac
									       DataSystemVariables::UseScheduledSunlitFrac
									       ScheduleManager::ScheduleFileShadingProcessed
			`AllocateModuleArrays()` [ok] --> organiza os dados que serão utilizados (acho q posso usar pandas)
			`AnisoSkyViewFactors()`
			`CHKBKS(NBS, NRS)`
			`CHKGSS(NRS, NSS, ZMIN, &CannotShade)`
			`polygon_contains_point(nsides, polygon_3d, &point_3d, ignorex, ignorey, ignorez)`
			`ComputeIntSolarAbsorpFactors()` [ok]
			`CLIP(NVT, &XVT, &YVT, &ZVT)`
			`CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)`
			`HTRANS(I, NS, NumVertices)`
			`HTRANS0(NS, NumVertices)`
			`HTRANS1(NS, NumVertices)`
			`INCLOS(N1, N1NumVert, N2, N2NumVert, &NumVerticesOverlap, &NIN)`
			`INTCPT(NV1, NV2, &NV3, NS1, NS2)`
			`CLIPPOLY(NS1, NS2, NV1, NV2, &NV3)`
			`MULTOL(NNN, LOC0, NRFIGS)`
			`ORDER(NV3, NS3)`
			`DeterminePolygonOverlap(NS1, NS2, NS3)`
			`CalcPerSolarBeam(AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)`
			`FigureSunCosines(iHour, iTimeStep, EqOfTime, SinSolarDeclin, CosSolarDeclin)`
			`FigureSolarBeamAtTimestep(iHour, iTimeStep)`
			*`DetermineShadowingCombinations()` [ok]
			`SHADOW(iHour, TS)`
			`SHDBKS(NGRS, CurSurf, NBKS, HTS)`
			`SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)`
			*`CalcInteriorSolarOverlaps(iHour, NBKS, HTSS, GRSNR, TS)`
			`SurfaceScheduledSolarInc(SurfNum, ConstNum)`
			`PerformSolarCalculations()`
			`SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime)`
			`SUN4(CurrentTime, EqOfTime, SinSolarDeclin, CosSolarDeclin)`
			*`WindowShadingManager()`
			*`SkyDifSolarShading()`
			`ReportSurfaceShading()`
			`ReportSurfaceErrors()`



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
