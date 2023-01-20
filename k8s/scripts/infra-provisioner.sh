#!/bin/bash

set -e

ACTION="$(echo "$1" | tr '[:upper:]' '[:lower:]')"

if [[ "$ACTION" == "up" ]]
then
    echo "Provisioning Infrastructure"
    cd iac/aws 
    terraform plan
    terraform apply --auto-approve
    aws eks update-kubeconfig --region eu-central-1 --profile dev01 --name notes-cluster
    cd ../..
    echo "Applying App Resources"
    kubectl apply -k k8s/remote
elif [[ "$ACTION" == "down" ]]
then
    echo "Destroying Infrastructure"
    aws eks update-kubeconfig --region eu-central-1 --profile dev01 --name notes-cluster
else
    echo "Pass in the Up or Down Arguments" && exit
fi
