SocialIndicatorsOldColumnNames = [
	'`Birth rate, crude (per 1,000 people)`',
	'`Compulsory education, duration (years)`',
	'`Death rate, crude (per 1,000 people)`',
	'`GDP (current US$)`',
	'`GNI (current US$)`',
	'`HFC gas emissions (thousand metric tons of CO2 equivalent)`',
	'`Life expectancy at birth, total (years)`',
	'`Literacy rate, adult total (% of people ages 15 and above)`',
	'`Literacy rate, youth total (% of people ages 15-24)`',
	'`Mortality rate, infant (per 1,000 live births)`',
	'`Population density (people per sq. km of land area)`',
	'`Population, total`']

SocialIndicatorsNewColumnNames = [
	'birthRateCrudeper1000people',
	'compulsoryEducationDurationYears',
	'deathRateCrudeper1000people',
	'GDPcurrentUSD',
	'GNIcurrentUSD',
	'lifeExpectancyAtBirthYears',
	'literacyRateOfAdultsPercent',
	'literacyRateOfYouthPercent',
	'mortalityRateInfant1000liveBirhts',
	'populationDensityPerSqKm',
	'population']

SocialIndicatorsOutputFolder = '/socialIndicators/socialIndicators.parquet'

SocialIndicatorsColumnDefinitions = (SocialIndicatorsOldColumnNames,
									SocialIndicatorsNewColumnNames,
									SocialIndicatorsOutputFolder)

LandUsageOldColumnNames = [
	'`Agricultural land (% of land area)`',
	'`Agricultural land (sq. km)`',
	'`Arable land (% of land area)`',
	'`Arable land (hectares)`',
	'`Forest area (% of land area)`',
	'`Forest area (sq. km)`',
	'`Land area (sq. km)`',
	'`Land under cereal production (hectares)`',
	'`Permanent cropland (% of land area)`',
	'`Rural land area (sq. km)`',
	'`Surface area (sq. km)`',
	'`Urban land area (sq. km)`']

LandUsageNewColumnNames = [
	'agriculturalLandPercent',
	'agriculturalLandSqKm',
	'arableLandPercent',
	'arableLandHectar',
	'forestAreaPercent',
	'forestAreaSqKm',
	'landAreaSqKm',
	'landUnderCerealProductionHectar',
	'permanentCorplandPercent',
	'ruralLandAreaSqKm',
	'surfaceAreaSqKm',
	'urbanLandAreaSqKm']

LandUsageOutputFolder = '/landUsage/landUsage.parquet'

LandUsageColumnDefinitions = (LandUsageOldColumnNames,
							LandUsageNewColumnNames,
							LandUsageOutputFolder)

AgriculturarAndNaturalResourcesOldColumnNames = [
	'`Agricultural raw materials exports (% of merchandise exports)`',
	'`Agricultural raw materials imports (% of merchandise imports)`',
	'`Agriculture, forestry, and fishing, value added (% of GDP)`',
	'`Coal rents (% of GDP)`',
	'`Forest rents (% of GDP)`',
	'`Mineral rents (% of GDP)`',
	'`Natural gas rents (% of GDP)`',
	'`Oil rents (% of GDP)`',
	'`Total natural resources rents (% of GDP)`']

AgriculturarAndNaturalResourcesNewColumnNames = [
	'agriculturalExportPercent',
	'agriculturalImportPercent',
	'agricultureForestryFishingPercentOfGDP',
	'coalRentsPercentOfGDP',
	'forestRentsPercentOfGDP',
	'mineralRentsPercentOfGDP',
	'naturalGasRentsPercentOfGDP',
	'oilRentsPercentOfGDP',
	'totalNaturalResourcesRentsPercentageOfGDP']

AgriculturarAndNaturalResourcesOutputFolder = '/agriculturarAndNaturalResources/agriculturarAndNaturalResources.parquet'

AgriculturarAndNaturalResourcesColumnDefinitions = (AgriculturarAndNaturalResourcesOldColumnNames,
													AgriculturarAndNaturalResourcesNewColumnNames,
													AgriculturarAndNaturalResourcesOutputFolder)

BiodiversityIndicatorsOldColumnNames = [
	'`Bird species, threatened`',
	'`Fish species, threatened`',
	'`Mammal species, threatened`',
	'`Marine protected areas (% of territorial waters)`',
	'`Plant species (higher), threatened`',
	'`Terrestrial and marine protected areas (% of total territorial area)`',
	'`Terrestrial protected areas (% of total land area)`']

BiodiversityIndicatorsNewColumnNames = [
	'birdSpeciesThreatened',
	'fishSpeciesThreatened',
	'mammalSpeciesThreatened',
	'marineProtectedAreasPercent',
	'plantSpeciesThreatened',
	'terrestrialAndMarineProtectedAreasPercent',
	'terrestrialProtectedAreasPercent']

BiodiversityIndicatorsOutputFolder = '/biodiversityIndicators/biodiversityIndicators.parquet'

BiodiversityIndicatorsColumnDefinitions = (BiodiversityIndicatorsOldColumnNames,
											BiodiversityIndicatorsNewColumnNames,
											BiodiversityIndicatorsOutputFolder)

EmissionIndicatorsOldColumnNames = [
	'`Agricultural methane emissions (thousand metric tons of CO2 equivalent)`',
	'`Agricultural nitrous oxide emissions (thousand metric tons of CO2 equivalent)`',
	'`CO2 emissions (kt)`',
	'`CO2 emissions from gaseous fuel consumption (kt)`',
	'`CO2 emissions from liquid fuel consumption (kt)`',
	'`CO2 emissions from manufacturing industries and construction (% of total fuel combustion)`',
	'`CO2 emissions from other sectors, excluding residential buildings and commercial and public services (% of total fuel combustion)`',
	'`CO2 emissions from residential buildings and commercial and public services (% of total fuel combustion)`',
	'`CO2 emissions from solid fuel consumption (kt)`',
	'`CO2 emissions from transport (% of total fuel combustion)`',
	'`CO2 intensity (kg per kg of oil equivalent energy use)`',
	'`Energy related methane emissions (% of total)`',
	'`Methane emissions (kt of CO2 equivalent)`',
	'`Nitrous oxide emissions (thousand metric tons of CO2 equivalent)`',
	'`Nitrous oxide emissions in energy sector (thousand metric tons of CO2 equivalent)`',
	'`Other greenhouse gas emissions, HFC, PFC and SF6 (thousand metric tons of CO2 equivalent)`',
	'`PFC gas emissions (thousand metric tons of CO2 equivalent)`',
	'`SF6 gas emissions (thousand metric tons of CO2 equivalent)`',
	'`Total greenhouse gas emissions (kt of CO2 equivalent)`']

EmissionIndicatorsNewColumnNames = [
	'agriculturalMethaneEmissionsThousandMetricTonsOfCO2equivalent',
	'agriculturalNitrousOxideEmissionsThousandMetricTonsOfCO2equivalent',
	'CO2EmissionsKt',
	'CO2EmissionsFromGaseousGuelConsumptionKt',
	'CO2EmissionsFromLiquidFuelConsumptionKt',
	'CO2EmissionsFromManufacturingIndustriesAndConstructionPercent',
	'CO2EmissionsFromOtherSectorsPercentage',
	'CO2EmissionsFromResidentialBuildingsAndCommercialAndPublicServicesPercent',
	'CO2EmissionsFromSolidFuelConsumptionKt',
	'CO2EmissionsFromTransportPercent',
	'energyRelatedMethaneEmissionsPercent',
	'HFCGasEmissionsThousandMetricTonsOfCO2equivalent',
	'methaneEmissionsKtofCO2Equivalent',
	'nitrousOxideEmissionsThousandMetricTonsOfCO2equivalent',
	'nitrousOxideEmissionsInEnergySectorThousandMetricTonsOfCO2equivalent',
	'otherGreenhouseGasEmissionsThousandMetricTonsOfCO2equivalent',
	'PFCGasEmissionsThousandMetricTonsOfCO2equivalent',
	'SF6GasEmissionsThousandMetricTonsOfCO2equivalent',
	'totalGreenhouseGasEmissionsKtOfCO2equivalent']

EmissionIndicatorsOutputFolder = '/emissionIndicators/emissionIndicators.parquet'

EmissionIndicatorsColumnDefinitions = (EmissionIndicatorsOldColumnNames,
									EmissionIndicatorsNewColumnNames,
									EmissionIndicatorsOutputFolder)

EnergyProductionIndicatorsOldColumnNames = [
	'`Alternative and nuclear energy (% of total energy use)`',
	'`Combustible renewables and waste (% of total energy)`',
	'`Electric power consumption (kWh per capita)`',
	'`Electric power transmission and distribution losses (% of output)`',
	'`Electricity production from coal sources (% of total)`',
	'`Electricity production from natural gas sources (% of total)`',
	'`Electricity production from nuclear sources (% of total)`',
	'`Electricity production from oil sources (% of total)`',
	'`Electricity production from oil, gas and coal sources (% of total)`',
	'`Electricity production from renewable sources, excluding hydroelectric (% of total)`']

EnergyProductionIndicatorsNewColumnNames = [
	'alternativeAndNuclearEnergyOfTotalEnergyPercent',
	'combustibleRenewablesAndWastePercent',
	'electricPowerConsumptionkWhpeople',
	'electricPowerTransmissionLossesPercent',
	'electricityFromCoalPercent',
	'electricityFromNaturalGasPercent',
	'electricityFromNuclearSourcesPercent',
	'electricityFromOilPercent',
	'electricityFromOilGasCoalPercent',
	'electricityFromRenewablePercent']

EnergyProductionIndicatorsOutputFolder = '/energyProductionIndicators/energyProductionIndicators.parquet'

EnergyProductionIndicatorsColumnDefinitions = (EnergyProductionIndicatorsOldColumnNames,
											EnergyProductionIndicatorsNewColumnNames,
											EnergyProductionIndicatorsOutputFolder)

ColumnDefinitions = [SocialIndicatorsColumnDefinitions, LandUsageColumnDefinitions, AgriculturarAndNaturalResourcesColumnDefinitions,
					BiodiversityIndicatorsColumnDefinitions, EmissionIndicatorsColumnDefinitions, EnergyProductionIndicatorsColumnDefinitions]