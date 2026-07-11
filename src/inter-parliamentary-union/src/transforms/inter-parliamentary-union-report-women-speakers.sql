-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report lists only chambers currently headed by a woman speaker; absent chambers should not be interpreted as missing source data.
SELECT
    "country_code",
    "country_name",
    "region",
    "structure_of_parliament",
    "chamber_name",
    "struct_parl_status",
    "is_suspended_chamber",
    "chamber_code",
    "first_name",
    "family_name",
    "sex",
    "year_of_birth",
    "official_title",
    "date_of_appointment",
    "end_of_appointment",
    "is_vacant"
FROM "inter-parliamentary-union-report-women-speakers"
