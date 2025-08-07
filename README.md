# 🧠 Process Variant Graph BPI

A comprehensive process mining toolkit to extract, filter, analyze, and visualize **process variants** from event logs using trees, DAGs, and semantic embeddings. Designed for logs in the [BPI Challenge 2017](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884), this project offers both structural and semantic insights into process behavior.

---

## 🚀 Features

- ✅ Extracts **unique process variants** from `.xes` event logs  
- 🌲 Builds **prefix trees** and **variant DAGs** to represent process flows  
- 📊 Visualizes structures using **Graphviz**  
- 📉 Filters variants using **Pareto cutoffs (e.g., 80/20 rule)**  
- 🧬 Uses **sentence transformers** for semantic similarity of events  
- 🔍 Supports **variant clustering** and relevance analysis  
- 📓 Includes a Jupyter notebook for interactive analysis and similarity heatmaps  

---

## 📁 Repository Structure

```
.
├── data_loader.py                  # Loads event logs from XES files
├── main.py                         # Main pipeline: extraction → filtering → tree building → visualization
├── pareto_cutoff_variants.py       # Filters variants using 80/20 principle
├── variant_extractor.py            # Extracts unique variants and their frequencies
├── variant_tree_builder.py         # Builds prefix tree from variants
├── variant_tree_visualizer.py      # Visualizes the variant tree using Graphviz
├── variant_tree_checker.py         # Validates structural correctness of the variant tree
├── variant_dag_builder.py          # Alternative DAG representation (WIP/optional)
├── variant_hierarchy_builder.py    # Builds a hierarchical layout of variants
├── test.ipynb                      # Semantic similarity, event weighting, clustering
└── requirements.txt                # Python dependencies
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
```
git clone https://github.com/uppili-srinivasan/Process_Variant_Graph_BPI.git
cd Process_Variant_Graph_BPI
```

2. **Create and Activate a Virtual Environment**
```
python -m venv venv
source venv/bin/activate       # On Windows: venv\\Scripts\\activate
```

3. **Install Dependencies**
```
pip install --upgrade pip
pip install -r requirements.txt
```

> Note: This installs pm4py, graphviz, hdbscan, sentence-transformers, scikit-learn, etc.  
> Ensure you have Graphviz installed separately on your system.

---

## 📥 Download Event Log Data

Download the **BPI Challenge 2017** `.xes` file from the [official BPI Challenge repository](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884) and place it in the project folder.

---

## 🚦 How to Use

### Step 1: Prepare Your Event Log

Place your `.xes` event log (e.g., `BPI2017.xes`) in the working directory or update the path in `main.py`.

### Step 2: Run the Pipeline

Edit and run `main.py`:

```python
log = load_log("BPI2017.xes")
variants = extract_variants(log)
top_variants = apply_pareto_cutoff(variants, threshold=0.8)

tree = build_variant_tree(top_variants)
check_variant_tree(tree, top_variants)
visualize_variant_tree(tree, output_path="output/tree_graph")
```

### Step 3: Explore Results in Notebook

Open `test.ipynb` to:
- Load the output CSV
- Analyze event frequencies
- Generate semantic embeddings
- Compute similarity scores
- Cluster variants using HDBSCAN

---

## 🧠 Semantic Relevance & Embeddings

The `test.ipynb` notebook adds **semantic context** to structural variant analysis:

- Uses `sentence-transformers` with the `BAAI/bge-base-en` model
- Generates embeddings for event labels
- Computes a **cosine similarity matrix**
- Visualizes **semantic similarity** via heatmaps

This enriches the analysis beyond simple activity sequences.

---

## 📊 Example Output

| Visualization Type | Description                                |
|--------------------|--------------------------------------------|
| Tree Graph         | Shows hierarchical flow of top variants    |
| DAG Graph          | (Optional) Flexible representation of flows|
| Heatmap            | Semantic similarity between event labels   |

---

## 📎 Requirements

Ensure **Graphviz** is installed on your system:

- macOS: `brew install graphviz`
- Windows: Download from [graphviz.org](https://graphviz.org/download/)
- Linux: `sudo apt install graphviz`

---

## 🙏 Acknowledgements

- [PM4Py](https://pm4py.fit.fraunhofer.de/) – event log handling  
- [HDBSCAN](https://hdbscan.readthedocs.io/) – clustering  
- [SentenceTransformers](https://www.sbert.net/) – semantic modeling  
- [BPI Challenge Datasets](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884)  

---
