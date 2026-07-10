-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time",
    "cg_consumer_durables",
    "cg_long_lasting_consumer_durables",
    "cg_long_lasting_consumer_durables_consumer_goods",
    "cg_short_lived_consumer_durables",
    "cg_convenience_goods",
    "fu_consumer_goods",
    "fu_capital_goods",
    "fu_intermediate_goods",
    "sg_seasonal_goods",
    "sg_non_seasonal_goods"
FROM "statistics-austria-ogd-pregps003-ghpi-20s-1"
