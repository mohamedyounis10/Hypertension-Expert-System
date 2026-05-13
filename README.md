<div align="center">
  <h1>Hypertension Expert System 🩺🧠💙</h1>
  <p>Knowledge-based clinical decision support for cardiovascular risk (RDF modeling 🧩 → forward chaining inference ⚙️ → explainable outputs 📋 → Streamlit deployment 🚀).</p>

  <p>
    <a href="#overview">Overview 🧾</a> •
    <a href="#problem-motivation">Problem &amp; Motivation 🎯</a> •
    <a href="#project-structure">Project Structure 🗂️</a> •
    <a href="#knowledge-base">Knowledge Base 🧩</a> •
    <a href="#notebook-journey">Notebook Journey 📒</a> •
    <a href="#inference-outputs">Inference &amp; Outputs 📊</a> •
    <a href="#challenges">Challenges ⚠️</a>
  </p>

  <p>
    <img alt="Python" src="https://img.shields.io/badge/Python-3.x-blue" />
    <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-Notebook-orange" />
    <img alt="RDFlib" src="https://img.shields.io/badge/RDFlib-Semantic_Web-004A99" />
    <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-App-FF4B4B" />
    <img alt="Course" src="https://img.shields.io/badge/Course-AIE212_KBS-6f42c1" />
  </p>
</div>

---

## Table of Contents 🧭

- [Overview 🧾](#overview)
- [Problem &amp; Motivation 🎯](#problem-motivation)
- [Project Structure 🗂️](#project-structure)
- [Knowledge Base 🧩](#knowledge-base)
- [Notebook Journey 📒](#notebook-journey)
- [Inference &amp; Outputs 📊](#inference-outputs)
- [Challenges ⚠️](#challenges)
- [Streamlit App 🖼️](#streamlit-app)
- [How to Run ▶️](#how-to-run)
- [Disclaimer ⚖️](#disclaimer)
- [Author ✍️](#author)

---

<a id="overview"></a>
## Overview 🧾

This repository implements a **Knowledge-Based System (KBS)** for **hypertension-related risk and urgency assessment**, aligned with a semantic-web style workflow:

- **Knowledge representation 🧩**: patient facts and domain concepts modeled with **RDF** (`rdflib`) and lightweight RDFS-style classing (symptoms, risk factors).
- **Rule-based reasoning ⚙️**: a **forward-chaining** inference routine that applies **15 IF–THEN-style rules** over asserted patient conditions.
- **Explainability 📋**: an **explanation facility** that lists the sequence of rules fired for transparency and auditability.
- **Interactive delivery 🚀**: a **Streamlit** questionnaire (18 clinical inputs) with structured diagnostic outputs and recommendations.

---

<a id="problem-motivation"></a>
## Problem &amp; Motivation 🎯

Hypertension is often called a **“silent killer”** because dangerous elevations can occur with subtle or intermittent symptoms. Clinicians and patients benefit from structured tools that:

- Organize **BP thresholds**, **symptoms**, and **risk factors** in a consistent way.
- Map inputs to **urgency tiers** (routine vs clinic vs urgent vs emergency-oriented guidance).
- Provide a **traceable rationale** (which rules fired and why).

**Goal:** support **education and prototyping** for a CDSS-style workflow: from facts → inferred status/urgency/suspicion → human-readable explanation.

---

<a id="project-structure"></a>
## Project Structure 🗂️

- **`notebook.ipynb`** — full KBS narrative, RDF setup, rule engine walkthrough, and CLI-style interaction.
- **`app.py`** — Streamlit expert system UI (questionnaire + inference + explanation panel).
- **`image.png`** — optional branding/visual used in the Streamlit sidebar.

Tree 🌳:

```text
Project/
├─ notebook.ipynb
├─ app.py
├─ image.png
└─ README.md
```

---

<a id="knowledge-base"></a>
## Knowledge Base 🧩

### Named facts (18) 🧾

The Streamlit app collects **18 checkbox-driven facts**, including (non-exhaustive):

- BP categories (e.g., elevated vs crisis-range framing in the questionnaire)
- Symptoms (e.g., headache, dizziness, blurred vision, chest pain, shortness of breath, confusion, nosebleed)
- Risk/context factors (e.g., pregnancy, heart disease history, smoking, obesity, age over 65, salt intake, diabetes, sedentary lifestyle, alcohol use)

Domain knowledge is framed using guideline-oriented thinking (e.g., **AHA / ESC** style concepts) as described in the notebook narrative.

### Rules (15) ⚙️

The inference engine applies **15 rules** that derive intermediate conclusions (e.g., elevated/crisis-related statuses), urgency classes, suspicion levels, comorbidity warnings, and emergency classifications—then returns a **step-by-step fired-rule list**.

---

<a id="notebook-journey"></a>
## Notebook Journey 📒

The notebook is organized as an end-to-end KBS story:

1. **Executive summary &amp; introduction** — objectives, scope, and hypertension framing.
2. **Knowledge acquisition &amp; modeling** — RDF representation and quantitative breakdown (facts/rules).
3. **Architecture** — fact base, rule base, forward chaining engine, explanation facility.
4. **Implementation** — `rdflib` graph construction, namespaces, and runnable inference demonstrations.

---

<a id="inference-outputs"></a>
## Inference &amp; Outputs 📊

### Outputs you can expect ✅

- **Suspicion level** (e.g., unlikely / possible / probable style framing used by the engine)
- **Urgency guidance** (e.g., routine vs clinic review vs urgent vs emergency referral messaging in the UI)
- **Recommendation text** (Streamlit uses color-coded guidance; emergency cases show an explicit emergency-care prompt)
- **Explanation trace** — numbered list of **rules fired** during inference

### Why this design 🏆

- **Traceability**: every conclusion is tied to explicit rule firings.
- **Extensibility**: RDF graphs are a natural scaffold for adding new concepts/predicates over time.

---

<a id="challenges"></a>
## Challenges ⚠️

- **Clinical complexity**: real patients require full vitals, labs, medication context, and clinician judgment—this project is intentionally simplified for coursework demonstration.
- **Knowledge engineering trade-offs**: rule thresholds and symptom mappings must be carefully validated before any real-world use.
- **UI assumptions**: checkbox inputs are coarse; continuous BP readings and temporal patterns are not modeled in depth.

These are addressed in-project through **clear documentation**, **explicit rule traces**, and a **prototype UI** focused on structured reasoning rather than diagnosis claims.

---

<a id="streamlit-app"></a>
## Streamlit App 🖼️

```bash
streamlit run app.py
```

**Note:** the Streamlit sidebar loads `image.png`. For portable runs (especially after cloning from GitHub), use a **relative path** in `app.py` (for example `image.png` next to `app.py`) instead of a machine-specific absolute path.

---

<a id="how-to-run"></a>
## How to Run ▶️

### 1) Setup environment 🧪

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2) Install dependencies 📦

```bash
pip install streamlit rdflib jupyter
```

### 3) Launch the notebook 🚀

```bash
jupyter notebook notebook.ipynb
```

Run cells in order to explore the RDF model and inference flow.

---

<a id="disclaimer"></a>
## Disclaimer ⚖️

This software is for **educational and demonstration purposes only**. It is **not** a medical device and **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for clinical decisions.

---

<a id="author"></a>
## Author ✍️

- **Name**: Mohamed Younis
