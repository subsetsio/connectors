-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("date_last_researched", '%Y/%m/%d')::DATE AS date_last_researched,
    "country_area",
    "project_name",
    "phase_name",
    "project_name_in_local_language_script",
    "other_name_s",
    "capacity_mw",
    "installation_type",
    "status",
    "start_year",
    "retired_year",
    "operator",
    "operator_name_in_local_language_script",
    "owner",
    "owner_name_in_local_language_script",
    CAST("hydrogen" AS BOOLEAN) AS hydrogen,
    CAST("associated_storage" AS BOOLEAN) AS associated_storage,
    "latitude",
    "longitude",
    "location_accuracy",
    "city",
    "local_area_taluk_county",
    "major_area_prefecture_district",
    "state_province",
    "subregion",
    "region",
    "gem_location_id",
    "gem_phase_id",
    "other_ids_location",
    "other_ids_unit_phase",
    "wiki_url"
FROM "gem-global-energy-monitor-wind-power-tracker"
