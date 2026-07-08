SELECT
    CAST(GlobalRank     AS BIGINT)  AS global_rank,
    CAST(TldRank        AS BIGINT)  AS tld_rank,
    Domain                          AS domain,
    TLD                             AS tld,
    CAST(RefSubNets     AS BIGINT)  AS ref_subnets,
    CAST(RefIPs         AS BIGINT)  AS ref_ips,
    IDN_Domain                      AS idn_domain,
    IDN_TLD                         AS idn_tld,
    CAST(PrevGlobalRank AS BIGINT)  AS prev_global_rank,
    CAST(PrevTldRank    AS BIGINT)  AS prev_tld_rank,
    CAST(PrevRefSubNets AS BIGINT)  AS prev_ref_subnets,
    CAST(PrevRefIPs     AS BIGINT)  AS prev_ref_ips
FROM "majestic-million-majestic-million"
WHERE Domain IS NOT NULL
