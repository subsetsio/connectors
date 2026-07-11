-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Records describe diamond sites, not country totals; country-level analysis requires explicit aggregation over sites.
SELECT
    "primkey",
    "country",
    "fipscode",
    "cowcode",
    "contcode",
    "sitenum",
    "name",
    "namevar",
    "nameinfo",
    "lat",
    "long",
    "locder",
    "locsource",
    "landmark",
    "locinfo",
    "res",
    "resinfo",
    "diainfo",
    "mineinfo",
    "sizeinfo",
    "disc",
    "discpres",
    "prod",
    "prodpres",
    "dateinfo",
    "otherinfo",
    "sourceinfo",
    "version"
FROM "prio-10"
