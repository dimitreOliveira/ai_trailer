FEATURE_NAME := ai_trailer
TAG ?= latest

trailer:
	make plot voice screenshot image_retrieval clip audio_clip join_clip

plot:
	python src/plot.py

voice:
	python src/voice.py

screenshot:
	python src/screenshot.py

image_retrieval:
	python src/image_retrieval.py

clip:
	python src/clip.py

audio_clip:
	python src/audio_clip.py

join_clip:
	python src/join_clip.py

build:
	pip install -r requirements.txt

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src