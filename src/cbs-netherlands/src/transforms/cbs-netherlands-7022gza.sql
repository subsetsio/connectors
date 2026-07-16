-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "Perioden" AS perioden,
    "TotaalZelfdoding_1" AS totaalzelfdoding_1,
    "Ongehuwd_2" AS ongehuwd_2,
    "Gehuwd_3" AS gehuwd_3,
    "Verweduwd_4" AS verweduwd_4,
    "Gescheiden_5" AS gescheiden_5,
    "OphangenVerwurgen_6" AS ophangenverwurgen_6,
    "MedicijnenEnOfAlcohol_7" AS medicijnenenofalcohol_7,
    "VoorTreinOfMetro_8" AS voortreinofmetro_8,
    "Verdrinken_9" AS verdrinken_9,
    "SpringenVanHoogte_10" AS springenvanhoogte_10,
    "OverigeWijzeVanZelfdoding_11" AS overigewijzevanzelfdoding_11,
    "OnbekendeWijzeVanZelfdoding_12" AS onbekendewijzevanzelfdoding_12,
    "PsychischeStoornissen_13" AS psychischestoornissen_13,
    "FysiekeStoornissen_14" AS fysiekestoornissen_14,
    "HuiselijkeOmstandigheden_15" AS huiselijkeomstandigheden_15,
    "OverigMotiefVanZelfdoding_16" AS overigmotiefvanzelfdoding_16,
    "OnbekendMotiefVanZelfdoding_17" AS onbekendmotiefvanzelfdoding_17,
    "TotaalZelfdoding_18" AS totaalzelfdoding_18,
    "Ongehuwd_19" AS ongehuwd_19,
    "Gehuwd_20" AS gehuwd_20,
    "Verweduwd_21" AS verweduwd_21,
    "Gescheiden_22" AS gescheiden_22,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-7022gza"
