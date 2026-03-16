#!/bin/bash

set -e

echo "=== Deploying FastAPI applications with different configurations ==="

# Production
echo -e "\n1. Deploying PRODUCTION..."
helm upgrade --install fastapi-prod ./fastapi-chart -f ./fastapi-chart/values-production.yaml
kubectl wait --for=condition=available --timeout=120s deployment/fastapi-prod-fastapi-chart

# Development
echo -e "\n2. Deploying DEVELOPMENT..."
helm upgrade --install fastapi-dev ./fastapi-chart -f ./fastapi-chart/values-development.yaml
kubectl wait --for=condition=available --timeout=120s deployment/fastapi-dev-fastapi-chart

# Testing
echo -e "\n3. Deploying TESTING..."
helm upgrade --install fastapi-test ./fastapi-chart -f ./fastapi-chart/values-testing.yaml
kubectl wait --for=condition=available --timeout=120s deployment/fastapi-test-fastapi-chart

# Highload
echo -e "\n4. Deploying HIGHLOAD..."
helm upgrade --install fastapi-highload ./fastapi-chart -f ./fastapi-chart/values-highload.yaml
kubectl wait --for=condition=available --timeout=120s deployment/fastapi-highload-fastapi-chart

echo -e "\n=== Deployment Summary ==="
helm list

echo -e "\n=== Pods Status ==="
kubectl get pods -l app.kubernetes.io/name=fastapi-chart

echo -e "\n=== Services ==="
kubectl get svc -l app.kubernetes.io/name=fastapi-chart

echo -e "\n=== Ingresses ==="
kubectl get ingress -l app.kubernetes.io/name=fastapi-chart

echo -e "\n=== Resource Usage ==="
kubectl top pods -l app.kubernetes.io/name=fastapi-chart
