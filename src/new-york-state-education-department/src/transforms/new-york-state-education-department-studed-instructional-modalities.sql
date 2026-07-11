-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Instructional modality measures are COVID-era reporting fields and may not represent a continuous annual series.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "remote",
    "per_remote",
    "in_person",
    "per_in_person",
    "both",
    "per_both",
    "tot_modalitites",
    "per_tot_modalitites",
    "data_reported"
FROM "new-york-state-education-department-studed-instructional-modalities"
