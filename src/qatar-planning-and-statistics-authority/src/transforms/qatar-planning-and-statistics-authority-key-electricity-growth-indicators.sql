-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "electricity_generated_gwh",
    "change_generated",
    "electricity_sent_out_gwh",
    "change_sent_out",
    "max_demand_mw",
    "change_max_demand",
    "no_of_customers_meters",
    "change_customers"
FROM "qatar-planning-and-statistics-authority-key-electricity-growth-indicators"
