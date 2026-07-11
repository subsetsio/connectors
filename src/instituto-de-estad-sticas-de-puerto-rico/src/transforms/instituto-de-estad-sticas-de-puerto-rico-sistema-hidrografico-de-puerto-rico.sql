-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("OBJECTID" AS BIGINT) AS objectid,
    "Permanent_" AS permanent,
    strptime("FDate", '%Y%m%d')::DATE AS fdate,
    CAST("StreamLeve" AS BIGINT) AS streamleve,
    CAST("StreamOrde" AS BIGINT) AS streamorde,
    CAST("FromNode" AS DOUBLE) AS fromnode,
    CAST("ToNode" AS DOUBLE) AS tonode,
    CAST("HydroSeq" AS DOUBLE) AS hydroseq,
    CAST("LevelPathI" AS DOUBLE) AS levelpathi,
    CAST("PathLength" AS DOUBLE) AS pathlength,
    CAST("TerminalPa" AS DOUBLE) AS terminalpa,
    CAST("ArbolateSu" AS DOUBLE) AS arbolatesu,
    CAST("Divergence" AS BIGINT) AS divergence,
    CAST("StartFlag" AS BIGINT) AS startflag,
    CAST("TerminalFl" AS BIGINT) AS terminalfl,
    CAST("DnLevel" AS BIGINT) AS dnlevel,
    CAST("ThinnerCod" AS BIGINT) AS thinnercod,
    CAST("UpLevelPat" AS DOUBLE) AS uplevelpat,
    CAST("UpHydroSeq" AS DOUBLE) AS uphydroseq,
    CAST("UpMinHydro" AS DOUBLE) AS upminhydro,
    CAST("DnLevelPat" AS DOUBLE) AS dnlevelpat,
    CAST("DnMinHydro" AS DOUBLE) AS dnminhydro,
    CAST("DnDrainCou" AS BIGINT) AS dndraincou
FROM "instituto-de-estad-sticas-de-puerto-rico-sistema-hidrografico-de-puerto-rico"
