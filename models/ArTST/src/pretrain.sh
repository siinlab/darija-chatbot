#!/bin/bash
# This script is copied from https://github.com/mbzuai-nlp/ArTST/blob/main/scripts/TTS/finetune.sh
# and is modified to fit the project structure
set -e

cd "$(dirname "$0")"
src_dir=$(pwd)

checkpoint1=$src_dir/../ArTST-huggingface/CLARTTS_ArTST_TTS.pt
# checkpoint2=$src_dir/../ArTST-huggingface/CLARTTS_ArTSTstar_TTS.pt

# pretrain the model
cd "$src_dir"

# DATASET=darija_tts
DATA_ROOT=/app/dataset/mohamed-1/bin_data
LABEL_DIR=/app/dataset/mohamed-1/hubert_features/
USER_DIR=$src_dir/../ArTST/artst

SAVE_DIR=$src_dir/checkpoints

TRAIN_SET="train|train"
VALID_SET="test|valid"
CHECKPOINT_PATH=$checkpoint1

fairseq-train ${DATA_ROOT} \
    --save-dir "${SAVE_DIR}" \
    --tensorboard-logdir "${SAVE_DIR}" \
    --train-subset ${TRAIN_SET} \
    --valid-subset ${VALID_SET} \
    --hubert-label-dir ${LABEL_DIR} \
    --distributed-world-size 4 \
    --distributed-port 0 \
    --ddp-backend legacy_ddp \
    --user-dir "$USER_DIR" \
    --log-format json \
    --seed 1337 \
    --fp16 \
    \
    --task artst \
    --t5-task pretrain \
    --label-rates 50 \
    --sample-rate 16000 \
    --random-crop \
    \
    --num-workers 0 \
    --max-tokens 1400000 \
    --max-speech-sample-size 250000 \
    --update-freq 2 \
    --batch-ratio "[1,0.0086]" \
    \
    --criterion artst \
    --optimizer adam \
    --reset-optimizer \
    --adam-betas "(0.9, 0.98)" \
    --adam-eps 1e-06 \
    --weight-decay 0.1 \
    --power 1 \
    --clip-norm 5.0 \
    --lr 0.0002 \
    --lr-scheduler polynomial_decay \
    \
    --max-update 4000000 \
    --warmup-updates 64000 \
    --total-num-update 800000 \
    --save-interval-updates 3000 \
    --skip-invalid-size-inputs-valid-test \
    --required-batch-size-multiple 1 \
    \
    --arch artst_transformer_base \
    --share-input-output-embed \
    --find-unused-parameters \
    --bert-init \
    --relative-position-embedding \
    --use-codebook \
    --codebook-prob 0.1 \
    --loss-weights="[10,0.1]" \
    --max-text-positions 600 \
    --finetune-from-model "$CHECKPOINT_PATH"
