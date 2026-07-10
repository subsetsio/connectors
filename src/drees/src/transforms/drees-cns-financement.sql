-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No clean row key: (annee, poste_code, fin_code) has a small number of duplicate rows in the source export — treat as keyless and de-duplicate before aggregating.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "poste_niveau",
    "poste_code",
    "poste_lib",
    "fin_niveau",
    "fin_code",
    "fin_lib",
    "montants"
FROM "drees-cns-financement"
