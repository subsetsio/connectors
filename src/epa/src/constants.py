"""Dataset-id selections for the epa connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    'acres.grant_property', 'acres.grants', 'acres.p_pilot_accomplishment', 'acres.tab_project',
    'acres.tech_assist_proj', 'frs.frs_alt_name', 'frs.frs_facility_site', 'frs.frs_interest',
    'frs.frs_naics', 'frs.frs_program_facility', 'frs.frs_sic', 'frs.frs_supplemental_interest',
    'frs.geo_facility_point', 'frs.geo_pgm_facility_coordinate', 'frs.v_frs_facility_site_geo_tribes', 'frs.v_frs_facility_site_geopgm',
    'frs.v_frs_pgm_facility_geotribes', 'frs.v_pub_frs_naics_ez', 'frs.v_pub_frs_sic_ez', 'icis.air_facility_interest',
    'icis.air_stack_test', 'icis.air_tvacc', 'icis.air_tvacc_review', 'icis.icis_activity',
    'icis.icis_activity_report', 'icis.icis_comp_monitor', 'icis.icis_comp_monitor_pretreatment', 'icis.icis_contact',
    'icis.icis_contact_electronic_addr', 'icis.icis_contact_phone', 'icis.icis_dmr', 'icis.icis_dmr_event',
    'icis.icis_dmr_form_parameter', 'icis.icis_dmr_form_value', 'icis.icis_dmr_parameter', 'icis.icis_dmr_value',
    'icis.icis_enf_conclusion', 'icis.icis_enf_regional_docket', 'icis.icis_enforcement', 'icis.icis_facility_interest',
    'icis.icis_limit', 'icis.icis_limit_set', 'icis.icis_limit_set_schedule', 'icis.icis_limit_value',
    'icis.icis_npdes_violation', 'icis.icis_perm_association', 'icis.icis_perm_biosolid', 'icis.icis_perm_feature',
    'icis.icis_perm_feature_coord', 'icis.icis_perm_narrative_condition', 'icis.icis_perm_pretreatment', 'icis.icis_perm_schedule_event',
    'icis.icis_perm_track_event', 'icis.icis_permit', 'icis.icis_prog_rpt', 'icis.icis_prog_rpt_pretreatment',
    'icis.icis_rpt_pre_removal_credit', 'nei.county_areas', 'nei.county_scc_summary', 'nei.county_sector_summary',
    'nei.emissions_tier', 'nei.emissions_tier2', 'nei.emissions_tier3', 'nei.facility',
    'nei.facility_pollutants', 'nei.facility_summary', 'nei.pollutant', 'nei.sector_pollutants',
    'nei.sectors', 'nei.state_scc_summary', 'nei.tier_pollutants', 'nei.tiers',
    'nei.with_names', 'radnet.erm_air_benchmark', 'radnet.erm_ana_proc', 'radnet.erm_analysis',
    'radnet.erm_analyte', 'radnet.erm_count', 'radnet.erm_location', 'radnet.erm_location_ll',
    'radnet.erm_matrix', 'radnet.erm_milk_benchmark', 'radnet.erm_precip_benchmark', 'radnet.erm_project',
    'radnet.erm_result', 'radnet.erm_sample', 'radnet.erm_study', 'radnet.erm_water_benchmark',
    'radnet.erm_years', 'rcra.br_reporting', 'rcra.br_reporting_year', 'rcra.rcr_br_lu_management_method',
    'rcra.rcr_br_lu_waste_minimization', 'rcra.rcr_ca_area', 'rcra.rcr_ca_area_event', 'rcra.rcr_ca_authority',
    'rcra.rcr_ca_authority_citation', 'rcra.rcr_ca_event', 'rcra.rcr_ca_event_authority', 'rcra.rcr_ca_lu_authority',
    'rcra.rcr_ca_lu_statutory_citation', 'rcra.rcr_ce_citation', 'rcra.rcr_ce_lu_citation', 'rcra.rcr_cmecomp3',
    'rcra.rcr_em_import', 'rcra.rcr_em_import_1', 'rcra.rcr_em_manifest', 'rcra.rcr_em_pcb_info',
    'rcra.rcr_em_rejection', 'rcra.rcr_em_transporter', 'rcra.rcr_em_waste_line', 'rcra.rcr_fa_cost_estimate',
    'rcra.rcr_fa_cost_mechanism_detail', 'rcra.rcr_fa_lu_cost_estimate_reason', 'rcra.rcr_fa_mechanism', 'rcra.rcr_fa_mechanism_detail',
    'rcra.rcr_hd_basic', 'rcra.rcr_hd_certification', 'rcra.rcr_hd_episodic_event', 'rcra.rcr_hd_episodic_project',
    'rcra.rcr_hd_episodic_waste', 'rcra.rcr_hd_handler', 'rcra.rcr_hd_hsm_activity', 'rcra.rcr_hd_hsm_basic',
    'rcra.rcr_hd_hsm_recycler', 'rcra.rcr_hd_lqg_closure', 'rcra.rcr_hd_lqg_consolidation', 'rcra.rcr_hd_lu_country',
    'rcra.rcr_hd_lu_county', 'rcra.rcr_hd_lu_episodic_project', 'rcra.rcr_hd_lu_foreign_state', 'rcra.rcr_hd_lu_naics',
    'rcra.rcr_hd_lu_other_permit', 'rcra.rcr_hd_lu_relationship', 'rcra.rcr_hd_lu_relationship_1', 'rcra.rcr_hd_lu_state',
    'rcra.rcr_hd_lu_state_activity', 'rcra.rcr_hd_lu_state_activity_1', 'rcra.rcr_hd_lu_state_district', 'rcra.rcr_hd_lu_universal_waste',
    'rcra.rcr_hd_naics', 'rcra.rcr_hd_other_permit', 'rcra.rcr_hd_owner_operator', 'rcra.rcr_hd_part_a',
    'rcra.rcr_hd_reporting', 'rcra.rcr_hd_state_activity', 'rcra.rcr_hd_universal_waste', 'rcra.rcr_pm_event',
    'rcra.rcr_pm_mod_event', 'rcra.rcr_pm_series', 'rcra.wt_ar_2024', 'rcra.wt_notices_exports',
    'rcra.wt_notices_imports', 'sdwis.enforcement', 'sdwis.enforcement_action', 'sdwis.geographic_area',
    'sdwis.lcr_sample', 'sdwis.lcr_sample_result', 'sdwis.pws', 'sdwis.pws_county',
    'sdwis.sdw_contaminants', 'sdwis.sdw_county_served', 'sdwis.sdw_viol_enforcement', 'sdwis.service_area',
    'sdwis.treatment', 'sdwis.violation', 'sdwis.water_system', 'sdwis.water_system_facility',
    'sems.envirofacts_contaminants', 'sems.envirofacts_site', 'tri.tri_additional_info', 'tri.tri_chem_activity',
    'tri.tri_chem_info', 'tri.tri_county', 'tri.tri_energy_recovery', 'tri.tri_facility',
    'tri.tri_facility_db', 'tri.tri_facility_db_history', 'tri.tri_facility_history', 'tri.tri_facility_npdes',
    'tri.tri_facility_npdes_history', 'tri.tri_facility_rcra', 'tri.tri_facility_rcra_history', 'tri.tri_facility_uic',
    'tri.tri_facility_uic_history', 'tri.tri_form_activity_subuse', 'tri.tri_form_r_schedule_one', 'tri.tri_form_totals',
    'tri.tri_off_site_transfer_location', 'tri.tri_onsite_waste_treatment_met', 'tri.tri_onsite_wastestream', 'tri.tri_potw_location',
    'tri.tri_recycling_process', 'tri.tri_release_qty', 'tri.tri_reporting_form', 'tri.tri_source_reduct_method',
    'tri.tri_source_reduct_qty', 'tri.tri_submission_naics', 'tri.tri_submission_sic', 'tri.tri_transfer_qty',
    'tri.tri_trips_comment', 'tri.tri_water_stream',
]
