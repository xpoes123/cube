"""Encoding tests: state and move encoders round-trip and have expected sizes."""

from cube.engine import SOLVED, Face, Move, Turn, parse_alg
from cube.training import (
    N_MOVES,
    STATE_FLAT_SIZE,
    decode_move,
    encode_history,
    encode_move,
    encode_state_flat,
    encode_state_indices,
)
from cube.training.split import split_by_source_id


def test_move_round_trip():
    for face in Face:
        for turn in Turn:
            m = Move(face, turn)
            assert decode_move(encode_move(m)) == m


def test_all_move_indices_unique():
    indices = {encode_move(Move(f, t)) for f in Face for t in Turn}
    assert len(indices) == N_MOVES
    assert min(indices) == 0
    assert max(indices) == N_MOVES - 1


def test_state_flat_size():
    out = encode_state_flat(SOLVED)
    assert len(out) == STATE_FLAT_SIZE


def test_state_flat_solved_one_hot_validity():
    """One-hot encoding for solved state: each position's block has exactly one 1."""
    out = encode_state_flat(SOLVED)
    # cp blocks: 8 × 8 = 64
    for i in range(8):
        block = out[i * 8 : (i + 1) * 8]
        assert sum(block) == 1
    # co blocks (offset 64)
    for i in range(8):
        block = out[64 + i * 3 : 64 + (i + 1) * 3]
        assert sum(block) == 1


def test_state_indices_round_trip_via_apply():
    """encode_state_indices returns the raw tuples; verify they match State fields."""
    state = SOLVED.apply_alg(parse_alg("R U R' U'"))
    enc = encode_state_indices(state)
    assert enc["cp"] == state.cp
    assert enc["co"] == state.co
    assert enc["ep"] == state.ep
    assert enc["eo"] == state.eo
    assert enc["eo_fb"] == state.eo_fb
    assert enc["eo_rl"] == state.eo_rl


def test_history_encoding():
    alg = parse_alg("R U R' U'")
    encoded = encode_history(tuple(alg))
    assert len(encoded) == 4
    assert all(0 <= i < N_MOVES for i in encoded)
    # Decoding back gives the same moves.
    assert tuple(decode_move(i) for i in encoded) == tuple(alg)


def test_split_by_source_id_is_deterministic():
    sids = [f"wca:{i}" for i in range(1000)]
    train1, val1, test1 = split_by_source_id(sids, seed=42)
    train2, val2, test2 = split_by_source_id(sids, seed=42)
    assert train1 == train2 and val1 == val2 and test1 == test2


def test_split_by_source_id_covers_all():
    sids = [f"wca:{i}" for i in range(1000)]
    train, val, test = split_by_source_id(sids, val_ratio=0.15, test_ratio=0.15)
    assert train | val | test == set(sids)
    assert not (train & val)
    assert not (train & test)
    assert not (val & test)


def test_split_by_source_id_proportions():
    sids = [f"wca:{i}" for i in range(10000)]
    train, val, test = split_by_source_id(sids, val_ratio=0.15, test_ratio=0.15)
    # Should be within a few percent of the target.
    assert 0.6 < len(train) / len(sids) < 0.8
    assert 0.10 < len(val) / len(sids) < 0.20
    assert 0.10 < len(test) / len(sids) < 0.20


def test_split_is_stable_when_adding_new_ids():
    """A new source ID added to the corpus doesn't shuffle existing assignments."""
    base = [f"wca:{i}" for i in range(100)]
    extended = base + [f"wca:new_{i}" for i in range(20)]
    train_base, val_base, test_base = split_by_source_id(base)
    train_ext, val_ext, test_ext = split_by_source_id(extended)
    # Every base ID must end up in the same split.
    for sid in base:
        if sid in train_base:
            assert sid in train_ext
        elif sid in val_base:
            assert sid in val_ext
        else:
            assert sid in test_ext
