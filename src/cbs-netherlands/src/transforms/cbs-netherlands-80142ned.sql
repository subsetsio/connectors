-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaalAlleOnderliggendeDoodsoorzaken_1" AS totaalalleonderliggendedoodsoorzaken_1,
    "Nieuwvormingen_2" AS nieuwvormingen_2,
    "ZiektenVanHartEnVaatstelsel_3" AS ziektenvanhartenvaatstelsel_3,
    "ZiektenVanAdemhalingsstelsel_4" AS ziektenvanademhalingsstelsel_4,
    "UitwendigeDoodsoorzaken_5" AS uitwendigedoodsoorzaken_5,
    "OverigeDoodsoorzaken_6" AS overigedoodsoorzaken_6,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80142ned"
