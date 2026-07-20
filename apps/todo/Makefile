BACKEND_IMAGE = localhost:5111/todo-backend
APP_IMAGE = localhost:5111/todo-app

.PHONY: build push apply apply-clean

build:
	docker build -t $(BACKEND_IMAGE) todo-backend/
	docker build -t $(APP_IMAGE) todo-app/

push: build
	docker push $(BACKEND_IMAGE)
	docker push $(APP_IMAGE)

apply:
	kubectl apply -f manifests/

apply-clean:
	kubectl delete -f manifests/ --ignore-not-found=true
	kubectl apply -f manifests/
