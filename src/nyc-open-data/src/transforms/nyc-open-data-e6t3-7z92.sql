-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "sth_removals",
    "sth_principal",
    "sth_superintendent",
    "sth_expulsions",
    "nonsth_removals",
    "nonsth_principal",
    "nonsth_superintendent",
    "nonsth_expulsions",
    "sy1617_total_removalssuspensions"
FROM "nyc-open-data-e6t3-7z92"
