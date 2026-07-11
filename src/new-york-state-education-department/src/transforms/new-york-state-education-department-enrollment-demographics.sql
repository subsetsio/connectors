-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This wide table carries overlapping race, gender, and program-population measures on each row; do not sum percentages or overlapping counts as mutually exclusive totals.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "num_ell",
    "per_ell",
    CAST("num_am_ind" AS BIGINT) AS num_am_ind,
    CAST("per_am_ind" AS BIGINT) AS per_am_ind,
    "num_black",
    "per_black",
    "num_hisp",
    "per_hisp",
    "num_asian",
    "per_asian",
    "num_white",
    "per_white",
    "num_multi",
    "per_multi",
    "num_swd",
    "per_swd",
    "num_female",
    "per_female",
    "num_male",
    "per_male",
    "num_ecdis",
    "per_ecdis",
    "num_migrant",
    "per_migrant",
    "num_homeless",
    "per_homeless",
    "num_foster",
    "per_foster",
    "num_armed",
    "per_armed",
    "num_nonbinary",
    "per_nonbinary"
FROM "new-york-state-education-department-enrollment-demographics"
