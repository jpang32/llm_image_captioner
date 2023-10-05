import json
import os

from pathlib import Path
from transformers import pipeline
from transformers.pipelines import SUPPORTED_TASKS, Pipeline
from tokenizers import Tokenizer

ARCHITECTURES_2_TASK = {
    "TapasForQuestionAnswering": "table-question-answering",
    "ForQuestionAnswering": "question-answering",
    "ForTokenClassification": "token-classification",
    "ForSequenceClassification": "text-classification",
    "ForMultipleChoice": "multiple-choice",
    "ForMaskedLM": "fill-mask",
    "ForCausalLM": "text-generation",
    "ForConditionalGeneration": "text2text-generation",
    "MTModel": "text2text-generation",
    "EncoderDecoderModel": "text2text-generation",
    # Model specific task for backward comp
    "GPT2LMHeadModel": "text-generation",
    "T5WithLMHeadModel": "text2text-generation",
}

def infer_task_from_model_architecture(model_config_path: str, architecture_index=0) -> str:
    """
    Infer task from `config.json` of trained model. It is not guaranteed to the detect, e.g. some models implement multiple architectures or
    trainend on different tasks https://huggingface.co/facebook/bart-large/blob/main/config.json. Should work for every on Amazon SageMaker fine-tuned model.
    It is always recommended to set the task through the env var `TASK`.
    """
    with open(model_config_path, "r") as config_file:
        config = json.loads(config_file.read())
        architecture = config.get("architectures", [None])[architecture_index]

    task = None
    for arch_options in ARCHITECTURES_2_TASK:
        if architecture.endswith(arch_options):
            task = ARCHITECTURES_2_TASK[arch_options]

    if task is None:
        raise ValueError(
            f"Task couldn't be inferenced from {architecture}."
            f"Inference Toolkit can only inference tasks from architectures ending with {list(ARCHITECTURES_2_TASK.keys())}."
            "Use env `HF_TASK` to define your task."
        )
    # set env to work with
    os.environ["HF_TASK"] = task
    return task

def get_pipeline(task: str, device: int, model_dir: Path, **kwargs) -> Pipeline:
    """
    create pipeline class for a specific task based on local saved model
    """
    if task is None:
        raise EnvironmentError(
            "The task for this model is not set: Please set one: https://huggingface.co/docs#how-is-a-models-type-of-inference-api-and-widget-determined"
        )
    # define tokenizer or feature extractor as kwargs to load it the pipeline correctly
    if task in {
        "automatic-speech-recognition",
        "image-segmentation",
        "image-classification",
        "audio-classification",
        "object-detection",
        "zero-shot-image-classification",
    }:
        kwargs["feature_extractor"] = model_dir

    tokenizer = Tokenizer.from_pretrained(os.environ["HF_MODEL_ID"])

    # load pipeline
    hf_pipeline = pipeline(task=task, model=model_dir, tokenizer=tokenizer, device=device, **kwargs)

    return hf_pipeline


def model_fn(self, model_dir, context=None):
        """
        The Load handler is responsible for loading the Hugging Face transformer model.
        It can be overridden to load the model from storage.

        Args:
            model_dir (str): The directory where model files are stored.
            context (obj): metadata on the incoming request data (default: None).

        Returns:
            hf_pipeline (Pipeline): A Hugging Face Transformer pipeline.
        """
        # gets pipeline from task tag
        if "HF_TASK" in os.environ:
            hf_pipeline = get_pipeline(task=os.environ["HF_TASK"], model_dir=model_dir, device=self.device)
        elif "config.json" in os.listdir(model_dir):
            task = infer_task_from_model_architecture(f"{model_dir}/config.json")
            hf_pipeline = get_pipeline(task=task, model_dir=model_dir, device=self.device)
        else:
            raise ValueError(
                f"You need to define one of the following {list(SUPPORTED_TASKS.keys())} as env 'HF_TASK'.", 403
            )
        return hf_pipeline