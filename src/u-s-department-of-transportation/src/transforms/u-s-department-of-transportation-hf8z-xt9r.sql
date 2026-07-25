-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("imo_number" AS BIGINT) AS imo_number,
    "vessel_name",
    "ship_type",
    CAST("gross_tons" AS BIGINT) AS gross_tons,
    CAST("deadweight_tons" AS BIGINT) AS deadweight_tons,
    CAST("year_of_build" AS BIGINT) AS year_of_build,
    "operator",
    CAST("msp" AS BOOLEAN) AS msp,
    CAST("visa" AS BOOLEAN) AS visa,
    CAST("vta" AS BOOLEAN) AS vta,
    CAST("jones_act_eligible" AS BOOLEAN) AS jones_act_eligible,
    CAST("militarily_useful" AS BOOLEAN) AS militarily_useful
FROM "u-s-department-of-transportation-hf8z-xt9r"
