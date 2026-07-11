-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "unique_id",
    "industrial_instrument",
    "ref_area",
    "activity",
    "unit_measure",
    "instrument_type",
    "rd",
    "capital",
    "fixed_capital",
    "financial_other_capital",
    "labour",
    "labour_costs",
    "skills_training",
    "energy_cost",
    "intermediate_inputs",
    "output_based",
    "sectoral",
    "sme",
    "other_firms",
    "clusters",
    "regional",
    "twin",
    "green",
    "digital",
    "tech_focused",
    "natural_disaster",
    "export_finance",
    "covid_support",
    "eu_support",
    "unit_mult",
    "instrument_original",
    "time_period",
    "value"
FROM "oecd-oecd.sti.pie:dsd-industrial-policy@df-grantax"
