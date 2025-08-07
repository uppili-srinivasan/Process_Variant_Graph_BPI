# Process_Variant_Graph_BPI

<details> <summary>Click to expand</summary>
markdown
Copy
Edit
# 🧠 Process Variant Graph BPI

A comprehensive process mining toolkit to extract, filter, analyze, and visualize **process variants** from event logs using trees, DAGs, and semantic embeddings. Designed for logs in the [BPI Challenge](https://data.4tu.nl/articles/dataset/BPI_Challenge_2017/12696884) format, this project offers both structural and semantic insights into process behavior.

---

## 🚀 Features

- ✅ Extracts **unique process variants** from `.xes` event logs  
- 🌲 Builds **prefix trees** and **variant DAGs** to represent process flows  
- 📊 Visualizes structures using **Graphviz**  
- 📉 Filters variants using **Pareto cutoffs (e.g., 80/20 rule)**  
- 🧬 Uses **sentence transformers** for semantic similarity of events  
- 🔍 Supports **variant clustering** and relevance analysis  
- 📓 Jupyter notebook for variant-level analysis and similarity heatmaps  

---

## 📁 Repository Structure

.
├── data_loader.py # Loads event logs from XES files
├── main.py # Main pipeline: extraction → filtering → tree building → visualization
├── pareto_cutoff_variants.py # Filters variants using 80/20 principle
├── variant_extractor.py # Extracts unique variants and their frequencies
├── variant_tree_builder.py # Builds prefix tree from variants
├── variant_tree_visualizer.py # Visualizes the variant tree using Graphviz
├── variant_tree_checker.py # Validates structural correctness of the variant tree
├── variant_dag_builder.py # Alternative DAG representation (WIP/optional)
├── variant_hierarchy_builder.py # Builds a hierarchical layout of variants
├── test.ipynb # Semantic similarity, event weighting, clustering
└── requirements.txt # Python dependencies


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/uppili-srinivasan/Process_Variant_Graph_BPI.git
cd Process_Variant_Graph_BPI
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
Note: This includes pm4py, graphviz, hdbscan, sentence-transformers, and scikit-learn. You may need to install Graphviz separately on your system (e.g., via Homebrew, Chocolatey, or apt).

### 4. Download Event Log Data
Download the BPI Challenge 2017 data from the official BPI Challenge site.

Place the .xes log file in the project folder or update the file path in main.py accordingly.

📌 How to Use
### Step 1: Prepare your Event Log
Place your .xes log file (e.g., BPI2017.xes) in a known location.

### Step 2: Run the Pipeline
Edit and run main.py:

```python
log = load_log("BPI2017.xes")
variants = extract_variants(log)
top_variants = apply_pareto_cutoff(variants, threshold=0.8)

tree = build_variant_tree(top_variants)
check_variant_tree(tree, top_variants)
visualize_variant_tree(tree, output_path="output/tree_graph")
```

### Step 3: Explore Results
Use test.ipynb to:

Load the CSV output

Analyze event frequencies

Generate semantic embeddings

Compute similarity scores

Cluster variants using hdbscan

🧠 Semantic Relevance & Embeddings
In test.ipynb, semantic embeddings are used to compute event relevance and similarity:

Uses sentence-transformers with the BAAI/bge-base-en model

Generates embeddings for event labels

Computes cosine similarity matrix

Visualizes semantic closeness via heatmaps

This adds semantic intelligence to purely structural variant analysis.

📊 Example Output
Visualization Type	Description
Tree Graph	Shows hierarchical flow of top variants
DAG Graph	(Optional) Flexible representation of variant flows
Heatmap	Semantic similarity between event types

📎 Requirements
Ensure Graphviz is installed:

macOS: brew install graphviz

Windows: Use Graphviz Installer

Linux: sudo apt install graphviz


🙏 Acknowledgements
PM4Py for event log handling

HDBSCAN for clustering

SentenceTransformers for semantic modeling

BPI Challenge datasets