"""Dataset-id selections for the nchs connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    '25m4-6qqq', '28df-2bwy', '2m93-xvra', '35bp-whkw', '367e-pucc', '36ue-xht5',
    '3apk-4u4f', '3h58-x6cd', '3j26-kg6d', '3nzu-udr9', '3yf8-kanr', '44rk-q6r2',
    '489q-934x', '4bc2-bbpq', '4q35-rqzk', '4va6-ph5s', '53g5-jf7x', '5h56-n989',
    '5pqj-rvh4', '6pdm-py4x', '6rkc-nb2q', '6rvp-rahv', '6tkz-y37d', '6tn6-vc33',
    '76vv-a7x8', '7aq9-prdf', '7ctq-myvs', '7pcd-2tnr', '7siw-u4fz', '89yk-m38d',
    '8ekv-ep3s', '8hzs-zshh', '8miz-siyd', '8pt5-q6wp', '8wmh-yzz9', '8xy9-ubqz',
    '95ax-ymtc', '9bhg-hcku', '9cpv-whbv', '9dzk-mvmi', '9gay-j69q', '9hdi-ekmb',
    '9j2v-jamp', 'a5a8-jsrq', 'a92y-5zud', 'aewi-gwni', 'be57-s94j', 'bi63-dtpu',
    'btv3-srcc', 'bxq8-mugm', 'daba-4vfq', 'ddsk-zebd', 'dmnu-8erf', 'dmzy-x2ad',
    'dtm2-meqi', 'e2d5-ggg7', 'e4ec-z5aa', 'e6fc-ccez', 'e8kx-wbww', 'epev-k6ss',
    'ga7k-kycn', 'gb4e-yj24', 'gebw-t5b7', 'ggsw-596z', 'gj3i-hsbz', 'gsea-w83j',
    'gu48-2cs8', 'gypc-kpgn', 'h3hw-hzvg', 'h7xa-837u', 'hc4f-j6nb', 'hdja-ybdg',
    'hk9y-quqm', 'hkhc-f7hg', 'hmz2-vwda', 'i667-sjhg', 'isx2-c2ii', 'it4f-frdc',
    'j7ym-uwqy', 'jb9g-gnvr', 'jqwm-z2g9', 'jvf6-ix4w', 'jwta-jxbg', 'jx6g-fdh6',
    'k8wy-p9cg', 'kk8c-wtm4', 'km5s-4339', 'kn79-hsxy', 'krhz-spsc', 'ks3g-spdg',
    'kusj-ex57', 'mc4y-cbbv', 'mnaa-qctp', 'mpx5-t7tu', 'mtgp-t7vw', 'muzy-jte6',
    'ncvk-7amm', 'nfuu-hu6j', 'nr4s-juj3', 'nt65-c7a7', 'p4r5-qsgs', 'p56q-jrxg',
    'p89x-xx88', 'pbkm-d27e', 'pj7m-y5uh', 'pjb2-jvdr', 'pqn7-e45s', 'q3t8-zr7t',
    'qfhf-uhaa', 'qgkx-mswu', 'r8kw-7aab', 'rdjz-vn2n', 'rg8a-czmp', 'rpvx-m2md',
    's54h-bixi', 's57w-7gbe', 'ss2j-8ajj', 'sz5x-j2c3', 'th9n-ghnr', 'tpcp-uiv5',
    'trpk-sp8z', 'u6jv-9ijr', 'uggs-hy5q', 'uzn2-cq9f', 'v2g4-wqg2', 'v6ab-adf5',
    'v7tk-n6v3', 'va5e-efw9', 'vc9m-u7tv', 'vdpk-qzpr', 'vsak-wrfu', 'w26f-tf3h',
    'w4cs-jspc', 'w9j2-ggv5', 'wd75-kcmv', 'wibz-pb5q', 'wpti-gvdi', 'wxz7-ekz9',
    'xb3p-q62w', 'xbxb-epbu', 'xkb8-kh2a', 'xkkf-xrst', 'xt86-xqxz', 'y268-sna3',
    'y5bj-9g5w', 'ycxr-emue', 'yib5-h3pw', 'yni7-er2q', 'ynw2-4viq', 'yrur-wghw',
    'yt7u-eiyg',
]
