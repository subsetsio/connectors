-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: An aggregate cross-tab, not a project list: one row per destination country by project status, with investment already summed. It carries no time dimension, so it is a snapshot as of the last refresh and cannot be used for trends. Project statuses partition the projects, so summing across statuses gives the country total.
SELECT
    "category",
    "series",
    "value"
FROM "bruegel-european-clean-tech-tracker"
