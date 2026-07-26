-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "encounter_datetime",
    "park_area_id",
    "park_division",
    "visit_reason",
    "patrol_method",
    "encounter_type",
    "simplified_encounter_type",
    "closed_amenity",
    "closed_patroncount",
    "closed_education",
    "closed_outcome",
    "closed_pdcontact",
    "closed_outcome_spec",
    "sd_patronscomplied",
    "sd_patronsnocomply",
    "sd_amenity",
    "sd_pdcontact",
    "sd_outcome_spec",
    "summonscount_a01",
    "summonscount_a03",
    "summonscount_a04",
    "summonscount_a22",
    "other_summonscount",
    "park_borough"
FROM "nyc-open-data-yv25-wqf9"
