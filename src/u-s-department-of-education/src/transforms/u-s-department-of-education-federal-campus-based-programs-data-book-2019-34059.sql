-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "archive_member",
    "sheet_name",
    "row_number",
    "Unnamed: 0" AS unnamed_0,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10,
    "Unnamed: 11" AS unnamed_11,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13,
    "Distribution of Awards in the Campus-Based Programs Award Year 2017-18" AS distribution_of_awards_in_the_campus_based_programs_award_year_2017_18,
    "_subsets_record_type" AS subsets_record_type,
    "error"
FROM "u-s-department-of-education-federal-campus-based-programs-data-book-2019-34059"
