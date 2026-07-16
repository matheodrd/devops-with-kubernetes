WRITER_IMAGE = localhost:5111/log-output-writer
SERVER_IMAGE = localhost:5111/log-output-server

.PHONY: build push apply apply-clean

build:
	docker build -t $(WRITER_IMAGE) writer/
	docker build -t $(SERVER_IMAGE) server/

push: build
	docker push $(WRITER_IMAGE)
	docker push $(SERVER_IMAGE)

apply:
	kubectl apply -f manifests/

apply-clean:
	kubectl delete -f manifests/ --ignore-not-found=true
	kubectl apply -f manifests/
