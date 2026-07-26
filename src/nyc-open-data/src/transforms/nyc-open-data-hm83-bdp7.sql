-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dftaid",
    "provider_name",
    "service_date",
    "total_daily",
    "breakfast_units",
    "lunch_units",
    "dinner_units",
    "tot_meals",
    "aib_tot",
    "sce_tot",
    "hpp_tot",
    "tot_serv_pp"
FROM "nyc-open-data-hm83-bdp7"
