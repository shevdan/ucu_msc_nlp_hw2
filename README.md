# HW2: ASR Hypothesis Selection with N-gram Language Models

## Setup

### 1. Create conda environment

```bash
conda create -n nlp-hw2 python=3.10
conda activate nlp-hw2
pip install -r requirements.txt
```

### 2. Build KenLM
Instructions for ubuntu

```bash
sudo apt-get install build-essential cmake libboost-all-dev zlib1g-dev libbz2-dev liblzma-dev

chmod +x setup_kenlm.sh
./setup_kenlm.sh
```

### 3. Download and prepare corpus

Download the **news cleansed** corpus from [UberText](https://lang.org.ua/en/ubertext/).


In HW I chose to use 10M lines as the full dataset is way too large. Any number of lines can be configured. It also creates 105, 225%, 50% subsets of the chosen one.

```bash
python scripts/preprocess_corpus.py \
    --input <path_to_news_cleansed.txt> \
    --output corpus/ \
    --max-lines 10000000 \
    --create-subsets
```

### 4. Train models

```bash
chmod +x scripts/train_lm.sh

./scripts/train_lm.sh corpus/corpus_full.txt models/

for pct in 10pct 25pct 50pct; do
    ./scripts/train_lm.sh corpus/corpus_${pct}.txt models/
done
```

## Run

Open and run the Jupyter notebook:

```bash
jupyter notebook hw2_asr_rescoring.ipynb
```
