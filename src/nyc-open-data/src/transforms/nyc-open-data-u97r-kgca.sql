-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city",
    "populaiton",
    "total_homicides",
    "total_domestic_violence_homicides",
    "total_intimate_partner_homicides",
    "rate_of_dv_homicides",
    "rate_of_ipv_homicides"
FROM "nyc-open-data-u97r-kgca"
