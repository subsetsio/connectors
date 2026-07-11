-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "workflow_id",
    "name",
    "workflow_group_name",
    "system",
    "gna_year",
    CAST("workflow_date" AS TIMESTAMP) AS workflow_date,
    CAST("gna_from_date" AS TIMESTAMP) AS gna_from_date,
    CAST("gna_to_date" AS TIMESTAMP) AS gna_to_date,
    CAST("flag_methodology_approved" AS TIMESTAMP) AS flag_methodology_approved,
    CAST("flag_data_saved" AS TIMESTAMP) AS flag_data_saved,
    CAST("flag_gna_published" AS TIMESTAMP) AS flag_gna_published,
    "author",
    "comments",
    "workflow_compare_id",
    "version",
    "geometry_filename",
    "use_prediction",
    "methodology_id",
    "methodology_description",
    "category_info",
    "model_type",
    "iso3",
    "new_workflow_group_name",
    "new_system_name",
    "is_reference",
    "score_family"
FROM "inform-workflows"
