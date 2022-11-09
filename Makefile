build:
	@echo "=========Building API Image========="
	docker build -t notes-api .

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
	docker run -d -p 5001:5000 --restart=always --name kind-registry registry:2

push-locally:
	@echo "=========Pushing to Local Docker Registry========="
	docker tag notes-api:latest localhost:5001/notes-api:latest
	docker push localhost:5001/notes-api:latest

create:
	@echo "=========Creating Kind Cluster========="
	kind create cluster --config k8s/local/cluster.yml
	@echo "=========Installing Database Workloads========="
	kubectl apply -f k8s/local/database.yml
	@echo "=========Applying Notes API Workloads========="
	kubectl apply -f k8s/local/notes-api.yml   

destroy:
	@echo "=========Destroying Kind Cluster========="
	kind delete cluster --name notes-api-cluster 
