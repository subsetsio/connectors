-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "projectid",
    "projtitle",
    "fmsid",
    "fmsagencyid",
    "leadagency",
    "managing_agency",
    "projectdescription",
    "projecttypecode",
    "projecttype",
    "projectstatus",
    "constructionfy",
    "designstartdate",
    "constructionenddate",
    "currentfunding",
    "projectcost",
    "oversallscope",
    "otherscope",
    "projectjustification",
    "onstreetname",
    "fromstreetname",
    "tostreetname",
    "boroughname",
    "oftcode",
    "locationgeometrystlength",
    "designfy",
    "safetyscope"
FROM "nyc-open-data-jvk9-k4re"
