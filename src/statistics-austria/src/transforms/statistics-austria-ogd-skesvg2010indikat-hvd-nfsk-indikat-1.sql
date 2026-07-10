-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "sectors",
    "regional_breakdown",
    "value_type",
    "operating_surplus_gross_and_mixed_income_gross_b2_b3g",
    "gross_fixed_capital_formation_p51g",
    "net_lending_net_borrowing_b9",
    "total_liabilities_fl",
    "total_assets_fa",
    "saving_gross_b8g",
    "disposable_income_gross_b6g",
    "disposable_income_net_b6n"
FROM "statistics-austria-ogd-skesvg2010indikat-hvd-nfsk-indikat-1"
