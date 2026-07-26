-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "block",
    "lot",
    "building_class",
    "tax_class",
    "building_count",
    "dof_gross_square_footage",
    "address",
    "boroughname",
    "bbl",
    "energy_star_score",
    "letterscore"
FROM "nyc-open-data-355w-xvp2"
