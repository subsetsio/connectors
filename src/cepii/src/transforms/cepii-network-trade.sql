-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Network-trade measures are centrality and fragmentation indicators, not additive bilateral trade flows.
SELECT
    "t",
    "id",
    "i",
    "iso3",
    "country",
    "Out-degree" AS out_degree,
    "In-degree" AS in_degree,
    "Out-strength" AS out_strength,
    "In-strength" AS in_strength,
    "Out-degree_percent" AS out_degree_percent,
    "In-degree percent" AS in_degree_percent,
    "Out-strength-percent" AS out_strength_percent,
    "In-strength_percent" AS in_strength_percent,
    "Out-closenness" AS out_closenness,
    "In-closenness" AS in_closenness,
    "W-Out-closenness" AS w_out_closenness,
    "W-In-closenness" AS w_in_closenness,
    "Out-eigenvector" AS out_eigenvector,
    "In-eigenvector" AS in_eigenvector,
    "W-Out-eigenvector" AS w_out_eigenvector,
    "W-In-eigenvector" AS w_in_eigenvector
FROM "cepii-network-trade"
