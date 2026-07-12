-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is keyed by source program table, not by program id; one monitoring program can contribute multiple source tables.
SELECT
    "programid",
    "programname",
    "programtableid",
    "programtable",
    "programtype",
    "fundingsource",
    "fundingsourcename",
    "labtype",
    "metadataid",
    "programlink",
    "programstatus",
    "dataprovider",
    "sourceid",
    "sourcename",
    "organization",
    "sourcedescription",
    "beg_year",
    "end_year",
    "variable_list",
    "lakecount"
FROM "lagos-ne-data-source-and-program-information"
