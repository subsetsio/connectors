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
    "family",
    "rpt_apt_grp_cd1",
    "prt_apt_grp_name",
    "Y1" AS y1,
    "Y2" AS y2,
    "Y3" AS y3,
    "Y4" AS y4,
    "Y5" AS y5,
    "Y6" AS y6,
    "Y7" AS y7,
    "Y8" AS y8,
    "Y9" AS y9,
    "Y10" AS y10,
    "Y11" AS y11
FROM "civil-aviation-authority-airport-10-3"
