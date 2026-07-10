-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ano",
    "causa_obito",
    "homicidios",
    "prop_homicidios_total"
FROM "base-dos-dados-br-ggb-relatorio-lgbtqi--causa-obito"
