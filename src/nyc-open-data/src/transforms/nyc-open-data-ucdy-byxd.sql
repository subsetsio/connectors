-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "projectdwid",
    "projectid",
    "projectname",
    "programgroup",
    "startdate",
    "projectedcompletiondate",
    "counted_rental_units",
    "counted_homeownership_units",
    "all_counted_units",
    "totalprojectunits",
    "commercialsquarefootage",
    "borrowerlegalentityname",
    "generalcontractorname",
    "isdavisbacon",
    "issection220nyslaborlaw"
FROM "nyc-open-data-ucdy-byxd"
