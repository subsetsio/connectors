-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census Year" AS BIGINT) AS census_year,
    "LGD2014" AS lgd2014,
    "Local Government District" AS local_government_district,
    CAST("RELIGION_OR_RELIGION_BROUGHT_UP_IN" AS BIGINT) AS religion_or_religion_brought_up_in,
    "Religion or religion brought up in" AS religion_or_religion_brought_up_in_2,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-ts014"
