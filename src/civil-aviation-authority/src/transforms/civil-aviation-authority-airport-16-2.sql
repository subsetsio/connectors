-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "span",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "yr01",
    "yr02",
    "yr03",
    "yr04",
    "yr05",
    "yr06",
    "yr07",
    "yr08",
    "yr09",
    "yr10",
    "yr11",
    "pc_change",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-16-2"
