"""Dataset-id selections for the nchs connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.

ENTITY_IDS is the accept-stage entity union (accepted NCHS data.cdc.gov dataset
4x4 ids). Regenerate from data/sources/nchs/work/entity_union.json when accept
changes.
"""


ENTITY_IDS = [
    '25m4-6qqq', '2m93-xvra', '2na8-fe6s', '35bp-whkw', '367e-pucc', '36ue-xht5',
    '3apk-4u4f', '3em4-f5qt', '3h58-x6cd', '3j26-kg6d', '3nzu-udr9', '3q3z-9ucr',
    '489q-934x', '4bc2-bbpq', '4q35-rqzk', '4ueh-89p9', '4va6-ph5s', '53g5-jf7x',
    '5pqj-rvh4', '65mz-jvh5', '6mjs-pnrx', '6pdm-py4x', '6rvp-rahv', '6tn6-vc33',
    '6vwk-ensg', '76vv-a7x8', '7aq9-prdf', '7ctq-myvs', '7siw-u4fz', '83mw-v57c',
    '8ekv-ep3s', '8hzs-zshh', '8miz-siyd', '8pt5-q6wp', '8wmh-yzz9', '8xy9-ubqz',
    '95ax-ymtc', '9bhg-hcku', '9cpv-whbv', '9dzk-mvmi', '9gay-j69q', '9hdi-ekmb',
    '9xc7-3a4q', '9z9x-g48e', 'a5a8-jsrq', 'a92y-5zud', 'aewi-gwni', 'be57-s94j',
    'btv3-srcc', 'daba-4vfq', 'dmnu-8erf', 'dmzy-x2ad', 'dnhi-s2bf', 'dtm2-meqi',
    'e2d5-ggg7', 'e4ec-z5aa', 'ezfr-g6hf', 'f3a8-hmpp', 'fdpm-fddm', 'ga7k-kycn',
    'gb4e-yj24', 'gebw-t5b7', 'ggsw-596z', 'gj3i-hsbz', 'gjsp-ircr', 'gpsd-ru5i',
    'gsea-w83j', 'gu48-2cs8', 'gypc-kpgn', 'h3hw-hzvg', 'h7xa-837u', 'hdja-ybdg',
    'hk9y-quqm', 'hkhc-f7hg', 'hmz2-vwda', 'i667-sjhg', 'ikd3-vynf', 'iqm3-hbev',
    'it4f-frdc', 'ite7-j2w7', 'j7ym-uwqy', 'jb9g-gnvr', 'jfbs-8cpp', 'jqg8-ycmh',
    'jqwm-z2g9', 'jwta-jxbg', 'k5dc-apj8', 'k8wy-p9cg', 'kk8c-wtm4', 'km5s-4339',
    'kn79-hsxy', 'krhz-spsc', 'ks3g-spdg', 'kusj-ex57', 'm74n-4hbs', 'mawz-airi',
    'mk5r-qxdg', 'mnaa-qctp', 'mpx5-t7tu', 'mqmc-4b9n', 'mtgp-t7vw', 'muzy-jte6',
    'mzhq-xsdd', 'ncvk-7amm', 'nfuu-hu6j', 'nr4s-juj3', 'p4r5-qsgs', 'p89x-xx88',
    'pj7m-y5uh', 'pjb2-jvdr', 'pqn7-e45s', 'q3t8-zr7t', 'q85u-gmyc', 'qfhf-uhaa',
    'qgkx-mswu', 'r5pw-bk5t', 'r8kw-7aab', 'rdjz-vn2n', 'rpvx-m2md', 's57w-7gbe',
    'siwp-yg6m', 'ss2j-8ajj', 'sz5x-j2c3', 'th9n-ghnr', 'tpcp-uiv5', 'trpk-sp8z',
    'u6jv-9ijr', 'uggs-hy5q', 'uzn2-cq9f', 'v2g4-wqg2', 'v728-xui5', 'v7tk-n6v3',
    'va5e-efw9', 'vsak-wrfu', 'w26f-tf3h', 'w4cs-jspc', 'wd75-kcmv', 'wibz-pb5q',
    'wpti-gvdi', 'wxz7-ekz9', 'xb3p-q62w', 'xkb8-kh2a', 'xkkf-xrst', 'xy7w-35q7',
    'y268-sna3', 'y5bj-9g5w', 'ycxr-emue', 'yib5-h3pw', 'yni7-er2q', 'ynw2-4viq',
    'ypxr-mz8e', 'yrur-wghw',
]
