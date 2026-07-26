-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "final_section_fs",
    "left_side",
    "top",
    "right_side",
    "bottom"
FROM "nyc-open-data-avcv-kcyf"
