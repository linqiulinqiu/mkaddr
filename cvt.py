#!/usr/bin/env python3

from chia.util.byte_types import hexstr_to_bytes
from blspy import G1Element
from chia.util.bech32m import encode_puzzle_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import puzzle_for_pk

pkcache = {}

pk0 = 'a64671eab9a99ee37657853cb3278fbb00edf9087a6172dac8db9c013605cc766ebcffe73db3df4cbd68db5c3ebd9890'

def create_address_by_pk(pk: str, address_prefix: str) -> str:
    jpk = f"{address_prefix}-{pk}"
    if jpk in pkcache:
        return pkcache[jpk]
    addr = encode_puzzle_hash(
        puzzle_for_pk(
            G1Element.from_bytes(hexstr_to_bytes(pk))
        ).get_tree_hash(),
        address_prefix
    )
    pkcache[jpk] = addr

if __name__ == "__main__":
    addr = create_address_by_pk(pk0,'xch')
    print('addr',addr)
