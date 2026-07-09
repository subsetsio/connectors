-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Capital measures are split by asset type in separate columns; compare or aggregate only after selecting compatible variables and units.
SELECT
    "countrycode",
    "year",
    "Ic_Struc" AS ic_struc,
    "Ic_Mach" AS ic_mach,
    "Ic_TraEq" AS ic_traeq,
    "Ic_Other" AS ic_other,
    "Ip_Struc" AS ip_struc,
    "Ip_Mach" AS ip_mach,
    "Ip_TraEq" AS ip_traeq,
    "Ip_Other" AS ip_other,
    "Nc_Struc" AS nc_struc,
    "Nc_Mach" AS nc_mach,
    "Nc_TraEq" AS nc_traeq,
    "Nc_Other" AS nc_other,
    "Np_Struc" AS np_struc,
    "Np_Mach" AS np_mach,
    "Np_TraEq" AS np_traeq,
    "Np_Other" AS np_other,
    "Dc_Struc" AS dc_struc,
    "Dc_Mach" AS dc_mach,
    "Dc_TraEq" AS dc_traeq,
    "Dc_Other" AS dc_other,
    "Kc_Struc" AS kc_struc,
    "Kc_Mach" AS kc_mach,
    "Kc_TraEq" AS kc_traeq,
    "Kc_Other" AS kc_other,
    "Kp_Struc" AS kp_struc,
    "Kp_Mach" AS kp_mach,
    "Kp_TraEq" AS kp_traeq,
    "Kp_Other" AS kp_other,
    "Ksh_Struc" AS ksh_struc,
    "Ksh_Mach" AS ksh_mach,
    "Ksh_TraEq" AS ksh_traeq,
    "Ksh_Other" AS ksh_other
FROM "penn-world-table-capital-detail"
