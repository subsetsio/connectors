-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe funding requests by component, allocation period, and status; compare requests within the same component and period.
SELECT
    "submissionDate" AS submissiondate,
    "window",
    "reviewApproach" AS reviewapproach,
    "reviewDate" AS reviewdate,
    "reviewOutcome" AS reviewoutcome,
    "differentiationCategory" AS differentiationcategory,
    "geographyId" AS geographyid,
    "id",
    "code",
    "name",
    "title",
    "description",
    "statusId" AS statusid,
    "periodStartDate" AS periodstartdate,
    "periodEndDate" AS periodenddate,
    CAST("periodFrom" AS BIGINT) AS periodfrom,
    CAST("periodTo" AS BIGINT) AS periodto,
    "iatI_ActivityIdentifier" AS iati_activityidentifier,
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated
FROM "global-fund-fundingrequests"
