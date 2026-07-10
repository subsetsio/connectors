-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("zeit" AS BIGINT) AS zeit,
    "hauptaggregate_der_vgr",
    "nominell_in_mio_eur",
    "verkettete_volumenindizes"
FROM "statistics-austria-ogd-vgr101-vgrjahresr-2"
