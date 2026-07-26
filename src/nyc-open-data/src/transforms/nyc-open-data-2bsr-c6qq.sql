-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "_name" AS name,
    "latitude",
    "longitude",
    "_domain" AS domain,
    "asset_class",
    "nta_code",
    "responsible_agency",
    "operated_by",
    "_owner" AS owner,
    "number",
    "street",
    "city",
    "postcode",
    "borough",
    "bin",
    "bbl",
    "num_floors",
    "connected_to_fiber",
    "wireless_on_roof",
    "fiber_pathways_in_building",
    "landmarked",
    "senior_center_flag",
    "community_cornerstone_center_flag",
    "franchise_agreement",
    "community_board",
    "council_district",
    "census_tract",
    "nta",
    "target_neighborhood_id",
    "target_neighborhood"
FROM "nyc-open-data-2bsr-c6qq"
