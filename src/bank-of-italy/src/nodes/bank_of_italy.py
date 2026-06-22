"""Bank of Italy - Base Dati Statistica (BDS) connector.

Data source: the InfoStat "inquiry" web application
(https://infostat.bancaditalia.it/inquiry/). There is no clean bulk/SDMX surface
for the general BDS (the public a2a SDMX export only serves a tiny curated set),
so this connector drives the same JSON services the web UI uses. The fetch is a
stateful sequence within one cookie session (the httpx client persists JSESSIONID):

    GET /inquiry/home            seed JSESSIONID
    GETINQUIRYSCOPE              establish session scope
    SUBTREENODES(table node)     -> the table's member leaf time-series ("cubes")
    GETDEFAULTREPORT(cubes)      -> the default report = a full TABLEREQUEST with
                                    the cube's SDMX dimensions (the server rejects
                                    a hand-built minimal request)
    PROSPETTODATI(TABLEREQUEST)  -> GRAPHDATA.observations: long-format records
                                    {CUBEID, DATA_OSS, VALORE, DFCUBEID, +dims}

One published subset per Bollettino table (the leaf-bearing CUBESET; entity id =
its localId). The server builds a pivot per request whose cost is super-linear in
the series count and is view-capped at ~104 series, so member series are fetched
in chunks of CHUNK_SIZE and concatenated.

Stateless full re-pull: there is no upstream incremental/delta query, so every run
re-fetches the whole table and overwrites. Freshness gating is the maintain step's
concern.
"""

import json
import time
from concurrent.futures import ThreadPoolExecutor

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, post, save_raw_ndjson

_HOME = "https://infostat.bancaditalia.it/inquiry/home"
_HDRS = {
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://infostat.bancaditalia.it/inquiry/home",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}
# Starting group size for the adaptive fetch. PROSPETTODATI returns flat
# observations only under a ~9000-cell (series x periods) graph-mode cap; 15 fits
# the common monthly tables first-try, and _fetch_group splits when it doesn't.
CHUNK_SIZE = 15

# Accepted Bollettino tables (rank >= threshold): entity localId -> taxonomy nodePath.
ENTITIES = {
    'AGGM0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/AGGM0100',
    'AGGM0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/AGGM0200',
    'AGGM0300': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/AGGM0300',
    'AGGM0400': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/AGGM0400',
    'AGGM0500': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/AGGM0500',
    'AIMF0001': '/PUBBL_00/PUBBL_00_02_01_06/AIMF0001',
    'ATEC2025': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/ATEC2025',
    'ATECO100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_04/ATECO100',
    'ATECO200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_04/ATECO200',
    'BMK0100': '/PUBBL_00/PUBBL_00_02_01_05/BMK0100',
    'BMK0200': '/PUBBL_00/PUBBL_00_02_01_05/BMK0200',
    'BMON0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/BMON0100',
    'BOT0100': '/PUBBL_00/PUBBL_00_02_01_05/BOT0100',
    'BSFC0100': '/PUBBL_00/PUBBL_00_02_01_05/BSFC0100',
    'BSFC0200': '/PUBBL_00/PUBBL_00_02_01_05/BSFC0200',
    'BSFC0300': '/PUBBL_00/PUBBL_00_02_01_05/BSFC0300',
    'BSIA0100': '/PUBBL_00/PUBBL_00_02_01_05/BSIA0100',
    'BSIB0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0100',
    'BSIB0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0200',
    'BSIB0300': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0300',
    'BSIB0400': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0400',
    'BSIB0500': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0500',
    'BSIB0600': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0600',
    'BSIB0700': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0700',
    'BSIB0800': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB0800',
    'BSIB0900': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_04/BSIB0900',
    'BSIB1000': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB1000',
    'BSIB1010': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB1010',
    'BSIB1100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB1100',
    'BSIB1110': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSIB1110',
    'BSID0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSID0100',
    'BSID0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/BSID0200',
    'BSIO0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/BSIO0100',
    'BSIO0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/BSIO0200',
    'CARB0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/CARB0100',
    'CARB0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/CARB0200',
    'CARB0300': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/CARB0300',
    'CE00100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/CE00100',
    'GESP0100': '/PUBBL_00/PUBBL_00_02_01_05/GESP0100',
    'MID0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MID0100',
    'MIR0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0100',
    'MIR0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0200',
    'MIR0300': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0300',
    'MIR0400': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0400',
    'MIR0500': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0500',
    'MIR0600': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0600',
    'MIR0700': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0700',
    'MIR0800': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0800',
    'MIR0900': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_02/MIR0900',
    'PRINC_IND_01_01': '/PRINC_IND_00/PRINC_IND_01/PRINC_IND_01_01',
    'PRINC_IND_02_01': '/PRINC_IND_00/PRINC_IND_01/PRINC_IND_02/PRINC_IND_02_01',
    'PRINC_IND_02_02': '/PRINC_IND_00/PRINC_IND_01/PRINC_IND_02/PRINC_IND_02_02',
    'PRINC_IND_03_01': '/PRINC_IND_00/PRINC_IND_03/PRINC_IND_03_01',
    'PRINC_IND_03_02': '/PRINC_IND_00/PRINC_IND_03/PRINC_IND_03_02',
    'PRINC_IND_05_01': '/PRINC_IND_00/PRINC_IND_RAPP_EST/PRINC_IND_05_01',
    'PRINC_IND_05_02': '/PRINC_IND_00/PRINC_IND_RAPP_EST/PRINC_IND_05_02',
    'PRINC_IND_06': '/PRINC_IND_00/PRINC_IND_RAPP_EST/PRINC_IND_06',
    'PRINC_IND_07': '/PRINC_IND_00/PRINC_IND_RAPP_EST/PRINC_IND_07',
    'PRINC_IND_08_01': '/PRINC_IND_00/PRINC_IND_08/PRINC_IND_08_01',
    'PRINC_IND_08_02': '/PRINC_IND_00/PRINC_IND_08/PRINC_IND_08_02',
    'PRINC_IND_08_03': '/PRINC_IND_00/PRINC_IND_08/PRINC_IND_08_03',
    'PRINC_IND_09': '/PRINC_IND_00/PRINC_IND_08/PRINC_IND_09',
    'PRINC_IND_09_02': '/PRINC_IND_00/PRINC_IND_01/PRINC_IND_09_02',
    'PUBBL_00_02_01_04_03': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03',
    'PUBBL_00_04_01_02': '/PUBBL_00/PUBBL_00_04/PUBBL_00_04_01_02',
    'QMOT0100': '/PUBBL_00/PUBBL_00_02_01_05/QMOT0100',
    'QMTS0100': '/PUBBL_00/PUBBL_00_02_01_05/QMTS0100',
    'ROB0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/ROB0100',
    'RTIT0100': '/PUBBL_00/PUBBL_00_02_01_05/RTIT0100',
    'SPBI0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/SPBI0100',
    'SPBI0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_03/SPBI0200',
    'TAGGM100': '/PUBBL_00/PUBBL_00_10/TAGGM100',
    'TAIF0100': '/PUBBL_00/PUBBL_00_10/TAIF0100',
    'TALE0100': '/PUBBL_00/PUBBL_00_02_01_02/TALE0100',
    'TALE0110': '/PUBBL_00/PUBBL_00_02_01_02/TALE0110',
    'TALE0120': '/PUBBL_00/PUBBL_00_02_01_02/TALE0120',
    'TALE0130': '/PUBBL_00/PUBBL_00_02_01_02/TALE0130',
    'TALE0140': '/PUBBL_00/PUBBL_00_02_01_02/TALE0140',
    'TALE0150': '/PUBBL_00/PUBBL_00_02_01_02/TALE0150',
    'TALE0160': '/PUBBL_00/PUBBL_00_02_01_02/TALE0160',
    'TALE0170': '/PUBBL_00/PUBBL_00_02_01_02/TALE0170',
    'TALE0180': '/PUBBL_00/PUBBL_00_02_01_02/TALE0180',
    'TALE0190': '/PUBBL_00/PUBBL_00_02_01_02/TALE0190',
    'TALE0200': '/PUBBL_00/PUBBL_00_02_01_02/TALE0200',
    'TALE0210': '/PUBBL_00/PUBBL_00_02_01_02/TALE0210',
    'TALE0220': '/PUBBL_00/PUBBL_00_02_01_02/TALE0220',
    'TALE0230': '/PUBBL_00/PUBBL_00_02_01_02/TALE0230',
    'TALE0240': '/PUBBL_00/PUBBL_00_02_01_02/TALE0240',
    'TALE0250': '/PUBBL_00/PUBBL_00_02_01_02/TALE0250',
    'TALE0260': '/PUBBL_00/PUBBL_00_02_01_02/TALE0260',
    'TALE0270': '/PUBBL_00/PUBBL_00_02_01_02/TALE0270',
    'TALE0280': '/PUBBL_00/PUBBL_00_02_01_02/TALE0280',
    'TALE0290': '/PUBBL_00/PUBBL_00_02_01_02/TALE0290',
    'TALE0300': '/PUBBL_00/PUBBL_00_02_01_02/TALE0300',
    'TALE0310': '/PUBBL_00/PUBBL_00_02_01_02/TALE0310',
    'TALE0320': '/PUBBL_00/PUBBL_00_02_01_02/TALE0320',
    'TALE0330': '/PUBBL_00/PUBBL_00_02_01_02/TALE0330',
    'TALE0340': '/PUBBL_00/PUBBL_00_02_01_02/TALE0340',
    'TALE0350': '/PUBBL_00/PUBBL_00_02_01_02/TALE0350',
    'TALE0360': '/PUBBL_00/PUBBL_00_02_01_02/TALE0360',
    'TALE0370': '/PUBBL_00/PUBBL_00_02_01_02/TALE0370',
    'TALE0380': '/PUBBL_00/PUBBL_00_02_01_02/TALE0380',
    'TALE0390': '/PUBBL_00/PUBBL_00_02_01_02/TALE0390',
    'TAV00100': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_01/TAV00100',
    'TAV00200': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_01/TAV00200',
    'TBEXR230': '/PUBBL_00/PUBBL_00_02_01_07/TBEXR230',
    'TBILC100': '/PUBBL_00/PUBBL_00_02_02/IBF_CS/TBILC100',
    'TBILC110': '/PUBBL_00/PUBBL_00_02_02/IBF_CS/TBILC110',
    'TBILC200': '/PUBBL_00/PUBBL_00_02_02/IBF_CS/TBILC200',
    'TBILC300': '/PUBBL_00/PUBBL_00_02_02/IBF_CS/TBILC300',
    'TBILC400': '/PUBBL_00/PUBBL_00_02_02/IBF_CS/TBILC400',
    'TBILF100': '/PUBBL_00/PUBBL_00_02_02/IBF_BF/TBILF100',
    'TBILF110': '/PUBBL_00/PUBBL_00_02_02/IBF_BF/TBILF110',
    'TBILF200': '/PUBBL_00/PUBBL_00_02_02/IBF_BF/TBILF200',
    'TBILF300': '/PUBBL_00/PUBBL_00_02_02/IBF_BF/TBILF300',
    'TBILF400': '/PUBBL_00/PUBBL_00_02_02/IBF_BF/TBILF400',
    'TBP60050': '/PUBBL_00/PUBBL_00_02_01_07/TBP60050',
    'TBP60060': '/PUBBL_00/PUBBL_00_02_01_07/TBP60060',
    'TBP60070': '/PUBBL_00/PUBBL_00_02_01_07/TBP60070',
    'TBP60080': '/PUBBL_00/PUBBL_00_02_01_07/TBP60080',
    'TBP60085': '/PUBBL_00/PUBBL_00_02_01_07/TBP60085',
    'TBP60090': '/PUBBL_00/PUBBL_00_02_01_07/TBP60090',
    'TBP60100': '/PUBBL_00/PUBBL_00_02_01_07/TBP60100',
    'TBP60123': '/PUBBL_00/PUBBL_00_02_01_07/TBP60123',
    'TBP60124': '/PUBBL_00/PUBBL_00_02_01_07/TBP60124',
    'TBP60125': '/PUBBL_00/PUBBL_00_02_01_07/TBP60125',
    'TBP60160': '/PUBBL_00/PUBBL_00_02_01_07/TBP60160',
    'TBP60170': '/PUBBL_00/PUBBL_00_02_01_07/TBP60170',
    'TBP60180': '/PUBBL_00/PUBBL_00_02_01_07/TBP60180',
    'TBP60200': '/PUBBL_00/PUBBL_00_02_01_07/TBP60200',
    'TBP60230': '/PUBBL_00/PUBBL_00_02_01_07/TBP60230',
    'TBP60240': '/PUBBL_00/PUBBL_00_02_01_07/TBP60240',
    'TBP60250': '/PUBBL_00/PUBBL_00_02_01_07/TBP60250',
    'TBP60260': '/PUBBL_00/PUBBL_00_02_01_07/TBP60260',
    'TBP60270': '/PUBBL_00/PUBBL_00_02_01_07/TBP60270',
    'TBP60280': '/PUBBL_00/PUBBL_00_02_01_07/TBP60280',
    'TBP60300': '/PUBBL_00/PUBBL_00_02_01_07/TBP60300',
    'TBP60310': '/PUBBL_00/PUBBL_00_02_01_07/TBP60310',
    'TBP60320': '/PUBBL_00/PUBBL_00_02_01_07/TBP60320',
    'TBP60400': '/PUBBL_00/PUBBL_00_02_01_07/TBP60400',
    'TBP60600': '/PUBBL_00/PUBBL_00_02_01_07/TBP60600',
    'TBP60610': '/PUBBL_00/PUBBL_00_02_01_07/TBP60610',
    'TBP60620': '/PUBBL_00/PUBBL_00_02_01_07/TBP60620',
    'TBSF0100': '/PUBBL_00/PUBBL_00_10/TBSF0100',
    'TCCE0100': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0100',
    'TCCE0125': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0125',
    'TCCE0155': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0155',
    'TCCE0175': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0175',
    'TCCE0200': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0200',
    'TCCE0225': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0225',
    'TCCE0250': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0250',
    'TCCE0275': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0275',
    'TCCE0300': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0300',
    'TCCE0325': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0325',
    'TCCE0350': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0350',
    'TCCE0375': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0375',
    'TCCE0400': '/PUBBL_00/PUBBL_00_02_01_01/TCCE0400',
    'TDB20207': '/PUBBL_00/PUBBL_00_05/TDB20207',
    'TDB20210': '/PUBBL_00/PUBBL_00_05/TDB20210',
    'TDB20212': '/PUBBL_00/PUBBL_00_05/TDB20212',
    'TDB20225': '/PUBBL_00/PUBBL_00_05/TDB20225',
    'TDB20230': '/PUBBL_00/PUBBL_00_05/TDB20230',
    'TDTIT010': '/PUBBL_00/PUBBL_00_08/SDP_009/TDTIT010',
    'TDTIT020': '/PUBBL_00/PUBBL_00_08/SDP_009/TDTIT020',
    'TDTIT030': '/PUBBL_00/PUBBL_00_08/SDP_009/TDTIT030',
    'TED60500': '/PUBBL_00/PUBBL_00_02_01_07/TED60500',
    'TFAA0000': '/PUBBL_00/PUBBL_00_02_01_06/TFAA0000',
    'TFAT0001': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0001',
    'TFAT0002': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0002',
    'TFAT0003': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0003',
    'TFAT0004': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0004',
    'TFAT0005': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0005',
    'TFAT0006': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0006',
    'TFAT0007': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0007',
    'TFAT0008': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0008',
    'TFAT0009': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0009',
    'TFAT0010': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0010',
    'TFAT0011': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0011',
    'TFAT0012': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0012',
    'TFAT0013': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0013',
    'TFAT0014': '/PUBBL_00/PUBBL_00_02_01_06/TFAT0014',
    'TFPT0100': '/PUBBL_00/PUBBL_00_10/TFPT0100',
    'TFPT0200': '/PUBBL_00/PUBBL_00_10/TFPT0200',
    'TFR10194': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_06/PUBBL_00_07_06_01/TFR10194',
    'TFR10269': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_06/PUBBL_00_07_06_02/TFR10269',
    'TFR10281': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_06/PUBBL_00_07_06_01/TFR10281',
    'TFR10283': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_06/PUBBL_00_07_06_02/TFR10283',
    'TFR10286': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_06/PUBBL_00_07_06_01/TFR10286',
    'TFR10288': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR10288',
    'TFR10289': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR10289',
    'TFR20269': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_03/TFR20269',
    'TFR20281': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR20281',
    'TFR30274': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR30274',
    'TFR30309': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR30309',
    'TFR30315': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_02/TFR30315',
    'TFR30970': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_04/TFR30970',
    'TFR30980': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_04/TFR30980',
    'TFR40020': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_01/TFR40020',
    'TFR40082': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_05/TFR40082',
    'TFR40087': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_05/TFR40087',
    'TFR40400': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_05/TFR40400',
    'TFR40500': '/PUBBL_00/PUBBL_00_07/PUBBL_00_07_05/TFR40500',
    'TFS00100': '/PUBBL_00/PUBBL_00_10/TFS00100',
    'TICOM250': '/PUBBL_00/PUBBL_00_02_01_07/TICOM250',
    'TIIP0200': '/PUBBL_00/PUBBL_00_02_01_07/PUBBL_00_02_01_07_01/TIIP0200',
    'TIIP0300': '/PUBBL_00/PUBBL_00_02_01_07/PUBBL_00_02_01_07_01/TIIP0300',
    'TIIP0400': '/PUBBL_00/PUBBL_00_02_01_07/PUBBL_00_02_01_07_01/TIIP0400',
    'TIIP0500': '/PUBBL_00/PUBBL_00_02_01_07/PUBBL_00_02_01_07_01/TIIP0500',
    'TITD0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/TITD0100',
    'TITD0200': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/TITD0200',
    'TITP0100': '/PUBBL_00/PUBBL_00_02_01_04/PUBBL_00_02_01_04_01/TITP0100',
    'TOAPA000': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_03/TOAPA000',
    'TOAPT000': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_03/TOAPT000',
    'TREGO010': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TREGO010',
    'TREGO020': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TREGO020',
    'TREGO030': '/PUBBL_00/PUBBL_00_08/SDP_009/TREGO030',
    'TREGO040': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TREGO040',
    'TREGO050': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TREGO050',
    'TREGO060': '/PUBBL_00/PUBBL_00_08/SDP_009/TREGO060',
    'TRI30021': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_01/TRI30021',
    'TRI30031': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30031',
    'TRI30033': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30033',
    'TRI30101': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_01/TRI30101',
    'TRI30126': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30126',
    'TRI30136': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30136',
    'TRI30146': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30146',
    'TRI30156': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30156',
    'TRI30166': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30166',
    'TRI30171': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_01/TRI30171',
    'TRI30181': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_01/TRI30181',
    'TRI30190': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_02/TRI30190',
    'TRI30206': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30206',
    'TRI30211': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30211',
    'TRI30226': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30226',
    'TRI30241': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30241',
    'TRI30251': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30251',
    'TRI30265': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30265',
    'TRI30266': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30266',
    'TRI30267': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30267',
    'TRI30268': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30268',
    'TRI30269': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30269',
    'TRI30271': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_05/TRI30271',
    'TRI30290': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_08/PUBBL_00_06_05_02/TRI30290',
    'TRI30361': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_04/TRI30361',
    'TRI30401': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_04/TRI30401',
    'TRI30431': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_03/TRI30431',
    'TRI30466': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_03/TRI30466',
    'TRI30476': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_03/TRI30476',
    'TRI30486': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30486',
    'TRI30496': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30496',
    'TRI30507': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30507',
    'TRI30516': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30516',
    'TRI30524': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30524',
    'TRI30529': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30529',
    'TRI30601': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30601',
    'TRI30602': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30602',
    'TRI30603': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30603',
    'TRI30604': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30604',
    'TRI30605': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30605',
    'TRI30606': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30606',
    'TRI30631': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30631',
    'TRI30632': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30632',
    'TRI30633': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30633',
    'TRI30634': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30634',
    'TRI30635': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30635',
    'TRI30636': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_06/TRI30636',
    'TRI30871': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_01/TRI30871',
    'TRI30881': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_01/TRI30881',
    'TRI30890': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_01/TRI30890',
    'TRI30900': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_01/TRI30900',
    'TRI30950': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30950',
    'TRI30951': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30951',
    'TRI30952': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30952',
    'TRI30953': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30953',
    'TRI30954': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30954',
    'TRI30955': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI30955',
    'TRI31100': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI31100',
    'TRI31101': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI31101',
    'TRI31102': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI31102',
    'TRI31103': '/PUBBL_00/PUBBL_00_06/PUBBL_00_06_07/PUBBL_00_06_07_02/TRI31103',
    'TRUF0100': '/PUBBL_00/PUBBL_00_10/TRUF0100',
    'TRUF0200': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_02/TRUF0200',
    'TRUF0300': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_02/TRUF0300',
    'TRUF0400': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_02/TRUF0400',
    'TRUF0450': '/PUBBL_00/PUBBL_00_02_01_07/PUBBL_00_02_01_07_01/TRUF0450',
    'TRUF0500': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_02/TRUF0500',
    'TRUF0600': '/PUBBL_00/PUBBL_00_10/PUBBL_00_10_02/TRUF0600',
    'TSDPAL010': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL010',
    'TSDPAL020': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL020',
    'TSDPAL030': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL030',
    'TSDPAL040': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL040',
    'TSDPAL050': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL050',
    'TSDPAL060': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL060',
    'TSDPAL070': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL070',
    'TSDPAL080': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL080',
    'TSDPAL090': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL090',
    'TSDPAL100': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL100',
    'TSDPAL110': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL110',
    'TSDPAL120': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL120',
    'TSDPAL130': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL130',
    'TSDPAL140': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL140',
    'TSDPAL150': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL150',
    'TSDPAL160': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL160',
    'TSDPAL170': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL170',
    'TSDPAL180': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL180',
    'TSDPAL190': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL190',
    'TSDPAL200': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL200',
    'TSDPAL210': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL210',
    'TSDPAL220': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL220',
    'TSDPAL230': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL230',
    'TSDPAL240': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL240',
    'TSDPAL250': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL250',
    'TSDPAL260': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL260',
    'TSDPAL270': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL270',
    'TSDPAL280': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_007/TSDPAL280',
    'TSDPN010': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN010',
    'TSDPN020': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN020',
    'TSDPN030': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN030',
    'TSDPN040': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN040',
    'TSDPN050': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN050',
    'TSDPN060': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN060',
    'TSDPN070': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN070',
    'TSDPN080': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN080',
    'TSDPN090': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN090',
    'TSDPN100': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN100',
    'TSDPN110': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN110',
    'TSDPN120': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN120',
    'TSDPN130': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN130',
    'TSDPN140': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN140',
    'TSDPN150': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN150',
    'TSDPN160': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN160',
    'TSDPN170': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN170',
    'TSDPN180': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN180',
    'TSDPN190': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN190',
    'TSDPN200': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN200',
    'TSDPN210': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN210',
    'TSDPN220': '/PUBBL_00/PUBBL_00_08/SDP_004/TSDPN220',
    'TSDPT010': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT010',
    'TSDPT020': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT020',
    'TSDPT030': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT030',
    'TSDPT040': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT040',
    'TSDPT050': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT050',
    'TSDPT060': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT060',
    'TSDPT070': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT070',
    'TSDPT080': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT080',
    'TSDPT090': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT090',
    'TSDPT100': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT100',
    'TSDPT110': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT110',
    'TSDPT120': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT120',
    'TSDPT130': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT130',
    'TSDPT140': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT140',
    'TSDPT150': '/PUBBL_00/PUBBL_00_08/SDP_005/TSDPT150',
    'TSDPTS010': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS010',
    'TSDPTS020': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS020',
    'TSDPTS030': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS030',
    'TSDPTS040': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS040',
    'TSDPTS050': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS050',
    'TSDPTS060': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS060',
    'TSDPTS070': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS070',
    'TSDPTS080': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS080',
    'TSDPTS090': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS090',
    'TSDPTS100': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS100',
    'TSDPTS110': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS110',
    'TSDPTS120': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS120',
    'TSDPTS130': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS130',
    'TSDPTS140': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS140',
    'TSDPTS150': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS150',
    'TSDPTS160': '/PUBBL_00/PUBBL_00_08/SDP_008/SDP_006/TSDPTS160',
    'TSPAG020': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG020',
    'TSPAG030': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG030',
    'TSPAG070': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG070',
    'TSPAG080': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG080',
    'TSPAG090': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG090',
    'TSPAG100': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG100',
    'TSPAG120': '/PUBBL_00/PUBBL_00_08/PUBBL_00_08_01/TSPAG120',
    'TTDEB100': '/PUBBL_00/PUBBL_00_10/TTDEB100',
    'TUEE0100': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0100',
    'TUEE0110': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0110',
    'TUEE0120': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0120',
    'TUEE0130': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0130',
    'TUEE0140': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0140',
    'TUEE0150': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0150',
    'TUEE0160': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0160',
    'TUEE0170': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0170',
    'TUEE0180': '/PUBBL_00/PUBBL_00_02_01_03/FPE_003/TUEE0180',
    'TUEE0210': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0210',
    'TUEE0220': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0220',
    'TUEE0230': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0230',
    'TUEE0240': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0240',
    'TUEE0250': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0250',
    'TUEE0260': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0260',
    'TUEE0270': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0270',
    'TUEE0280': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0280',
    'TUEE0290': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0290',
    'TUEE0300': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0300',
    'TUEE0330': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0330',
    'TUEE0350': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0350',
    'TUEE0400': '/PUBBL_00/PUBBL_00_02_01_03/TUEE0400',
    'VALM0100': '/PUBBL_00/PUBBL_00_02_01_05/VALM0100',
    'VALM0200': '/PUBBL_00/PUBBL_00_02_01_05/VALM0200',
}

_SPEC_TO_ENTITY = {
    "bank-of-italy-" + e.lower().replace("_", "-"): e for e in ENTITIES
}

# Genuine infra blips that a plain retry of the SAME call clears: connection
# setup failures, pool exhaustion, and server 5xx / 429. The Bank of Italy app
# flaps 500s on /inquiry/home under load (a cold seed sometimes 500s), so these
# are retried at the _service layer.
_RETRY_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout, httpx.ProxyError,
)
# Symptoms of an oversized PROSPETTODATI pivot (or a mid-stream server drop):
# retrying the same too-big request just times out again. _fetch_group reacts
# to these by HALVING the series group, not by retrying as-is.
_SPLIT_EXC = (
    httpx.ReadTimeout, httpx.WriteTimeout, httpx.ReadError, httpx.RemoteProtocolError,
)


class _DegradedResponse(Exception):
    """A PROSPETTODATI pivot that came back in the server's DEGRADED shape.

    Besides "full graph mode" (per-series observations, full SDMX columns) and
    "too big -> empty GRAPHDATA" (handled by splitting), the app has a third,
    failure-mode shape under load: it still returns observations, but their
    `values` are stripped down to {DATA_OSS, FENEC, VALORE} — the CUBEID series
    key and every dimension column are gone. Those rows are unusable (thousands
    of indistinguishable breakdown rows collapse onto one (measure, date)), so
    they must never be saved. A healthy observation always carries CUBEID, so a
    missing CUBEID is the tell; _fetch_group reacts by splitting / retrying to
    coax the server back into full graph mode."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _RETRY_EXC):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _service(service: str, data: dict) -> object:
    """POST one inquiry service. Body is JSON (mislabelled text/html, leading BOM)."""
    resp = post(
        _HOME + "?calltype=asin&service=" + service,
        data=data,
        headers=_HDRS,
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return json.loads(resp.content.decode("utf-8-sig"))


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(6),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _seed_session() -> None:
    # The seed GET + GETINQUIRYSCOPE establish the JSESSIONID-scoped session.
    # A cold /inquiry/home intermittently 500s; the whole seed is retried as a
    # unit (a partial seed is useless) so a transient blip doesn't fail the node.
    resp = get(_HOME, headers=_HDRS, timeout=(10.0, 60.0))
    resp.raise_for_status()
    _service("GETINQUIRYSCOPE", {})


def _member_series(local_id: str, node_path: str) -> list:
    """Direct leaf CUBE children of a table CUBESET = its member time series."""
    nodes = _service("SUBTREENODES", {
        "surveytree": "false",
        "id": "BANKITALIA:DIFF:CUBE:" + local_id,
        "taxoSurveyId": "TAXO",
        "nodeType": "CUBESET",
        "nodePath": node_path,
        "childrenNumber": 99999,
        "NUMITEMS": 100000,
        "STARTINDEX": 0,
        "localId": local_id,
    })
    return [n for n in nodes if n.get("nodeType") == "CUBE"]


def _try_chunk(chunk: list) -> list:
    """One PROSPETTODATI request for a group of member series -> its observations.

    PROSPETTODATI only returns flat GRAPHDATA.observations while the selection
    stays under a server "graph mode" cap (roughly series x periods ~ 9000); above
    it the response flips to a paginated table (requestType 0) and GRAPHDATA is
    empty. So an empty result here means "too big" (caller splits) OR "this series
    genuinely has no graph data"."""
    report = _service("GETDEFAULTREPORT", {"nodes": json.dumps(chunk)})
    prospetto = _service("PROSPETTODATI", {
        "VIEW_MODE": "",
        "GRAPH_MODE": "lines",
        "COMM": "BANKITALIA",
        "CTX": "DIFF",
        "CUBEIDS": ";".join(n["localId"] for n in chunk),
        "TABLEREQUEST": json.dumps(report),
    })
    obs = prospetto.get("GRAPHDATA", {}).get("observations", []) or []
    # Reject the degraded (stripped) shape before it can reach the raw file. The
    # stripped shape is {DATA_OSS, FENEC, VALORE} — it carries VALORE but has lost
    # the CUBEID series key + dimensions (see _DegradedResponse), so the tell is
    # "VALORE present AND CUBEID absent". Measure-named tables (no VALORE; value
    # lives in a measure-named column) legitimately have no CUBEID and must NOT be
    # flagged — guarding on VALORE keeps that healthy shape from misfiring.
    # Splitting/retrying recovers the full shape, so surface it as its own signal.
    if any(
        "VALORE" in (v := (o.get("values") or {})) and "CUBEID" not in v
        for o in obs
    ):
        raise _DegradedResponse(
            "stripped observations (missing CUBEID) for "
            + str(len(chunk)) + " series"
        )
    return obs


def _fetch_group(nodes: list) -> list:
    """Adaptive fetch. Halve-and-recurse on BOTH failure modes of an oversized
    pivot:

    - empty result  -> the selection blew the graph-mode cell cap; split.
    - read timeout / mid-stream drop (_SPLIT_EXC) -> the pivot is too big/slow
      to serve in one go; split so each call carries fewer cells.

    Recursion bottoms out at one series. A lone series that still times out is
    a genuine infra problem, retried a few times before giving up; a lone series
    that returns empty genuinely carries no graph observations (returns [])."""
    try:
        obs = _try_chunk(nodes)
    except _SPLIT_EXC:
        if len(nodes) > 1:
            mid = len(nodes) // 2
            return _fetch_group(nodes[:mid]) + _fetch_group(nodes[mid:])
        # Single series can't be split — give the server a few more tries.
        for attempt in range(3):
            time.sleep(2 * (attempt + 1))
            try:
                return _try_chunk(nodes)
            except _SPLIT_EXC:
                continue
        raise
    except _DegradedResponse:
        # Degraded (stripped) pivot. A smaller selection drops back under the
        # graph-mode cap and returns full columns, so split when we can; a lone
        # series can't be split, so retry it a few times (the degradation is
        # transient under load). If it stays stripped, let it propagate — the
        # asset fails loudly rather than publishing keyless, dimensionless rows.
        if len(nodes) > 1:
            mid = len(nodes) // 2
            return _fetch_group(nodes[:mid]) + _fetch_group(nodes[mid:])
        for attempt in range(4):
            time.sleep(2 * (attempt + 1))
            try:
                return _try_chunk(nodes)
            except (_DegradedResponse, *_SPLIT_EXC):
                continue
        raise
    if obs:
        return obs
    if len(nodes) <= 1:
        return []
    mid = len(nodes) // 2
    return _fetch_group(nodes[:mid]) + _fetch_group(nodes[mid:])


# Per-table thread pool over chunks: the PROSPETTODATI pivot is the bottleneck, so
# a few concurrent calls cut big-table wall time several-fold. Verified safe - each
# call carries its own (report, cubeids); no shared server state.
_MAX_WORKERS = 5


def fetch_one(node_id: str) -> None:
    asset = node_id
    local_id = _SPEC_TO_ENTITY[node_id]
    node_path = ENTITIES[local_id]

    _seed_session()
    members = _member_series(local_id, node_path)
    if not members:
        raise AssertionError(node_id + ": no member series for table " + local_id)

    groups = [members[i:i + CHUNK_SIZE] for i in range(0, len(members), CHUNK_SIZE)]
    rows = []
    with ThreadPoolExecutor(max_workers=min(_MAX_WORKERS, len(groups))) as pool:
        for obs in pool.map(_fetch_group, groups):
            for o in obs:
                values = o.get("values")
                if values:
                    rows.append(values)

    if not rows:
        raise AssertionError(node_id + ": table " + local_id + " returned no observations")

    # Stabilise the raw schema: a Bollettino table's observations carry different
    # SDMX dimension keys per series (and the rate-registry tables omit CUBEID/
    # VALORE entirely), so the saved ndjson is heterogeneous. The SQL transform's
    # view is built with a bare read_json_auto(<paths>) whose schema is inferred
    # from a leading sample; on a large, drifty table (e.g. TRI30021, ~1.8M obs)
    # a column present only in later/other rows — CUBEID included — can be missed,
    # and the transform's `* EXCLUDE (CUBEID, ...)` then fails to bind. Filling
    # every row out to the full key union (missing -> null) makes the first row
    # carry every column, so inference sees the complete schema regardless of
    # ordering or sample window. Done in place to avoid doubling RSS.
    all_keys = set().union(*(r.keys() for r in rows))
    for r in rows:
        for k in all_keys:
            r.setdefault(k, None)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=sid, fn=fetch_one, kind="download")
    for sid in _SPEC_TO_ENTITY
]

# Most Bollettino tables are clean long-format: one observation row per
# (CUBEID series, DATA_OSS date) with a numeric VALORE. CUBEID is the full SDMX
# series key, so it alone identifies the series; the remaining SDMX dimension
# columns are redundant descriptive coordinates carried through by *.
_STD_SQL = '''
    SELECT
        CAST(DATA_OSS AS TIMESTAMP)::DATE AS date,
        CUBEID AS series_key,
        TRY_CAST(VALORE AS DOUBLE) AS value,
        * EXCLUDE (DATA_OSS, CUBEID, VALORE)
    FROM "{dep}"
    WHERE TRY_CAST(VALORE AS DOUBLE) IS NOT NULL
      AND DATA_OSS IS NOT NULL
'''

# A handful of tables use a "measure-named" wide layout instead: there is no
# VALORE/DATA_OSS column; each row's MEASURES field names the column that holds
# its value (e.g. MEASURES='TASSO_UFF' -> the value lives in column TASSO_UFF),
# and the date is in DATA_DECOR/DATA_PROV. We serialise the row to JSON so the
# value column can be addressed dynamically by name without the column having to
# exist statically, key the series by (CUBEID, MEASURES), and keep only rows
# whose measure is numeric (date-valued measures like DATA_DECOR cast to NULL
# and drop out). These are rate-decision registries: one effective date can
# carry several provisions (different DATA_PROV/NUM_ORD), so we keep the latest
# provision per (date, series) to get one clean point per effective date.
# Verified against PRINC_IND_01_01, PUBBL_00_04_01_02, PUBBL_00_02_01_04_03.
_MEASURE_TABLES = {"PRINC_IND_01_01", "PUBBL_00_04_01_02", "PUBBL_00_02_01_04_03"}
_MEASURE_SQL = '''
    WITH src AS (SELECT to_json(d) AS j FROM "{dep}" d)
    SELECT date, series_key, value FROM (
        SELECT
            TRY_CAST(COALESCE(j->>'DATA_OSS', j->>'DATA_DECOR', j->>'DATA_PROV') AS TIMESTAMP)::DATE AS date,
            concat_ws(':', j->>'CUBEID', j->>'MEASURES') AS series_key,
            TRY_CAST(j ->> (j->>'MEASURES') AS DOUBLE) AS value,
            j->>'DATA_PROV' AS _prov,
            TRY_CAST(j->>'NUM_ORD' AS BIGINT) AS _ord
        FROM src
    )
    WHERE date IS NOT NULL AND value IS NOT NULL
    QUALIFY row_number() OVER (
        PARTITION BY date, series_key ORDER BY _prov DESC NULLS LAST, _ord DESC NULLS LAST
    ) = 1
'''


def _transform_sql(spec_id: str) -> str:
    eid = _SPEC_TO_ENTITY[spec_id]
    template = _MEASURE_SQL if eid in _MEASURE_TABLES else _STD_SQL
    return template.format(dep=spec_id)


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=s.id + "-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
