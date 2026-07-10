-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable unique row identifier: `identifier` is nearly unique but the source contains a small number of duplicate rows, so no key is declared. `id` is a low-cardinality source grouping code, not a row key.
SELECT
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
    "id"
FROM "dbt-uk-legislation-and-orp--uk-legislation-pdg"
