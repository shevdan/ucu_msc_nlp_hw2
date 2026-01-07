#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
KENLM_BIN="${PROJECT_DIR}/kenlm/build/bin"

if [ ! -f "${KENLM_BIN}/lmplz" ]; then
    echo "Error: KenLM not built. Run setup_kenlm.sh first."
    exit 1
fi

CORPUS="${1:-${PROJECT_DIR}/corpus/corpus_full.txt}"
OUTPUT_DIR="${2:-${PROJECT_DIR}/models}"

mkdir -p "$OUTPUT_DIR"

echo "Training LMs from: $CORPUS"
CORPUS_NAME=$(basename "$CORPUS" .txt)

for ORDER in 2 3; do
    echo "Training ${ORDER}-gram..."
    ARPA_FILE="${OUTPUT_DIR}/${CORPUS_NAME}_${ORDER}gram.arpa"
    BIN_FILE="${OUTPUT_DIR}/${CORPUS_NAME}_${ORDER}gram.bin"

    "${KENLM_BIN}/lmplz" -o "$ORDER" --discount_fallback < "$CORPUS" > "$ARPA_FILE"
    "${KENLM_BIN}/build_binary" "$ARPA_FILE" "$BIN_FILE"
    ls -lh "$BIN_FILE"
done

echo "Done. Models in: $OUTPUT_DIR"
