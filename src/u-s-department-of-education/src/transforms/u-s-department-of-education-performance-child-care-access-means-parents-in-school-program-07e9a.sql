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
    "Unnamed: 0" AS unnamed_0,
    "Unnamed: 1" AS unnamed_1,
    "Number of grants per category" AS number_of_grants_per_category,
    "Average numbers of parents served" AS average_numbers_of_parents_served,
    "Average numbers of children served" AS average_numbers_of_children_served,
    "Average persistence rate" AS average_persistence_rate,
    "Average graduation rate" AS average_graduation_rate,
    "Average federal cost per parent persisting or completing" AS average_federal_cost_per_parent_persisting_or_completing,
    "Average federal cost per parent served" AS average_federal_cost_per_parent_served,
    "Average funding" AS average_funding,
    "Grantee" AS grantee,
    "State" AS state,
    "Institution sector" AS institution_sector,
    "FY 2002-04 funding" AS fy_2002_04_funding,
    "Parents served" AS parents_served,
    "Children served" AS children_served,
    "Parents' persistence rate" AS parents_persistence_rate,
    "Parents' completion rate" AS parents_completion_rate,
    "Federal cost per parent persisting or completing" AS federal_cost_per_parent_persisting_or_completing,
    "Federal cost per parent served" AS federal_cost_per_parent_served
FROM "u-s-department-of-education-performance-child-care-access-means-parents-in-school-program-07e9a"
