-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "totalflyer",
    "date",
    "long",
    "lat",
    "x",
    "y"
FROM "nyc-open-data-j62s-m9yf"
