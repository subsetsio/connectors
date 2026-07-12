-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "craft",
    "lhrf",
    "nationality",
    "ljnsy",
    "gender",
    "ljns",
    "number"
FROM "qatar-planning-and-statistics-authority-practitioners-of-the-character-popular-in-the-social-development-center-by-nationality-and-gender"
