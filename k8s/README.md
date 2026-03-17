# ML Service in k8s

## Build app image

```shell
docker build -t diabetes-mlservice:latest .
```

## Deploy

```shell
minikube image load diabetes-mlservice:latest
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl port-forward svc/diabetes-mlservice 8000:8000
```

## Set Hosts

```shell
sudo nano /etc/hosts
192.168.49.2 diabetes.local
```

## Helm Charts

```shell
helm create diabetes-ml-chart
```