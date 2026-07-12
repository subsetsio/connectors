-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population",
    "consumption_of_ozone_depletion_metric_tons_according_to_montreal_protocol",
    "consumption_of_ozone_depleting_substances_per_person_kg"
FROM "qatar-planning-and-statistics-authority-consumption-of-ozone-depleting-substances-per-person-kg"
