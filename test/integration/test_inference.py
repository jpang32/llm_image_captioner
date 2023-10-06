from src.code.inference import model_fn
import pytest
import os

from pathlib import Path
from transformers import pipeline
from transformers.pipelines import SUPPORTED_TASKS, Pipeline
from tokenizers import Tokenizer


def test_load_model_and_make_prediction():
    HF_MODEL_ID = os.environ.get("HF_MODEL_ID", "yesidcanoc/image-captioning-swin-tiny-distilgpt2")

    pipeline = model_fn(model_dir=HF_MODEL_ID)
    output = pipeline("https://huggingface.co/spaces/impira/docquery/resolve/2359223c1837a7587402bda0f2643382a6eefeab/invoice.png")
    print(output)