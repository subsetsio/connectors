"""US Census Bureau — Census Data API connector.

Mechanism: the Census Data API (https://api.census.gov/data), REST, api-key
(env CENSUS_API_KEY) required on every *data* request. Each entity is one
catalog dataset endpoint (a vintage-stamped aggregate dataset such as
`acs/acs1`, `cbp`, `dec/pl`, or a `timeseries/*` series collection). The
discovery surface (data.json catalog, variables.json, geography.json) needs no
key and is what we enumerate from.

Fetch shape: **stateless full re-pull** (shape 1). Census vintages are immutable
once published; we re-pull the corpus each refresh and overwrite. Per dataset we
pull the latest vintage (aggregate datasets) or the single timeseries endpoint.

The data path is heterogeneous: every dataset has its own variable list (13 to
~37k variables) and its own geography hierarchy, and a single `get` request
accepts at most ~50 variables, so wide tables must be split across requests.
Rather than rejoin chunks on the geography key, we publish a uniform **long /
EAV** table per dataset: every cell of every API response row becomes one
`(vintage, geo_level, row_id, variable, value)` record. `row_id` ties the cells
of one response row together so an observation can be pivoted back; `variable`
holds the column header (an estimate code, a dimension like `time` /
`category_code`, a geography key like `state`, or `NAME`). This is the format
the collect step intended ("vintage, group, variable and geography as columns")
and it sidesteps the per-dataset schema problem entirely — the raw is NDJSON
(columns differ per dataset) and the transform re-types `value` on read.

Bounding: to keep a full run feasible across 329 datasets we pull, per dataset,
only the most-aggregate geography levels (those with no `requires` hierarchy,
queried `for=<level>:*`) and cap the variable list at MAX_VARS (logged when a
dataset is wider). The handful of pathological datasets (ACS detailed tables,
~37k variables) are necessarily truncated; everything else is pulled in full.

Raw format: **NDJSON** (gzip-streamed). The EAV record schema is stable, but the
value column is intentionally a string (Census mixes numeric estimates with
annotation codes like '-', 'N', '(X)'); the transform casts to value_num.
"""

import json
import logging
import os

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

logger = logging.getLogger(__name__)

SLUG = "us-census-bureau"

# Per-dataset access config, keyed by download spec id. Value is
# (base_url, is_timeseries, vintage). base_url is the vintage-stamped API
# endpoint from the discovery catalog (data.json); variables.json /
# geography.json hang off it. Generated from the catalog at authoring time —
# static data, no module-level I/O.
ENTITY_CONFIG = {
    'us-census-bureau-abscb': ('https://api.census.gov/data/2023/abscb', False, 2023),
    'us-census-bureau-abscbo': ('https://api.census.gov/data/2023/abscbo', False, 2023),
    'us-census-bureau-abscs': ('https://api.census.gov/data/2023/abscs', False, 2023),
    'us-census-bureau-absmcb': ('https://api.census.gov/data/2023/absmcb', False, 2023),
    'us-census-bureau-absnesd': ('https://api.census.gov/data/2023/absnesd', False, 2023),
    'us-census-bureau-absnesdo': ('https://api.census.gov/data/2023/absnesdo', False, 2023),
    'us-census-bureau-abstcb': ('https://api.census.gov/data/2018/abstcb', False, 2018),
    'us-census-bureau-acs/acs1': ('https://api.census.gov/data/2024/acs/acs1', False, 2024),
    'us-census-bureau-acs/acs1/cprofile': ('https://api.census.gov/data/2024/acs/acs1/cprofile', False, 2024),
    'us-census-bureau-acs/acs1/profile': ('https://api.census.gov/data/2024/acs/acs1/profile', False, 2024),
    'us-census-bureau-acs/acs1/sdataprofile/cd119': ('https://api.census.gov/data/2023/acs/acs1/sdataprofile/cd119', False, 2023),
    'us-census-bureau-acs/acs1/spp': ('https://api.census.gov/data/2024/acs/acs1/spp', False, 2024),
    'us-census-bureau-acs/acs1/subject': ('https://api.census.gov/data/2024/acs/acs1/subject', False, 2024),
    'us-census-bureau-acs/acs3': ('https://api.census.gov/data/2013/acs/acs3', False, 2013),
    'us-census-bureau-acs/acs3/cprofile': ('https://api.census.gov/data/2013/acs/acs3/cprofile', False, 2013),
    'us-census-bureau-acs/acs3/profile': ('https://api.census.gov/data/2013/acs/acs3/profile', False, 2013),
    'us-census-bureau-acs/acs3/spp': ('https://api.census.gov/data/2013/acs/acs3/spp', False, 2013),
    'us-census-bureau-acs/acs3/subject': ('https://api.census.gov/data/2013/acs/acs3/subject', False, 2013),
    'us-census-bureau-acs/acs5': ('https://api.census.gov/data/2024/acs/acs5', False, 2024),
    'us-census-bureau-acs/acs5/aian': ('https://api.census.gov/data/2021/acs/acs5/aian', False, 2021),
    'us-census-bureau-acs/acs5/aianprofile': ('https://api.census.gov/data/2021/acs/acs5/aianprofile', False, 2021),
    'us-census-bureau-acs/acs5/cprofile': ('https://api.census.gov/data/2024/acs/acs5/cprofile', False, 2024),
    'us-census-bureau-acs/acs5/eeo': ('https://api.census.gov/data/2018/acs/acs5/eeo', False, 2018),
    'us-census-bureau-acs/acs5/profile': ('https://api.census.gov/data/2024/acs/acs5/profile', False, 2024),
    'us-census-bureau-acs/acs5/spt': ('https://api.census.gov/data/2021/acs/acs5/spt', False, 2021),
    'us-census-bureau-acs/acs5/sptprofile': ('https://api.census.gov/data/2021/acs/acs5/sptprofile', False, 2021),
    'us-census-bureau-acs/acs5/subject': ('https://api.census.gov/data/2024/acs/acs5/subject', False, 2024),
    'us-census-bureau-acs/acsse': ('https://api.census.gov/data/2024/acs/acsse', False, 2024),
    'us-census-bureau-acs/flows': ('https://api.census.gov/data/2022/acs/flows', False, 2022),
    'us-census-bureau-acs1/cd113': ('https://api.census.gov/data/2011/acs1/cd113', False, 2011),
    'us-census-bureau-acs1/cd115': ('https://api.census.gov/data/2015/acs1/cd115', False, 2015),
    'us-census-bureau-acs5': ('https://api.census.gov/data/2009/acs5', False, 2009),
    'us-census-bureau-aiesnonemp': ('https://api.census.gov/data/2023/aiesnonemp', False, 2023),
    'us-census-bureau-ase/csa': ('https://api.census.gov/data/2016/ase/csa', False, 2016),
    'us-census-bureau-ase/cscb': ('https://api.census.gov/data/2016/ase/cscb', False, 2016),
    'us-census-bureau-ase/cscbo': ('https://api.census.gov/data/2016/ase/cscbo', False, 2016),
    'us-census-bureau-cbp': ('https://api.census.gov/data/2023/cbp', False, 2023),
    'us-census-bureau-cfsarea': ('https://api.census.gov/data/2022/cfsarea', False, 2022),
    'us-census-bureau-cfsexport': ('https://api.census.gov/data/2022/cfsexport', False, 2022),
    'us-census-bureau-cfshazmat': ('https://api.census.gov/data/2022/cfshazmat', False, 2022),
    'us-census-bureau-cfsprelim': ('https://api.census.gov/data/2017/cfsprelim', False, 2017),
    'us-census-bureau-cfstemp': ('https://api.census.gov/data/2022/cfstemp', False, 2022),
    'us-census-bureau-cre': ('https://api.census.gov/data/2024/cre', False, 2024),
    'us-census-bureau-crepuertorico': ('https://api.census.gov/data/2024/crepuertorico', False, 2024),
    'us-census-bureau-dec/aian': ('https://api.census.gov/data/2010/dec/aian', False, 2010),
    'us-census-bureau-dec/aianprofile': ('https://api.census.gov/data/2000/dec/aianprofile', False, 2000),
    'us-census-bureau-dec/as': ('https://api.census.gov/data/2010/dec/as', False, 2010),
    'us-census-bureau-dec/asyoe': ('https://api.census.gov/data/2010/dec/asyoe', False, 2010),
    'us-census-bureau-dec/cd110h': ('https://api.census.gov/data/2000/dec/cd110h', False, 2000),
    'us-census-bureau-dec/cd110hprofile': ('https://api.census.gov/data/2000/dec/cd110hprofile', False, 2000),
    'us-census-bureau-dec/cd110s': ('https://api.census.gov/data/2000/dec/cd110s', False, 2000),
    'us-census-bureau-dec/cd110sprofile': ('https://api.census.gov/data/2000/dec/cd110sprofile', False, 2000),
    'us-census-bureau-dec/cd113': ('https://api.census.gov/data/2010/dec/cd113', False, 2010),
    'us-census-bureau-dec/cd113profile': ('https://api.census.gov/data/2010/dec/cd113profile', False, 2010),
    'us-census-bureau-dec/cd115': ('https://api.census.gov/data/2010/dec/cd115', False, 2010),
    'us-census-bureau-dec/cd115profile': ('https://api.census.gov/data/2010/dec/cd115profile', False, 2010),
    'us-census-bureau-dec/cd116': ('https://api.census.gov/data/2010/dec/cd116', False, 2010),
    'us-census-bureau-dec/cd118': ('https://api.census.gov/data/2020/dec/cd118', False, 2020),
    'us-census-bureau-dec/cd119': ('https://api.census.gov/data/2020/dec/cd119', False, 2020),
    'us-census-bureau-dec/cqr': ('https://api.census.gov/data/2000/dec/cqr', False, 2000),
    'us-census-bureau-dec/crosstabas': ('https://api.census.gov/data/2020/dec/crosstabas', False, 2020),
    'us-census-bureau-dec/crosstabgu': ('https://api.census.gov/data/2020/dec/crosstabgu', False, 2020),
    'us-census-bureau-dec/crosstabmp': ('https://api.census.gov/data/2020/dec/crosstabmp', False, 2020),
    'us-census-bureau-dec/crosstabvi': ('https://api.census.gov/data/2020/dec/crosstabvi', False, 2020),
    'us-census-bureau-dec/ddhca': ('https://api.census.gov/data/2020/dec/ddhca', False, 2020),
    'us-census-bureau-dec/ddhcb': ('https://api.census.gov/data/2020/dec/ddhcb', False, 2020),
    'us-census-bureau-dec/dhc': ('https://api.census.gov/data/2020/dec/dhc', False, 2020),
    'us-census-bureau-dec/dhcas': ('https://api.census.gov/data/2020/dec/dhcas', False, 2020),
    'us-census-bureau-dec/dhcgu': ('https://api.census.gov/data/2020/dec/dhcgu', False, 2020),
    'us-census-bureau-dec/dhcmp': ('https://api.census.gov/data/2020/dec/dhcmp', False, 2020),
    'us-census-bureau-dec/dhcvi': ('https://api.census.gov/data/2020/dec/dhcvi', False, 2020),
    'us-census-bureau-dec/dp': ('https://api.census.gov/data/2020/dec/dp', False, 2020),
    'us-census-bureau-dec/dpas': ('https://api.census.gov/data/2020/dec/dpas', False, 2020),
    'us-census-bureau-dec/dpgu': ('https://api.census.gov/data/2020/dec/dpgu', False, 2020),
    'us-census-bureau-dec/dpmp': ('https://api.census.gov/data/2020/dec/dpmp', False, 2020),
    'us-census-bureau-dec/dpvi': ('https://api.census.gov/data/2020/dec/dpvi', False, 2020),
    'us-census-bureau-dec/gu': ('https://api.census.gov/data/2010/dec/gu', False, 2010),
    'us-census-bureau-dec/guyoe': ('https://api.census.gov/data/2010/dec/guyoe', False, 2010),
    'us-census-bureau-dec/mp': ('https://api.census.gov/data/2010/dec/mp', False, 2010),
    'us-census-bureau-dec/mpyoe': ('https://api.census.gov/data/2010/dec/mpyoe', False, 2010),
    'us-census-bureau-dec/pes': ('https://api.census.gov/data/2020/dec/pes', False, 2020),
    'us-census-bureau-dec/pl': ('https://api.census.gov/data/2020/dec/pl', False, 2020),
    'us-census-bureau-dec/plnat': ('https://api.census.gov/data/2010/dec/plnat', False, 2010),
    'us-census-bureau-dec/responserate': ('https://api.census.gov/data/2020/dec/responserate', False, 2020),
    'us-census-bureau-dec/sdhc': ('https://api.census.gov/data/2020/dec/sdhc', False, 2020),
    'us-census-bureau-dec/selfresponserate': ('https://api.census.gov/data/2020/dec/selfresponserate', False, 2020),
    'us-census-bureau-dec/sf1': ('https://api.census.gov/data/2010/dec/sf1', False, 2010),
    'us-census-bureau-dec/sf2': ('https://api.census.gov/data/2010/dec/sf2', False, 2010),
    'us-census-bureau-dec/sf2profile': ('https://api.census.gov/data/2000/dec/sf2profile', False, 2000),
    'us-census-bureau-dec/sf3': ('https://api.census.gov/data/2000/dec/sf3', False, 2000),
    'us-census-bureau-dec/sf3profile': ('https://api.census.gov/data/2000/dec/sf3profile', False, 2000),
    'us-census-bureau-dec/sf4': ('https://api.census.gov/data/2000/dec/sf4', False, 2000),
    'us-census-bureau-dec/sf4profile': ('https://api.census.gov/data/2000/dec/sf4profile', False, 2000),
    'us-census-bureau-dec/sldh': ('https://api.census.gov/data/2000/dec/sldh', False, 2000),
    'us-census-bureau-dec/sldhprofile': ('https://api.census.gov/data/2000/dec/sldhprofile', False, 2000),
    'us-census-bureau-dec/slds': ('https://api.census.gov/data/2000/dec/slds', False, 2000),
    'us-census-bureau-dec/sldsprofile': ('https://api.census.gov/data/2000/dec/sldsprofile', False, 2000),
    'us-census-bureau-dec/vi': ('https://api.census.gov/data/2010/dec/vi', False, 2010),
    'us-census-bureau-ecn/islandareas': ('https://api.census.gov/data/2022/ecn/islandareas', False, 2022),
    'us-census-bureau-ecn/islandareas/comp': ('https://api.census.gov/data/2022/ecn/islandareas/comp', False, 2022),
    'us-census-bureau-ecn/islandareas/ind': ('https://api.census.gov/data/2022/ecn/islandareas/ind', False, 2022),
    'us-census-bureau-ecn/islandareas/lines': ('https://api.census.gov/data/2012/ecn/islandareas/lines', False, 2012),
    'us-census-bureau-ecn/islandareas/napcs': ('https://api.census.gov/data/2022/ecn/islandareas/napcs', False, 2022),
    'us-census-bureau-ecnadbnprop': ('https://api.census.gov/data/2017/ecnadbnprop', False, 2017),
    'us-census-bureau-ecnadmben': ('https://api.census.gov/data/2017/ecnadmben', False, 2017),
    'us-census-bureau-ecnbasic': ('https://api.census.gov/data/2022/ecnbasic', False, 2022),
    'us-census-bureau-ecnbranddeal': ('https://api.census.gov/data/2022/ecnbranddeal', False, 2022),
    'us-census-bureau-ecnbridge1': ('https://api.census.gov/data/2022/ecnbridge1', False, 2022),
    'us-census-bureau-ecnbridge2': ('https://api.census.gov/data/2022/ecnbridge2', False, 2022),
    'us-census-bureau-ecnbrordeal': ('https://api.census.gov/data/2017/ecnbrordeal', False, 2017),
    'us-census-bureau-ecncashadv': ('https://api.census.gov/data/2012/ecncashadv', False, 2012),
    'us-census-bureau-ecnccard': ('https://api.census.gov/data/2022/ecnccard', False, 2022),
    'us-census-bureau-ecnclcust': ('https://api.census.gov/data/2022/ecnclcust', False, 2022),
    'us-census-bureau-ecnclientorg': ('https://api.census.gov/data/2022/ecnclientorg', False, 2022),
    'us-census-bureau-ecncomm': ('https://api.census.gov/data/2022/ecncomm', False, 2022),
    'us-census-bureau-ecncomp': ('https://api.census.gov/data/2022/ecncomp', False, 2022),
    'us-census-bureau-ecnconact': ('https://api.census.gov/data/2022/ecnconact', False, 2022),
    'us-census-bureau-ecnconcess': ('https://api.census.gov/data/2012/ecnconcess', False, 2012),
    'us-census-bureau-ecncrfin': ('https://api.census.gov/data/2022/ecncrfin', False, 2022),
    'us-census-bureau-ecndirprem': ('https://api.census.gov/data/2017/ecndirprem', False, 2017),
    'us-census-bureau-ecndissmed': ('https://api.census.gov/data/2017/ecndissmed', False, 2017),
    'us-census-bureau-ecnecomm': ('https://api.census.gov/data/2022/ecnecomm', False, 2022),
    'us-census-bureau-ecnelmenu': ('https://api.census.gov/data/2022/ecnelmenu', False, 2022),
    'us-census-bureau-ecnempfunc': ('https://api.census.gov/data/2022/ecnempfunc', False, 2022),
    'us-census-bureau-ecnentsup': ('https://api.census.gov/data/2022/ecnentsup', False, 2022),
    'us-census-bureau-ecneoyinv': ('https://api.census.gov/data/2022/ecneoyinv', False, 2022),
    'us-census-bureau-ecneoyinvwh': ('https://api.census.gov/data/2017/ecneoyinvwh', False, 2017),
    'us-census-bureau-ecnequip': ('https://api.census.gov/data/2012/ecnequip', False, 2012),
    'us-census-bureau-ecnexpbyaux': ('https://api.census.gov/data/2022/ecnexpbyaux', False, 2022),
    'us-census-bureau-ecnexpnrg': ('https://api.census.gov/data/2017/ecnexpnrg', False, 2017),
    'us-census-bureau-ecnexpsvc': ('https://api.census.gov/data/2017/ecnexpsvc', False, 2017),
    'us-census-bureau-ecnflspace': ('https://api.census.gov/data/2017/ecnflspace', False, 2017),
    'us-census-bureau-ecnfoodsvc': ('https://api.census.gov/data/2017/ecnfoodsvc', False, 2017),
    'us-census-bureau-ecnfran': ('https://api.census.gov/data/2017/ecnfran', False, 2017),
    'us-census-bureau-ecngrant': ('https://api.census.gov/data/2022/ecngrant', False, 2022),
    'us-census-bureau-ecngrmargprof': ('https://api.census.gov/data/2022/ecngrmargprof', False, 2022),
    'us-census-bureau-ecnguest': ('https://api.census.gov/data/2012/ecnguest', False, 2012),
    'us-census-bureau-ecnguestsize': ('https://api.census.gov/data/2012/ecnguestsize', False, 2012),
    'us-census-bureau-ecnhosp': ('https://api.census.gov/data/2022/ecnhosp', False, 2022),
    'us-census-bureau-ecnhotel': ('https://api.census.gov/data/2017/ecnhotel', False, 2017),
    'us-census-bureau-ecninstr': ('https://api.census.gov/data/2017/ecninstr', False, 2017),
    'us-census-bureau-ecninvval': ('https://api.census.gov/data/2022/ecninvval', False, 2022),
    'us-census-bureau-ecnipa': ('https://api.census.gov/data/2012/ecnipa', False, 2012),
    'us-census-bureau-ecnkob': ('https://api.census.gov/data/2022/ecnkob', False, 2022),
    'us-census-bureau-ecnlabor': ('https://api.census.gov/data/2017/ecnlabor', False, 2017),
    'us-census-bureau-ecnlifomfg': ('https://api.census.gov/data/2022/ecnlifomfg', False, 2022),
    'us-census-bureau-ecnlifomine': ('https://api.census.gov/data/2022/ecnlifomine', False, 2022),
    'us-census-bureau-ecnlifoval': ('https://api.census.gov/data/2012/ecnlifoval', False, 2012),
    'us-census-bureau-ecnlines': ('https://api.census.gov/data/2012/ecnlines', False, 2012),
    'us-census-bureau-ecnloan': ('https://api.census.gov/data/2017/ecnloan', False, 2017),
    'us-census-bureau-ecnloccons': ('https://api.census.gov/data/2022/ecnloccons', False, 2022),
    'us-census-bureau-ecnlocmfg': ('https://api.census.gov/data/2022/ecnlocmfg', False, 2022),
    'us-census-bureau-ecnlocmine': ('https://api.census.gov/data/2022/ecnlocmine', False, 2022),
    'us-census-bureau-ecnmargin': ('https://api.census.gov/data/2017/ecnmargin', False, 2017),
    'us-census-bureau-ecnmatfuel': ('https://api.census.gov/data/2022/ecnmatfuel', False, 2022),
    'us-census-bureau-ecnmealcost': ('https://api.census.gov/data/2012/ecnmealcost', False, 2012),
    'us-census-bureau-ecnmenutype': ('https://api.census.gov/data/2012/ecnmenutype', False, 2012),
    'us-census-bureau-ecnnapcsind': ('https://api.census.gov/data/2022/ecnnapcsind', False, 2022),
    'us-census-bureau-ecnnapcsprd': ('https://api.census.gov/data/2022/ecnnapcsprd', False, 2022),
    'us-census-bureau-ecnpatient': ('https://api.census.gov/data/2022/ecnpatient', False, 2022),
    'us-census-bureau-ecnpetrfac': ('https://api.census.gov/data/2017/ecnpetrfac', False, 2017),
    'us-census-bureau-ecnpetrprod': ('https://api.census.gov/data/2017/ecnpetrprod', False, 2017),
    'us-census-bureau-ecnpetrrec': ('https://api.census.gov/data/2017/ecnpetrrec', False, 2017),
    'us-census-bureau-ecnpetrstat': ('https://api.census.gov/data/2017/ecnpetrstat', False, 2017),
    'us-census-bureau-ecnprofit': ('https://api.census.gov/data/2017/ecnprofit', False, 2017),
    'us-census-bureau-ecnpurelec': ('https://api.census.gov/data/2022/ecnpurelec', False, 2022),
    'us-census-bureau-ecnpurgas': ('https://api.census.gov/data/2022/ecnpurgas', False, 2022),
    'us-census-bureau-ecnpurmode': ('https://api.census.gov/data/2022/ecnpurmode', False, 2022),
    'us-census-bureau-ecnrdacq': ('https://api.census.gov/data/2012/ecnrdacq', False, 2012),
    'us-census-bureau-ecnrdofc': ('https://api.census.gov/data/2022/ecnrdofc', False, 2022),
    'us-census-bureau-ecnseat': ('https://api.census.gov/data/2012/ecnseat', False, 2012),
    'us-census-bureau-ecnsize': ('https://api.census.gov/data/2022/ecnsize', False, 2022),
    'us-census-bureau-ecnsocial': ('https://api.census.gov/data/2017/ecnsocial', False, 2017),
    'us-census-bureau-ecntelemeds': ('https://api.census.gov/data/2022/ecntelemeds', False, 2022),
    'us-census-bureau-ecntype': ('https://api.census.gov/data/2022/ecntype', False, 2022),
    'us-census-bureau-ecntypepayer': ('https://api.census.gov/data/2022/ecntypepayer', False, 2022),
    'us-census-bureau-ecntypop': ('https://api.census.gov/data/2022/ecntypop', False, 2022),
    'us-census-bureau-ecnvalcon': ('https://api.census.gov/data/2022/ecnvalcon', False, 2022),
    'us-census-bureau-ewks': ('https://api.census.gov/data/2012/ewks', False, 2012),
    'us-census-bureau-intltrade/imp-exp': ('https://api.census.gov/data/2018/intltrade/imp_exp', False, 2018),
    'us-census-bureau-nonemp': ('https://api.census.gov/data/2023/nonemp', False, 2023),
    'us-census-bureau-pdb/blockgroup': ('https://api.census.gov/data/2024/pdb/blockgroup', False, 2024),
    'us-census-bureau-pdb/tract': ('https://api.census.gov/data/2024/pdb/tract', False, 2024),
    'us-census-bureau-pep/agesex': ('https://api.census.gov/data/2014/pep/agesex', False, 2014),
    'us-census-bureau-pep/agespecial5': ('https://api.census.gov/data/2014/pep/agespecial5', False, 2014),
    'us-census-bureau-pep/agespecial6': ('https://api.census.gov/data/2014/pep/agespecial6', False, 2014),
    'us-census-bureau-pep/agespecialpr': ('https://api.census.gov/data/2014/pep/agespecialpr', False, 2014),
    'us-census-bureau-pep/charage': ('https://api.census.gov/data/2019/pep/charage', False, 2019),
    'us-census-bureau-pep/charagegroups': ('https://api.census.gov/data/2019/pep/charagegroups', False, 2019),
    'us-census-bureau-pep/charv': ('https://api.census.gov/data/2023/pep/charv', False, 2023),
    'us-census-bureau-pep/cochar5': ('https://api.census.gov/data/2014/pep/cochar5', False, 2014),
    'us-census-bureau-pep/cochar6': ('https://api.census.gov/data/2014/pep/cochar6', False, 2014),
    'us-census-bureau-pep/components': ('https://api.census.gov/data/2019/pep/components', False, 2019),
    'us-census-bureau-pep/cty': ('https://api.census.gov/data/2014/pep/cty', False, 2014),
    'us-census-bureau-pep/housing': ('https://api.census.gov/data/2019/pep/housing', False, 2019),
    'us-census-bureau-pep/int-charage': ('https://api.census.gov/data/2000/pep/int_charage', False, 2000),
    'us-census-bureau-pep/int-charagegroups': ('https://api.census.gov/data/2000/pep/int_charagegroups', False, 2000),
    'us-census-bureau-pep/int-housingunits': ('https://api.census.gov/data/2000/pep/int_housingunits', False, 2000),
    'us-census-bureau-pep/int-natcivpop': ('https://api.census.gov/data/1990/pep/int_natcivpop', False, 1990),
    'us-census-bureau-pep/int-natmonthly': ('https://api.census.gov/data/2000/pep/int_natmonthly', False, 2000),
    'us-census-bureau-pep/int-natresafo': ('https://api.census.gov/data/1990/pep/int_natresafo', False, 1990),
    'us-census-bureau-pep/int-natrespop': ('https://api.census.gov/data/1990/pep/int_natrespop', False, 1990),
    'us-census-bureau-pep/int-population': ('https://api.census.gov/data/2000/pep/int_population', False, 2000),
    'us-census-bureau-pep/monthlynatchar5': ('https://api.census.gov/data/2014/pep/monthlynatchar5', False, 2014),
    'us-census-bureau-pep/monthlynatchar6': ('https://api.census.gov/data/2014/pep/monthlynatchar6', False, 2014),
    'us-census-bureau-pep/natmonthly': ('https://api.census.gov/data/2021/pep/natmonthly', False, 2021),
    'us-census-bureau-pep/natstprc': ('https://api.census.gov/data/2014/pep/natstprc', False, 2014),
    'us-census-bureau-pep/natstprc18': ('https://api.census.gov/data/2014/pep/natstprc18', False, 2014),
    'us-census-bureau-pep/population': ('https://api.census.gov/data/2021/pep/population', False, 2021),
    'us-census-bureau-pep/prcagesex': ('https://api.census.gov/data/2014/pep/prcagesex', False, 2014),
    'us-census-bureau-pep/prm': ('https://api.census.gov/data/2014/pep/prm', False, 2014),
    'us-census-bureau-pep/prmagesex': ('https://api.census.gov/data/2014/pep/prmagesex', False, 2014),
    'us-census-bureau-pep/projagegroups': ('https://api.census.gov/data/2014/pep/projagegroups', False, 2014),
    'us-census-bureau-pep/projbirths': ('https://api.census.gov/data/2014/pep/projbirths', False, 2014),
    'us-census-bureau-pep/projdeaths': ('https://api.census.gov/data/2014/pep/projdeaths', False, 2014),
    'us-census-bureau-pep/projnat': ('https://api.census.gov/data/2014/pep/projnat', False, 2014),
    'us-census-bureau-pep/projnim': ('https://api.census.gov/data/2014/pep/projnim', False, 2014),
    'us-census-bureau-pep/projpop': ('https://api.census.gov/data/2014/pep/projpop', False, 2014),
    'us-census-bureau-pep/stchar5': ('https://api.census.gov/data/2014/pep/stchar5', False, 2014),
    'us-census-bureau-pep/stchar6': ('https://api.census.gov/data/2014/pep/stchar6', False, 2014),
    'us-census-bureau-pep/subcty': ('https://api.census.gov/data/2014/pep/subcty', False, 2014),
    'us-census-bureau-popproj/agegroups': ('https://api.census.gov/data/2017/popproj/agegroups', False, 2017),
    'us-census-bureau-popproj/births': ('https://api.census.gov/data/2017/popproj/births', False, 2017),
    'us-census-bureau-popproj/deaths': ('https://api.census.gov/data/2017/popproj/deaths', False, 2017),
    'us-census-bureau-popproj/nat': ('https://api.census.gov/data/2017/popproj/nat', False, 2017),
    'us-census-bureau-popproj/nim': ('https://api.census.gov/data/2017/popproj/nim', False, 2017),
    'us-census-bureau-popproj/pop': ('https://api.census.gov/data/2017/popproj/pop', False, 2017),
    'us-census-bureau-pubschlfin': ('https://api.census.gov/data/2012/pubschlfin', False, 2012),
    'us-census-bureau-rhfs': ('https://api.census.gov/data/2024/rhfs', False, 2024),
    'us-census-bureau-timeseries/aies/basic': ('https://api.census.gov/data/timeseries/aies/basic', True, None),
    'us-census-bureau-timeseries/aies/ecom': ('https://api.census.gov/data/timeseries/aies/ecom', True, None),
    'us-census-bureau-timeseries/aies/exp01': ('https://api.census.gov/data/timeseries/aies/exp01', True, None),
    'us-census-bureau-timeseries/aies/exp02': ('https://api.census.gov/data/timeseries/aies/exp02', True, None),
    'us-census-bureau-timeseries/aies/inv': ('https://api.census.gov/data/timeseries/aies/inv', True, None),
    'us-census-bureau-timeseries/aies/miscsector': ('https://api.census.gov/data/timeseries/aies/miscsector', True, None),
    'us-census-bureau-timeseries/asm/area2012': ('https://api.census.gov/data/timeseries/asm/area2012', True, None),
    'us-census-bureau-timeseries/asm/area2017': ('https://api.census.gov/data/timeseries/asm/area2017', True, None),
    'us-census-bureau-timeseries/asm/benchmark2017': ('https://api.census.gov/data/timeseries/asm/benchmark2017', True, None),
    'us-census-bureau-timeseries/asm/benchmark2022': ('https://api.census.gov/data/timeseries/asm/benchmark2022', True, None),
    'us-census-bureau-timeseries/asm/industry': ('https://api.census.gov/data/timeseries/asm/industry', True, None),
    'us-census-bureau-timeseries/asm/product': ('https://api.census.gov/data/timeseries/asm/product', True, None),
    'us-census-bureau-timeseries/asm/state': ('https://api.census.gov/data/timeseries/asm/state', True, None),
    'us-census-bureau-timeseries/asm/value2012': ('https://api.census.gov/data/timeseries/asm/value2012', True, None),
    'us-census-bureau-timeseries/asm/value2017': ('https://api.census.gov/data/timeseries/asm/value2017', True, None),
    'us-census-bureau-timeseries/bds': ('https://api.census.gov/data/timeseries/bds', True, None),
    'us-census-bureau-timeseries/eits/advm3': ('https://api.census.gov/data/timeseries/eits/advm3', True, None),
    'us-census-bureau-timeseries/eits/bfs': ('https://api.census.gov/data/timeseries/eits/bfs', True, None),
    'us-census-bureau-timeseries/eits/ftd': ('https://api.census.gov/data/timeseries/eits/ftd', True, None),
    'us-census-bureau-timeseries/eits/ftdadv': ('https://api.census.gov/data/timeseries/eits/ftdadv', True, None),
    'us-census-bureau-timeseries/eits/hv': ('https://api.census.gov/data/timeseries/eits/hv', True, None),
    'us-census-bureau-timeseries/eits/m3': ('https://api.census.gov/data/timeseries/eits/m3', True, None),
    'us-census-bureau-timeseries/eits/marts': ('https://api.census.gov/data/timeseries/eits/marts', True, None),
    'us-census-bureau-timeseries/eits/mhs': ('https://api.census.gov/data/timeseries/eits/mhs', True, None),
    'us-census-bureau-timeseries/eits/mhs2': ('https://api.census.gov/data/timeseries/eits/mhs2', True, None),
    'us-census-bureau-timeseries/eits/mrts': ('https://api.census.gov/data/timeseries/eits/mrts', True, None),
    'us-census-bureau-timeseries/eits/mrtsadv': ('https://api.census.gov/data/timeseries/eits/mrtsadv', True, None),
    'us-census-bureau-timeseries/eits/mtis': ('https://api.census.gov/data/timeseries/eits/mtis', True, None),
    'us-census-bureau-timeseries/eits/mwts': ('https://api.census.gov/data/timeseries/eits/mwts', True, None),
    'us-census-bureau-timeseries/eits/mwtsadv': ('https://api.census.gov/data/timeseries/eits/mwtsadv', True, None),
    'us-census-bureau-timeseries/eits/qfr': ('https://api.census.gov/data/timeseries/eits/qfr', True, None),
    'us-census-bureau-timeseries/eits/qpr': ('https://api.census.gov/data/timeseries/eits/qpr', True, None),
    'us-census-bureau-timeseries/eits/qss': ('https://api.census.gov/data/timeseries/eits/qss', True, None),
    'us-census-bureau-timeseries/eits/qtax': ('https://api.census.gov/data/timeseries/eits/qtax', True, None),
    'us-census-bureau-timeseries/eits/resconst': ('https://api.census.gov/data/timeseries/eits/resconst', True, None),
    'us-census-bureau-timeseries/eits/ressales': ('https://api.census.gov/data/timeseries/eits/ressales', True, None),
    'us-census-bureau-timeseries/eits/vip': ('https://api.census.gov/data/timeseries/eits/vip', True, None),
    'us-census-bureau-timeseries/govs': ('https://api.census.gov/data/timeseries/govs', True, None),
    'us-census-bureau-timeseries/govsemp': ('https://api.census.gov/data/timeseries/govsemp', True, None),
    'us-census-bureau-timeseries/govspension': ('https://api.census.gov/data/timeseries/govspension', True, None),
    'us-census-bureau-timeseries/govsschfin': ('https://api.census.gov/data/timeseries/govsschfin', True, None),
    'us-census-bureau-timeseries/govsstatefin': ('https://api.census.gov/data/timeseries/govsstatefin', True, None),
    'us-census-bureau-timeseries/govsstatetax': ('https://api.census.gov/data/timeseries/govsstatetax', True, None),
    'us-census-bureau-timeseries/healthins/sahie': ('https://api.census.gov/data/timeseries/healthins/sahie', True, None),
    'us-census-bureau-timeseries/hhpulse': ('https://api.census.gov/data/timeseries/hhpulse', True, None),
    'us-census-bureau-timeseries/hps': ('https://api.census.gov/data/timeseries/hps', True, None),
    'us-census-bureau-timeseries/idb/1year': ('https://api.census.gov/data/timeseries/idb/1year', True, None),
    'us-census-bureau-timeseries/idb/5year': ('https://api.census.gov/data/timeseries/idb/5year', True, None),
    'us-census-bureau-timeseries/intltrade/exports/enduse': ('https://api.census.gov/data/timeseries/intltrade/exports/enduse', True, None),
    'us-census-bureau-timeseries/intltrade/exports/enduseexport': ('https://api.census.gov/data/timeseries/intltrade/exports/enduseexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/hitech': ('https://api.census.gov/data/timeseries/intltrade/exports/hitech', True, None),
    'us-census-bureau-timeseries/intltrade/exports/hitechexport': ('https://api.census.gov/data/timeseries/intltrade/exports/hitechexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/hs': ('https://api.census.gov/data/timeseries/intltrade/exports/hs', True, None),
    'us-census-bureau-timeseries/intltrade/exports/hsexport': ('https://api.census.gov/data/timeseries/intltrade/exports/hsexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/naics': ('https://api.census.gov/data/timeseries/intltrade/exports/naics', True, None),
    'us-census-bureau-timeseries/intltrade/exports/naicsexport': ('https://api.census.gov/data/timeseries/intltrade/exports/naicsexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/porths': ('https://api.census.gov/data/timeseries/intltrade/exports/porths', True, None),
    'us-census-bureau-timeseries/intltrade/exports/porthsexport': ('https://api.census.gov/data/timeseries/intltrade/exports/porthsexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/sitc': ('https://api.census.gov/data/timeseries/intltrade/exports/sitc', True, None),
    'us-census-bureau-timeseries/intltrade/exports/sitcexport': ('https://api.census.gov/data/timeseries/intltrade/exports/sitcexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/statehs': ('https://api.census.gov/data/timeseries/intltrade/exports/statehs', True, None),
    'us-census-bureau-timeseries/intltrade/exports/statehsexport': ('https://api.census.gov/data/timeseries/intltrade/exports/statehsexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/statenaics': ('https://api.census.gov/data/timeseries/intltrade/exports/statenaics', True, None),
    'us-census-bureau-timeseries/intltrade/exports/statenaicsexport': ('https://api.census.gov/data/timeseries/intltrade/exports/statenaicsexport', True, None),
    'us-census-bureau-timeseries/intltrade/exports/usda': ('https://api.census.gov/data/timeseries/intltrade/exports/usda', True, None),
    'us-census-bureau-timeseries/intltrade/exports/usdaexport': ('https://api.census.gov/data/timeseries/intltrade/exports/usdaexport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/enduse': ('https://api.census.gov/data/timeseries/intltrade/imports/enduse', True, None),
    'us-census-bureau-timeseries/intltrade/imports/enduseimport': ('https://api.census.gov/data/timeseries/intltrade/imports/enduseimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/hitech': ('https://api.census.gov/data/timeseries/intltrade/imports/hitech', True, None),
    'us-census-bureau-timeseries/intltrade/imports/hitechimport': ('https://api.census.gov/data/timeseries/intltrade/imports/hitechimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/hs': ('https://api.census.gov/data/timeseries/intltrade/imports/hs', True, None),
    'us-census-bureau-timeseries/intltrade/imports/hsimport': ('https://api.census.gov/data/timeseries/intltrade/imports/hsimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/naics': ('https://api.census.gov/data/timeseries/intltrade/imports/naics', True, None),
    'us-census-bureau-timeseries/intltrade/imports/naicsimport': ('https://api.census.gov/data/timeseries/intltrade/imports/naicsimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/porths': ('https://api.census.gov/data/timeseries/intltrade/imports/porths', True, None),
    'us-census-bureau-timeseries/intltrade/imports/porthsimport': ('https://api.census.gov/data/timeseries/intltrade/imports/porthsimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/sitc': ('https://api.census.gov/data/timeseries/intltrade/imports/sitc', True, None),
    'us-census-bureau-timeseries/intltrade/imports/sitcimport': ('https://api.census.gov/data/timeseries/intltrade/imports/sitcimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/statehs': ('https://api.census.gov/data/timeseries/intltrade/imports/statehs', True, None),
    'us-census-bureau-timeseries/intltrade/imports/statehsimport': ('https://api.census.gov/data/timeseries/intltrade/imports/statehsimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/statenaics': ('https://api.census.gov/data/timeseries/intltrade/imports/statenaics', True, None),
    'us-census-bureau-timeseries/intltrade/imports/statenaicsimport': ('https://api.census.gov/data/timeseries/intltrade/imports/statenaicsimport', True, None),
    'us-census-bureau-timeseries/intltrade/imports/usda': ('https://api.census.gov/data/timeseries/intltrade/imports/usda', True, None),
    'us-census-bureau-timeseries/intltrade/imports/usdaimport': ('https://api.census.gov/data/timeseries/intltrade/imports/usdaimport', True, None),
    'us-census-bureau-timeseries/poverty/histpov2': ('https://api.census.gov/data/timeseries/poverty/histpov2', True, None),
    'us-census-bureau-timeseries/poverty/saipe': ('https://api.census.gov/data/timeseries/poverty/saipe', True, None),
    'us-census-bureau-timeseries/poverty/saipe/schdist': ('https://api.census.gov/data/timeseries/poverty/saipe/schdist', True, None),
    'us-census-bureau-timeseries/pseo/earnings': ('https://api.census.gov/data/timeseries/pseo/earnings', True, None),
    'us-census-bureau-timeseries/pseo/flows': ('https://api.census.gov/data/timeseries/pseo/flows', True, None),
    'us-census-bureau-timeseries/qwi/rh': ('https://api.census.gov/data/timeseries/qwi/rh', True, None),
    'us-census-bureau-timeseries/qwi/sa': ('https://api.census.gov/data/timeseries/qwi/sa', True, None),
    'us-census-bureau-timeseries/qwi/se': ('https://api.census.gov/data/timeseries/qwi/se', True, None),
    'us-census-bureau-timeseries/soma': ('https://api.census.gov/data/timeseries/soma', True, None),
    'us-census-bureau-viusa': ('https://api.census.gov/data/2021/viusa', False, 2021),
    'us-census-bureau-viusb': ('https://api.census.gov/data/2021/viusb', False, 2021),
    'us-census-bureau-viusc': ('https://api.census.gov/data/2021/viusc', False, 2021),
    'us-census-bureau-viusd': ('https://api.census.gov/data/2021/viusd', False, 2021),
    'us-census-bureau-viuse': ('https://api.census.gov/data/2021/viuse', False, 2021),
    'us-census-bureau-viusf': ('https://api.census.gov/data/2021/viusf', False, 2021),
    'us-census-bureau-zbp': ('https://api.census.gov/data/2018/zbp', False, 2018),
}

# Cap on value-variables requested per dataset (a handful of ACS detailed
# tables expose ~37k variables; pulling all of them across geographies is not
# feasible in one run). Truncation is logged, never silent.
MAX_VARS = 120
# Cap on the number of (no-requires) geography levels pulled per dataset.
MAX_LEVELS = 8
# Census `get` accepts at most ~50 variables per request.
GET_LIMIT = 50

# Pseudo-variables that are query clauses, never data columns.
_SKIP_VARS = {"for", "in", "ucgid"}


@transient_retry()
def _get_json(url: str, params=None):
    """GET a Census endpoint and return parsed JSON.

    The data path returns an HTML 'Missing Key' / 'Invalid Key' page with HTTP
    200 when the key is absent or wrong (not a JSON error) — detect that and
    raise loudly so a misconfigured key fails the whole run instead of silently
    producing empty tables. Metadata endpoints need no key.
    """
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    ctype = resp.headers.get("content-type", "")
    if "json" not in ctype.lower():
        head = resp.text[:200].replace("\n", " ")
        if "Missing Key" in resp.text or "Invalid Key" in resp.text:
            raise RuntimeError(
                f"Census API key missing/invalid (set CENSUS_API_KEY): {url} -> {head}"
            )
        # Non-JSON, non-key page: treat as a permanent slice error.
        raise httpx.HTTPStatusError(
            f"non-JSON response ({ctype}) from {url}: {head}",
            request=resp.request, response=resp,
        )
    return resp.json()


def _classify_variables(variables: dict):
    """Split a dataset's variables.json into (always_cols, value_vars, has_time).

    always_cols are columns that must be in every chunk's `get`: required
    dimensions (required=='true', non-predicate-only) plus one geography
    identity column (GEO_ID or NAME) so each chunk's rows carry an id.
    value_vars are the remaining requestable data columns. has_time flags a
    required predicate-only 'time' dimension (timeseries), passed as a range.
    """
    required_dims, candidates = [], []
    has_time = False
    for name, meta in variables.items():
        if name in _SKIP_VARS:
            continue
        pred_only = meta.get("predicateOnly") is True
        required = meta.get("required") == "true"
        if name == "time":
            if required and pred_only:
                has_time = True
            continue
        if pred_only:
            continue
        if required:
            required_dims.append(name)
        else:
            candidates.append(name)
    # Surface a stable geography identity in every chunk.
    identity = [c for c in ("GEO_ID", "NAME") if c in variables]
    always = []
    for c in identity[:1] + required_dims:
        if c not in always:
            always.append(c)
    value_vars = [c for c in candidates if c not in always]
    # Keep identity-ish columns early; otherwise preserve catalog order.
    return always, value_vars, has_time


def _no_requires_levels(geography: dict):
    levels = []
    for g in geography.get("fips", []):
        if not g.get("requires"):
            name = g.get("name")
            if name:
                levels.append(name)
    return levels[:MAX_LEVELS] or ["us"]


def _emit_response(out, rows, vintage, geo_level, rid_start):
    """Melt one array-of-arrays response into EAV NDJSON lines. Returns the
    next row id. rows[0] is the header; each subsequent row is one observation
    whose cells share a row_id."""
    if not rows or len(rows) < 2:
        return rid_start
    header = rows[0]
    rid = rid_start
    for datarow in rows[1:]:
        for col, val in zip(header, datarow):
            if val is None:
                continue
            out.write(json.dumps({
                "vintage": vintage,
                "geo_level": geo_level,
                "row_id": rid,
                "variable": col,
                "value": str(val),
            }, separators=(",", ":")))
            out.write("\n")
        rid += 1
    return rid


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    base, is_ts, vintage = ENTITY_CONFIG[node_id]
    if not os.environ.get("CENSUS_API_KEY"):
        raise RuntimeError("CENSUS_API_KEY is not set; the Census data API requires a key")
    key = os.environ["CENSUS_API_KEY"]

    variables = _get_json(f"{base}/variables.json").get("variables", {})
    geography = _get_json(f"{base}/geography.json")
    always, value_vars, has_time = _classify_variables(variables)
    levels = _no_requires_levels(geography)

    if len(value_vars) > MAX_VARS:
        logger.warning(
            "%s: %d value variables exceeds MAX_VARS=%d; pulling first %d only",
            node_id, len(value_vars), MAX_VARS, MAX_VARS,
        )
        value_vars = value_vars[:MAX_VARS]

    budget = GET_LIMIT - len(always)
    if budget < 1:
        raise RuntimeError(f"{node_id}: required dimensions exceed get limit ({always})")
    chunks = [value_vars[i:i + budget] for i in range(0, len(value_vars), budget)] or [[]]

    base_params = {"key": key}
    if has_time:
        base_params["time"] = "from 1900 to 2099"

    rid = 0
    n_lines = 0
    n_ok = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for level in levels:
            for chunk in chunks:
                get_cols = always + chunk
                if not get_cols:
                    continue
                params = dict(base_params)
                params["get"] = ",".join(get_cols)
                params["for"] = f"{level}:*"
                url = base
                try:
                    rows = _get_json(url, params=params)
                except RuntimeError:
                    raise  # key misconfig — fail the whole run
                except (httpx.HTTPError, ValueError) as exc:
                    logger.warning(
                        "%s: slice level=%r chunk=%d failed (%s); skipping",
                        node_id, level, chunks.index(chunk), type(exc).__name__,
                    )
                    continue
                before = rid
                rid = _emit_response(out, rows, vintage, level, rid)
                if rid > before:
                    n_ok += 1
                    n_lines += sum(len(r) for r in rows[1:])
        print(f"  -> {asset}: {n_lines:,} cells from {n_ok} successful slice(s)")

    if n_ok == 0:
        raise RuntimeError(f"{node_id}: no data returned from any geography/variable slice")


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in ENTITY_CONFIG
]


# One published Delta table per dataset. The raw is uniform EAV NDJSON, so the
# transform is a thin re-type: cast vintage/row_id, expose a numeric value
# alongside the raw string (Census mixes numeric estimates with annotation
# codes), and drop blank cells. 0 rows fails the node by design.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                CAST(vintage AS INTEGER)   AS vintage,
                CAST(geo_level AS VARCHAR) AS geo_level,
                CAST(row_id AS BIGINT)     AS row_id,
                CAST(variable AS VARCHAR)  AS variable,
                CAST(value AS VARCHAR)     AS value,
                TRY_CAST(value AS DOUBLE)  AS value_num
            FROM "{s.id}"
            WHERE value IS NOT NULL AND TRIM(CAST(value AS VARCHAR)) <> ''
        ''',
    )
    for s in DOWNLOAD_SPECS
]
