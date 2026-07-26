-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "facility_name",
    "facility_id",
    "facility_type",
    "name_of_disposal_site_used",
    "disposal_site_id",
    "facility_tonsday_by_disposal_site",
    "type_of_disposal_site",
    "miles_to_site",
    "truck_or_rr",
    "disposal_site_hudson_river_crossing"
FROM "nyc-open-data-99xv-he3n"
