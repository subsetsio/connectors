-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the reference projection scenario and mixes historical observations with long-run projections.
SELECT
    "code_wb",
    "name",
    "year",
    "gdp",
    "gdp_cap",
    "gdp_crt",
    "capital",
    "labor_force",
    "energy_cons",
    "investment_rate",
    "savings_rate",
    "population",
    "secondary_educ",
    "tertiary_educ",
    "tfp",
    "energy_productivity"
FROM "cepii-econmap"
