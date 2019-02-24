'''
SPDX-License-Identifier: MIT License
For more information check at: https://spdx.org/licenses/MIT.html

Copyright (C) 2018 - 2019
Yuri Bastos Gabrich <yuribgabrich[at]gmail.com>
'''

# C++ Headers
include <cmath>

# EnergyPlus Headers
include <DataEnvironment.hh>
include <DataGlobals.hh>
include <DataPrecisionGlobals.hh>
include <General.hh>
include <UtilityRoutines.hh>

def EnergyPlus():

    def DataEnvironment():
        '''
        MODULE INFORMATION:
              AUTHOR         Rick Strand, Dan Fisher, Linda Lawrie
              DATE WRITTEN   December 1997
              MODIFIED       November 1998, Fred Winkelmann
              MODIFIED       June 1999,June 2000, Linda Lawrie
              RE-ENGINEERED  na

        PURPOSE OF THIS MODULE:
        This data-only module is a repository for the variables that relate specifically
        to the "environment" (i.e. current date data, tomorrow's date data, and
        current weather variables)

        METHODOLOGY EMPLOYED:
        na

        REFERENCES:
        na

        OTHER NOTES:
        na
        '''
        # Using/Aliasing
        using namespace DataPrecisionGlobals;
        using DataGlobals::KelvinConv;

        # Data
        # -only module should be available to other modules and routines.
        # Thus, all variables in this module must be PUBLIC.

        # MODULE PARAMETER DEFINITIONS:
        EarthRadius = 6356000.0              # Radius of the Earth (m)
        AtmosphericTempGradient = 0.0065     # Standard atmospheric air temperature gradient (K/m)
        SunIsUpValue = 0.00001               # if Cos Zenith Angle of the sun is >= this value, the sun is "up"
        StdPressureSeaLevel = 101325.0       # Standard barometric pressure at sea level (Pa)

        # DERIVED TYPE DEFINITIONS:
        # na

        # INTERFACE BLOCK SPECIFICATIONS:
        # na

        # MODULE VARIABLE DECLARATIONS:
        BeamSolarRad = 0.0                       # Current beam normal solar irradiance
        EMSBeamSolarRadOverrideOn = False     # EMS flag for beam normal solar irradiance
        EMSBeamSolarRadOverrideValue = 0.0       # EMS override value for beam normal solar irradiance
        DayOfMonth = 0                            # Current day of the month
        DayOfMonthTomorrow = 0                    # Tomorrow's day of the month
        DayOfWeek = 0                             # Current day of the week (Sunday=1, Monday=2, ...)
        DayOfWeekTomorrow = 0                     # Tomorrow's day of the week (Sunday=1, Monday=2, ...)
        DayOfYear = 0                             # Current day of the year (01JAN=1, 02JAN=2, ...)
        DayOfYear_Schedule = 0                    # Schedule manager always assumes leap years...
        DifSolarRad = 0.0                        # Current sky diffuse solar horizontal irradiance
        EMSDifSolarRadOverrideOn = False      # EMS flag for sky diffuse solar horizontal irradiance
        EMSDifSolarRadOverrideValue = 0.0        # EMS override value for sky diffuse solar horizontal irradiance
        DSTIndicator;                          # Daylight Saving Time Indicator (1=yes, 0=no) for Today
        Elevation = 0.0                          # Elevation of this building site
        EndMonthFlag = 0.0                         # Set to true on last day of month
        EndYearFlag = 0.0                          # Set to true on the last day of year
        GndReflectanceForDayltg = 0.0            # Ground visible reflectance for use in daylighting calc
        GndReflectance = 0.0                     # Ground visible reflectance from input
        GndSolarRad = 0.0                        # Current ground reflected radiation
        GroundTemp = 0.0                         # Current ground temperature {C}
        GroundTempKelvin = 0.0                   # Current ground temperature {K}
        GroundTempFC = 0.0                       # Current ground temperature defined for F or C factor method {C}
        GroundTemp_Surface = 0.0                 # Current surface ground temperature {C}
        GroundTemp_Deep = 0.0                    # Current deep ground temperature
        HolidayIndex = 0                          # Indicates whether current day is a holiday and if so what type
        #    HolidayIndex=(0-no holiday, 1-holiday type 1, ...)
        HolidayIndexTomorrow = 0                  # Tomorrow's Holiday Index
        IsRain = 0.0                               # Surfaces are wet for this time interval
        IsSnow = 0.0                               # Snow on the ground for this time interval
        Latitude = 0.0                           # Latitude of building location
        Longitude = 0.0                          # Longitude of building location
        Month = 0                                 # Current calendar month
        MonthTomorrow = 0                         # Tomorrow's calendar month
        OutBaroPress = 0.0                       # Current outdoor air barometric pressure
        OutDryBulbTemp = 0.0                     # Current outdoor air dry bulb temperature
        EMSOutDryBulbOverrideOn = False       # EMS flag for outdoor air dry bulb temperature
        EMSOutDryBulbOverrideValue = 0.0         # EMS override value for outdoor air dry bulb temperature
        OutHumRat = 0.0                          # Current outdoor air humidity ratio
        OutRelHum = 0.0                          # Current outdoor relative humidity [%]
        OutRelHumValue = 0.0                     # Current outdoor relative humidity value [0.0-1.0]
        EMSOutRelHumOverrideOn = False        # EMS flag for outdoor relative humidity value
        EMSOutRelHumOverrideValue = 0.0          # EMS override value for outdoor relative humidity value
        OutEnthalpy = 0.0                        # Current outdoor enthalpy
        OutAirDensity = 0.0                      # Current outdoor air density
        OutWetBulbTemp = 0.0                     # Current outdoor air wet bulb temperature
        OutDewPointTemp = 0.0                    # Current outdoor dewpotemperature
        EMSOutDewPointTempOverrideOn = False  # EMS flag for outdoor dewpotemperature
        EMSOutDewPointTempOverrideValue = 0.0    # EMS override value for outdoor dewpotemperature
        SkyTemp = 0.0                            # Current sky temperature {C}
        SkyTempKelvin = 0.0                      # Current sky temperature {K}
        LiquidPrecipitation = 0.0                # Current liquid precipitation amount (rain) {m}
        SunIsUp = 0.0                              # True when Sun is over horizon, False when not
        WindDir = 0.0                            # Current outdoor air wind direction
        EMSWindDirOverrideOn = False          # EMS flag for outdoor air wind direction
        EMSWindDirOverrideValue = 0.0            # EMS override value for outdoor air wind direction
        WindSpeed = 0.0                          # Current outdoor air wind speed
        EMSWindSpeedOverrideOn = False        # EMS flag for outdoor air wind speed
        EMSWindSpeedOverrideValue = 0.0          # EMS override value for outdoor air wind speed
        WaterMainsTemp = 0.0                     # Current water mains temperature
        Year = 0                                  # Current calendar year of the simulation from the weather file
        YearTomorrow = 0                          # Tomorrow's calendar year of the simulation
        Array1D<Real64> SOLCOS(3);                 # Solar direction cosines at current time step
        CloudFraction = 0.0                      # Fraction of sky covered by clouds
        HISKF = 0.0                              # Exterior horizontal illuminance from sky (lux).
        HISUNF = 0.0                             # Exterior horizontal beam illuminance (lux)
        HISUNFnorm = 0.0                         # Exterior beam normal illuminance (lux)
        PDIRLW = 0.0                             # Luminous efficacy (lum/W) of beam solar radiation
        PDIFLW = 0.0                             # Luminous efficacy (lum/W) of sky diffuse solar radiation
        SkyClearness = 0.0                       # Sky clearness (see subr. DayltgLuminousEfficacy)
        SkyBrightness = 0.0                      # Sky brightness (see subr. DayltgLuminousEfficacy)
        StdBaroPress(StdPressureSeaLevel) = 0.0  # Standard "atmospheric pressure" based on elevation (ASHRAE HOF p6.1)
        StdRhoAir = 0.0                          # Standard "rho air" set in WeatherManager - based on StdBaroPress
        rhoAirSTP = 0.0                          # Standard density of dry air at 101325 Pa, 20.0C temperaure
        TimeZoneNumber = 0.0                     # Time Zone Number of building location
        TimeZoneMeridian = 0.0                   # Standard Meridian of TimeZone
        std::string EnvironmentName;               # Current environment name (longer for weather file names)
        std::string WeatherFileLocationTitle;      # Location Title from Weather File
        std::string CurMnDyHr;                     # Current Month/Day/Hour timestamp info
        std::string CurMnDy;                       # Current Month/Day timestamp info
        std::string CurMnDyYr;                     # Current Month/Day/Year timestamp info
        CurEnvirNum = 0                           # current environment number
        TotDesDays = 0                         # Total number of Design days to Setup
        TotRunDesPersDays = 0                  # Total number of Run Design Periods [Days] (Weather data) to Setup
        CurrentOverallSimDay = 0               # Count of current simulation day in total of all sim days
        TotalOverallSimDays = 0                   # Count of all possible simulation days in all environments
        MaxNumberSimYears = 0                     # Maximum number of simulation years requested in all RunPeriod statements
        RunPeriodStartDayOfWeek = 0               # Day of week of the first day of the run period. (or design day - day of week)

        CosSolarDeclinAngle = 0.0                # Cosine of the solar declination angle
        EquationOfTime = 0.0                     # Value of the equation of time formula
        SinLatitude = 0.0                        # Sine of Latitude
        CosLatitude = 0.0                        # Cosine of Latitude
        SinSolarDeclinAngle = 0.0                # Sine of the solar declination angle
        TS1TimeOffset(-0.5);                # offset when TS=1 for solar calculations

        WeatherFileWindModCoeff(1.5863);     =(WindBLHeight/WindSensorHeight)**WindExp for conditions at the weather station
        WeatherFileTempModCoeff(0.0);        =AtmosphericTempGradient*EarthRadius*SensorHeight/(EarthRadius+SensorHeight)

        SiteWindExp(0.22);                  # Exponent for the wind velocity profile at the site
        SiteWindBLHeight(370.0);            # Boundary layer height for the wind velocity profile at the site (m)
        SiteTempGradient(0.0065);           # Air temperature gradient coefficient (K/m)

        GroundTempObjInput = False            # Ground temperature object input
        GroundTemp_SurfaceObjInput = False    # Surface ground temperature object input
        GroundTemp_DeepObjInput = False       # Deep ground temperature object input
        FCGroundTemps = False
        DisplayWeatherMissingDataWarnings = False     Display missing/out of range weather warnings
        IgnoreSolarRadiation = False                  TRUE if all solar radiation is to be ignored
        IgnoreBeamRadiation = False                   TRUE if beam (aka direct normal) radiation is to be ignored
        IgnoreDiffuseRadiation = False                TRUE if diffuse horizontal radiation is to be ignored

        PrintEnvrnStampWarmup = False
        PrintEnvrnStampWarmupPrinted = False

        RunPeriodEnvironment = False          # True if Run Period, False if DesignDay
        std::string EnvironmentStartEnd;           # Start/End dates for Environment
        CurrentYearIsLeapYear = False         # true when current year is leap year (convoluted logic dealing with
            whether weather file allows leap years, runperiod inputs.

        varyingLocationSchedIndexLat = 0
        varyingLocationSchedIndexLong = 0
        varyingOrientationSchedIndex = 0

        # SUBROUTINE SPECIFICATIONS FOR MODULE DataEnvironment:
        # PUBLIC OutBaroPressAt
        # PUBLIC OutAirDensityAt

        # Functions (não sei se pode ser 'def' de 'def' ou se deveria ser 'def' de 'class')

        def clear_state():
            '''
            Clears the global data in DataEnvironment.
            Needed for unit tests, should not be normally called.
            '''
            BeamSolarRad = 0.0
            EMSBeamSolarRadOverrideOn = False
            EMSBeamSolarRadOverrideValue = 0.0
            DayOfMonth = 0
            DayOfMonthTomorrow = 0
            DayOfWeek = 0
            DayOfWeekTomorrow = 0
            DayOfYear = 0
            DayOfYear_Schedule = 0
            DifSolarRad = 0.0
            EMSDifSolarRadOverrideOn = False
            EMSDifSolarRadOverrideValue = 0.0
            DSTIndicator = 0
            Elevation = 0.0
            EndMonthFlag = bool();
            GndReflectanceForDayltg = 0.0
            GndReflectance = 0.0
            GndSolarRad = 0.0
            GroundTemp = 0.0
            GroundTempKelvin = 0.0
            GroundTempFC = 0.0
            GroundTemp_Surface = 0.0
            GroundTemp_Deep = 0.0
            HolidayIndex = 0
            HolidayIndexTomorrow = 0
            IsRain = bool();
            IsSnow = bool();
            Latitude = 0.0
            Longitude = 0.0
            Month = 0
            MonthTomorrow = 0
            OutBaroPress = 0.0
            OutDryBulbTemp = 0.0
            EMSOutDryBulbOverrideOn = False
            EMSOutDryBulbOverrideValue = 0.0
            OutHumRat = 0.0
            OutRelHum = 0.0
            OutRelHumValue = 0.0
            EMSOutRelHumOverrideOn = False
            EMSOutRelHumOverrideValue = 0.0
            OutEnthalpy = 0.0
            OutAirDensity = 0.0
            OutWetBulbTemp = 0.0
            OutDewPointTemp = 0.0
            EMSOutDewPointTempOverrideOn = False
            EMSOutDewPointTempOverrideValue = 0.0
            SkyTemp = 0.0
            SkyTempKelvin = 0.0
            LiquidPrecipitation = 0.0
            SunIsUp = bool();
            WindDir = 0.0
            EMSWindDirOverrideOn = False
            EMSWindDirOverrideValue = 0.0
            WindSpeed = 0.0
            EMSWindSpeedOverrideOn = False
            EMSWindSpeedOverrideValue = 0.0
            WaterMainsTemp = 0.0
            Year = 0
            YearTomorrow = 0
            SOLCOS.dimension(3);
            CloudFraction = 0.0
            HISKF = 0.0
            HISUNF = 0.0
            HISUNFnorm = 0.0
            PDIRLW = 0.0
            PDIFLW = 0.0
            SkyClearness = 0.0
            SkyBrightness = 0.0
            StdBaroPress = 101325.0;
            StdRhoAir = 0.0
            TimeZoneNumber = 0.0
            TimeZoneMeridian = 0.0
            EnvironmentName = std::string();
            WeatherFileLocationTitle = std::string();
            CurMnDyHr = std::string();
            CurMnDy = std::string();
            CurMnDyYr = std::string();
            CurEnvirNum = 0
            TotDesDays = 0;
            TotRunDesPersDays = 0;
            CurrentOverallSimDay = 0
            TotalOverallSimDays = 0
            MaxNumberSimYears = 0
            RunPeriodStartDayOfWeek = 0
            CosSolarDeclinAngle = 0.0
            EquationOfTime = 0.0
            SinLatitude = 0.0
            CosLatitude = 0.0
            SinSolarDeclinAngle = 0.0
            TS1TimeOffset = -0.5;
            WeatherFileWindModCoeff = 1.5863;
            WeatherFileTempModCoeff = 0.0;
            SiteWindExp = 0.22;
            SiteWindBLHeight = 370.0;
            SiteTempGradient = 0.0065;
            GroundTempObjInput = False
            GroundTemp_SurfaceObjInput = False
            GroundTemp_DeepObjInput = False
            FCGroundTemps = False
            DisplayWeatherMissingDataWarnings = False
            IgnoreSolarRadiation = False
            IgnoreBeamRadiation = False
            IgnoreDiffuseRadiation = False
            PrintEnvrnStampWarmup = False
            PrintEnvrnStampWarmupPrinted = False
            RunPeriodEnvironment = False
            EnvironmentStartEnd = std::string();
            CurrentYearIsLeapYear = False
            varyingLocationSchedIndexLat = 0;
            varyingLocationSchedIndexLong = 0;
            varyingOrientationSchedIndex = 0;

            return None


        def OutDryBulbTempAt(Z):
            '''
            FUNCTION INFORMATION:
                  AUTHOR         Peter Graham Ellis
                  DATE WRITTEN   January 2006
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS FUNCTION:
            Calculates outdoor dry bulb temperature at a given altitude.
            'Z' is the height above ground (m).

            METHODOLOGY EMPLOYED:
            1976 U.S. Standard Atmosphere.

            REFERENCES:
            1976 U.S. Standard Atmosphere. 1976. U.S. Government Printing Office, Washington, D.C.
            '''
            # Using/Aliasing
            using General::RoundSigDigits;

            # Return value declaration
            LocalOutDryBulbTemp = 0     # Return result for function (C)

            # Locals
            # FUNCTION ARGUMENT DEFINITIONS:

            # FUNCTION LOCAL VARIABLE DECLARATIONS:
            BaseTemp = OutDryBulbTemp + WeatherFileTempModCoeff     # Base temperature at Z = 0 (C)

            if (SiteTempGradient == 0.0):
                LocalOutDryBulbTemp = OutDryBulbTemp
            elif (Z <= 0.0):
                LocalOutDryBulbTemp = BaseTemp
            else:
                LocalOutDryBulbTemp = BaseTemp - SiteTempGradient * EarthRadius * Z / (EarthRadius + Z)


            if (LocalOutDryBulbTemp < -100.0):
                # raise...
                ShowSevereError("OutDryBulbTempAt: outdoor drybulb temperature < -100 C")
                ShowContinueError("...check heights, this height=[" + RoundSigDigits(Z, 0) + "].")
                ShowFatalError("Program terminates due to preceding condition(s).")

            return LocalOutDryBulbTemp


        def OutWetBulbTempAt(Z):
            '''
            FUNCTION INFORMATION:
                  AUTHOR         Peter Graham Ellis
                  DATE WRITTEN   January 2006
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS FUNCTION:
            Calculates outdoor wet bulb temperature at a given altitude.
            'Z' is the height above ground (m).

            METHODOLOGY EMPLOYED:
            1976 U.S. Standard Atmosphere.

            REFERENCES:
            1976 U.S. Standard Atmosphere. 1976. U.S. Government Printing Office, Washington, D.C.
            '''
            # Using/Aliasing
            using General::RoundSigDigits;

            # Return value declaration
            LocalOutWetBulbTemp = 0     # Return result for function (C)

            # Locals
            # FUNCTION ARGUMENT DEFINITIONS:

            # FUNCTION LOCAL VARIABLE DECLARATIONS:
            BaseTemp = OutWetBulbTemp + WeatherFileTempModCoeff;    # Base temperature at Z = 0 (C)

            if (SiteTempGradient == 0.0):
                LocalOutWetBulbTemp = OutWetBulbTemp
            elif (Z <= 0.0):
                LocalOutWetBulbTemp = BaseTemp
            else:
                LocalOutWetBulbTemp = BaseTemp - SiteTempGradient * EarthRadius * Z / (EarthRadius + Z)
            
                
            if (LocalOutWetBulbTemp < -100.0):
                # raise <nome do erro>("msg para ser mostrada")
                ShowSevereError("OutWetBulbTempAt: outdoor wetbulb temperature < -100 C")
                ShowContinueError("...check heights, this height=[" + RoundSigDigits(Z, 0) + "].")
                ShowFatalError("Program terminates due to preceding condition(s).")

            return LocalOutWetBulbTemp


        def OutDewPointTempAt(Z): #     Height above ground (m)
            '''
            FUNCTION INFORMATION:
                  AUTHOR         Linda Lawrie
                  DATE WRITTEN   March 2007
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS FUNCTION:
            Calculates outdoor dew potemperature at a given altitude.

            METHODOLOGY EMPLOYED:
            1976 U.S. Standard Atmosphere.
            copied from outwetbulbtempat

            REFERENCES:
            1976 U.S. Standard Atmosphere. 1976. U.S. Government Printing Office, Washington, D.C.
            '''
            # Using/Aliasing
            using General::RoundSigDigits;

                Return value
            LocalOutDewPointTemp;     Return result for function (C)

                Locals
                FUNCTION ARGUMENT DEFINITIONS:

                FUNCTION LOCAL VARIABLE DECLARATIONS:
            BaseTemp;     Base temperature at Z = 0 (C)

            BaseTemp = OutDewPointTemp + WeatherFileTempModCoeff;

            if (SiteTempGradient == 0.0):
                LocalOutDewPointTemp = OutDewPointTemp
            elif (Z <= 0.0):
                LocalOutDewPointTemp = BaseTemp
            else:
                LocalOutDewPointTemp = BaseTemp - SiteTempGradient * EarthRadius * Z / (EarthRadius + Z)

            if (LocalOutDewPointTemp < -100.0):
                # raise <nome do erro>
                ShowSevereError("OutDewPointTempAt: outdoor dewpotemperature < -100 C");
                ShowContinueError("...check heights, this height=[" + RoundSigDigits(Z, 0) + "].");
                ShowFatalError("Program terminates due to preceding condition(s).");

            return LocalOutDewPointTemp


        def WindSpeedAt(Z): #     Height above ground (m)
            '''
            FUNCTION INFORMATION:
                  AUTHOR         Peter Graham Ellis
                  DATE WRITTEN   January 2006
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS FUNCTION:
            Calculates local wind speed at a given altitude.

            METHODOLOGY EMPLOYED:
            2005 ASHRAE Fundamentals, Chapter 16, Equation 4.  (Different depending on terrain).

            REFERENCES:
            2005 ASHRAE Fundamentals, Chapter 16, Equation 4.  (Different depending on terrain).
            Terrain variables are set in HeatBalanceManager or entered by the user.

            Return value
            LocalWindSpeed;     Return result for function (m/s)
            '''
            Locals
            # FUNCTION ARGUMENT DEFINITIONS:

            if (Z <= 0.0):
                LocalWindSpeed = 0.0
            elif (SiteWindExp == 0.0):
                LocalWindSpeed = WindSpeed
            else:
                 # [Met] - at meterological Station, Height of measurement is usually 10m above ground
                 LocalWindSpeed = Windspeed [Met] * (Wind Boundary LayerThickness [Met]/Height [Met])**Wind Exponent[Met] &
                                        * (Height above ground / Site Wind Boundary Layer Thickness) ** Site Wind Exponent
                LocalWindSpeed = WindSpeed * WeatherFileWindModCoeff * std::pow(Z / SiteWindBLHeight, SiteWindExp)

            return LocalWindSpeed


        def OutBaroPressAt(Z): #     Height above ground (m)
            '''
            FUNCTION INFORMATION:
                  AUTHOR         Daeho Kang
                  DATE WRITTEN   August 2009
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS FUNCTION:
            Calculates local air barometric pressure at a given altitude.

            METHODOLOGY EMPLOYED:
            U.S. Standard Atmosphere1976, Part 1, Chapter 1.3, Equation 33b.

            REFERENCES:
            U.S. Standard Atmosphere1976, Part 1, Chapter 1.3, Equation 33b.

            Return value
            LocalAirPressure;     Return result for function (Pa)
            '''
            # Locals
            # FUNCTION ARGUMENT DEFINITIONS:

            # FUNCTION PARAMETER DEFINITIONS:
            StdGravity = 9.80665            # The acceleration of gravity at the sea level (m/s2)
            AirMolarMass = 0.028964         # Molar mass of Earth's air (kg/mol)
            GasConstant = 8.31432           # Molar gas constant (J/Mol-K)
            TempGradient = -0.0065          # Molecular-scale temperature gradient (K/m)
            GeopotentialH = 0.0             # Geopotential height (zero within 11km from the sea level) (m)

            # FUNCTION LOCAL VARIABLE DECLARATIONS:
            BaseTemp = OutDryBulbTempAt(Z) + KelvinConv;    # Base temperature at Z

            if (Z <= 0.0):
                LocalAirPressure = 0.0
            elif (SiteTempGradient == 0.0):
                LocalAirPressure = OutBaroPress
            else:
                LocalAirPressure = StdBaroPress * std::pow(BaseTemp / (BaseTemp + TempGradient * (Z - GeopotentialH)),
                                                           (StdGravity * AirMolarMass) / (GasConstant * TempGradient))

            return LocalAirPressure


        def SetOutBulbTempAt_error(std::string const &Settings, max_height, std::string const &SettingsName):
            '''
            Using/Aliasing
            using General::RoundSigDigits;
            '''
            ShowSevereError("SetOutBulbTempAt: " + Settings + " Outdoor Temperatures < -100 C")
            ShowContinueError("...check " + Settings + " Heights - Maximum " + Settings + " Height=[" + RoundSigDigits(max_height, 0) + "].")

            if (max_height >= 20000.0):
                # raise ...
                ShowContinueError("...according to your maximum Z height, your building is somewhere in the Stratosphere.");
                ShowContinueError("...look at " + Settings + " Name= " + SettingsName);

            #raise ...
            ShowFatalError("Program terminates due to preceding condition(s).");


        def SetWindSpeedAt(NumItems, Heights, LocalWindSpeed, std::string const &EP_UNUSED(Settings)):
            '''
            SUBROUTINE INFORMATION:
                  AUTHOR         Linda Lawrie
                  DATE WRITTEN   June 2013
                  MODIFIED       na
                  RE-ENGINEERED  na

            PURPOSE OF THIS SUBROUTINE:
            Routine provides facility for doing bulk Set Windspeed at Height.

            METHODOLOGY EMPLOYED:
            na

            REFERENCES:
            na

            Using/Aliasing

            Argument array dimensioning
            '''

            Locals
            SUBROUTINE ARGUMENT DEFINITIONS:

            SUBROUTINE PARAMETER DEFINITIONS:
            na

            INTERFACE BLOCK SPECIFICATIONS:
            na

            DERIVED TYPE DEFINITIONS:
            na

            SUBROUTINE LOCAL VARIABLE DECLARATIONS:

            if (SiteWindExp == 0.0):
                LocalWindSpeed = WindSpeed
            else:
                fac(WindSpeed * WeatherFileWindModCoeff * std::pow(SiteWindBLHeight, -SiteWindExp))
                Z = 0       # Centroid value
                for i in range(1, NumItems): # REVER
                    Z = Heights(i)
                    if (Z <= 0.0):
                        LocalWindSpeed(i) = 0.0
                    else:
                        # [Met] - at meterological Station, Height of measurement is usually 10m above ground
                        LocalWindSpeed = Windspeed [Met] * (Wind Boundary LayerThickness [Met]/Height [Met])**Wind Exponent[Met] &
                                                * (Height above ground / Site Wind Boundary Layer Thickness) ** Site Wind Exponent
                        LocalWindSpeed(i) = fac * std::pow(Z, SiteWindExp)

            return None


    # end of DataEnvironment
# end of EnergyPlus
