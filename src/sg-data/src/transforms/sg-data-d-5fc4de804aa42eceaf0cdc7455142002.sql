-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "identifier_uri",
    "identifier_uuid",
    "title",
    "alternative",
    "creator",
    "creator_people",
    "creator_people_cn",
    "creator_orgs",
    "creator_orgs_cn",
    "creator_lcna",
    "contributor",
    "contributor_people",
    "contributor_people_cn",
    "contributor_orgs",
    "contributor_orgs_cn",
    "contributor_lcna",
    "digital_publisher",
    "original_publisher",
    "date_created",
    "has_part_uuid",
    "description",
    "abstract",
    "table_of_contents",
    "subject_lcsh",
    "subject_singheritage",
    "language",
    "ispartof_collection",
    "nlb_type",
    "rights",
    "access_rights"
FROM "sg-data-d-5fc4de804aa42eceaf0cdc7455142002"
