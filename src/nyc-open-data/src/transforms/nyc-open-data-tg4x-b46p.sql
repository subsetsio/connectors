-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "eventid",
    "eventtype",
    "startdatetime",
    "enddatetime",
    "enteredon",
    "eventagency",
    "parkingheld",
    "borough",
    "communityboards",
    "policeprecincts",
    "category",
    "subcategoryname",
    "country",
    "zipcodes"
FROM "nyc-open-data-tg4x-b46p"
