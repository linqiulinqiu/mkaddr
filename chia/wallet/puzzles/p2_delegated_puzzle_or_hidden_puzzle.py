"""
Pay to delegated puzzle or hidden puzzle

In this puzzle program, the solution must choose either a hidden puzzle or a
delegated puzzle on a given public key.

The given public key is morphed by adding an offset from the hash of the hidden puzzle
and itself, giving a new so-called "synthetic" public key which has the hidden puzzle
hidden inside of it.

If the hidden puzzle path is taken, the hidden puzzle and original public key will be revealed
which proves that it was hidden there in the first place.

This roughly corresponds to bitcoin's taproot.
"""
import hashlib

from blspy import G1Element, PrivateKey
from clvm.casts import int_from_bytes

from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32

from .load_clvm import load_clvm
from .p2_conditions import puzzle_for_conditions

DEFAULT_HIDDEN_PUZZLE = Program.from_bytes(bytes.fromhex("ff0980"))

DEFAULT_HIDDEN_PUZZLE_HASH = DEFAULT_HIDDEN_PUZZLE.get_tree_hash()  # this puzzle `(x)` always fails

MOD = load_clvm("p2_delegated_puzzle_or_hidden_puzzle.clvm")

SYNTHETIC_MOD = load_clvm("calculate_synthetic_public_key.clvm")

GROUP_ORDER = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001


def calculate_synthetic_offset(public_key: G1Element, hidden_puzzle_hash: bytes32) -> int:
    blob = hashlib.sha256(bytes(public_key) + hidden_puzzle_hash).digest()
    offset = int_from_bytes(blob)
    offset %= GROUP_ORDER
    return offset


def calculate_synthetic_public_key(public_key: G1Element, hidden_puzzle_hash: bytes32) -> G1Element:
    r = SYNTHETIC_MOD.run([bytes(public_key), hidden_puzzle_hash])
    return G1Element.from_bytes(r.as_atom())

def puzzle_for_synthetic_public_key(synthetic_public_key: G1Element) -> Program:
    return MOD.curry(bytes(synthetic_public_key))


def puzzle_for_public_key_and_hidden_puzzle_hash(public_key: G1Element, hidden_puzzle_hash: bytes32) -> Program:
    synthetic_public_key = calculate_synthetic_public_key(public_key, hidden_puzzle_hash)

    return puzzle_for_synthetic_public_key(synthetic_public_key)

def puzzle_for_pk(public_key: G1Element) -> Program:
    r = SYNTHETIC_MOD.run([bytes(public_key), DEFAULT_HIDDEN_PUZZLE_HASH])
    synthetic_public_key = G1Element.from_bytes(r.as_atom())

    return MOD.curry(bytes(synthetic_public_key))

def solution_for_delegated_puzzle(delegated_puzzle: Program, solution: Program) -> Program:
    return Program.to([[], delegated_puzzle, solution])
