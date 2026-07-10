-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "county",
    "resPenetrationRateSfha" AS respenetrationratesfha,
    "resPenetrationRate" AS respenetrationrate,
    "resContractsInForce" AS rescontractsinforce,
    "resContractsInForceSfha" AS rescontractsinforcesfha,
    "totalResStructuresSfha" AS totalresstructuressfha,
    "totalResStructures" AS totalresstructures,
    "fipsCode" AS fipscode,
    "asOfDate" AS asofdate,
    "id"
FROM "fema-nfipresidentialpenetrationrates"
