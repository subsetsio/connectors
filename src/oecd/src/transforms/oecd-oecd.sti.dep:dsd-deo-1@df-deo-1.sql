-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "measure",
    "dimensions",
    "theme",
    "type",
    "nds_link",
    "name",
    "description",
    "start_date",
    "end_date",
    "domains",
    "resp_development",
    "resp_implementation",
    "resp_monitoring",
    "budget",
    "budget_amount",
    "budget_currency",
    "budget_timeframe",
    "budget_timeframe_years",
    "target_population",
    "target_population_size",
    "source",
    "market_openness",
    "trust",
    "society",
    "jobs",
    "innovation",
    "use",
    "access",
    "response_id",
    "time_period",
    "value"
FROM "oecd-oecd.sti.dep:dsd-deo-1@df-deo-1"
