-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Agency" AS agency,
    "Total" AS total,
    "Astronomy" AS astronomy,
    "Chemistry" AS chemistry,
    "Physics" AS physics,
    "Other physical sciences" AS other_physical_sciences
FROM "ncses-nsf21329-tab048"
