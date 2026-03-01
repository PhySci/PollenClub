IMAGE_NAME = pollenclub
TAG = local

build:
	docker build . -t ${IMAGE_NAME}:${TAG}
	docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest

run:
	docker run --rm -it \
			   -v "$(shell pwd)"/data:/data  \
			   --env-file "$(shell pwd)"/env/.env  \
			   ${IMAGE_NAME}:latest


test:
	docker pull physci/pollenclub:latest
	docker run --rm -it \
               -v "$(shell pwd)"/data:/data \
               --env-file "$(shell pwd)"/env/.env \
               physci/pollenclub:0.2
