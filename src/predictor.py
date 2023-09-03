# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import io
import json
import os
import pickle

import pandas as pd
from fastapi import FastAPI, status, Request, Response

model_path = os.environ.get("ARTIFACT_PATH", "/opt/ml/model")

BLIP_MODEL_VERSION = os.environ.get("BLIP_MODEL_VERSION", 1)
BLIP_PATH = os.environ.get("BLIP_PATH", f"blip/{BLIP_MODEL_VERSION}/model.pt")

LLAMA_MODEL_VERSION = os.environ.get("LLAMA_MODEL_VERSION", 1)
LLAMA_PATH = os.environ.get("LLAMA_PATH", f"llama/{LLAMA_MODEL_VERSION}/model.pt")

FEATURES = os.environ.get("FEATURES", "")
FEATURES = FEATURES.split(",")

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class BlipModel(object):
    model = None  # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls, model_path):
        """Get the model object for this instance, loading it if it's not already loaded."""
        if cls.model == None:
            with open(os.path.join(model_path, BLIP_PATH), "rb") as inp:
                cls.model = pickle.load(inp)
        return cls.model

    @classmethod
    def predict(cls, data):
        """For the input, do the predictions and return them.
        Args:
            input (a pandas dataframe): The data on which to do the predictions. There will be
                one prediction per row in the dataframe"""
        clf = cls.get_model(model_path=model_path)

        if hasattr(clf, "predict_proba"):
            return clf.predict_proba(data)[:, 1]

        if hasattr(clf, "predict"):
            return clf.predict(data)

        raise "Model does not have predict_proba or predict methods"

# The flask app for serving predictions
app = FastAPI()

@app.route("/ping", methods=["GET"])
def ping(request: Request):
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    print(model_path)
    print(request)
    health = BlipModel.get_model(model_path) is not None  # You can insert a health check here

    status = 200 if health else 404
    response = Response(
        content="Healthy",
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )
    return response

@app.route("/invocations", methods=["POST"])
def invocations(request: Request):
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    
    # TODO: Implement the prediction
    # predictions = BlipModel.predict(data)

    status = 200
    response = Response(
        content="Successful /invocations call",
        status_code=status.HTTP_200_OK,
        media_type="text/plain",
    )
    return response