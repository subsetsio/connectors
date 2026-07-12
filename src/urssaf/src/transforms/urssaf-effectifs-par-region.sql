-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "code_ancienne_region",
    "ancienne_region",
    "code_nouvelle_region",
    "nouvelle_region",
    "effectifs_urssaf",
    "effectifs_urssaf_caisse_nationale",
    "date_unix"
FROM "urssaf-effectifs-par-region"
