-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "ProtectingUnitID" AS protectingunitid,
    "ProtectingUnitID_sansUS" AS protectingunitid_sansus,
    "ProtectingUnitName" AS protectingunitname,
    "ProtectingUnitKind" AS protectingunitkind,
    "ProtectingUnitCategory" AS protectingunitcategory,
    "State" AS state,
    "Agreement" AS agreement,
    "AgreementDate" AS agreementdate,
    "Contact" AS contact,
    "Comments" AS comments,
    "DataSource" AS datasource,
    "SourceUniqueID" AS sourceuniqueid,
    "GISSourceDate" AS gissourcedate,
    "ImportDate" AS importdate,
    "RevisionDate" AS revisiondate,
    "GlobalID" AS globalid
FROM "nifc-c23e282aae534f798e6e231a2cfe584a-0"
