-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each measure identifies one station-parameter-period-statistic stream; observed values and units are interpreted through the measure metadata.
SELECT
    "measure_id",
    "name",
    "parameter",
    "parameter_name",
    "period",
    "period_name",
    "value_type",
    "value_statistic",
    "observation_type",
    "observed_property",
    "observed_property_label",
    "station_guid",
    "station_label",
    "unit",
    "unit_name"
FROM "environment-agency-measures"
