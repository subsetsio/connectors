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
    "2010 2009 2008" AS 2010_2009_2008,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Institution" AS institution,
    "Purpose" AS purpose,
    "City" AS city,
    "State" AS state,
    "Amount" AS amount,
    "House Sponsors" AS house_sponsors,
    "Senate Sponsors" AS senate_sponsors,
    "Project" AS project,
    "House sponsor" AS house_sponsor,
    "Senate sponsor" AS senate_sponsor,
    "Name of Institution" AS name_of_institution,
    "Goal" AS goal,
    "Congressional Sponsor" AS congressional_sponsor,
    "Final Amount" AS final_amount
FROM "u-s-department-of-education-awards-ope-directed-grants-f62a9"
