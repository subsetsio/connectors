-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "identifier_uri",
    "identifier_uuid",
    "title",
    "alternative",
    "digital_publisher",
    "is_version_of",
    "description",
    "abstract",
    "subject_lcsh",
    "subject_singheritage",
    "language",
    "ispartof_collection",
    "nlb_type",
    "rights",
    "access_rights"
FROM "sg-data-d-ec5e08ce1e8bfe7a2f016ecc250d085a"
