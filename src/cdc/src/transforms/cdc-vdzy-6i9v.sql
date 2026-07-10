-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jurisdiction",
    strptime("weekEndingDate", '%Y-%m-%d')::DATE AS weekendingdate,
    CAST("totalConfC19NewAdm" AS BIGINT) AS totalconfc19newadm,
    CAST("totalConfFluNewAdm" AS BIGINT) AS totalconfflunewadm,
    CAST("totalConfRSVNewAdm" AS BIGINT) AS totalconfrsvnewadm,
    CAST("totalConfC19NewAdmPer100k" AS DOUBLE) AS totalconfc19newadmper100k,
    CAST("totalConfFluNewAdmPer100k" AS DOUBLE) AS totalconfflunewadmper100k,
    CAST("totalConfRSVNewAdmPer100k" AS DOUBLE) AS totalconfrsvnewadmper100k,
    "totalConfC19NewAdmPer100kLevel" AS totalconfc19newadmper100klevel,
    "totalConfFluNewAdmPer100kLevel" AS totalconfflunewadmper100klevel,
    "totalConfRSVNewAdmPer100kLevel" AS totalconfrsvnewadmper100klevel,
    CAST("totalConfC19NewAdmHospRep" AS BIGINT) AS totalconfc19newadmhosprep,
    CAST("totalConfFluNewAdmHospRep" AS BIGINT) AS totalconfflunewadmhosprep,
    CAST("totalConfRSVNewAdmHospRep" AS BIGINT) AS totalconfrsvnewadmhosprep,
    CAST("totalConfC19NewAdmPercHospRep" AS DOUBLE) AS totalconfc19newadmperchosprep,
    CAST("totalConfFluNewAdmPercHospRep" AS DOUBLE) AS totalconfflunewadmperchosprep,
    CAST("totalConfRSVNewAdmPercHospRep" AS DOUBLE) AS totalconfrsvnewadmperchosprep
FROM "cdc-vdzy-6i9v"
