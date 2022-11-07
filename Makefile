build:
	@echo "=========Building API Image========="
	docker build -t notes-api .

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
	helm install postgresql-dev -f k8s/local/values.yml bitnami/postgresql
	kubectl apply -f k8s/local/local-pv.yml
	kubectl apply -f k8s/local/pv-claim.yml
	kubectl apply -f k8s/local/deployment.yml

destroy:
	@echo "=========Destroying Kind Cluster========="
	kind delete cluster --name notes-api-cluster 
