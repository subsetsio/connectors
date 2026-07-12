-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Provision type" AS provision_type,
    "Level" AS level,
    "Sector subject area" AS sector_subject_area,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-d71e3dfe-dc62-4c4c-b735-2fdebb1e595e"
