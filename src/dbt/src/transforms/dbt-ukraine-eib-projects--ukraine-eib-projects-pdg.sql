-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "title",
    "description",
    "status",
    "status_date",
    CAST("proposed_eib_finance_euros" AS BIGINT) AS proposed_eib_finance_euros,
    CAST("proposed_eib_finance_gbp" AS BIGINT) AS proposed_eib_finance_gbp,
    CAST("total_cost_euros" AS BIGINT) AS total_cost_euros,
    CAST("total_cost_gbp" AS BIGINT) AS total_cost_gbp,
    "sectors",
    "project_url"
FROM "dbt-ukraine-eib-projects--ukraine-eib-projects-pdg"
