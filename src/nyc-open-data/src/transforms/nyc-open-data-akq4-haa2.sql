-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "boro",
    "volume_number",
    "section_number",
    "eop_overlap_flag",
    "jagged_st_flag",
    "block"
FROM "nyc-open-data-akq4-haa2"
