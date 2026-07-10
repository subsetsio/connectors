-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "Level_nr" AS level_nr,
    "Code" AS code,
    "Code_sup" AS code_sup,
    "Label_DE" AS label_de,
    "Label_EN" AS label_en,
    "Label_FR" AS label_fr,
    "Label_NL" AS label_nl
FROM "statbel-nodeid734"
