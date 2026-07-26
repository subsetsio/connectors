-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "description",
    "client_agency",
    "division",
    "phase",
    "projected_construction_completion",
    "_scope" AS scope,
    "dollar_amount",
    "status"
FROM "nyc-open-data-rukc-mmqu"
