-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Persoonskenmerken" AS persoonskenmerken,
    "GeboortelandOuders" AS geboortelandouders,
    "Herkomstland" AS herkomstland,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "BeroepsEnNietBeroepsbevolking_1" AS beroepsennietberoepsbevolking_1,
    "WerkzameBeroepsbevolking_2" AS werkzameberoepsbevolking_2,
    "NettoArbeidsparticipatie_3" AS nettoarbeidsparticipatie_3,
    "Werknemer_4" AS werknemer_4,
    "WerknemerMetVasteArbeidsrelatie_5" AS werknemermetvastearbeidsrelatie_5,
    "WerknemerMetFlexibeleArbeidsrelatie_6" AS werknemermetflexibelearbeidsrelatie_6,
    "Zelfstandige_7" AS zelfstandige_7,
    "ZelfstandigeZonderPersoneelZzp_8" AS zelfstandigezonderpersoneelzzp_8,
    "ZelfstMetPersoneelEnMeewGezinslid_9" AS zelfstmetpersoneelenmeewgezinslid_9,
    "Geslacht_label" AS geslacht_label,
    "Persoonskenmerken_label" AS persoonskenmerken_label,
    "GeboortelandOuders_label" AS geboortelandouders_label,
    "Herkomstland_label" AS herkomstland_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-86339ned"
