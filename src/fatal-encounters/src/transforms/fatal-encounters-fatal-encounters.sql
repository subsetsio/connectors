-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows represent people who died, not incidents; a single incident with multiple deaths can contribute multiple rows.
SELECT
    CAST("unique_id" AS BIGINT) AS unique_id,
    "name",
    "age",
    "gender",
    "race",
    "race_with_imputations",
    "imputation_probability",
    "image_url",
    strptime("date_of_death", '%Y-%m-%d')::DATE AS date_of_death,
    "location_address",
    "city",
    "state",
    "zip_code",
    "county",
    "full_address",
    "latitude",
    "longitude",
    "agency",
    "highest_level_of_force",
    "armed_unarmed",
    "alleged_weapon",
    "aggressive_physical_movement",
    "fleeing",
    "brief_description",
    "intended_use_of_force",
    "supporting_document_link"
FROM "fatal-encounters-fatal-encounters"
