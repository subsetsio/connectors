-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current country ranking snapshot of women's parliamentary representation, not a historical series.
SELECT
    "country_name",
    "country_code",
    "region",
    "subregion",
    "lower_chamber_current_women_number",
    "lower_chamber_current_members_number",
    CAST("lower_chamber_percent_women" AS DOUBLE) AS lower_chamber_percent_women,
    "lower_is_suspended_chamber",
    "lower_data_missing",
    "upper_chamber_current_women_number",
    "upper_chamber_current_members_number",
    CAST("upper_chamber_percent_women" AS DOUBLE) AS upper_chamber_percent_women,
    "upper_is_suspended_chamber",
    "upper_data_missing",
    "rank"
FROM "inter-parliamentary-union-report-women-ranking"
