IMAGE_NAME := ai_trailer
TAG ?= latest

trailer:
	make subplot voice frame image_retrieval clip audio_clip join_clip

trailer_imdb:
	make plot_retrieval subplot voice frame image_retrieval clip audio_clip join_clip

trailer_youtube:
	make video_retrieval subplot voice frame image_retrieval clip audio_clip join_clip

trailer_imdb_youtube:
	make video_retrieval plot_retrieval subplot voice frame image_retrieval clip audio_clip join_clip

video_retrieval:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	-v $(PWD)/movies/:/app/movies/ \
	${IMAGE_NAME}:${TAG} \
	python src/video_retrieval.py

plot_retrieval:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/plot_retrieval.py

subplot:
	docker run --rm \
	-v $(PWD)/projects/:/app/projects/ \
	${IMAGE_NAME}:${TAG} \
	python src/subplot.py

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