-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "24hr_psi",
    "north",
    "south",
    "east",
    "west",
    "central"
FROM "sg-data-d-b4cf557f8750260d229c49fd768e11ed"
