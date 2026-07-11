-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some chambers have multiple current secretary-general or clerk roles, and the source may emit duplicate vacancy rows; do not assume one row per chamber.
SELECT
    "country_code",
    "country_name",
    "region",
    "structure_of_parliament",
    "chamber_name",
    "chamber_code",
    "struct_parl_status",
    "is_suspended_chamber",
    "first_name",
    "family_name",
    "sex",
    "official_title",
    "date_of_appointment",
    "end_of_appointment",
    "is_vacant"
FROM "inter-parliamentary-union-report-secretaries-general"
