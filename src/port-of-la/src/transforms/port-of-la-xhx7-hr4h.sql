-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grant_project_description",
    CAST("federal_cfda_number" AS DOUBLE) AS federal_cfda_number,
    "grant_number_pass_through_grantor_s_number",
    CAST("federal_entitlement_amount" AS BIGINT) AS federal_entitlement_amount,
    "grant_receivable_as_of_7_1_2012",
    "grant_revenue_received",
    "federal_grant_expenditures",
    "grant_receivable_as_of_6_30_2013",
    "grant_receivable_prior_year_adjustment",
    "federal_grant_pass_through_liability"
FROM "port-of-la-xhx7-hr4h"
