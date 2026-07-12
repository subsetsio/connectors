-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Nested advisory fields such as affected packages, ranges, references, severity, credits, and database-specific data are preserved as JSON strings.
SET arrow_large_buffer_size=true;
SELECT
    "id",
    "schema_version",
    "published",
    "modified",
    "withdrawn",
    "source_path",
    "source_ecosystem",
    "aliases",
    "related",
    "summary",
    "details",
    "severity",
    "affected",
    "references",
    "credits",
    "database_specific"
FROM "osv-vulnerabilities"
