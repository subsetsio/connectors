-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The verified row identity includes the marginal cost value because duplicate timestamps and subsystems can occur without another exposed discriminator.
SELECT
    "id_subsistema",
    "nom_subsistema",
    "din_instante",
    CAST("val_cmo" AS DOUBLE) AS val_cmo
FROM "ons-brazil-cmo-semi-horario"
