-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State outlying area and institution" AS state_outlying_area_and_institution,
    "All agencies" AS all_agencies,
    "AID" AS aid,
    "ARC" AS arc,
    "DHS" AS dhs,
    "DOC" AS doc,
    "DODa - Total" AS doda_total,
    "DODa - Research" AS doda_research,
    "DODa - Development - Advanced technology" AS doda_development_advanced_technology,
    "DODa - Development - Major systems" AS doda_development_major_systems,
    "DOE - Development - Major systems" AS doe_development_major_systems,
    "DOI - Development - Major systems" AS doi_development_major_systems
FROM "ncses-nsf25339-tab014"
