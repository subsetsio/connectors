# Entity union for eurocontrol-network-manager — copied from
# data/sources/eurocontrol-network-manager/work/entity_union.json.
# Each id is a EUROCONTROL Performance Review bulk dataset; the download spec
# id is f"eurocontrol-network-manager-{id.lower().replace('_','-')}".
ENTITY_IDS = [
    "ACE_Yearly_Operational_Data",
    "ANSP_Financial_Data",
    "ASMA_Additional_Time",
    "ATC_Pre-Departure_Delay",
    "ATFM_Slot_Adherence",
    "Airport_Arrival_ATFM_Delay",
    "Airport_Arrival_ATFM_Delay_post_ops",
    "Airport_Traffic",
    "All_Pre-Departure_Delay",
    "CO2_emissions_by_state",
    "En-Route_ATFM_Delay_AUA",
    "En-Route_ATFM_Delay_AUA_post_ops",
    "En-Route_ATFM_Delay_FIR",
    "En-Route_ATFM_Delay_FIR_post_ops",
    "Horizontal_Flight_Efficiency",
    "Taxi-In_Additional_Time",
    "Taxi-Out_Additional_Time",
    "Vertical_Flight_Efficiency_cdo_cco",
    "g2g_emissions",
]
