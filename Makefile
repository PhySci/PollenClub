IMAGE_NAME = pollenclub
TAG = 0.1

build:
	docker build . -t ${IMAGE_NAME}:${TAG}
	docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest

run:
	docker run --rm -it \
			   -v "$(shell pwd)"/../data:/data  \
			   --env-file "$(shell pwd)"/env/.env  \
			   ${IMAGE_NAME}:latest

run_bash:
	docker run --rm -it -v "$(shell pwd)"/../data:/data  ${IMAGE_NAME}:latest bash

push:
	docker tag ${IMAGE_NAME}:${TAG} physci/pollenclub:latest
	docker push physci/pollenclub:latest

	docker tag ${IMAGE_NAME}:${TAG} physci/pollenclub:${TAG}
	docker push physci/pollenclub:${TAG}