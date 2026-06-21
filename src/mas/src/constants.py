"""Dataset-id selections for the mas connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "d_023c0f38584a4b42587ebd74bb773db8",
    "d_0396bc943075a37d44c720ceb5be660a",
    "d_046ff8d521a218d9178178cfbfc45c2c",
    "d_0ca674c3af2fe1aa6a52e34327daafa8",
    "d_10036483fced016b239ce7d2ab175125",
    "d_17425483a24f4f07f6d36cb365d942ec",
    "d_1d49896b0fe9a5a8600c7c6ccaa76e2d",
    "d_2ae5431b27f1b2ce0a850d78e9fd4531",
    "d_3c62d5eed03c40aeafbb6d0fa324e976",
    "d_3e7180df0c6ac5684f5c3e52f66858e5",
    "d_4c6bd8b2c4aa7041a31f3ed0cd122c47",
    "d_4f73f4471a84f944ed37b651a8227ad8",
    "d_5c8e5801c2a64e2e6b16608296ef3e02",
    "d_5ee316e9f36b58ae54fbd68cf749c912",
    "d_5fe5a4bb4a1ecc4d8a56a095832e2b24",
    "d_6dd6162d59737d67edfb35026dfd58c2",
    "d_74edc21bac7b0aa8c4253b227a7540c3",
    "d_75d4534cdd518326f7355b2f951fb346",
    "d_7737cfb4e470d51b545d74e13d796bf1",
    "d_7ed3eccba609ac0bdfcf406d939bdb0b",
    "d_88ecfee25dff217289d1e588eb8c2649",
    # d_8dae...: dropped — byte-identical duplicate of d_1d49 (same SingStat
    # source table M920361, published twice on data.gov.sg).
    "d_92afecf58ad03196ff6a7abb7a03d631",
    "d_abcfd12381e7f8d175280d999cdb2dea",
    "d_ad861cfc83aa1f4ce6be45d31290dba8",
    "d_af0415517a3a3a94b3b74039934ef976",
    "d_b09aeaf8eb591c4bfe347b66148c6b53",
    "d_b40deadbdc470e97b9e16de99c5e6ee2",
    "d_c718a41412670c78793b8b7864a957c0",
    "d_cdd73fd4341b345fa4307e44d6f82175",
    "d_d4f7c9d15692b3c08aa9bc8bc56c0a72",
    "d_f357c61441e2850ca4eae05813ebd37b",
    "d_fd4b8728cb059c04fc0322199f4b2696",
]
