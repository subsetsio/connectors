-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dfta_id",
    "provider_name",
    "event_name",
    "event_type",
    "description",
    "topics",
    "max_attendees",
    "event_location",
    "city",
    "state",
    "zipcode",
    "borough",
    "start_time",
    "endtime",
    "is_virtual",
    "is_live",
    "is_recurring",
    "event_accessibility",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-fzy4-e84j"
