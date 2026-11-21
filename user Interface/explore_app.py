"""Minimal Streamlit viewer for ollama_calls_test.predict_proba (exploration only).

Run from anywhere:  streamlit run "master code/user Interface/explore_app.py"
(the theme in user Interface/.streamlit/ sits next to the script, so it loads from any folder)
Not the thesis demo interface (that is built last, on the real pipeline).
"""
import math
from dataclasses import asdict
from pathlib import Path

import inspect
import sys

import requests
import streamlit as st

CODE_ROOT = Path(__file__).resolve().parent.parent  # master code/
sys.path.insert(0, str(CODE_ROOT))  # so the test scripts in master code/ import

from data import load_samples  # noqa: E402
from ollama_calls_test import LABELS, predict_proba  # noqa: E402

MODEL = inspect.signature(predict_proba).parameters["model"].default

# Material 3 Expressive tokens: sage-green primary, sand tertiary, terracotta for errors.
CSS = """
<style>
:root {
  --background: #EDE7DA;
  --primary: #262522; --on-primary: #F3EEE3;
  --primary-container: #262522; --on-primary-container: #F3EEE3;
  --secondary-container: #D6DCC4; --on-secondary-container: #1F2414;
  --tertiary-container: #E9D9AE; --on-tertiary-container: #2A2000;
  --error-container: #EBCFC4; --on-error-container: #3A1408;
  --surface-container: #E4DDCD; --surface-container-high: #D9D1BF;
  --on-surface: #1E1D1A; --on-surface-variant: #5A564D; --outline: #C9C1AF;
}
.stApp { background: var(--background); }
.block-container { max-width: 760px; padding-top: 2.5rem; }
h1 { font-weight: 800; letter-spacing: -0.02em; color: var(--on-surface); }
.stButton > button, .stFormSubmitButton > button {
  border-radius: 999px; padding: 0.55rem 1.6rem; font-weight: 600;
  background: var(--primary); color: var(--on-primary); border: none;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: #3A3833; color: var(--on-primary);
}
.stTextArea textarea { border-radius: 20px; background: var(--surface-container); }
.card {
  background: var(--surface-container); border-radius: 28px;
  padding: 1.4rem 1.6rem; margin: 0.8rem 0;
}
.hero { background: var(--primary-container); color: var(--on-primary-container); }
.hero .label { font-size: 2.4rem; font-weight: 800; line-height: 1.1; }
.hero .sub { opacity: 0.8; font-size: 0.95rem; }
.chip {
  display: inline-block; border-radius: 999px; padding: 0.2rem 0.8rem;
  font-size: 0.85rem; font-weight: 600; margin-right: 0.4rem;
}
.chip.ok { background: var(--secondary-container); color: var(--on-secondary-container); }
.chip.bad { background: var(--error-container); color: var(--on-error-container); }
.chip.info { background: var(--tertiary-container); color: var(--on-tertiary-container); }
.row { display: flex; align-items: center; gap: 0.8rem; margin: 0.45rem 0; }
.row .name { width: 5.5rem; font-weight: 600; color: var(--on-surface-variant); }
.row .track {
  flex: 1; height: 14px; border-radius: 999px; background: var(--surface-container-high);
  overflow: hidden;
}
.row .fill { height: 100%; border-radius: 999px; background: #A39C8C; }
.row .fill.top { background: var(--primary); }
.row .pct { width: 3.8rem; text-align: right; font-variant-numeric: tabular-nums; }
.tok { font-family: ui-monospace, monospace; }
.section { font-weight: 700; margin-bottom: 0.4rem; color: var(--on-surface); }
.cm { width: 100%; border-collapse: separate; border-spacing: 4px; }
.cm th { font-weight: 600; color: var(--on-surface-variant); font-size: 0.85rem; text-align: center; }
.cm th.rowh { text-align: left; padding-right: 0.4rem; }
.cm td { text-align: center; border-radius: 12px; padding: 0.55rem 0; font-variant-numeric: tabular-nums; font-weight: 600; }
.stTabs [data-baseweb="tab"] { border-radius: 999px; padding: 0.3rem 1rem; }
</style>
"""


@st.cache_data
def load_dev_set() -> list[dict]:
    """Load the 60-text dev set (id, text, label)."""
    return [asdict(s) for s in load_samples("dev")]


@st.cache_data(show_spinner=False)
def cached_predict(text: str, model: str = MODEL) -> tuple[dict, list]:
    """Cache Ollama calls per (text, model) so re-renders don't re-query the model."""
    return predict_proba(text, model=model)


@st.cache_data(show_spinner=False)
def cached_predict_hf(text: str) -> dict:
    """HF transformers backend (bf16, offloaded). Imported lazily so torch only loads when used."""
    import llama_hf_test
    return llama_hf_test.predict_details(text)


def load_hf_model() -> None:
    """Load the bf16 model once; llama_hf_test.load_model is lru-cached per process."""
    import llama_hf_test
    llama_hf_test.load_model()


def bars_html(probs: dict) -> str:
    pred = max(probs, key=probs.get)
    rows = []
    for label in sorted(probs, key=probs.get, reverse=True):
        p = probs[label]
        cls = "fill top" if label == pred else "fill"
        rows.append(
            f'<div class="row"><span class="name">{label}</span>'
            f'<div class="track"><div class="{cls}" style="width:{p * 100:.1f}%"></div></div>'
            f'<span class="pct">{p:.1%}</span></div>'
        )
    return '<div class="card"><div class="section">Probability per emotion</div>' + "".join(rows) + "</div>"


def tokens_html(top: list) -> str:
    rows = "".join(
        f'<div class="row"><span class="name tok">{t["token"]!r}</span>'
        f'<span style="flex:1;color:var(--on-surface-variant)">logprob {t["logprob"]:.2f}</span>'
        f'<span class="pct">{math.exp(t["logprob"]):.1%}</span></div>'
        for t in top
    )
    return '<div class="card"><div class="section">Top first-token guesses</div>' + rows + "</div>"


def torch_oom_error() -> type:
    """torch.cuda.OutOfMemoryError if torch is already loaded, else a never-raised placeholder."""
    import sys
    torch = sys.modules.get("torch")
    return torch.cuda.OutOfMemoryError if torch else type("NoTorch", (Exception,), {})


def single_tab(rows: list[dict]) -> None:
    """Tab 1: classify one sentence and show probabilities + top tokens."""
    backend = st.radio(
        "Backend",
        ["Ollama · 4-bit", "Transformers · bf16 (slow)"],
        horizontal=True,
        help="Transformers loads the full Llama 3.1 8B Instruct, offloaded to CPU RAM and disk.",
    )
    use_hf = backend.startswith("Transformers")
    options = ["Type my own"] + [f'{r["label"]:<9} · {r["text"][:70]}' for r in rows]
    choice = st.selectbox("Dev-set sentence", options, index=0)
    picked = None if choice == options[0] else rows[options.index(choice) - 1]

    with st.form("predict"):
        text = st.text_area("Text", value=picked["text"] if picked else "", height=100)
        submitted = st.form_submit_button("Classify")

    if not submitted or not text.strip():
        return

    details = None
    try:
        if use_hf:
            with st.spinner("Loading Llama 3.1 8B in bf16 (first time takes minutes)…"):
                load_hf_model()
            with st.spinner("Running a forward pass…"):
                details = cached_predict_hf(text.strip())
            probs, top = details["probs"], details["top"]
        else:
            with st.spinner("Asking the model…"):
                probs, top = cached_predict(text.strip())
    except ImportError as e:
        st.error(f"Missing package for the transformers backend: {e}")
        return
    except OSError as e:  # gated repo, no token, missing files
        st.error(f"Couldn't load the model from Hugging Face: {e}")
        return
    except torch_oom_error() as e:
        st.error(f"Out of memory. Lower LLAMA_GPU_MEM / LLAMA_CPU_MEM and restart. ({e})")
        return
    except requests.ConnectionError:
        st.error("Can't reach Ollama at localhost:11434. Is `ollama serve` running?")
        return
    except (KeyError, IndexError) as e:
        st.error(f"Unexpected Ollama response (no logprobs?): {e!r}")
        return

    pred = max(probs, key=probs.get)
    chips = f'<span class="chip info">{probs[pred]:.0%} confident</span>'
    if details:
        chips += (
            f'<span class="chip info">{details["seconds"]:.1f}s forward pass</span>'
            f'<span class="chip info">label mass {details["label_mass"]:.0%}</span>'
        )
    if picked and picked["text"] == text.strip():
        ok = pred == picked["label"]
        chips += (
            f'<span class="chip {"ok" if ok else "bad"}">'
            f'{"correct" if ok else "wrong"} · true: {picked["label"]}</span>'
        )
    st.markdown(
        f'<div class="card hero"><div class="sub">Predicted emotion</div>'
        f'<div class="label">{pred}</div><div style="margin-top:0.7rem">{chips}</div></div>',
        unsafe_allow_html=True,
    )
    if sum(probs.values()) == 0:
        st.warning("No label tokens in the top-20 logprobs, so there is no real prediction.")
    st.markdown(bars_html(probs), unsafe_allow_html=True)
    st.markdown(tokens_html(top), unsafe_allow_html=True)


def run_dev_set(rows: list[dict]) -> list[dict]:
    """Predict every dev-set text; returns rows with `pred` added (None if no label token)."""
    results = []
    bar = st.progress(0.0, text="Classifying dev set…")
    for i, row in enumerate(rows, 1):
        probs, _ = cached_predict(row["text"].strip())
        pred = max(probs, key=probs.get) if sum(probs.values()) > 0 else None
        results.append({**row, "model": MODEL, "pred": pred, "conf": probs[pred] if pred else 0.0})
        bar.progress(i / len(rows), text=f"Classifying dev set… {i}/{len(rows)}")
    bar.empty()
    return results


def macro_f1(results: list[dict]) -> float:
    """Unweighted mean of per-emotion F1 (no-prediction rows count as misses)."""
    f1s = []
    for l in LABELS:
        tp = sum(r["label"] == l and r["pred"] == l for r in results)
        fp = sum(r["label"] != l and r["pred"] == l for r in results)
        fn = sum(r["label"] == l and r["pred"] != l for r in results)
        f1s.append(2 * tp / (2 * tp + fp + fn) if tp else 0.0)
    return sum(f1s) / len(f1s)


def matrix_html(results: list[dict]) -> str:
    """Confusion matrix as an HTML table: rows = true label, columns = predicted."""
    cols = LABELS + (["none"] if any(r["pred"] is None for r in results) else [])
    head = "".join(f"<th>{c[:4]}</th>" for c in cols)
    body = []
    for t in LABELS:
        row_total = sum(r["label"] == t for r in results) or 1
        cells = []
        for c in cols:
            p = None if c == "none" else c
            n = sum(r["label"] == t and r["pred"] == p for r in results)
            a = n / row_total
            fg = "#F3EEE3" if a > 0.5 else "var(--on-surface)"
            ring = "box-shadow: inset 0 0 0 2px #262522;" if c == t else ""
            cells.append(
                f'<td style="background: rgba(38,37,34,{a * 0.9:.2f}); color:{fg}; {ring}">'
                f'{n if n else "·"}</td>'
            )
        body.append(f'<tr><th class="rowh">{t}</th>{"".join(cells)}</tr>')
    return (
        '<div class="card"><div class="section">Confusion matrix '
        '<span style="font-weight:400;color:var(--on-surface-variant)">'
        "· rows = true, columns = predicted</span></div>"
        f'<table class="cm"><tr><th></th>{head}</tr>{"".join(body)}</table></div>'
    )


def matrix_tab(rows: list[dict]) -> None:
    """Tab 2: run the whole dev set and show a confusion matrix."""
    st.caption(f"Runs all {len(rows)} dev-set texts. Cached calls are reused, so reruns are fast.")
    if st.button("Run confusion matrix"):
        try:
            st.session_state["cm_results"] = run_dev_set(rows)
        except requests.ConnectionError:
            st.error("Can't reach Ollama at localhost:11434. Is `ollama serve` running?")
            return
        except (KeyError, IndexError) as e:
            st.error(f"Unexpected Ollama response (no logprobs?): {e!r}")
            return

    results = st.session_state.get("cm_results")
    if results and results[0].get("model") != MODEL:
        results = None  # stale results from another model
    if not results:
        return

    acc = sum(r["pred"] == r["label"] for r in results) / len(results)
    none = sum(r["pred"] is None for r in results)
    chips = (
        f'<span class="chip info">accuracy {acc:.0%}</span>'
        f'<span class="chip info">macro-F1 {macro_f1(results):.2f}</span>'
        f'<span class="chip info">{len(results)} texts</span>'
    )
    if none:
        chips += f'<span class="chip bad">{none} without a label token</span>'
    st.markdown(f'<div style="margin:0.6rem 0">{chips}</div>', unsafe_allow_html=True)
    st.markdown(matrix_html(results), unsafe_allow_html=True)

    wrong = [r for r in results if r["pred"] != r["label"]]
    with st.expander(f"Misclassified texts ({len(wrong)})"):
        for r in wrong:
            st.markdown(
                f'<span class="chip ok">true: {r["label"]}</span>'
                f'<span class="chip bad">pred: {r["pred"] or "none"}</span> {r["text"]}',
                unsafe_allow_html=True,
            )


def main() -> None:
    st.set_page_config(page_title="Emotion check", page_icon="🌿", layout="centered")
    st.html(CSS)  # style-only HTML is applied globally (Streamlit >= 1.33)
    if "eesys-thesis" not in sys.prefix:
        st.warning(
            f"Running on {sys.executable}, not the thesis env, so the Transformers backend "
            "won't work. Stop this server and start it with `user Interface/run_app.ps1`."
        )
    st.title("Emotion check")
    st.caption("Exploration viewer · Llama 3.1 8B via Ollama · first-token logprobs")

    rows = load_dev_set()
    tab1, tab2 = st.tabs(["Single text", "Confusion matrix"])
    with tab1:
        single_tab(rows)
    with tab2:
        matrix_tab(rows)


if __name__ == "__main__":
    main()
