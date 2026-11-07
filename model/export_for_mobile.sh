#!/usr/bin/env bash
# Turns ./zorn-1.1 into a small GGUF file that runs on phones (Android/iOS) and in Ollama.
# Needs: git, python3, cmake, a C++ compiler. Run on Colab/PC after train_zorn.py.
set -e
git clone --depth 1 https://github.com/ggml-org/llama.cpp || true
pip install -r llama.cpp/requirements/requirements-convert_hf_to_gguf.txt
python llama.cpp/convert_hf_to_gguf.py zorn-1.1 --outfile zorn-1.1-f16.gguf --outtype f16
cmake -S llama.cpp -B llama.cpp/build && cmake --build llama.cpp/build --target llama-quantize -j
llama.cpp/build/bin/llama-quantize zorn-1.1-f16.gguf zorn-1.1-q4.gguf Q4_K_M
echo "Done: zorn-1.1-q4.gguf  (about 1 GB for the 1.5B model)"
