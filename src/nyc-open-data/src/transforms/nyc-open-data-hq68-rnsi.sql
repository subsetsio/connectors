-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "project_name",
    "program_group",
    "project_start_date",
    "project_completion_date",
    "extended_affordability_only",
    "prevailing_wage_status",
    "planned_tax_benefit",
    "extremely_low_income_units",
    "very_low_income_units",
    "low_income_units",
    "moderate_income_units",
    "middle_income_units",
    "other_income_units",
    "counted_rental_units",
    "counted_homeownership_units",
    "all_counted_units",
    "total_units",
    "senior_units"
FROM "nyc-open-data-hq68-rnsi"
