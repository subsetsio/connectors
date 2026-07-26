-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_site",
    "sample_date",
    "ph_unit",
    "alkalinity_mgl_caco3",
    "calcium_mgl",
    "specific_conductance_scm",
    "temperature_f",
    "orthophosphate_mgl",
    "lead_gl",
    "copper_mgl"
FROM "nyc-open-data-aa5e-digs"
