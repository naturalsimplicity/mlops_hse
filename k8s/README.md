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
kubectl port-forward svc/diabetes-mlservice 8110:80
```
