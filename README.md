## Homework 13

Лекция https://kinescope.io/qhN5E4cMae3Wijn25KxGg1

Создаем докер-образ

```shell
docker build -t ser1ous/fastapi-hello:v1 .
docker login
docker push ser1ous/fastapi-hello:v1
```

Установка minicube

```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

Развертывание

```shell
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get pods

# Port forwarding
kubectl port-forward deployment/fastapi-deployment 8000:8000

curl http://localhost:8000

```

Включение ингресс

```shell
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```

Развертывание

```shell
kubectl apply -f ingress.yaml
kubectl get ingress

minikube ip

# <minikube-ip> fastapi.local
echo "$(minikube ip) fastapi.local" | sudo tee -a /etc/hosts

# check
curl http://fastapi.local

# or using tunnel
minikube tunnel

curl http://fastapi.local

```

