-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "LGD2014" AS lgd2014,
    "Local Government District" AS local_government_district,
    "BroadIndustryGroup" AS broadindustrygroup,
    "Broad industry group" AS broad_industry_group,
    "EMPBAND" AS empband,
    "Employee size band" AS employee_size_band,
    "TOBAND" AS toband,
    "Turnover size band (£'000)" AS turnover_size_band_000,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-businessbandlgd"
