IMAGE_NAME := ai_trailer
TAG ?= latest

trailer:
	make plot voice frame image_retrieval clip audio_clip join_clip

plot:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/plot.py

voice:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	-v $(PWD)/voices/:/app/voices/ \
	${IMAGE_NAME}:${TAG} \
	python src/voice.py

frame:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	-v $(PWD)/movies/:/app/movies/ \
	${IMAGE_NAME}:${TAG} \
	python src/frame.py

image_retrieval:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/image_retrieval.py

clip:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	-v $(PWD)/movies/:/app/movies/ \
	${IMAGE_NAME}:${TAG} \
	python src/clip.py

audio_clip:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/audio_clip.py

join_clip:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/join_clip.py

build:
	docker build -t ${IMAGE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src