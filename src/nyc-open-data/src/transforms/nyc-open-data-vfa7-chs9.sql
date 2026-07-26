-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "accession_number",
    "accession_title",
    "accession_date",
    "container_summary",
    "extent",
    "linked_resources_identifier",
    "linked_resources_title"
FROM "nyc-open-data-vfa7-chs9"
