-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Counts are global daily aggregates of public GitHub events only; private repository activity and raw event payload details are intentionally not published.
-- caution: The table is a rolling recent window rather than full GH Archive history, so compare only dates present in the current published table.
SELECT
    "date",
    "event_type",
    "event_count"
FROM "gh-archive-github-events-daily"
