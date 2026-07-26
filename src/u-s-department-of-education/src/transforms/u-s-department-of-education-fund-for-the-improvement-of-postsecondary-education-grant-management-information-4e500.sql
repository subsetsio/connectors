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
    "sheet_name",
    "row_number",
    "Links to National and State Award Programs" AS links_to_national_and_state_award_programs,
    "Unnamed: 1" AS unnamed_1
FROM "u-s-department-of-education-fund-for-the-improvement-of-postsecondary-education-grant-management-information-4e500"
