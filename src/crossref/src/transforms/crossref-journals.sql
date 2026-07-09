-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Journal records do not expose a stable single-record identifier in the flattened Crossref response; rows should be treated as source title records rather than deduplicated journals.
SELECT
    "title",
    "issn",
    "publisher",
    "total_dois",
    "current_dois",
    "backfile_dois"
FROM "crossref-journals"
