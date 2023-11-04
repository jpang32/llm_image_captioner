FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt utils.py lambda_handler.py ./
RUN python3.10 -m pip install -r requirements.txt

#RUN mkdir model
#RUN curl -L https://huggingface.co/Salesforce/blip-image-captioning-large/resolve/main/pytorch_model.bin -o ./model/pytorch_model.bin
#RUN curl https://huggingface.co/Salesforce/blip-image-captioning-large/resolve/main/config.json -o ./model/config.json
#RUN curl https://huggingface.co/Salesforce/blip-image-captioning-large/resolve/main/tokenizer.json -o ./model/tokenizer.json
#RUN curl https://huggingface.co/Salesforce/blip-image-captioning-large/resolve/main/tokenizer_config.json -o ./model/tokenizer_config.json

# Set the CMD to your handler
# Note: this specifies the function that will be run when the container starts,
# the input that is passed to this container (the event object) is done so
# through something called AWS Lambda Runtime Inference Client:
# https://github.com/aws/aws-lambda-python-runtime-interface-client
CMD ["lambda_handler.lambda_handler"]