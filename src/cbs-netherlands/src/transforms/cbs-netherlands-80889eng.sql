-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Regions" AS regions,
    "Periods" AS periods,
    "RateSurchargeMotorVehicleTax_1" AS ratesurchargemotorvehicletax_1,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80889eng"
