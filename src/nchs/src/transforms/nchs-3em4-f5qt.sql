-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "focus_area_code",
    "objective_code",
    "focusdesc",
    "objective_desc",
    "begyear",
    "endyear",
    "fipscode",
    "state",
    "population_group",
    "population",
    "estimate_num",
    "estimate_label",
    "stderr",
    "lowerci",
    "upperci",
    "period",
    "target",
    "lhi",
    "ageadj",
    "flag_no_target",
    "unit",
    "source",
    "footnote1",
    "footnote2",
    "footnote3"
FROM "nchs-3em4-f5qt"
