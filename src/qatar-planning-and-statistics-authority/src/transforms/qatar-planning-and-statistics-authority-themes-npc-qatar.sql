-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "theme_english",
    "theme_arabic",
    "description_english",
    "lwsf_arabic"
FROM "qatar-planning-and-statistics-authority-themes-npc-qatar"
