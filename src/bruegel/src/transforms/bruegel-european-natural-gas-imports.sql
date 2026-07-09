-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Source mixes an aggregate, supplying countries, and individual pipeline routes that are subsets of those countries. EU total is the aggregate, Russia overlaps route rows, and LNG is a delivery mode rather than an origin. Summing over source double counts. Flows are GWh per day.
SELECT
    "date",
    "source",
    "flow_gwh_d"
FROM "bruegel-european-natural-gas-imports"
