-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Pais" AS pais,
    CAST("IdPilar" AS BIGINT) AS idpilar,
    "TituloPilar" AS titulopilar,
    CAST("IdComponente" AS BIGINT) AS idcomponente,
    "TituloComponente" AS titulocomponente,
    CAST("IdIndicador" AS BIGINT) AS idindicador,
    "TituloIndicador" AS tituloindicador,
    CAST("IdRequisito" AS BIGINT) AS idrequisito,
    "TituloRequisito" AS titulorequisito,
    "RespuestaRequisito" AS respuestarequisito,
    CAST("Porcentaje" AS DOUBLE) AS porcentaje,
    CAST("Dias" AS BIGINT) AS dias,
    CAST("Promedio" AS DOUBLE) AS promedio,
    "TituloSector" AS titulosector,
    CAST("Ano_Texto" AS BIGINT) AS ano_texto,
    CAST("Ano_FechayHora" AS BIGINT) AS ano_fechayhora,
    "ID_PaisRequisito" AS id_paisrequisito,
    "source_resource"
FROM "idb-managing-for-development-results-mfdr-indicators-database-2013"
