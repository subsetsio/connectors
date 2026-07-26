-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "request_type",
    "number_of_complaints_fy_18_7120176302018",
    "number_of_complaints_fy_19_7120186302019",
    "number_of_complaints_fy_20_7_1_2019_6_30_2020"
FROM "nyc-open-data-3fes-huds"
