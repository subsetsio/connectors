-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objektart_verkehrsteilnahme",
    "mutmassliche_verantwortlichkeit_des_objekts",
    "geschlecht_fussgänger_in_bzw_fahrzeuglenker_in" AS geschlecht_fussg_nger_in_bzw_fahrzeuglenker_in,
    "altersklasse_fussgänger_in_bzw_fahrzeuglenker_in" AS altersklasse_fussg_nger_in_bzw_fahrzeuglenker_in,
    "jahre_seit_erteilung_des_führerausweises_an_fahrzeuglenker_in" AS jahre_seit_erteilung_des_f_hrerausweises_an_fahrzeuglenker_in,
    "unfallschwere",
    CAST("jahr" AS BIGINT) AS jahr,
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1106010100-105"
