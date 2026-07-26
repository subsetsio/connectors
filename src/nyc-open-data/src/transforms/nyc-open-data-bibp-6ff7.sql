-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "material_group",
    "comparative_category",
    "dsny_diversion_summary_category",
    "aggregate_percent",
    "refuse_percent",
    "mgp_metal_glass_plastic_percent",
    "paper_percent",
    "organics_percent",
    "generator_residential_schools_nycha"
FROM "nyc-open-data-bibp-6ff7"
