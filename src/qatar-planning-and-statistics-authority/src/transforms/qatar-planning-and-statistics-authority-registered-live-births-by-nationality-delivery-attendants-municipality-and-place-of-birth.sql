-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "jnsy",
    "municipality",
    "lbldy",
    "place_of_delivery",
    "mkn_lwld",
    "delivery_attendent",
    "mdyf_ltslym",
    "total",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-nationality-delivery-attendants-municipality-and-place-of-birth"
