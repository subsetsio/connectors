-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "title_description",
    "open_competitive_or_promotional",
    "list_title_code",
    "exam_no",
    "list_agency_code",
    "agency_description",
    "list_divison_code",
    "list_establishment_date",
    "aac_count",
    "aol_count",
    "dce_count",
    "dea_count",
    "dlx_count",
    "fra_count",
    "frh_count",
    "fri_count",
    "frm_count",
    "frp_count",
    "ftr_count",
    "nfp_count",
    "nle_count",
    "ova_count",
    "rli_count",
    "tin_count",
    "unf_count",
    "appointed_count",
    "cns_count",
    "restored_after_cns_count",
    "count_of_restored_to_a_list_following_removal_from_a_list_by_their_own_action"
FROM "nyc-open-data-qjzt-ytn9"
