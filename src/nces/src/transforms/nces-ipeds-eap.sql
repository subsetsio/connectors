-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Early EAP vintages include repeated institution-year rows where the later category fields are blank, so this raw component has no stable row key across the full historical union.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    "EAPCAT" AS eapcat,
    "OCCUPCAT" AS occupcat,
    "FACSTAT" AS facstat,
    "XEAPTOT" AS xeaptot,
    "EAPTOT" AS eaptot,
    "XEAPTYP" AS xeaptyp,
    "EAPTYP" AS eaptyp,
    "XEAPMED" AS xeapmed,
    "EAPMED" AS eapmed,
    "XEAPFT" AS xeapft,
    "EAPFT" AS eapft,
    "XEAPFTTY" AS xeapftty,
    "EAPFTTYP" AS eapfttyp,
    "XEAPFTMD" AS xeapftmd,
    "EAPFTMED" AS eapftmed,
    "XEAPPT" AS xeappt,
    "EAPPT" AS eappt,
    "XEAPPTTY" AS xeapptty,
    "EAPPTTYP" AS eappttyp,
    "XEAPPTMD" AS xeapptmd,
    "EAPPTMED" AS eapptmed,
    "year"
FROM "nces-ipeds-eap"
