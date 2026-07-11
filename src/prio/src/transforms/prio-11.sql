-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Records describe petroleum sites or fields, not country totals; country-level analysis requires explicit aggregation over sites.
-- caution: The raw extract contains exact duplicate petroleum-site rows, so there is no source-stable row key.
SELECT
    "primkey",
    "country",
    "fipscode",
    "cowcode",
    "contcode",
    "sitenum",
    "name",
    "lat",
    "long",
    "res",
    "resinfo",
    "locsource",
    "fieldinfo",
    "disc",
    "discpres",
    "prod",
    "prodpres",
    "otherinfo",
    "sourceinfo",
    "version"
FROM "prio-11"
