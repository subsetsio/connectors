-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "item",
    "Title" AS title,
    "Authors" AS authors,
    "R1" AS r1,
    "R2" AS r2,
    "Confidence" AS confidence,
    "source_resource"
FROM "idb-informing-citizen-security-policy-an-evidence-gap-map-on-policing-interventions-dataset"
