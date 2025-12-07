#!/bin/bash
echo "About to deploy the messaging_app"
kubectl apply -f deployment.yaml
echo "Deployed"
kubectl get pods
