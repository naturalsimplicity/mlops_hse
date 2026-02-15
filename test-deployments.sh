#!/bin/bash

echo "=== Testing Different Deployments ==="

# Функция для тестирования
test_deployment() {
    local name=$1
    local port=$2
    
    echo -e "\n--- Testing $name ---"
    
    # Проверка статуса
    kubectl get pods -l app.kubernetes.io/instance=$name
    
    # Port-forward и curl
    kubectl port-forward service/${name}-fastapi-chart $port:80 &
    PF_PID=$!
    sleep 3
    
    echo "Calling http://localhost:$port/"
    curl -s http://localhost:$port/ | jq .
    
    kill $PF_PID 2>/dev/null
    sleep 1
}

# Тестируем каждый деплоймент
test_deployment "fastapi-prod" 8081
test_deployment "fastapi-dev" 8082
test_deployment "fastapi-test" 8083
test_deployment "fastapi-highload" 8084

echo -e "\n=== Comparing Resource Configurations ==="

for release in fastapi-prod fastapi-dev fastapi-test fastapi-highload; do
    echo -e "\n--- $release ---"
    kubectl describe pod -l app.kubernetes.io/instance=$release | grep -A 5 "Limits\|Requests" | head -10
done
