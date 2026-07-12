-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source species code vocabulary includes alternate and taxonomy-version fields; use the taxonomy columns when comparing names across source versions.
SELECT
    "species_code",
    "alt_full_spp_code",
    "n_locations",
    "scientific_name",
    "american_english_name",
    "taxonomy_version",
    "taxonomic_sort_order"
FROM "feederwatch-species-translation"
