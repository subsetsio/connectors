-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "bundesland_nuts_2_einheit",
    "operating_surplus_mixed_income_b_2_b_3_net",
    "compensation_of_employees_d_1_received",
    "property_income_d_4_received",
    "property_income_d_4_paid",
    "primary_income_b_5n_net",
    "social_benefits_other_than_social_transfers_in_kind_d_62_received",
    "other_current_transfers_d_7_received",
    "current_taxes_on_income_wealth_etc_d_5_paid",
    "social_contributions_d_61_paid",
    "other_current_transfers_d_7_paid",
    "disposable_income_b_6n_net"
FROM "statistics-austria-ogd-vgrrgr202-rgr202-1"
