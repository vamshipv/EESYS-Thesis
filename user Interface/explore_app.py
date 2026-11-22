"""Minimal Streamlit viewer for the prompt versions v1/v2/v3 (exploration only).

Scores with experiments/prompt_comparison/backends.py, so it uses the same prompts, label-token
rule and label mass as the prompt-comparison runs.

Run from anywhere:  streamlit run "master code/user Interface/explore_app.py"
(the theme in user Interface/.streamlit/ sits next to the script, so it loads from any folder)
Not the thesis demo interface (that is built last, on the real pipeline).
"""
import html
import sys
from dataclasses import asdict
from pathlib import Path

import requests
import streamlit as st

CODE_ROOT = Path(__file__).resolve().parent.parent  # master code/
sys.path.insert(0, str(CODE_ROOT))  # so the test scripts in master code/ import

from data import EMOTIONS as LABELS, load_samples  # noqa: E402
from experiments.prompt_comparison.backends import score_ollama  # noqa: E402
from prompts import PROMPTS_DIR, build_messages  # noqa: E402

MODEL = "llama3.1"  # Ollama model name
VERSIONS = sorted(p.stem for p in PROMPTS_DIR.glob("v*.txt"))
VERSION_NOTES = {
    "v1": "original prompt",
    "v2": "v1 + answer in lowercase",
    "v3": "v2 wording as a system message, text only in the user message",
}

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
.msg { font-family: ui-monospace, monospace; font-size: 0.85rem; white-space: pre-wrap;
  background: var(--surface-container-high); border-radius: 14px; padding: 0.6rem 0.8rem; margin: 0.3rem 0; }
.role { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--on-surface-variant); }
.cmp { width: 100%; border-collapse: collapse; }
.cmp th, .cmp td { text-align: left; padding: 0.35rem 0.4rem; border-bottom: 1px solid var(--outline); }
.cmp th { font-size: 0.85rem; color: var(--on-surface-variant); }
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
def cached_predict(text: str, version: str, model: str = MODEL) -> dict:
    """Ollama score per (text, prompt version, model); cached so re-renders don't re-query."""
    return score_ollama(build_messages(text, version), model=model)


@st.cache_data(show_spinner=False)
def cached_predict_hf(text: str, version: str) -> dict:
    """HF transformers backend (bf16, offloaded). Imported lazily so torch only loads when used."""
    from experiments.prompt_comparison.backends import score_hf
    return score_hf(build_messages(text, version))


def predict(text: str, version: str, use_hf: bool) -> dict:
    """Score one text with one prompt version on the chosen backend."""
    return cached_predict_hf(text, version) if use_hf else cached_predict(text, version)


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
        f'<div class="row"><span class="name tok">{html.escape(repr(t["token"]))}</span>'
        f'<span style="flex:1"></span><span class="pct">{t["prob"]:.1%}</span></div>'
        for t in top
    )
    return '<div class="card"><div class="section">Top first-token guesses</div>' + rows + "</div>"


def prompt_html(text: str, version: str) -> str:
    """The chat messages actually sent for this prompt version."""
    msgs = "".join(
        f'<div class="role">{m["role"]}</div><div class="msg">{html.escape(m["content"])}</div>'
        for m in build_messages(text, version)
    )
    return f'<div class="card"><div class="section">Prompt sent · {version}</div>{msgs}</div>'


def compare_html(results: dict[str, dict], true_label: str | None) -> str:
    """One row per prompt version: prediction, confidence, label mass, top token."""
    head = ("<tr><th>prompt</th><th>prediction</th><th>confidence</th>"
            "<th>label mass</th><th>top token</th></tr>")
    rows = []
    for v, r in results.items():
        chip = ""
        if true_label:
            ok = r["pred"] == true_label
            chip = f' <span class="chip {"ok" if ok else "bad"}">{"right" if ok else "wrong"}</span>'
        top = r["top_tokens"][0]
        rows.append(f'<tr><td><b>{v}</b> <span style="color:var(--on-surface-variant)">'
                    f'{VERSION_NOTES.get(v, "")}</span></td><td><b>{r["pred"]}</b>{chip}</td>'
                    f'<td>{r["probs"][r["pred"]]:.0%}</td><td>{r["label_mass"]:.0%}</td>'
                    f'<td class="tok">{html.escape(repr(top["token"]))} {top["prob"]:.0%}</td></tr>')
    return ('<div class="card"><div class="section">All prompt versions</div>'
            f'<table class="cmp">{head}{"".join(rows)}</table></div>')


def torch_oom_error() -> type:
    """torch.cuda.OutOfMemoryError if torch is already loaded, else a never-raised placeholder."""
    import sys
    torch = sys.modules.get("torch")
    return torch.cuda.OutOfMemoryError if torch else type("NoTorch", (Exception,), {})


def single_tab(rows: list[dict], version: str) -> None:
    """Tab 1: classify one sentence with the chosen prompt; compare with the other versions."""
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

    if submitted:  # keep the last classified text, so changing prompt/backend re-shows it
        st.session_state["shown_text"] = text.strip()
    text = st.session_state.get("shown_text", "")
    if not text:
        return

    try:
        if use_hf:
            with st.spinner("Loading Llama 3.1 8B in bf16 (first time takes minutes)…"):
                load_hf_model()
        with st.spinner("Asking the model…"):
            details = predict(text.strip(), version, use_hf)
    except ImportError as e:
        st.error(f"Missing package for the transformers backend: {e}")
        return
    except requests.ConnectionError:  # requests errors before OSError: they subclass it
        st.error("Can't reach Ollama at localhost:11434. Is `ollama serve` running?")
        return
    except requests.RequestException as e:
        st.error(f"Ollama request failed: {e}")
        return
    except OSError as e:  # gated repo, no token, missing files
        st.error(f"Couldn't load the model from Hugging Face: {e}")
        return
    except torch_oom_error() as e:
        st.error(f"Out of memory. Lower LLAMA_GPU_MEM / LLAMA_CPU_MEM and restart. ({e})")
        return
    except (KeyError, IndexError) as e:
        st.error(f"Unexpected Ollama response (no logprobs?): {e!r}")
        return

    probs, top, pred = details["probs"], details["top_tokens"], details["pred"]
    chips = (
        f'<span class="chip info">{version}</span>'
        f'<span class="chip info">{probs[pred]:.0%} confident</span>'
        f'<span class="chip info">{details["seconds"]:.1f}s</span>'
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
    if details["label_mass"] == 0:
        st.warning("No label tokens among the scored first tokens, so there is no real prediction.")
    st.markdown(bars_html(probs), unsafe_allow_html=True)
    st.markdown(tokens_html(top), unsafe_allow_html=True)
    st.markdown(prompt_html(text.strip(), version), unsafe_allow_html=True)

    others = [v for v in VERSIONS if v != version]
    if use_hf and not st.session_state.get("hf_compare"):
        st.caption(f"Each bf16 call takes ~25 s, so the other prompts ({', '.join(others)}) "
                   "run only when you tick the box below.")
    if use_hf and not st.checkbox(f"Also run {', '.join(others)}", key="hf_compare"):
        return
    with st.spinner("Scoring the other prompt versions…"):
        results = {v: details if v == version else predict(text.strip(), v, use_hf) for v in VERSIONS}
    true_label = picked["label"] if picked and picked["text"] == text.strip() else None
    st.markdown(compare_html(results, true_label), unsafe_allow_html=True)


def run_dev_set(rows: list[dict], version: str) -> list[dict]:
    """Predict every dev-set text; returns rows with `pred` added (None if no label token)."""
    results = []
    bar = st.progress(0.0, text="Classifying dev set…")
    for i, row in enumerate(rows, 1):
        r = cached_predict(row["text"].strip(), version)
        pred = r["pred"] if r["label_mass"] > 0 else None
        results.append({**row, "model": MODEL, "version": version, "pred": pred,
                        "conf": r["probs"][pred] if pred else 0.0})
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


def matrix_tab(rows: list[dict], version: str) -> None:
    """Tab 2: run the whole dev set with the chosen prompt (Ollama) and show a confusion matrix."""
    st.caption(f"Runs all {len(rows)} dev-set texts on Ollama with prompt {version}. "
               "Cached calls are reused, so reruns are fast.")
    key = f"cm_results_{version}"
    if st.button(f"Run confusion matrix ({version})"):
        try:
            st.session_state[key] = run_dev_set(rows, version)
        except requests.ConnectionError:
            st.error("Can't reach Ollama at localhost:11434. Is `ollama serve` running?")
            return
        except (KeyError, IndexError) as e:
            st.error(f"Unexpected Ollama response (no logprobs?): {e!r}")
            return

    results = st.session_state.get(key)
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
    st.caption("Exploration viewer · Llama 3.1 8B · first-token probabilities")

    version = st.selectbox("Prompt version", VERSIONS, index=len(VERSIONS) - 1,
                           format_func=lambda v: f"{v} · {VERSION_NOTES.get(v, '')}")
    rows = load_dev_set()
    tab1, tab2 = st.tabs(["Single text", "Confusion matrix"])
    with tab1:
        single_tab(rows, version)
    with tab2:
        matrix_tab(rows, version)


if __name__ == "__main__":
    main()
