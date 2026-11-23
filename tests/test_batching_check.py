"""Tests for the batched scorer's padding and ordering (tokenizer only, no model weights)."""
from experiments.batching_check.batch_scoring import (pad_token_id, render_batch,
                                                      score_hf_batch)
from experiments.prompt_comparison.backends import hf_input_ids
from prompts import build_messages

TEXTS = ["Wow.", "I can't believe they did that to me again, I'm furious.",
         "This is the saddest thing I have read all week and I have read a lot of sad things."]


def test_left_padding_matches_unpadded():
    msgs = [build_messages(t, "v3") for t in TEXTS]
    b = render_batch(msgs)
    width = b["input_ids"].shape[1]
    assert len({len(hf_input_ids(m)[0]) for m in msgs}) == 3  # really different lengths
    for i, m in enumerate(msgs):
        ids = hf_input_ids(m)[0]
        n_pad = width - len(ids)
        assert b["n_pad"][i] == n_pad
        assert b["input_ids"][i, -1] == ids[-1]
        assert b["input_ids"][i, n_pad:].tolist() == ids.tolist()
        assert b["attention_mask"][i, :n_pad].sum() == 0
        assert b["attention_mask"][i, n_pad:].all()
        assert (b["input_ids"][i, :n_pad] == pad_token_id()).all()
    assert min(b["n_pad"]) == 0


def test_position_ids_of_real_tokens():
    b = render_batch([build_messages(t, "v3") for t in TEXTS])
    for i, n_pad in enumerate(b["n_pad"]):
        real = b["position_ids"][i, n_pad:].tolist()
        assert real == list(range(len(real)))


def test_output_order_equals_input_order():
    def fake(chunk):  # echoes each prompt's user text back as its "pred"
        return [{"pred": m[-1]["content"], "n_pad_tokens": 0} for m in chunk], 1.0

    msgs = [build_messages(f"text {i}", "v3") for i in range(7)]
    out = score_hf_batch(msgs, 3, score_fn=fake)
    assert [r["pred"] for r in out] == [m[-1]["content"] for m in msgs]
    assert [r["chunk_index"] for r in out] == [0, 0, 0, 1, 1, 1, 2]
    assert out[-1]["seconds_per_text"] == 1.0 and out[0]["seconds_per_text"] == 1 / 3


def test_pad_token_is_finetune_pad():
    from experiments.prompt_comparison.backends import hf_tokenizer
    assert hf_tokenizer().convert_ids_to_tokens(pad_token_id()) == "<|finetune_right_pad_id|>"
