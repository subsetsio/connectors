-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "other_organics_tons_collected_dsny",
    "other_organics_tons_collected_nondsny",
    "other_organics_total_tons_collected_dsny_nondsny"
FROM "nyc-open-data-6yag-pnij"
