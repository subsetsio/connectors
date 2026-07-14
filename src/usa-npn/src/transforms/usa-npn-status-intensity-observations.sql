-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are status/intensity observation events; repeated observer, site, species, phenophase, and date combinations can occur and should not be treated as one unique observation without considering the source's status/intensity fields.
SELECT
    "observation_id",
    "update_datetime",
    "site_id",
    "latitude",
    "longitude",
    "elevation_in_meters",
    "state",
    "species_id",
    "genus",
    "species",
    "common_name",
    "kingdom",
    "individual_id",
    "phenophase_id",
    "phenophase_description",
    "observation_date",
    "day_of_year",
    "phenophase_status",
    "intensity_category_id",
    "intensity_value",
    "abundance_value"
FROM "usa-npn-status-intensity-observations"
