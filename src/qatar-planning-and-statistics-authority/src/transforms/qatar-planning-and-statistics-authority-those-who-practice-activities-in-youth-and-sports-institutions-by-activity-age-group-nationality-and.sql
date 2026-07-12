-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnsht",
    "activity",
    "lfy_t_l_mry",
    "age_groups",
    "ljnsy",
    "nationality",
    "lnw",
    "gender",
    "value"
FROM "qatar-planning-and-statistics-authority-those-who-practice-activities-in-youth-and-sports-institutions-by-activity-age-group-nationality-and"
