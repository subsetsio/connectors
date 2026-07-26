-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_category",
    "administrative_district",
    "sth_removals",
    "sth_principal",
    "sth_superintendent",
    "sth_expulsions",
    "nonsth_removals",
    "nonsth_principal",
    "nonsth_superintendent",
    "nonsth_expulsions"
FROM "nyc-open-data-q7r2-64fm"
