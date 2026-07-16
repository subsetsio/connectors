-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaalPersonenInHuishoudens_1" AS totaalpersoneninhuishoudens_1,
    "TotaalInParticuliereHuishoudens_2" AS totaalinparticulierehuishoudens_2,
    "ThuiswonendKind_3" AS thuiswonendkind_3,
    "Alleenstaand_4" AS alleenstaand_4,
    "TotaalSamenwonendePersonen_5" AS totaalsamenwonendepersonen_5,
    "PartnerInNietGehuwdPaarZonderKi_6" AS partnerinnietgehuwdpaarzonderki_6,
    "PartnerInGehuwdPaarZonderKinderen_7" AS partneringehuwdpaarzonderkinderen_7,
    "PartnerInNietGehuwdPaarMetKinderen_8" AS partnerinnietgehuwdpaarmetkinderen_8,
    "PartnerInGehuwdPaarMetKinderen_9" AS partneringehuwdpaarmetkinderen_9,
    "OuderInEenouderhuishouden_10" AS ouderineenouderhuishouden_10,
    "OverigLidHuishouden_11" AS overiglidhuishouden_11,
    "PersonenInInstitutioneleHuishoudens_12" AS personenininstitutionelehuishoudens_12,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71488ned"
