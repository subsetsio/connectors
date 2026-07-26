-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "project_id",
    "bbl",
    "validated_borough",
    "validated_block",
    "validated_lot",
    "validated",
    "validated_date",
    "unverified_borough",
    "unverified_block",
    "unverified_lot"
FROM "nyc-open-data-2iga-a6mk"
