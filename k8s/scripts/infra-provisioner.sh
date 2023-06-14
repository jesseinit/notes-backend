#!/bin/bash

set -e

ACTION="$(echo "$1" | tr '[:upper:]' '[:lower:]')"

if [[ "$ACTION" == "up" ]]
then
    echo "Provisioning Infrastructure"
    cd iac/aws 
    terraform plan
    terraform apply --auto-approve
    aws eks update-kubeconfig --region eu-central-1 --name notes-cluster
    cd ../..
    echo "Applying App Resources"
    kubectl apply -k k8s/remote
elif [[ "$ACTION" == "down" ]]
then
    echo "Destroying Infrastructure"
    aws eks update-kubeconfig --region eu-central-1 --name notes-cluster
    cd iac/aws
    terraform destroy --auto-approve
else
    echo "Pass in the Up or Down Arguments" && exit
fi
