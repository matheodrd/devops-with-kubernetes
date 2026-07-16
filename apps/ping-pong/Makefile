IMAGE = localhost:5111/ping-pong

.PHONY: build push apply apply-clean

build:
	docker build -t $(IMAGE) ./

push: build
	docker push $(IMAGE)

apply:
	kubectl apply -f manifests/

apply-clean:
	kubectl delete -f manifests/ --ignore-not-found=true
	kubectl apply -f manifests/
