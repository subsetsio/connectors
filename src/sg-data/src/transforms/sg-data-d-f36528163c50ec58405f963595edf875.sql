-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "tax_group",
    "no_of_companies_assessed",
    "total_income",
    "donations",
    "assessable_income",
    "ci_before_reliefs_exemption",
    "group_relief",
    "loss_carryback_relief",
    "tax_exemption",
    "ci",
    "gross_tax_payable",
    "tax_deducted_at_source",
    "other_tax_set_offs",
    "net_tax_assessed"
FROM "sg-data-d-f36528163c50ec58405f963595edf875"
