#ifndef OutputReportTabularAnnual_hh_INCLUDED
#define OutputReportTabularAnnual_hh_INCLUDED

// C++ Headers
#include <string>
#include <vector>

// ObjexxFCL Headers
#include <ObjexxFCL/Array1D.hh>
#include <ObjexxFCL/Array1S.hh>
#include <ObjexxFCL/Array2D.hh>
#include <ObjexxFCL/Array2S.hh>
#include <ObjexxFCL/Array3D.hh>
#include <ObjexxFCL/Optional.hh>

// EnergyPlus Headers
#include <EnergyPlus.hh>
#include <OutputReportData.hh>
#include <ScheduleManager.hh>


namespace EnergyPlus {

namespace OutputReportTabularAnnual {

	// these functions are not in the class and act as an interface between procedural code and object oriented

	void
	GetInputTabularAnnual(); 

	void
	GatherAnnualResultsForTimeStep( int kindOfTypeStep );

	void
	GatherAnnualOneTimeEntries();

	void
	WriteAnnualTables();

	AnnualFieldSet::AggregationKind
	stringToAggKind( std::string inString );



class AnnualTable
{
public:

	// Default Constructor
	AnnualTable() :
		m_name(""),
		m_reportGroupName(""),
		m_filter( "" ),
		m_scheduleName( "" ),
		m_scheduleNum(0)
	{};

	// Member Constructor
	AnnualTable(
		std::string name,
		std::string reportGroupName,
		std::string filter,
		std::string scheduleName ) 
	{
		m_name = name;
		m_reportGroupName = reportGroupName;
		m_filter = filter;
		m_scheduleName = scheduleName;
		if ( !m_scheduleName.empty() ){
			m_scheduleNum = ScheduleManager::GetScheduleIndex( m_scheduleName ); //index to the period schedule
		} else {
			m_scheduleNum = 0;
		}
	};

	void
	addFieldSet( std::string, AnnualFieldSet::AggregationKind, int );

	void
	addFieldSet( std::string, std::string, AnnualFieldSet::AggregationKind, int );

	void
	setupGathering();

	void
	gatherForTimestep( int kindOfTypeStep );

	void
	gatherOneTimeEntries();

	void
	writeTable( int unitsStyle );

	void
	clear_state(); // for unit tests


private:
	// Members

	std::string m_name; // identifier
	std::string m_reportGroupName;
	std::string m_filter;
	std::string m_scheduleName;
	int m_scheduleNum;
	std::vector < std::string > m_objectNames; //for each row of annual table
	std::vector < AnnualFieldSet > m_annualFields; // for each column

	Real64
	getElapsedTime( int );

	Real64 
	getSecondsInTimeStep( int );

	void
	computeBinColumns();

	std::vector < std::string >
	setupAggString();

	Real64
	setEnergyUnitStringAndFactor( int const unitsStyle, std::string & unitString );

	int
	columnCountForAggregation( AnnualFieldSet::AggregationKind curAgg );
	
	std::string
	trim( const std::string& str );

	void
	AnnualTable::fixUnitsPerSecond( std::string & unitString, Real64 & conversionFactor );


}; // class AnnualTable

}; // namespace OutputReportTabularAnnual

} // EnergyPlus


//     NOTICE

//     Copyright (c) 1996-2015 The Board of Trustees of the University of Illinois
//     and The Regents of the University of
//     Berkeley National Laboratory.  All rights reserved.

//     Portions of the EnergyPlus software package have been developed and copyrighted
//     by other individuals, companies and institutions.  These portions have been
//     incorporated into the EnergyPlus software package under license.   For a complete
//     list of contributors, see "Notice" located in main.cc.

//     NOTICE: The U.S. Government is granted for itself and others acting on its
//     behalf a paid-up, nonexclusive, irrevocable, worldwide license in this data to
//     reproduce, prepare derivative works, and perform publicly and display publicly.
//     Beginning five (5) years after permission to assert copyright is granted,
//     subject to two possible five year renewals, the U.S. Government is granted for
//     itself and others acting on its behalf a paid-up, non-exclusive, irrevocable
//     worldwide license in this data to reproduce, prepare derivative works,
//     distribute copies to the public, perform publicly and display publicly, and to
//     permit others to do so.

//     TRADEMARKS: EnergyPlus is a trademark of the US Department of Energy.



#endif
