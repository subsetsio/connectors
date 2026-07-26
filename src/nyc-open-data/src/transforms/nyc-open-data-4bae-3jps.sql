-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "physicalid",
    "objectid",
    "stname_lab",
    "boroughcod",
    "segmentlen",
    "b5sc",
    "bphys_id",
    "plntseas"
FROM "nyc-open-data-4bae-3jps"
