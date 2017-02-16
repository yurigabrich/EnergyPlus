// EnergyPlus, Copyright (c) 1996-2017, The Board of Trustees of the University of Illinois and
// The Regents of the University of California, through Lawrence Berkeley National Laboratory
// (subject to receipt of any required approvals from the U.S. Dept. of Energy). All rights
// reserved.
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
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

// C++ Headers
#include<memory>
#include<vector>

// EnergyPlus Headers
#include <EnergyPlus.hh>
#include <GroundTemperatureModeling/BaseGroundTemperatureModel.hh>
#include <GroundTemperatureModeling/FiniteDifferenceGroundTemperatureModel.hh>
#include <GroundTemperatureModeling/GroundTemperatureModelManager.hh>
#include <GroundTemperatureModeling/KusudaAchenbachGroundTemperatureModel.hh>
#include <GroundTemperatureModeling/SiteBuildingSurfaceGroundTemperatures.hh>
#include <GroundTemperatureModeling/SiteDeepGroundTemperatures.hh>
#include <GroundTemperatureModeling/SiteFCFactorMethodGroundTemperatures.hh>
#include <GroundTemperatureModeling/SiteShallowGroundTemperatures.hh>
#include <GroundTemperatureModeling/XingGroundTemperatureModel.hh>
#include <InputProcessor.hh>

namespace EnergyPlus {

namespace GroundTemperatureManager {

	int const objectType_KusudaGroundTemp( 1 );
	int const objectType_FiniteDiffGroundTemp( 2 );
	int const objectType_SiteBuildingSurfaceGroundTemp( 3 );
	int const objectType_SiteShallowGroundTemp( 4 );
	int const objectType_SiteDeepGroundTemp( 5 );
	int const objectType_SiteFCFactorMethodGroundTemp( 6 );
	int const objectType_XingGroundTemp( 7 );

	Array1D_string const CurrentModuleObjects( 7, { "Site:Groundtemperature:Undisturbed:KusudaAchenbach", "Site:GroundTemperature:Undisturbed:FiniteDifference", "Site:GroundTemperature:BuildingSurface", "Site:GroundTemperature:Shallow", "Site:GroundTemperature:Deep", "Site:GroundTemperature:FCfactorMethod", "Site:GroundTemperature:Undisturbed:Xing"} );

	std::vector < std::shared_ptr < BaseGroundTempsModel > > groundTempModels;

	//******************************************************************************

	std::shared_ptr< BaseGroundTempsModel >
	GetGroundTempModelAndInit(
		std::string const & objectType_str,
		std::string const & objectName
	)
	{
		// SUBROUTINE INFORMATION:
		//       AUTHOR         Matt Mitchell
		//       DATE WRITTEN   Summer 2015
		//       MODIFIED       na
		//       RE-ENGINEERED  na

		// PURPOSE OF THIS SUBROUTINE:
		// Called by objects requireing ground temperature models. Determines type and calls appropriate factory method.

		// USE STATEMENTS:
		using InputProcessor::MakeUPPERCase;

		// Locals
		// SUBROUTINE LOCAL VARIABLE DECLARATIONS:
		int objectType( 0 );

		std::string objectType_str_UPPERCase = MakeUPPERCase( objectType_str );

		// Set object type
		if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_KusudaGroundTemp ) ) ) {
			objectType = objectType_KusudaGroundTemp;
		} else if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_FiniteDiffGroundTemp ) ) ) {
			objectType = objectType_FiniteDiffGroundTemp;
		} else if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_SiteBuildingSurfaceGroundTemp ) ) ) {
			objectType = objectType_SiteBuildingSurfaceGroundTemp;
		} else if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_SiteShallowGroundTemp ) ) ){
			objectType = objectType_SiteShallowGroundTemp;
		} else if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_SiteDeepGroundTemp ) ) ) {
			objectType = objectType_SiteDeepGroundTemp;
		} else if ( objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_SiteFCFactorMethodGroundTemp ) ) ) {
			objectType = objectType_SiteFCFactorMethodGroundTemp;
		} else if (objectType_str_UPPERCase == MakeUPPERCase( CurrentModuleObjects( objectType_XingGroundTemp ) ) ) {
			objectType = objectType_XingGroundTemp;
		} else {
			// Error out if no ground temperature object types recognized
			ShowFatalError( "GetGroundTempsModelAndInit: Ground temperature object " + objectType_str + " not recognized." );
		}

		int numGTMs = groundTempModels.size();

		// Check if this instance of this model has already been retrieved
		for ( int i = 0; i < numGTMs; ++i ) {
			auto currentModel( groundTempModels[i] );
			// Check if the type and name match
			if ( objectType == currentModel->objectType && objectName == currentModel->objectName) {
				return groundTempModels[i];
			}
		}

		// If not found, create new instance of the model
		if ( objectType == objectType_KusudaGroundTemp ) {
			return KusudaGroundTempsModel::KusudaGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_FiniteDiffGroundTemp ) {
			return FiniteDiffGroundTempsModel::FiniteDiffGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_SiteBuildingSurfaceGroundTemp ) {
			return SiteBuildingSurfaceGroundTemps::BuildingSurfaceGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_SiteShallowGroundTemp ) {
			return SiteShallowGroundTemps::ShallowGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_SiteDeepGroundTemp ) {
			return SiteDeepGroundTemps::DeepGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_SiteFCFactorMethodGroundTemp ) {
			return SiteFCFactorMethodGroundTemps::FCFactorGTMFactory( objectType, objectName );
		} else if ( objectType == objectType_XingGroundTemp ) {
			return XingGroundTempsModel::XingGTMFactory( objectType, objectName );
		} else {
			// Error
			return nullptr;
		}
	}

	//******************************************************************************

	void
	clear_state() {
		groundTempModels.clear();
	}

	//******************************************************************************

}	// GroundTemperatureManager

}	// EnergyPlus