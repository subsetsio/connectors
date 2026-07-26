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
    "row_number",
    "conformsTo" AS conformsto,
    "describedBy" AS describedby,
    "@context" AS context,
    "@type" AS type,
    "@id" AS id,
    "title",
    "description",
    "dataset",
    "modified"
FROM "u-s-department-of-education-ed-enterprise-data-inventory-edi-f8f97"
