-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mass_of_consumption_of_ozone_depleting_substances",
    "ozone_depleting_potential_metric_tons_according_to_montreal_protocol",
    "global_warming_potential",
    "mass_of_consumption_of_ozone_depleting_substances_2",
    "ozone_depleting_potential_metric_tons_according_to_montreal_protocol_2",
    "global_warming_potential_2"
FROM "qatar-planning-and-statistics-authority-mass-of-consumption-of-ozone-depleting-substances-gwp-and-odp"
