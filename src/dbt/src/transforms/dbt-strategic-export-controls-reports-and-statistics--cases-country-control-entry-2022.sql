-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `licences` is the count of licence cases for each country/rating/incorporation/application-type combination — filter or group by those dimensions before summing; the rows are already aggregated.
SELECT
    "country_name",
    "rating",
    "incorporation",
    "app_type",
    "app_sub_type",
    "outcome",
    CAST("licences" AS BIGINT) AS licences
FROM "dbt-strategic-export-controls-reports-and-statistics--cases-country-control-entry-2022"
