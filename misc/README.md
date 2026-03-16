## ДЗ 13

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

### ДЗ 14

Применение лимитов

```shell
kubectl apply -f deployment.yaml
kubectl get pods
kubectl describe pod <pod-name> | grep -A 5 "Limits\|Requests"
```

Пересбор образа

```shell
docker build -t yourusername/fastapi-hello:v2 .
docker push yourusername/fastapi-hello:v2
```

Тестирование превышения лимитов

```shell
# Port-forward для тестирования
kubectl port-forward service/fastapi-service 8080:80

# В другом терминале:

# Проверяем текущее состояние
curl http://localhost:8080/metrics

# Тест 1: Превышение Memory Limit (лимит 128Mi)
# Пытаемся выделить 150MB
curl http://localhost:8080/stress-memory/150

# Смотрим, что происходит с подом
kubectl get pods -w
kubectl describe pod <pod-name>

# Под будет убит с ошибкой OOMKilled (Out Of Memory)
# Проверяем:
kubectl get pods
kubectl describe pod <pod-name> | grep -A 5 "Last State"

# Тест 2: Превышение CPU Limit
# CPU троттлится, но под не убивается
curl http://localhost:8080/stress-cpu/30

# В другом терминале смотрим метрики:
kubectl top pods
```

Тестирование с очень низкими лимитами

```shell
kubectl apply -f deployment-low-limits.yaml
kubectl port-forward service/fastapi-service 8080:80

# Попытка выделить 80MB убьёт под
curl http://localhost:8080/stress-memory/80
kubectl get pods -w
```

Публикация стресс-приложения

```shell
docker build -f Dockerfile.stress -t yourusername/stress-app:v1 .
docker push yourusername/stress-app:v1
```

Тестирование второго приложения без лимитов

```shell
# Сначала убедимся, что первое приложение работает
kubectl get pods -l app=fastapi
kubectl port-forward service/fastapi-service 8080:80 &
curl http://localhost:8080/

# Деплоим стресс-приложение БЕЗ лимитов
kubectl apply -f stress-deployment-no-limits.yaml

# Наблюдаем за ресурсами
kubectl top nodes
kubectl top pods

# Проверяем первое приложение - оно может тормозить
time curl http://localhost:8080/
kubectl describe nodes | grep -A 5 "Allocated resources"

# Смотрим события
kubectl get events --sort-by='.lastTimestamp' | head -20
```

Тестируем второе приложение с лимитами

```shell
# Удаляем предыдущую версию
kubectl delete deployment stress-deployment

# Деплоим с лимитами
kubectl apply -f stress-deployment-with-limits.yaml

# Смотрим статус
kubectl get pods
kubectl top pods

# Первое приложение должно работать стабильнее
curl http://localhost:8080/
```

Тестируем второе приложение с лимитами

```shell
kubectl delete deployment stress-deployment
kubectl apply -f stress-deployment-huge.yaml

# Некоторые поды будут в состоянии Pending
kubectl get pods
kubectl describe pod <pending-pod-name> | grep -A 10 "Events"

# Увидим: "Insufficient cpu" или "Insufficient memory"
```

Вывод ноды из планировщика

```shell
# Проверяем текущие ноды
kubectl get nodes

# Для minikube обычно одна нода с именем "minikube"
# Выводим ноду из планировщика (cordon)
kubectl cordon minikube

# Проверяем статус
kubectl get nodes
# Увидим: STATUS = Ready,SchedulingDisabled

# Проверяем, что первое приложение работает
kubectl get pods -l app=fastapi
curl http://localhost:8080/

# Поды продолжают работать на ноде!
kubectl describe node minikube | grep -A 5 "Non-terminated Pods"
```

Попытка задеплоить второе приложение

```shell
# Удаляем старый деплоймент стресс-приложения (если есть)
kubectl delete deployment stress-deployment --ignore-not-found=true

# Пытаемся задеплоить новый
kubectl apply -f stress-deployment-with-limits.yaml

# Проверяем статус подов
kubectl get pods -l app=stress

# Поды будут в состоянии Pending!
# Смотрим причину:
kubectl describe pod <stress-pod-name>

# В Events увидим:
# "0/1 nodes are available: 1 node(s) were unschedulable"
```

Drain - вывод ноды из обслуживания

```shell
# Drain эвиктит все поды с ноды
kubectl drain minikube --ignore-daemonsets --delete-emptydir-data

# Смотрим, что происходит с первым приложением
kubectl get pods -l app=fastapi -w

# Поды первого приложения будут удалены!
# Они не могут переехать, т.к. нода одна в minikube

# Проверяем
kubectl get pods -l app=fastapi
# Увидим: No resources found или Pending

# Проверяем деплоймент
kubectl get deployment fastapi-deployment
# DESIRED=2, CURRENT=0, READY=0, AVAILABLE=0
```

Возврат ноды в кластер

```shell
# Uncordon - возвращаем ноду в планировщик
kubectl uncordon minikube

# Проверяем статус ноды
kubectl get nodes
# STATUS должен быть: Ready (без SchedulingDisabled)

# Наблюдаем за подами
kubectl get pods -w

# Поды первого приложения начнут создаваться!
# Ждём, пока они станут Ready
kubectl wait --for=condition=Ready pod -l app=fastapi --timeout=120s

# Проверяем работоспособность
kubectl get pods -l app=fastapi
kubectl port-forward service/fastapi-service 8080:80 &
curl http://localhost:8080/

# Должно вернуться: {"message":"Hello World from FastAPI!", ...}
```