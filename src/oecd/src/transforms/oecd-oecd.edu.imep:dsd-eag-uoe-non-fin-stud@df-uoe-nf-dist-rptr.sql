-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "education_lev",
    "measure",
    "education_type",
    "intensity",
    "education_field",
    "grade",
    "freq",
    "origin",
    "destination",
    "inst_type_edu",
    "mobility",
    "unit_measure",
    "sex",
    "age",
    "ref_year_ages",
    "origin_criterion",
    "repyearstart",
    "repyearend",
    "obs_status",
    "conf_status",
    "comment_obs",
    "decimals",
    "time_per_collect",
    "unit_mult",
    "time_period",
    "value"
FROM "oecd-oecd.edu.imep:dsd-eag-uoe-non-fin-stud@df-uoe-nf-dist-rptr"
