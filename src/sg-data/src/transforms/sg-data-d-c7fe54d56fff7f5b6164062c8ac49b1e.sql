-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "persons_moc_count"
FROM "sg-data-d-c7fe54d56fff7f5b6164062c8ac49b1e"
