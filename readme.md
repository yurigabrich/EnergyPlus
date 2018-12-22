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
			`AllocateModuleArrays()` [ok] --> organiza os dados que serão utilizados (acho q posso usar pandas) E retirar o conteúdo relacionado a subsurfaces.
			`CHKBKS(NBS, NRS)` --> check back surfaces: analisa a ordem entre os pontos da parte frontal e posterior de uma determinada superfície (Only base heat transfer surfaces are checked) --> shaming on me?!
			`CHKGSS(NRS, NSS, ZMIN, &CannotShade)` --> determina as combinações possíveis de sombreamento
			`polygon_contains_point(nsides, polygon_3d, &point_3d, ignorex, ignorey, ignorez)` --> Determine if a point is inside a simple 2d polygon. --> tem uma função em geopandas para isso
			`ComputeIntSolarAbsorpFactors()` [ok] --> shaming on me?!
			`CLIP(NVT, &XVT, &YVT, &ZVT)` --> evita sombras falsas
			`CTRANS(NS, NGRS, &NVT, &XVT, &YVT, &ZVT)` --> converte as coordenadas da superfície em outro plano (pertence a 'CalcCoordinateTransformation'?)
			`HTRANS(I, NS, NumVertices)` --> converts cartesian to homogeneous coordinates --> acho q tem uma função para isso em geopandas
			`HTRANS0(NS, NumVertices)` --> ''
			`HTRANS1(NS, NumVertices)` --> ''
			`INCLOS(N1, N1NumVert, N2, N2NumVert, &NumVerticesOverlap, &NIN)` --> determina os vértices da figura N1 que estão dentro da figura N2 (geopandas faz isso, não sei se retorna a mesma coisa)
			`INTCPT(NV1, NV2, &NV3, NS1, NS2)` --> determina as intercepções das bordas das figuras N1 e N2 (geopandas faz isso, não sei se retorna a mesma coisa)
			`CLIPPOLY(NS1, NS2, NV1, NV2, &NV3)` --> Populate global arrays XTEMP and YTEMP with overlap status
			`MULTOL(NNN, LOC0, NRFIGS)` --> determines the overlaps of figure 'NS2' with previous figures (geopandas faz isso, não sei se retorna a mesma coisa) --> chama a função `DeterminePolygonOverlap`
			`ORDER(NV3, NS3)` --> organize overlap polygons to be used in computing subsequent overlaps
			`DeterminePolygonOverlap(NS1, NS2, NS3)` --> Computes the possible overlap of two polygons. Results are stored in the homogeneous coordinate (HC) arrays. (geopandas faz isso, não sei se retorna a mesma coisa)
			`CalcPerSolarBeam(AvgEqOfTime, AvgSinSolarDeclin, AvgCosSolarDeclin)` --> manages computation of solar gain multipliers for beam radiation for a period of days depending on the input "Shadowing Calculations"
			`FigureSunCosines(iHour, iTimeStep, EqOfTime, SinSolarDeclin, CosSolarDeclin)` --> Determine solar position.
			`FigureSolarBeamAtTimestep(iHour, iTimeStep)` --> computes solar gain multipliers for beam solar
			*`DetermineShadowingCombinations()` [ok] --> list of heat transfer surfaces and their possible shadowers which is used to direct the hourly calculation of shadows and sunlit areas
			`SHADOW(iHour, TS)` --> driving routine for calculations of shadows and sunlit areas used in computing the solar beam flux multipliers
			`SHDGSS(NGRS, iHour, TS, CurSurf, NGSS, HTS)` --> determines the shadows on a general receiving surface
			`SurfaceScheduledSolarInc(SurfNum, ConstNum)` --> Returns scheduled surface gain pointer for given surface-construction combination
			`PerformSolarCalculations()` --> determines if new solar/shading calculations need to be performed and calls the proper routines to do the job
			`SUN3(JulianDayOfYear, &SineOfSolarDeclination, &EquationOfTime)` --> computes the coefficients for determining the solar position
			`SUN4(CurrentTime, EqOfTime, SinSolarDeclin, CosSolarDeclin)` --> computes solar direction cosines for a given hour used in the shadowing calculations
			*`SkyDifSolarShading()` --> Calculates factors that account for shading of sky diffuse solar radiation by shadowing surfaces such as overhangs and detached shades (acho q é só para transferência de calor)
			`ReportSurfaceShading()` --> uses the internal variables used in the Shading calculations and prepares them for reporting (at timestep level)
			`ReportSurfaceErrors()` --> reports some recurring type errors that can get mixed up with more important errors in the error file



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
