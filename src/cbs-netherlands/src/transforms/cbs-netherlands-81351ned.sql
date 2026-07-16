-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BedrijfstakkenBranchesSBI2008" AS bedrijfstakkenbranchessbi2008,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "InvesteringenInMaterieleVasteActiva_1" AS investeringeninmaterielevasteactiva_1,
    "GrondEnTerreinen_2" AS grondenterreinen_2,
    "Bedrijfsgebouwen_3" AS bedrijfsgebouwen_3,
    "GrondWaterEnWegenbouwkundigeWerken_4" AS grondwaterenwegenbouwkundigewerken_4,
    "Vervoermiddelen_5" AS vervoermiddelen_5,
    "ComputersEnRandapparatuur_6" AS computersenrandapparatuur_6,
    "MachinesEnInstallaties_7" AS machineseninstallaties_7,
    "OverigeMaterieleVasteActiva_8" AS overigematerielevasteactiva_8,
    "BedrijfstakkenBranchesSBI2008_label" AS bedrijfstakkenbranchessbi2008_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81351ned"
