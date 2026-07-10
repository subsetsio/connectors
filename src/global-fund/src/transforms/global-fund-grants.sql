-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Grant rows include period and financial amount fields for signed grant agreements; avoid summing across statuses, periods, or recipient roles without filtering.
SELECT
    "geographyId" AS geographyid,
    "activityAreaId" AS activityareaid,
    "principalRecipientId" AS principalrecipientid,
    "leadImplementerId" AS leadimplementerid,
    "differentiationCategory" AS differentiationcategory,
    "fundPortfolioManagerId" AS fundportfoliomanagerid,
    "currency_ReferenceRate" AS currency_referencerate,
    "totalBoardApprovedAmount_ReferenceRate" AS totalboardapprovedamount_referencerate,
    "totalSignedAmount_ReferenceRate" AS totalsignedamount_referencerate,
    "totalCommitmentAmount_ReferenceRate" AS totalcommitmentamount_referencerate,
    "totalDisbursedAmount_ReferenceRate" AS totaldisbursedamount_referencerate,
    "id",
    "code",
    "name",
    "title",
    "description",
    "statusId" AS statusid,
    "periodStartDate" AS periodstartdate,
    "periodEndDate" AS periodenddate,
    "periodFrom" AS periodfrom,
    "periodTo" AS periodto,
    "iatI_ActivityIdentifier" AS iati_activityidentifier,
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated
FROM "global-fund-grants"
