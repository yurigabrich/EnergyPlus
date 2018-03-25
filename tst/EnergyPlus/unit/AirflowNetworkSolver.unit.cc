// EnergyPlus, Copyright (c) 1996-2018, The Board of Trustees of the University of Illinois,
// The Regents of the University of California, through Lawrence Berkeley National Laboratory
// (subject to receipt of any required approvals from the U.S. Dept. of Energy), Oak Ridge
// National Laboratory, managed by UT-Battelle, Alliance for Sustainable Energy, LLC, and other
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
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

// EnergyPlus::AirflowNetworkSolver unit tests

// Google test headers
#include <gtest/gtest.h>

// EnergyPlus Headers
#include <AirflowNetworkBalanceManager.hh>
#include <AirflowNetworkSolver.hh>
#include <Psychrometrics.hh>
#include <EnergyPlus/UtilityRoutines.hh>

#include "Fixtures/EnergyPlusFixture.hh"

using namespace EnergyPlus;
using namespace AirflowNetworkBalanceManager;
using namespace DataAirflowNetwork;
using namespace AirflowNetworkSolver;

TEST_F( EnergyPlusFixture, AirflowNetworkSolverTest_HorizontalOpening )
{

	int i = 1;
	int j = 1;
	int n;
	int m;
	int NF;
	std::array< Real64, 2 > F{ { 0.0, 0.0 } };
	std::array< Real64, 2 > DF{ { 0.0, 0.0 } };

	n = 1;
	m = 2;

	AirflowNetworkCompData.allocate( j );
	AirflowNetworkCompData( j ).TypeNum = 1;
	MultizoneSurfaceData.allocate( i );
	MultizoneSurfaceData( i ).Width = 10.0;
	MultizoneSurfaceData( i ).Height = 5.0;
	MultizoneSurfaceData( i ).OpenFactor = 1.0;

	RHOZ.allocate( 2 );
	RHOZ( 1 ) = 1.2;
	RHOZ( 2 ) = 1.18;

	MultizoneCompHorOpeningData.allocate( 1 );
	MultizoneCompHorOpeningData( 1 ).FlowCoef = 0.1;
	MultizoneCompHorOpeningData( 1 ).FlowExpo = 0.5;
	MultizoneCompHorOpeningData( 1 ).Slope = 90.0;
	MultizoneCompHorOpeningData( 1 ).DischCoeff = 0.2;

	AirflowNetworkLinkageData.allocate( i );
	AirflowNetworkLinkageData( i ).nodeHeights[ 0 ] = 4.0;
	AirflowNetworkLinkageData( i ).nodeHeights[ 1 ] = 2.0;

	NF = AFEHOP( 1, 1, 0.05, 1, 1, 2, F, DF );
	EXPECT_NEAR( 3.47863, F[ 0 ], 0.00001 );
	EXPECT_NEAR( 34.7863, DF[ 0 ], 0.0001 );
	EXPECT_NEAR( 2.96657, F[ 1 ], 0.00001 );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AFEHOP( 1, 1, -0.05, 1, 1, 2, F, DF );
	EXPECT_NEAR( -3.42065, F[ 0 ], 0.00001 );
	EXPECT_NEAR( 34.20649, DF[ 0 ], 0.0001 );
	EXPECT_NEAR( 2.96657, F[ 1 ], 0.00001 );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	AirflowNetworkLinkageData.deallocate();
	RHOZ.deallocate();
	MultizoneCompHorOpeningData.deallocate();
	MultizoneSurfaceData.deallocate();
	AirflowNetworkCompData.deallocate();
}

TEST_F( EnergyPlusFixture, AirflowNetworkSolverTest_Crack )
{
	int NF;
	std::array< Real64, 2 > F{ { 0.0, 0.0 } };
	std::array< Real64, 2 > DF{ { 0.0, 0.0 } };


	Real64 tz1 = 20.0;

	AirflowNetworkSolver::NetworkNumOfLinks = 1;

	DataAirflowNetwork::AirflowNetworkCompData.allocate( 1 );
	DataAirflowNetwork::AirflowNetworkCompData( 1 ).TypeNum = 1;
	DataAirflowNetwork::MultizoneSurfaceData.allocate( 1 );
	DataAirflowNetwork::MultizoneSurfaceData( 1 ).Width = 10.0;
	DataAirflowNetwork::MultizoneSurfaceData( 1 ).Height = 5.0;
	DataAirflowNetwork::MultizoneSurfaceData( 1 ).OpenFactor = 1.0;
	DataAirflowNetwork::MultizoneSurfaceData( 1 ).Factor = 1.0;

	AirflowNetworkSolver::RHOZ.allocate( 2 );
	Real64 density = Psychrometrics::PsyRhoAirFnPbTdbW( 101325.0, tz1, 0.0 );
	AirflowNetworkSolver::RHOZ( 1 ) = density;
	AirflowNetworkSolver::RHOZ( 2 ) = density;
	AirflowNetworkSolver::SQRTDZ.allocate( 2 );
	AirflowNetworkSolver::SQRTDZ( 1 ) = sqrt( density );
	AirflowNetworkSolver::SQRTDZ( 2 ) = sqrt( density );
	AirflowNetworkSolver::VISCZ.allocate( 2 );
	Real64 viscosity = AirflowNetworkBalanceManager::airDynamicVisc( tz1 );
	AirflowNetworkSolver::VISCZ( 1 ) = viscosity;
	AirflowNetworkSolver::VISCZ( 2 ) = viscosity;
	AirflowNetworkSolver::TZ.allocate( 2 );
	AirflowNetworkSolver::TZ( 1 ) = tz1;
	AirflowNetworkSolver::TZ( 2 ) = tz1;

	DataAirflowNetwork::MultizoneSurfaceCrackData.allocate( 1 );
	DataAirflowNetwork::MultizoneSurfaceCrackData( 1 ).FlowCoef = 0.0006;
	DataAirflowNetwork::MultizoneSurfaceCrackData( 1 ).FlowExpo = 0.5;
	DataAirflowNetwork::MultizoneSurfaceCrackData( 1 ).StandardP = 101325.0;
	DataAirflowNetwork::MultizoneSurfaceCrackData( 1 ).StandardT = tz1;
	DataAirflowNetwork::MultizoneSurfaceCrackData( 1 ).StandardW = 0.0;

	DataAirflowNetwork::AirflowNetworkLinkageData.allocate( 1 );
	DataAirflowNetwork::AirflowNetworkLinkageData( 1 ).nodeHeights[ 0 ] = 1.0;
	DataAirflowNetwork::AirflowNetworkLinkageData( 1 ).nodeHeights[ 1 ] = 1.0;

	NF = AirflowNetworkSolver::AFESCR( 1, 0, 100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	EXPECT_NEAR( 0.006, F[ 0 ], 1.0e-12 );
	EXPECT_NEAR( 0.00003, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AirflowNetworkSolver::AFESCR( 1, 0, -100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	EXPECT_NEAR( -0.006, F[ 0 ], 1.0e-12 );
	EXPECT_NEAR( 0.00003, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AirflowNetworkSolver::AFESCR( 1, 1, 100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	//EXPECT_NEAR( 0.06*sqrt( density )/viscosity, F[ 0 ], 1.0e-12);
	EXPECT_NEAR( 0.0006*sqrt( density )/viscosity, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AirflowNetworkSolver::AFESCR(1, 1, -100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF);
	//EXPECT_NEAR( 0.06*sqrt( density )/viscosity, F[ 0 ], 1.0e-12);
	EXPECT_NEAR( 0.0006*sqrt( density ) / viscosity, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	Real64 tz2 = 22.0;
	Real64 density2 = Psychrometrics::PsyRhoAirFnPbTdbW( 101325.0, tz2, 0.0 );
	AirflowNetworkSolver::RHOZ( 2 ) = density2;
	AirflowNetworkSolver::SQRTDZ( 2 ) = sqrt(density2);
	Real64 viscosity2 = AirflowNetworkBalanceManager::airDynamicVisc( tz2 );
	AirflowNetworkSolver::VISCZ( 2 ) = viscosity2;
	AirflowNetworkSolver::TZ( 2 ) = tz2;

	//RhoCor = (TZ(n) + DataGlobals::KelvinConv) / (Tave + DataGlobals::KelvinConv);
	//Ctl = std::pow(RhozNorm / RHOZ(n) / RhoCor, expn - 1.0) * std::pow(VisczNorm / VisAve, 2.0 * expn - 1.0);
	Real64 VisczNorm = viscosity;
	Real64 RhozNorm = density;
	Real64 VisAve = 0.5*( viscosity + viscosity2 );
	Real64 Tave = 21.0;
	Real64 Ctl = std::pow( RhozNorm * ( Tave + DataGlobals::KelvinConv ) / ( density * ( tz1 + DataGlobals::KelvinConv ) ), -0.5 )
		* std::pow( VisczNorm / VisAve, 0.0 );

	NF = AirflowNetworkSolver::AFESCR( 1, 0, 100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	EXPECT_NEAR( Ctl*0.006, F[ 0 ], 1.0e-12 );
	EXPECT_NEAR( Ctl*0.00003, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AirflowNetworkSolver::AFESCR( 1, 1, 100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	//EXPECT_NEAR( 0.06*sqrt( density )/viscosity, F[ 0 ], 1.0e-12);
	EXPECT_NEAR( Ctl*0.0006*sqrt( density )/viscosity, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	Ctl = std::pow(RhozNorm * (Tave + DataGlobals::KelvinConv) / (density2 * (tz2 + DataGlobals::KelvinConv)), -0.5)
		* std::pow(VisczNorm / VisAve, 0.0);

	NF = AirflowNetworkSolver::AFESCR( 1, 0, -100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	EXPECT_NEAR( -Ctl*0.006, F[ 0 ], 1.0e-12 );
	EXPECT_NEAR( Ctl*0.00003, DF[ 0 ], 1.0e-12 );
	EXPECT_EQ( 0.0, F[ 1 ] );
	EXPECT_EQ( 0.0, DF[ 1 ] );

	NF = AirflowNetworkSolver::AFESCR( 1, 1, -100.0, 1, 1, 2, F, DF );
	EXPECT_EQ( 1, NF );
	//EXPECT_NEAR( 0.06*sqrt( density )/viscosity, F[ 0 ], 1.0e-12);
	EXPECT_NEAR( Ctl*0.0006*sqrt(density2) / viscosity2, DF[0], 1.0e-12 );
	EXPECT_EQ( 0.0, F[1] );
	EXPECT_EQ( 0.0, DF[1] );

	DataAirflowNetwork::MultizoneSurfaceCrackData.deallocate();
	DataAirflowNetwork::AirflowNetworkLinkageData.deallocate();
	AirflowNetworkSolver::RHOZ.deallocate();
	DataAirflowNetwork::MultizoneCompHorOpeningData.deallocate();
	DataAirflowNetwork::MultizoneSurfaceData.deallocate();
	DataAirflowNetwork::AirflowNetworkCompData.deallocate();
}
