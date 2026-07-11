-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "StationName" AS stationname,
    CAST("WXID" AS BIGINT) AS wxid,
    "ObservedDate" AS observeddate,
    "NESSID" AS nessid,
    "NWSID" AS nwsid,
    "Elevation" AS elevation,
    "SiteDescription" AS sitedescription,
    "Latitude" AS latitude,
    "Longitude" AS longitude,
    "State" AS state,
    "County" AS county,
    "Agency" AS agency,
    "Region" AS region,
    "Unit" AS unit,
    "SubUnit" AS subunit,
    "Status" AS status,
    "RainAccumulation" AS rainaccumulation,
    "WindSpeedMPH" AS windspeedmph,
    "WindDirDegrees" AS winddirdegrees,
    "AirTempStandPlace" AS airtempstandplace,
    "FuelTemp" AS fueltemp,
    "RelativeHumidity" AS relativehumidity,
    "BatteryVoltage" AS batteryvoltage,
    "FuelMoisture" AS fuelmoisture,
    "WindDirPeak" AS winddirpeak,
    "WindSpeedPeak" AS windspeedpeak,
    "SolarRadiation" AS solarradiation,
    CAST("StationID" AS BIGINT) AS stationid,
    "MesoWestStationID" AS mesoweststationid,
    "MesoWestURL" AS mesowesturl,
    "NOAA_URL" AS noaa_url
FROM "nifc-29185087b4594a35abe059cbdbf97ee4-1"
