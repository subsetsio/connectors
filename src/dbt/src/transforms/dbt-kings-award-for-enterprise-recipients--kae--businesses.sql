-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "company_name",
    "post_town",
    "county",
    CAST("year_of_award" AS BIGINT) AS year_of_award,
    "award_won",
    "product_trade",
    "address",
    "post_code",
    "expiry",
    "country",
    "region",
    "notes",
    "qa_ka_ref",
    "innovation_type",
    "innovation_description",
    "casesummaryoverallgrade",
    "overallstatus",
    "siccode",
    "employees",
    "governmentsupport",
    "companyregno",
    "address2",
    "unitwebsite",
    "immediateparentname",
    "immediateparentcountry",
    "organisationwithultimatecontrol",
    "organisationwithultimatecontrolcountry",
    "finalyearoverseassales",
    "finalyeartotalsales",
    "currentqueensawardholder",
    "datestartedtrading",
    "exportmarkets"
FROM "dbt-kings-award-for-enterprise-recipients--kae--businesses"
