-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "gender",
    "lnw",
    "labour_force_status",
    "hl_lqw_l_ml",
    "count"
FROM "qatar-planning-and-statistics-authority-population-15-years-and-above-by-relation-to-labour-force-nationality-and-gender"
