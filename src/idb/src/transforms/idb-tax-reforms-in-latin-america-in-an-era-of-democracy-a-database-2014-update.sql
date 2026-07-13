-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    CAST("year" AS BIGINT) AS year,
    CAST("TaxRefOverhaul" AS BIGINT) AS taxrefoverhaul,
    CAST("TaxRefMinorDuties" AS BIGINT) AS taxrefminorduties,
    CAST("TaxRefVATCreation" AS BIGINT) AS taxrefvatcreation,
    CAST("TaxRefVATExpansion" AS BIGINT) AS taxrefvatexpansion,
    CAST("TaxRefVATRate" AS BIGINT) AS taxrefvatrate,
    CAST("TaxRefPITBroad" AS BIGINT) AS taxrefpitbroad,
    CAST("TaxRefPITRate" AS BIGINT) AS taxrefpitrate,
    CAST("TaxRefCITBroad" AS BIGINT) AS taxrefcitbroad,
    CAST("TaxRefCITRate" AS BIGINT) AS taxrefcitrate,
    CAST("TaxRefAdmReform" AS BIGINT) AS taxrefadmreform,
    CAST("TaxRefFinancialTax" AS BIGINT) AS taxreffinancialtax,
    CAST("TaxRefExcise" AS BIGINT) AS taxrefexcise,
    CAST("TaxRefOtherTaxes" AS BIGINT) AS taxrefothertaxes,
    CAST("TaxRefIncentives" AS BIGINT) AS taxrefincentives,
    CAST("TaxRefSocialSecurity" AS BIGINT) AS taxrefsocialsecurity,
    "source_resource"
FROM "idb-tax-reforms-in-latin-america-in-an-era-of-democracy-a-database-2014-update"
