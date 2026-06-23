# RMF Web

## Команды для старта

1. Запуск Dashboard 
```bash
docker run \
  --network host -it --rm \
  -e RMF_SERVER_URL=http://localhost:8000 \
  -e TRAJECTORY_SERVER_URL=ws://localhost:8006 \
  ghcr.io/open-rmf/rmf-web/demo-dashboard:latest
```
2. Запуск сервера
```bash
docker run \
  --network host -it --rm \
  -e ROS_DOMAIN_ID=55 \
  -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
  ghcr.io/open-rmf/rmf-web/api-server:jazzy
```

Подробнее в репозитории [rmf-web](https://github.com/open-rmf/rmf-web#rmf-web)