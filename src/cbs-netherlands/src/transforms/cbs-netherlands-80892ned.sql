-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Waterschappen" AS waterschappen,
    "Perioden" AS perioden,
    "WatersysteemheffingIngezetenen_1" AS watersysteemheffingingezetenen_1,
    "WatersysteemheffingOngebouwd_2" AS watersysteemheffingongebouwd_2,
    "WatersysteemheffingNatuur_3" AS watersysteemheffingnatuur_3,
    "WatersysteemheffingGebouwd_4" AS watersysteemheffinggebouwd_4,
    "WatersysteemheffingWoningen_5" AS watersysteemheffingwoningen_5,
    "WatersysteemheffingNietWoningen_6" AS watersysteemheffingnietwoningen_6,
    "HeffingWegenbeheerIngezetenen_7" AS heffingwegenbeheeringezetenen_7,
    "HeffingWegenbeheerOngebouwd_8" AS heffingwegenbeheerongebouwd_8,
    "HeffingWegenbeheerNatuur_9" AS heffingwegenbeheernatuur_9,
    "HeffingWegenbeheerGebouwd_10" AS heffingwegenbeheergebouwd_10,
    "HeffingWegenbeheerWoningen_11" AS heffingwegenbeheerwoningen_11,
    "HeffingWegenbeheerNietWoningen_12" AS heffingwegenbeheernietwoningen_12,
    "NietTaakgebondenHeffingIngezetenen_13" AS niettaakgebondenheffingingezetenen_13,
    "NietTaakgebondenHeffingOngebouwd_14" AS niettaakgebondenheffingongebouwd_14,
    "NietTaakgebondenHeffingNatuur_15" AS niettaakgebondenheffingnatuur_15,
    "NietTaakgebondenHeffingGebouwd_16" AS niettaakgebondenheffinggebouwd_16,
    "Zuiveringsheffing_17" AS zuiveringsheffing_17,
    "Verontreinigingsheffing_18" AS verontreinigingsheffing_18,
    "Waterschappen_label" AS waterschappen_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80892ned"
