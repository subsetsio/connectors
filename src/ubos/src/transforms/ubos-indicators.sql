-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Indicator metadata includes all indicators exposed by the Open SDG metadata endpoint; not every metadata indicator has observation rows in the values export.
SELECT
    "indicator_id",
    "indicator_name",
    "graph_title",
    "reporting_status",
    "sdg_goal",
    "sdg_target",
    "sdg_indicator",
    "unit_measure",
    "source_type",
    "meta_last_update",
    "copyright",
    "raw_metadata_json"
FROM "ubos-indicators"
