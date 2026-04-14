# Review AI Intelligence Engine

An end-to-end AI system that fine-tunes FLAN-T5 with LoRA on 200,000 Google Play reviews across 20 apps, classifies user sentiment at scale, and surfaces structured product insights through a live interactive dashboard.

**Live Demo:** https://ai-review-intelligence-engine-jsppq2a3uwylunlmmccnjg.streamlit.app

---

## What This Project Does

Most product teams read reviews manually. This system replaces that process entirely.

It ingests raw Google Play reviews, fine-tunes a language model to understand sentiment in the context of mobile apps, processes reviews in bundles, and outputs structured product intelligence: what users hate, what they love, what the engineering and product team should fix first, and why.

The output is not a spreadsheet. It is a live dashboard with four views designed for product analysts and PMs to act on immediately.

---

## Architecture

```
200,000 Google Play Reviews
        |
        v
  Data Collection
  (20 apps, Google Play Store API)
        |
        v
  FLAN-T5 Base Model
  + LoRA Fine-Tuning
  (3,449 steps, Tesla T4 GPU)
        |
        v
  Sentiment Classification
  positive / negative / mixed
  (85.74% accuracy)
        |
        v
  VoC Pipeline
  Bundle processing, theme extraction,
  pain points, delighters, action generation
        |
        v
  Structured Output CSV
  (100 bundles, 35 product actions)
        |
        v
  Streamlit Dashboard
  Overview / App Analysis / Recommendations / Data Explorer
```

---

## Model Details

| Parameter | Value |
|---|---|
| Base Model | google/flan-t5-base |
| Fine-tuning Method | LoRA (Low-Rank Adaptation) |
| Training Steps | 3,449 |
| Hardware | Tesla T4 GPU |
| Accuracy | 85.74% |
| Training Data | 200,000 Google Play reviews |
| Apps Covered | 20 (Candy Crush, WhatsApp, TikTok, Netflix, Spotify, and 15 others) |
| Output Classes | positive, negative, mixed |

LoRA was chosen specifically to make fine-tuning feasible on a single GPU without degrading the base model's general language understanding. Only a small number of adapter weights are trained, keeping memory footprint low while achieving meaningful accuracy on app-review sentiment.

---

## Dataset

Reviews were collected from the Google Play Store across 20 high-traffic consumer apps spanning gaming, social media, productivity, and entertainment categories:

Candy Crush Saga, Dropbox, Facebook, Facebook Lite, Facebook Messenger, Flipboard, Instagram, LINE, Microsoft PowerPoint, Microsoft Word, Netflix, SHAREit, Skype, Snapchat, Spotify, Subway Surfers, TikTok, Twitter, Viber, WhatsApp

**Key finding from the data:** Despite training the model as a 3-class classifier (positive, negative, mixed), all 100 processed bundles returned binary sentiment. User sentiment on mobile apps is polarized. Users either love an app or they do not. Mixed sentiment was not observed in any bundle, which is itself a meaningful product insight.

---

## Results

| Metric | Value |
|---|---|
| Total reviews processed | 200,000 |
| Bundles analyzed | 100 |
| Positive bundles | 50 (50%) |
| Negative bundles | 50 (50%) |
| Product actions generated | 35 |
| P0 critical issues | 3 |
| P1 sprint actions | 25 |
| P2 backlog items | 7 |

**Action breakdown by owner:**

| Team | Actions |
|---|---|
| Engineering | 19 |
| Product | 10 |
| Design | 6 |

Engineering owns 54% of all recommended actions, indicating that product quality and stability issues are the primary driver of user dissatisfaction across these apps, more so than design or strategy gaps.

---

## Dashboard Pages

### Overview
High-level sentiment summary across all 20 apps. Includes KPI cards, sentiment-by-app bar chart, cumulative trend line, donut chart, action owner breakdown, and priority distribution. Designed for a 10-second read.

### App Analysis
Per-app deep dive. Select any of the 20 apps and see deduplicated pain points, product delighters filtered for signal quality, all recommended actions sorted by priority, and AI-generated summaries for every review bundle analyzed.

### Recommendations
Full product backlog of 35 AI-generated actions. Filterable by priority (P0 / P1 / P2) and team owner (Engineering / Product / Design). Designed for sprint planning and cross-functional team alignment.

### Data Explorer
Complete results table with filters by sentiment and app. Exportable as CSV. Shows raw AI summaries for every processed bundle.

---

## Notebooks

Two notebooks cover the full pipeline:

**lora-finetuning-sentiment.ipynb**
Fine-tunes FLAN-T5 with LoRA on Google Play review data. Covers data preparation, tokenization, LoRA adapter configuration, training loop, evaluation, and checkpoint saving.

**voice-of-customer-voc-review-intelligence-engine.ipynb**
Runs the full VoC pipeline on top of the fine-tuned model. Processes review bundles, extracts pain points, delighters, and themes, generates prioritized product actions, and outputs the structured CSV that powers the dashboard.

---

## Project Structure

```
ai-review-intelligence-engine/
|
|-- app.py                          # Streamlit dashboard (4 pages)
|-- requirements.txt                # Python dependencies
|-- review_intel_outputs.csv        # Pipeline output (100 bundles, 35 actions)
|
|-- .streamlit/
|   |-- config.toml                 # Dark theme configuration
|
|-- notebooks/
|   |-- lora-finetuning-sentiment.ipynb
|   |-- voice-of-customer-voc-review-intelligence-engine.ipynb
|
|-- outputs/
    |-- checkpoint-3449/            # Fine-tuned LoRA weights
```

---

## Setup and Installation

**Clone the repository**

```bash
git clone https://github.com/tanushree2000/ai-review-intelligence-engine.git
cd ai-review-intelligence-engine
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Run the dashboard**

```bash
streamlit run app.py
```

The app will open at http://localhost:8501

**Dependencies**

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## Skills Demonstrated

**Machine Learning**
Fine-tuning a pre-trained transformer (FLAN-T5) using parameter-efficient methods (LoRA) for a domain-specific classification task. Training on GPU, evaluating with accuracy metrics, and deploying model outputs into a production pipeline.

**Product Analytics**
Translating raw unstructured user feedback into prioritized, actionable product intelligence. Structuring output by team owner, severity level, and business impact in a format directly usable for sprint planning.

**Data Engineering**
Processing 200,000 reviews through a multi-stage pipeline: collection, cleaning, deduplication, bundle aggregation, model inference, theme extraction, and structured output generation.

**Data Visualization**
Building an interactive multi-page analytics dashboard with real data, filterable views, and charts designed for non-technical stakeholders to read in under 10 seconds.

---

## What I Would Do Next

Given more time and compute, the next iterations would be:

1. Expand to 500,000 reviews across 50 apps for broader signal coverage
2. Add version-based filtering to detect sentiment changes after app updates
3. Implement true semantic clustering using sentence embeddings rather than keyword matching
4. Build a pipeline that runs automatically on new reviews weekly
5. Add competitive benchmarking by comparing pain points across competing apps in the same category

---

## About

Built by Tanushree Poojary 

This project was designed to demonstrate end-to-end AI product analytics capability: from raw data collection through model fine-tuning to deployed, interactive business intelligence.

**GitHub:** https://github.com/tanushree2000/ai-review-intelligence-engine

**Live App:** https://ai-review-intelligence-engine-jsppq2a3uwylunlmmccnjg.streamlit.app
