-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Source of funds and R and D field" AS source_of_funds_and_r_and_d_field,
    "All institutions" AS all_institutions,
    "Survey population - Short form" AS survey_population_short_form,
    "Survey population - Standard form" AS survey_population_standard_form
FROM "ncses-nsf26304-tab003"
