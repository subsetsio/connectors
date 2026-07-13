-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("noticeid" AS BIGINT) AS noticeid,
    "type",
    "countryname",
    "projectnumber",
    "proyecturl",
    "loannumber",
    "noticetitle",
    "ezshareid",
    "documenturl",
    "projectname",
    CAST("publicationyear" AS BIGINT) AS publicationyear,
    CAST("publicationdate" AS TIMESTAMP) AS publicationdate,
    strptime("deadline", '%Y-%m-%d')::DATE AS deadline,
    "sector",
    "sectorenglnm",
    "projectstatus",
    "procurement_id",
    "process_id",
    "category_nm",
    "prcrmnt_mthd_engl_nm",
    "process_nm",
    "process_desc",
    "source_resource"
FROM "idb-project-procurement-bidding-notices-and-notification-of-contract-awards"
