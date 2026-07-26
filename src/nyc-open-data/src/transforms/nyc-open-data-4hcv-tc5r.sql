-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "trackerid",
    "fmsid",
    "title",
    "summary",
    "currentphase",
    "designpercentcomplete",
    "procurementpercentcomplete",
    "constructionpercentcomplete",
    "designstart",
    "designprojectedcompletion",
    "designadjustedcompletion",
    "designactualcompletion",
    "procurementstart",
    "procurementprojectedcompletion",
    "procurementadjustedcompletion",
    "procurementactualcompletion",
    "constructionstart",
    "constructionprojectedcompletion",
    "constructionadjustedcompletion",
    "constructionactualcompletion",
    "totalfunding",
    "projectliaison",
    "lastupdated",
    "fundingsource",
    "_name" AS name,
    "parkid",
    "latitude",
    "longitude",
    "borough"
FROM "nyc-open-data-4hcv-tc5r"
