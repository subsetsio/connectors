-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_page",
    "source_workbook",
    "source_url",
    "resolved_url",
    "release_year_start",
    "release_year_end",
    "fragment"
FROM "saps-crime-stats-releases"
