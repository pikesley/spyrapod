PROJECT = $(shell basename $$(pwd))
ID = pikesley/${PROJECT}

build:
	docker build --tag ${ID} .

run:
	docker run \
		--name ${PROJECT} \
		--volume $(shell pwd):/opt/${PROJECT} \
		--volume $(shell pwd)/tiny-data:/data/tiny-data \
		--env CLIENT_ID=${CLIENT_ID} \
		--env CLIENT_SECRET=${CLIENT_SECRET} \
		--interactive \
		--tty \
		--rm \
		${ID} bash

connect:
	docker exec \
		--interactive \
		--tty \
		${PROJECT} bash
