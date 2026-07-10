-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the station list of ONE product — the historical daily climate (kl) series. Stations that only ever reported other products (10-minute, hourly, precipitation-only) are absent, so it is not the full DWD network.
-- caution: Most rows are closed historic stations: `from_date`/`to_date` bound the station's daily-climate record, and only a station whose `to_date` is near today is still reporting.
-- caution: `bundesland` is spelled with umlauts (Baden-Württemberg), whereas `region` in the regional-averages tables uses the transliterated form (Baden-Wuerttemberg) and carries combination regions — the two do not join without normalising.
-- caution: `height_m` is the station's elevation above sea level, not the height of the instrument.
SELECT
    "station_id",
    "from_date",
    "to_date",
    "height_m",
    "latitude",
    "longitude",
    "name",
    "bundesland"
FROM "dwd-stations"
