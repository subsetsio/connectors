-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("notice_id" AS BIGINT) AS notice_id,
    "ecepp_id",
    "title",
    "notice_url",
    "notice_type",
    "procurement_exercise_title",
    "country",
    "published_date",
    "closing_date",
    "current_state",
    "published_date_raw",
    CAST("published_sort" AS BIGINT) AS published_sort,
    "closing_sort",
    "project_name",
    "project_id",
    "client_name",
    "procurement_type",
    "procurement_method",
    "business_sector",
    "publication_date",
    "issue_date",
    "status",
    "contract_value",
    "contract_currency",
    "contract_currency_gbp",
    "procurement_exercise_name"
FROM "dbt-ukraine-ebrd-contract-notices--ukraine-ebrd-contract-notices-pdg"
