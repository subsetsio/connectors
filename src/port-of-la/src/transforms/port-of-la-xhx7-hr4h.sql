SELECT
    grant_project_description,
    federal_cfda_number,
    grant_number_pass_through_grantor_s_number,
    TRY_CAST(federal_entitlement_amount AS DOUBLE) AS federal_entitlement_amount,
    TRY_CAST(grant_receivable_as_of_7_1_2012 AS DOUBLE) AS grant_receivable_as_of_7_1_2012,
    TRY_CAST(grant_receivable_prior_year_adjustment AS DOUBLE) AS grant_receivable_prior_year_adjustment,
    TRY_CAST(grant_revenue_received AS DOUBLE) AS grant_revenue_received,
    TRY_CAST(federal_grant_expenditures AS DOUBLE) AS federal_grant_expenditures,
    TRY_CAST(federal_grant_pass_through_liability AS DOUBLE) AS federal_grant_pass_through_liability,
    TRY_CAST(grant_receivable_as_of_6_30_2013 AS DOUBLE) AS grant_receivable_as_of_6_30_2013
FROM "port-of-la-xhx7-hr4h"
WHERE grant_project_description IS NOT NULL
