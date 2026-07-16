-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "RegelmatigWerkzaamTotaal_1" AS regelmatigwerkzaamtotaal_1,
    "GezinsarbeidskrachtenTotaal_2" AS gezinsarbeidskrachtentotaal_2,
    "Bedrijfshoofden_3" AS bedrijfshoofden_3,
    "Echtgenoten_4" AS echtgenoten_4,
    "MeewerkendeFamilie_5" AS meewerkendefamilie_5,
    "NietGezinsarbeidskrachtenTotaal_6" AS nietgezinsarbeidskrachtentotaal_6,
    "Bedrijfsleiders_7" AS bedrijfsleiders_7,
    "OverigeRegelmatigWerkzamePersonen_8" AS overigeregelmatigwerkzamepersonen_8,
    "NietRegelmatigWerkzaam_9" AS nietregelmatigwerkzaam_9,
    "RegelmatigWerkzaamTotaal_10" AS regelmatigwerkzaamtotaal_10,
    "GezinsarbeidskrachtenTotaal_11" AS gezinsarbeidskrachtentotaal_11,
    "Bedrijfshoofden_12" AS bedrijfshoofden_12,
    "Echtgenoten_13" AS echtgenoten_13,
    "MeewerkendeFamilie_14" AS meewerkendefamilie_14,
    "NietGezinsarbeidskrachtenTotaal_15" AS nietgezinsarbeidskrachtentotaal_15,
    "Bedrijfsleiders_16" AS bedrijfsleiders_16,
    "OverigeRegelmatigWerkzamePersonen_17" AS overigeregelmatigwerkzamepersonen_17,
    "NietRegelmatigWerkzaam_18" AS nietregelmatigwerkzaam_18,
    "RegelmatigWerkzaamTotaal_19" AS regelmatigwerkzaamtotaal_19,
    "GezinsarbeidskrachtenTotaal_20" AS gezinsarbeidskrachtentotaal_20,
    "Bedrijfshoofden_21" AS bedrijfshoofden_21,
    "Echtgenoten_22" AS echtgenoten_22,
    "MeewerkendeFamilie_23" AS meewerkendefamilie_23,
    "NietGezinsarbeidskrachtenTotaal_24" AS nietgezinsarbeidskrachtentotaal_24,
    "Bedrijfsleiders_25" AS bedrijfsleiders_25,
    "OverigeRegelmatigWerkzamePersonen_26" AS overigeregelmatigwerkzamepersonen_26,
    "NietRegelmatigWerkzaam_27" AS nietregelmatigwerkzaam_27,
    "Geslacht_label" AS geslacht_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80784ned"
