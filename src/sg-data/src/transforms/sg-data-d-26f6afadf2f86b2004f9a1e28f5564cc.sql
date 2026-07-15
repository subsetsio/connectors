-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ave_speed_expressway",
    "ave_speed_arterial_roads"
FROM "sg-data-d-26f6afadf2f86b2004f9a1e28f5564cc"
