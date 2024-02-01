IMAGE_NAME := ai_trailer
TAG ?= latest

trailer:
	docker run --rm \
	-v $(PWD)/movies/:/app/movies/ \
	-v $(PWD)/voices/:/app/voices/ \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	make plot voice frame image_retrieval clip audio_clip join_clip

plot:
	python src/plot.py

voice:
	python src/voice.py

frame:
	python src/frame.py

image_retrieval:
	python src/image_retrieval.py

clip:
	python src/clip.py

audio_clip:
	python src/audio_clip.py

join_clip:
	python src/join_clip.py

build:
	docker build -t ${IMAGE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src