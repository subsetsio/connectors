-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: NES rows are expert-rated national framework-condition indicators; do not aggregate different indicator variables as if they were one measure.
-- caution: Economy identifiers and ISO-style codes are source-supplied and may vary in availability across years; use economy_name with year and variable for row identity.
SELECT
    "year",
    "economy_code",
    "economy_name",
    "economy_iso",
    "indicator",
    "variable",
    "label",
    "value"
FROM "gem-entrepreneurship-nes-national"
