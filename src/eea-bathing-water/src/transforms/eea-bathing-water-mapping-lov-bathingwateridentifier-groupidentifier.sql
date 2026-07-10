-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Group identifiers are valid over season ranges; constrain joins by the reporting season to avoid assigning stale or future groups.
SELECT
    "bathingWaterIdentifier" AS bathingwateridentifier,
    "countryCode" AS countrycode,
    "fromSeason" AS fromseason,
    "groupIdentifier" AS groupidentifier,
    "toSeason" AS toseason
FROM "eea-bathing-water-mapping-lov-bathingwateridentifier-groupidentifier"
