-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "community_school_district",
    "city_council_district",
    "school_dbn",
    "school_name",
    "number_of_graduates",
    "number_of_graduates_that_completed_2_credits_in_arts",
    "percent_of_graduates_that_completed_2_credits_in_arts"
FROM "nyc-open-data-h5j6-bv4u"
