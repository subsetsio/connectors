-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "species_id",
    "common_name",
    "genus",
    "genus_id",
    "genus_common_name",
    "species",
    "kingdom",
    "itis_taxonomic_sn",
    "functional_type",
    "class_id",
    "class_common_name",
    "class_name",
    "order_id",
    "order_common_name",
    "order_name",
    "family_id",
    "family_name",
    "family_common_name",
    "species_type"
FROM "usa-npn-species"
