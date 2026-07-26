-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "material",
    "aggregate_percent",
    "refuse_percent",
    "mgp_percent",
    "paper_percent",
    "organic_percent",
    "material_group",
    "dsny_diversion_summary_category",
    "_location" AS location
FROM "nyc-open-data-k3ks-jzek"
