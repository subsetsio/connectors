-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_com",
    "apl_ehpa",
    "apl_ra",
    "apl_sapa"
FROM "drees-accessibilite-potentielle-localisee-apl-aux-structures-medico-sociales-destinees"
