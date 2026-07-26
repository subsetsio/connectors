-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "encounter_datetime",
    "park_area_id",
    "city_agency",
    "encounter_type",
    "simplified_encounter_type",
    "sd_patronscomplied",
    "sd_patronsnocomply",
    "sd_amenity",
    "closed_amenity",
    "closed_patroncount",
    "closed_approach",
    "closed_outcome",
    "park_borough"
FROM "nyc-open-data-akzx-fghb"
