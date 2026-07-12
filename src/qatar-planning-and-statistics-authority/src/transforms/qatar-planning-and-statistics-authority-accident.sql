-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "accident_year",
    "accident_time",
    "weather",
    "road_status",
    "road_type",
    "accident_classification",
    "accident_nature",
    "accident_reason",
    "city",
    "zone",
    "street",
    "accident_severity",
    "death_count",
    "birth_year_of_accident_perpetr",
    "nationality_group_of_accident",
    "total"
FROM "qatar-planning-and-statistics-authority-accident"
