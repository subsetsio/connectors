-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "coal_terminal_name",
    "coal_terminal_name_detail_or_other",
    "parent_port_name",
    "wiki_url",
    "status",
    "project_type",
    "owner",
    "capacity_mt",
    "product_type",
    "terminal_type",
    "start_year",
    "retired_year",
    "location",
    "state_province",
    "country_area",
    "subregion",
    "region",
    "latitude",
    "longitude",
    "location_accuracy",
    "coal_source",
    "gem_terminal_id",
    "gem_unit_phase_id",
    "col_23"
FROM "gem-global-energy-monitor-coal-terminal-tracker"
