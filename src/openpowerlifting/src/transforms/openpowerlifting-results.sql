SELECT
    "Name"                                        AS name,
    "Sex"                                         AS sex,
    "Event"                                       AS event,
    "Equipment"                                   AS equipment,
    NULLIF("Place", '')                           AS place,
    NULLIF("Division", '')                        AS division,
    TRY_CAST("Age" AS DOUBLE)                     AS age,
    NULLIF("AgeClass", '')                        AS age_class,
    NULLIF("BirthYearClass", '')                  AS birth_year_class,
    TRY_CAST("BodyweightKg" AS DOUBLE)            AS bodyweight_kg,
    NULLIF("WeightClassKg", '')                   AS weight_class_kg,
    TRY_CAST("Best3SquatKg" AS DOUBLE)            AS best3_squat_kg,
    TRY_CAST("Best3BenchKg" AS DOUBLE)            AS best3_bench_kg,
    TRY_CAST("Best3DeadliftKg" AS DOUBLE)         AS best3_deadlift_kg,
    TRY_CAST("TotalKg" AS DOUBLE)                 AS total_kg,
    TRY_CAST("Dots" AS DOUBLE)                    AS dots,
    TRY_CAST("Wilks" AS DOUBLE)                   AS wilks,
    TRY_CAST("Glossbrenner" AS DOUBLE)            AS glossbrenner,
    TRY_CAST("Goodlift" AS DOUBLE)                AS goodlift,
    -- OPL sets Tested='Yes' only for drug-tested categories; blank
    -- means the lifter did NOT enter a tested category. Map blank to
    -- FALSE so this is a clean, fully-populated boolean.
    ("Tested" = 'Yes')                            AS tested,
    NULLIF("Country", '')                         AS country,
    NULLIF("State", '')                           AS state,
    "Federation"                                  AS federation,
    NULLIF("ParentFederation", '')                AS parent_federation,
    TRY_CAST("Date" AS DATE)                      AS date,
    "MeetCountry"                                 AS meet_country,
    NULLIF("MeetState", '')                       AS meet_state,
    NULLIF("MeetTown", '')                        AS meet_town,
    "MeetName"                                    AS meet_name
FROM "openpowerlifting-results"
