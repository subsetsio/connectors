-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "uuid",
    "title",
    "identifier",
    "publisher",
    "language",
    "format",
    "description",
    "date_issued",
    "date_modified",
    "date_valid",
    "audience",
    "coverage",
    "subject",
    "type",
    "license",
    "regulatory_topics",
    "status",
    "date_uploaded_to_orp",
    "has_format",
    "is_format_of",
    "has_version",
    "is_version_of",
    "references",
    "is_referenced_by",
    "has_part",
    "is_part_of",
    "is_replaced_by",
    "replaces",
    "related_legislation",
    "id",
    "related_legislation_dict"
FROM "dbt-uk-business-regulations--uk-legislation-pdg"
