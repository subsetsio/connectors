-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "NYC-3-1-1" AS nyc_3_1_1,
    "ACS" AS acs,
    "BPSI" AS bpsi,
    "CAU" AS cau,
    "CHALL" AS chall,
    "DEP" AS dep,
    "DOB" AS dob,
    "DOE" AS doe,
    "DOF" AS dof,
    "DOHMH" AS dohmh,
    "DPR" AS dpr,
    "FEMA" AS fema,
    "HPD" AS hpd,
    "HRA" AS hra,
    "MFANYC" AS mfanyc,
    "MOSE" AS mose,
    "NYCEM" AS nycem,
    "NYCHA" AS nycha,
    "NYCSERVICE" AS nycservice,
    "NYPD" AS nypd,
    "NYSDOL" AS nysdol,
    "SBS" AS sbs,
    "NYSEMERGENCYMG" AS nysemergencymg,
    "total"
FROM "fivethirtyeight-sandy-311-calls-sandy-311-calls-by-day"
