build:
	@echo "=========Building API Image========="
	docker build -t notes-api .
	# docker buildx build --platform linux/amd64 -t notes-api .

build-push-ecr:
	docker buildx build --platform linux/amd64 -t 450543847015.dkr.ecr.eu-central-1.amazonaws.com/notes-api .
	docker push 450543847015.dkr.ecr.eu-central-1.amazonaws.com/notes-api


bootstrap:
	@echo "=========Bootstraping API========="
	make build
	make start

start:
	@echo "=========Starting API========="
	docker compose up

stop:
	@echo "=========Stoping API========="
	docker compose down

start-local-registry:
	@echo "=========Starting Local Docker Registry========="
	docker run -d -p 5001:5000 --restart=unless-stopped --name kind-registry --net kind registry:2

push-locally:
	@echo "=========Pushing to Local Docker Registry========="
	docker tag notes-api:arm64 localhost:5001/notes-api:arm64
	docker push localhost:5001/notes-api:arm64

push:
	@echo "=========Pushing to Remote Registry========="
	docker buildx build --platform linux/amd64 -t notes-api:amd64 .
	docker tag notes-api:amd64 registry.digitalocean.com/notes-api-registry/notes-api:amd64
	docker push registry.digitalocean.com/notes-api-registry/notes-api:amd64

kind-create:
	@echo "=========Creating Kind Cluster========="
	kind create cluster --config k8s/local/cluster.yml
	@echo "=========Installing Ingress Controller ========="
	kubectl apply --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
	kubectl wait --namespace ingress-nginx  --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
	@echo "=========Installing Database Workloads========="
	kubectl apply -f k8s/local/database.yml
	@echo "=========Applying Notes API Workloads========="
	kubectl apply -f k8s/local/local-notes-api.yml
	kubectl apply -f k8s/local/local-ingress.yml

kind-destroy:
	@echo "=========Destroying Kind Cluster========="
	kind delete cluster --name notes-api-cluster 

plan:
	cd iac && terraform plan

apply:
	cd iac && terraform apply --auto-approve

destroy:
	cd iac && terraform destroy --auto-approve && terraform destroy --auto-approve
	
