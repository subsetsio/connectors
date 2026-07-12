-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups",
    "relation_to_labour_force",
    "type_of_relation_to_labour_force",
    "fy_t_l_mr",
    "l_lq_bqw_l_ml",
    "nw_l_lq_bqw_l_ml",
    "value"
FROM "qatar-planning-and-statistics-authority-male-population-15-years-and-above-by-relation-to-labor-force-and-age-groups0"
