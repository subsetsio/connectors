-- NIH RePORTER ExPORTER PATENT: patents acknowledging NIH support, linked to the
-- funding project. One row per (PATENT_ID, PROJECT_ID) association — a patent may
-- cite support from more than one project. Raw is stringly-typed NDJSON from a
-- single all-years file. PATENT_ID stays VARCHAR (USPTO numbers may carry a
-- letter prefix, e.g. reissue "RE.." / design "D.."). No temporal axis (the
-- export carries no grant/issue year).
SELECT
    PATENT_ID       AS patent_id,
    PATENT_TITLE    AS patent_title,
    PROJECT_ID      AS project_id,
    PATENT_ORG_NAME AS patent_org_name
FROM "nih-patent"
WHERE PATENT_ID IS NOT NULL
  AND PROJECT_ID IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY PATENT_ID, PROJECT_ID
    ORDER BY PATENT_TITLE DESC NULLS LAST
) = 1
