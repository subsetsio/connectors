-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("dot_number" AS BIGINT) AS dot_number,
    CAST("insp_total" AS BIGINT) AS insp_total,
    CAST("driver_insp_total" AS BIGINT) AS driver_insp_total,
    CAST("driver_oos_insp_total" AS BIGINT) AS driver_oos_insp_total,
    CAST("vehicle_insp_total" AS BIGINT) AS vehicle_insp_total,
    CAST("vehicle_oos_insp_total" AS BIGINT) AS vehicle_oos_insp_total,
    CAST("unsafe_driv_insp_w_viol" AS BIGINT) AS unsafe_driv_insp_w_viol,
    CAST("unsafe_driv_measure" AS DOUBLE) AS unsafe_driv_measure,
    "unsafe_driv_ac",
    CAST("hos_driv_insp_w_viol" AS BIGINT) AS hos_driv_insp_w_viol,
    "hos_driv_measure",
    "hos_driv_ac",
    CAST("driv_fit_insp_w_viol" AS BIGINT) AS driv_fit_insp_w_viol,
    CAST("driv_fit_measure" AS BIGINT) AS driv_fit_measure,
    "driv_fit_ac",
    CAST("contr_subst_insp_w_viol" AS BIGINT) AS contr_subst_insp_w_viol,
    CAST("contr_subst_measure" AS DOUBLE) AS contr_subst_measure,
    "contr_subst_ac",
    CAST("veh_maint_insp_w_viol" AS BIGINT) AS veh_maint_insp_w_viol,
    CAST("veh_maint_measure" AS BIGINT) AS veh_maint_measure,
    "veh_maint_ac"
FROM "u-s-department-of-transportation-h9zy-gjn8"
