-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "bin",
    "zipcode",
    "pre_type",
    "post_type",
    "objectid",
    "address_point_id",
    "complex_id",
    "house_number",
    "house_number_suffix",
    "hyphen_type",
    "sos_indicator",
    "special_condition",
    "address_source",
    "address_status",
    "validation",
    "borough_code",
    "collection_method",
    "created_date",
    "modified_date",
    "b7sc_actual",
    "b7sc_vanity",
    "a4id",
    "street_name",
    "house_number_range",
    "house_number_range_suffix",
    "premodifier",
    "predirectional",
    "post_directional",
    "post_modifier",
    "full_street_name"
FROM "nyc-open-data-uf93-f8nk"
