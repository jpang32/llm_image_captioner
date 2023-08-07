import sagemaker
import boto3
import boto3.session
from sagemaker.huggingface import HuggingFaceModel
import os

if __name__ == "__main__":
	session = boto3.session.Session(profile_name=os.environ['AWS_PROFILE'])

	iam = session.client('iam')
	role = iam.get_role(RoleName='sagemaker_llm')['Role']['Arn']

	# Hub Model configuration. https://huggingface.co/models
	hub = {
		'HF_MODEL_ID':'Salesforce/blip-image-captioning-base',
		'HF_TASK':'image-to-text'
	}

	# create Hugging Face Model Class
	huggingface_model = HuggingFaceModel(
		transformers_version='4.26.0',
		pytorch_version='1.13.1',
		py_version='py39',
		env=hub,
		role=role,
	)

	# deploy model to SageMaker Inference
	predictor = huggingface_model.deploy(
		initial_instance_count=1, # number of instances
		instance_type='ml.m5.xlarge' # ec2 instance type
	)

