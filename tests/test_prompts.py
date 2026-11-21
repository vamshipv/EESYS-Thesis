"""Tests for prompt templates and the chat-messages builder."""
from data.schema import EMOTIONS
from prompts import build_messages, build_prompt

TEXT = "I can't believe they cancelled the show."


def test_user_only_versions_match_build_prompt():
    for v in ("v1", "v2"):
        assert build_messages(TEXT, v) == [{"role": "user", "content": build_prompt(TEXT, v)}]


def test_v3_system_and_user():
    msgs = build_messages(TEXT, "v3")
    assert [m["role"] for m in msgs] == ["system", "user"]
    assert msgs[0]["content"] == ("You classify the emotion of a text. Answer in lowercase "
                                  "with exactly one word from: " + ", ".join(EMOTIONS) + ".")
    assert msgs[1]["content"] == TEXT


def test_custom_label_order():
    order = EMOTIONS[3:] + EMOTIONS[:3]
    for v in ("v2", "v3"):
        joined = "\n".join(m["content"] for m in build_messages(TEXT, v, labels=order))
        assert ", ".join(order) in joined
