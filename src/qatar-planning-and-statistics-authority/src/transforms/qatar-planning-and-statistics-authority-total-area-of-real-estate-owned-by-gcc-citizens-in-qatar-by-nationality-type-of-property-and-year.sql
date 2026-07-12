-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ljnsy",
    "nationality",
    "nw_l_qr",
    "type_of_property",
    "value"
FROM "qatar-planning-and-statistics-authority-total-area-of-real-estate-owned-by-gcc-citizens-in-qatar-by-nationality-type-of-property-and-year"
