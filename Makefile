SHELL := /bin/bash
 
inference:
	cd src && uvicorn predictor:app --reload --env-file ../.env

ping:
	curl --location --request GET 'http://127.0.0.1:8000/ping'