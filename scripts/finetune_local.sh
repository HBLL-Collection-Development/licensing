#!/usr/bin/env bash
set -euo pipefail
# Local fine-tuning instructions using Hugging Face transformers and PEFT (LoRA).
# Requires: python, torch, transformers, datasets, peft
# This script prepares a minimal run; adjust hyperparams and choose a model checkpoint.
DATA_DIR=data/llm-training
MODEL_NAME="declare-latest/llama-7b" # replace with a local or HF model
OUTPUT_DIR=artifacts/finetuned-llm
mkdir -p "$OUTPUT_DIR"

python3 - <<'PY'
from pathlib import Path
print('This script is a guideline. To actually fine-tune, use HuggingFace training examples or transformer-based fine-tuning with PEFT.')
print('Example: use transformers Trainer or accelerate + peft to train a causal LM on prompt-completion pairs.')
PY

echo "To fine-tune locally, consider the following steps:" 
echo "1) Convert dataset to huggingface dataset or use JSONL with prompt/completion pairs."
echo "2) Use a training script: transformers/examples/pytorch/language-modeling/run_clm.py with --model_name_or_path, --train_file, --validation_file, --output_dir, and PEFT args for LoRA."
echo "3) Example (pseudo): python run_clm.py --model_name_or_path $MODEL_NAME --train_file $DATA_DIR/openai_finetune.jsonl --validation_file $DATA_DIR/val.jsonl --output_dir $OUTPUT_DIR --per_device_train_batch_size 2 --num_train_epochs 3"

echo "See project README for more detailed commands and GPU recommendations."
