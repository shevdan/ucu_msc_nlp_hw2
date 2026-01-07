#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KENLM_DIR="${SCRIPT_DIR}/kenlm"

if [ -d "$KENLM_DIR" ]; then
    echo "KenLM directory exists, skipping clone."
else
    echo "Cloning KenLM..."
    git clone https://github.com/kpu/kenlm.git "$KENLM_DIR"
fi

echo "Building KenLM..."
cd "$KENLM_DIR"
mkdir -p build
cd build
cmake ..
make -j$(nproc)
