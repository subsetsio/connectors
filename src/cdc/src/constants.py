"""Dataset-id selections for the cdc connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


# Datasets too large to pull via the full bulk-CSV export. Row counts were
# measured directly against the SODA count endpoint (see the connector notes);
# each of these exceeds 50 million rows, so the `/rows.csv` export streams for
# hours under Socrata's throttled anonymous pool and would publish as a
# multi-GB Delta table — impractical for a full every-run re-pull. The fetch
# fn fails these fast (rather than stalling the sequential DAG for hours), and
# they are covered by run-level spec waivers. Revisit only if an incremental /
# partitioned fetch path is added for the giant environmental daily series.
#   96sd-hxdt  136,267,479  Daily Census Tract-Level PM2.5 Concentrations 2016-2020
#   hf2a-3ebq  136,267,479  (twin of 96sd-hxdt)
#   n8mc-b4w4  106,219,500
#   vbim-akqf  106,219,500  (twin of n8mc-b4w4)
#   b72x-p96c   61,156,480
#   vpk8-vfhm   61,156,480  (twin of b72x-p96c)
OVERSIZED_IDS = frozenset({
    "96sd-hxdt",
    "hf2a-3ebq",
    "n8mc-b4w4",
    "vbim-akqf",
    "b72x-p96c",
    "vpk8-vfhm",
})


ENTITY_IDS = [
    "24w5-nppr", "24xb-jxbc", "25m4-6qqq", "29hc-w46k", "2den-c3u2", "2dwv-vfam", "2ew6-ywp6",
    "2m7c-st88", "2m93-xvra", "2nf2-f75n", "2qxe-cmv4", "2snk-eav4", "2t2r-sf6s", "2v3t-r3np",
    "2vtj-68zm", "2yum-eg9f", "32fd-hyzc", "34p9-h4us", "35bp-whkw", "367e-pucc", "36ue-xht5",
    "373s-ayzu", "3apk-4u4f", "3bmy-cyyd", "3crz-97tw", "3h58-x6cd", "3j26-kg6d", "3myw-4j4q",
    "3nij-2pw6", "3nnj-6kcn", "3nzu-udr9", "3pbe-qh9z", "3q3z-9ucr", "3rge-nu2a", "3svv-v5nh",
    "3vxk-q2jk", "3x54-3thk", "3yf8-kanr", "45cq-cw4i", "489q-934x", "48mw-5apu", "4bc2-bbpq",
    "4bdk-kyzv", "4day-mt2f", "4g6p-3ed6", "4khb-4xch", "4q35-rqzk", "4r2x-hcfq", "4r3g-hv9c",
    "4tme-u33f", "4va6-ph5s", "4yy2-qa9v", "4yyu-3s69", "52ds-xw49", "52kb-ccu2", "533q-q3rp",
    "53g5-jf7x", "53mz-4zqd", "55uq-699y", "55yu-xksw", "58s6-s24x", "5c6r-xi2t", "5dqz-y4ea",
    "5eh7-pjx8", "5i5k-6cmh", "5iuf-feyd", "5jp2-pgaw", "5pqj-rvh4", "5una-zw6e", "5wdd-3g8t",
    "5xkq-dg7x", "66i6-hisz", "68sm-zh95", "6ie8-bpiy", "6jg4-xsqq", "6jwg-4k37", "6mjs-pnrx",
    "6nue-dx9c", "6p3a-6xr9", "6pdm-py4x", "6qm2-fbrx", "6rvp-rahv", "6ryw-hetw", "6svj-q4zv",
    "6tn6-vc33", "6uy5-4d9d", "6x7h-usvx", "6zuv-bn3z", "735e-byxc", "759d-qk63", "76vv-a7x8",
    "783t-9j9i", "7aq9-prdf", "7b9s-s8ck", "7cmc-7y5g", "7ctq-myvs", "7gnu-j6js", "7mra-9cq9",
    "7nbz-eajm", "7rci-qmm9", "7rih-tqi5", "7siw-u4fz", "7vg3-e5u2", "7xhe-mv2e", "7xva-uux8",
    "82nv-dn3y", "83mw-v57c", "83ng-twza", "84rx-ksgd", "88eg-qzed", "89qs-mr7i", "89x6-rgq5",
    "8ame-63pc", "8bda-nhxv", "8cyw-fici", "8dyx-9z99", "8ekv-ep3s", "8fbp-accd", "8gpz-j2fr",
    "8hus-y5nc", "8hxn-cvik", "8hzs-zshh", "8jp2-ecz7", "8miz-siyd", "8mrp-rmkw", "8na9-qgz7",
    "8nyy-xsq7", "8pt5-q6wp", "8v6a-z6zq", "8w4j-reb4", "8wmh-yzz9", "8xkx-amqh", "8yup-c35n",
    "8zbb-qqwc", "8zea-kwnt", "92ri-yjps", "94wp-9pid", "95ax-ymtc", "95m5-agj4", "96sd-hxdt",
    "97bc-2r74", "986w-8kut", "9976-4iqj", "9axm-gjt8", "9b5z-wnve", "9bhg-hcku", "9cpv-whbv",
    "9d9z-vf8f", "9dzk-mvmi", "9gay-j69q", "9hdi-ekmb", "9ikp-t8tw", "9j2v-jamp", "9k8a-cbgx",
    "9kbf-icdi", "9mw4-6adp", "9tjt-seye", "9umn-c3jf", "9vgf-r2z6", "9x7v-wy9u", "9xb7-9z99",
    "9xc7-3a4q", "9xt5-u42s", "9y49-tura", "a35h-9yn4", "a3gi-4phs", "a5a8-jsrq", "a92y-5zud",
    "a93x-tfzm", "a9xa-yrhn", "abgz-qs4g", "abzs-b3gw", "aemk-wcbf", "aemt-mg7g", "aetd-68ew",
    "aewi-gwni", "agqb-jgkw", "agz7-4mvg", "ahrf-yqdt", "ai6z-tcin", "akkj-j5ru", "akvg-8vrb",
    "amjr-ph5r", "ar8q-3jhn", "aspp-bzzu", "at7e-uhkc", "atcp-73re", "b5wa-ze9s", "b6ny-6cd5",
    "b6sy-qq3u", "b6uq-hdgz", "b72x-p96c", "b7pe-5nws", "b8tp-jsmh", "bdyv-z46f", "be57-s94j",
    "bigw-pgk2", "biid-68vb", "binw-6h77", "bk9t-cq4b", "bkcm-ybyk", "brsb-akdp", "bst4-hnte",
    "btv3-srcc", "bugr-bbfr", "bumh-rgsq", "bw3b-karf", "bwx3-gx66", "bx8m-di6q", "bxq8-mugm",
    "bytj-42x7", "bz96-hgr8", "c76y-7pzg", "c7b2-4ecy", "cah8-bpvk", "cchw-gdwa", "cf5u-bm9w",
    "ch5i-63ve", "ch83-ush6", "chmz-4uae", "cj8b-94cj", "cpdh-8cna", "cr56-k9wj", "cw4r-vcr3",
    "cwsq-ngmh", "d2rk-yvas", "d2tw-32xv", "d3i6-k6z5", "d4v7-r7ct", "d6p8-wqjm", "d89q-62iu",
    "d9u6-mdu6", "daba-4vfq", "de4p-4g3k", "djj9-kh3p", "dkyk-v5f5", "dmnu-8erf", "dmzy-x2ad",
    "dnnu-xtkq", "dp9i-idru", "dttw-5yxu", "duw2-7jbt", "dwmy-m9r6", "e28h-tx85", "e2a5-s9pr",
    "e2d5-ggg7", "e539-uadk", "e5zk-7tx5", "e6et-eg6c", "e6fc-ccez", "eanj-9nie", "eav7-hnsx",
    "eb4y-d4ic", "edkk-ze78", "ee48-w5t6", "ee83-ukst", "efqg-e273", "ekcb-r85s", "em5e-5hvn",
    "en3s-hzsr", "epbn-9bv3", "eudc-n39h", "ewpg-rz7g", "ex65-qa8z", "exs3-hbne", "ey8b-ejrf",
    "eze9-ahe5", "ezfr-g6hf", "f3a8-hmpp", "f3zz-zga5", "fdpm-fddm", "ffbi-is3j", "fh5p-vkps",
    "fhky-rtsk", "fj6i-3v3k", "fpsi-y8tj", "fu4u-a9bh", "fvm6-ic5r", "fxwg-3udm", "fztq-uwup",
    "g2ck-geg5", "g3c9-wbme", "g4jn-64pd", "g57i-yx3r", "g5fg-bgtw", "g653-rqe2", "g6fu-zp23",
    "ga7k-kycn", "gb4e-yj24", "gb67-x49c", "gd4x-jyhw", "gebw-t5b7", "ggsw-596z", "gj3i-hsbz",
    "gjsp-ircr", "gpsd-ru5i", "gr26-95h2", "gsea-w83j", "gu48-2cs8", "gvsb-yw6g", "gypc-kpgn",
    "h3ej-a9ec", "h3hw-hzvg", "h3kf-bqpq", "h3my-dzpj", "h4pd-hu6x", "h7pm-wmjc", "h7xa-837u",
    "hbbg-vj7f", "hbpe-6r8n", "hc4f-j6nb", "hdja-ybdg", "hea5-6w9c", "hf2a-3ebq", "hgv5-3wrn",
    "hgyx-uuxz", "hhvg-83jq", "hj2x-85ya", "hk9y-quqm", "hkhc-f7hg", "hkr7-mcee", "hksd-2xuw",
    "hky2-3tpn", "hmye-mqgq", "hmz2-vwda", "hn4x-zwk7", "htq2-rqve", "hwk8-wu83", "hwyy-s2tt",
    "hyak-nxqs", "i43m-djm6", "i46a-9kgh", "i667-sjhg", "i6u4-y3g4", "i8t6-whzd", "ijqb-a7ye",
    "iqm3-hbev", "ircd-wk4g", "it4f-frdc", "ite7-j2w7", "ithv-4e9m", "itia-u6fu", "iu3b-5ngj",
    "iuq5-y9ct", "ivdz-qhnr", "iwxc-qftf", "ix4g-rt8v", "iyx3-z4r8", "j32a-sa6u", "j7ym-uwqy",
    "j9g8-acpt", "jb9g-gnvr", "jbhn-e8xn", "jbmi-9jqv", "jbxj-8pnr", "jfbs-8cpp", "jiwm-ppbh",
    "jjpx-mxt8", "jk8p-fqhn", "jkcx-ndu8", "jnru-aqxk", "jqg8-ycmh", "jqwm-z2g9", "jr4g-zdpg",
    "jr58-6ysp", "ju63-2fep", "judz-8etw", "jwta-jxbg", "jxu8-x79m", "jz6n-v26y", "k4cb-dxd7",
    "k5dc-apj8", "k62p-6esq", "k87d-gv3u", "k8w5-7ju6", "k8wy-p9cg", "k9zj-b28y", "kebt-3t25",
    "kee5-23sr", "ker6-gs6z", "kgsi-35re", "kh8y-3es6", "khic-yj26", "kipu-qxy8", "kk8c-wtm4",
    "kkix-nh4v", "km4m-vcsb", "km5s-4339", "kmap-fsfn", "kmvs-jkvx", "kmxt-xb3i", "kn79-hsxy",
    "knu9-e7pg", "kp49-9dp8", "kpbd-vsd5", "krhz-spsc", "krqc-563j", "ks3g-spdg", "ksfb-ug5d",
    "ku7p-zn4c", "kusj-ex57", "kvib-3txy", "kwbr-syv2", "kxvg-q6s7", "m35w-spkz", "m74n-4hbs",
    "mb5y-ytti", "mcdp-77g7", "mcvh-596h", "mdwz-ar4b", "mfvi-hkb9", "mk5r-qxdg", "mnaa-qctp",
    "mpgq-jmmr", "mpx5-t7tu", "mqmc-4b9n", "mr4u-abm2", "mrip-2k2a", "msnx-y6hi", "mtc3-kq6r",
    "mtgp-t7vw", "mtpu-urpp", "muep-c3qd", "muzy-jte6", "mwkk-wzmy", "mzhq-xsdd", "n2x4-haas",
    "n2zz-25mk", "n322-ce6f", "n5b3-jati", "n5qs-vw3x", "n8mc-b4w4", "n97r-u9uh", "ncvk-7amm",
    "ndai-i7s4", "ne52-uraz", "nfuu-hu6j", "ngaa-n8ir", "nkr7-scx6", "nqu5-vn7d", "nr42-fsyk",
    "nr4s-juj3", "nsxk-tvbw", "ntaa-dtex", "nu3s-3dwd", "nw2y-v4gm", "p4r5-qsgs", "p5x4-u35c",
    "p89x-xx88", "paqx-33a8", "pbq2-7wr2", "pd5g-36s6", "ph8r-wzxn", "piju-vf3p", "pj7m-y5uh",
    "pjb2-jvdr", "ppmd-3u54", "pqn7-e45s", "pqpp-u99h", "psx4-wq38", "pttf-ck53", "pvk6-8bzd",
    "q2dj-esu7", "q3t8-zr7t", "q84f-e68r", "q8ig-wwk9", "q8j9-sue7", "q9mh-h2tw", "qcai-zfj9",
    "qeq7-f3ir", "qeru-k2y2", "qfhf-uhaa", "qfiq-jir6", "qgfq-p8ib", "qktg-6dmb", "qnzd-25i4",
    "qr63-vqq5", "qtbi-xd4i", "qve4-fp9c", "qvzb-qs6p", "qz99-wyhv", "r229-z6ma", "r85e-hjic",
    "r8kw-7aab", "rbrz-y4zd", "rcdh-n3ej", "rdjz-vn2n", "rdmq-nq56", "rdng-ki53", "rezz-ypcg",
    "rgnm-fkqb", "rh2h-3yt2", "rhwp-grxi", "rksx-33p3", "rnah-xd9n", "rnvb-cpxx", "rppv-wbiv",
    "rpvx-m2md", "rq85-buyi", "rsk5-566a", "rsk8-spa7", "rtjs-ain8", "rw4v-h7j9", "s57w-7gbe",
    "s5a6-fn5p", "s6p7-fvbw", "s85h-9xpy", "saz5-9hgg", "scrf-8d7w", "sd8v-uq83", "seuz-s2cv",
    "shc3-fzig", "si7g-c2bs", "siwp-yg6m", "sixg-saap", "sjpm-fk4b", "skkh-jsrk", "sks5-7yq7",
    "snev-n7vb", "snkv-n8f6", "ss2j-8ajj", "ssz5-s49e", "sumd-iwm8", "sw5n-wg2p", "swc5-untb",
    "sz5x-j2c3", "t6u2-f84c", "tczv-qfsi", "tdbk-8ubw", "tdge-ieq8", "tfcp-ufzp", "tfu6-pjxh",
    "th8y-thx5", "thir-stei", "tpcp-uiv5", "tqwu-4a7k", "trpk-sp8z", "tscn-ryh9", "tt3f-rr33",
    "tug7-57z5", "twtn-mxqy", "ty79-wym3", "u22r-ndns", "u2nj-bus9", "u6jv-9ijr", "u7e4-s8zi",
    "ua33-yiiu", "ua7e-t2fy", "uc9k-vc2j", "udwr-3en6", "uggs-hy5q", "ugzv-zzdr", "ui6g-vumy",
    "ukww-au2k", "unsk-b7fc", "uny6-e3dx", "uqxy-gepz", "ut5n-bmc3", "uuui-fh3m", "uw7a-a5t8",
    "uxgd-cqqc", "uxwq-vny5", "uzn2-cq9f", "v22g-tzpk", "v246-z5tb", "v2g4-wqg2", "v2mh-3yzr",
    "v2pi-w3up", "v2zw-2d2v", "v4tm-h8pe", "v58w-vynu", "v728-xui5", "v7tk-n6v3", "va5e-efw9",
    "vba9-s8jp", "vbim-akqf", "vdz4-qrri", "vdzy-6i9v", "vfj2-bfuw", "vfmq-diru", "vgc8-iyc4",
    "vh55-3he6", "vhcj-3k53", "vjzj-u7u8", "vkwg-yswv", "vmgc-uspy", "vncy-2ds7", "vpk8-vfhm",
    "vq7a-fvin", "vqyf-z2g3", "vsak-wrfu", "vugp-mqip", "vuhn-dxkt", "vutn-jzwm", "vutr-sfkh",
    "vyry-2yfg", "w26f-tf3h", "w46e-8kr3", "w4cs-jspc", "w76m-r924", "w79a-dgrh", "w9h3-6bpu",
    "w9zu-fywh", "wan8-w4er", "wd75-kcmv", "wff4-m3q3", "wgvr-7mvz", "whhs-7a5d", "wi5c-cscz",
    "wibz-pb5q", "wpti-gvdi", "wrev-kwxu", "wrrd-u9wx", "wtw5-4wi3", "wxz7-ekz9", "wzwe-859x",
    "x4dz-rafm", "x5j9-wybp", "x66v-w5ka", "x6ag-8y7r", "x8jf-txib", "x8ni-jytx", "x9gk-5huc",
    "xerk-pcm8", "xf9s-d895", "xgy8-wnft", "xkb8-kh2a", "xkkf-xrst", "xnjn-rdmd", "xpxn-rzgz",
    "xssa-9qw5", "xsta-sbh5", "xt86-xqxz", "xvdv-hq7x", "xx8k-iu94", "xyst-f73f", "y268-sna3",
    "y4ft-s73h", "y52v-k5rz", "y5bj-9g5w", "yctb-fv7w", "ycxr-emue", "yhkp-cczf", "yib5-h3pw",
    "yjkw-uj5s", "ymmh-divb", "yn8z-e2cm", "yni7-er2q", "ynw2-4viq", "ype6-idgy", "ypxr-mz8e",
    "yrur-wghw", "ysd3-txwj", "yt7u-eiyg"
]
