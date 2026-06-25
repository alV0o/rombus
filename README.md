> Program
> # **Rombus** - **R**obotics, **O**rchestration, **M**ES and **B**atch **U**nit **S**ystem

# Запуск с помощью Docker
1. Зайти в корневую папку проекта, где лежат файлы `Dockerfile` и `docker-compose.yml`
2. Открыть ее в терминале и написать команду `sudo docker compose build rombus_app
3. После окончания сборки запустить контейнер командой `sudo docker compose up -d`
4. Перейти в терминал изолированной среды Docker с помощью команды `docker exec -it rombus_container bash`
### Теперь вы можете запускать окружение контейнера для корректной работы с программой когда угодно последними двумя командами

## Вам понадобится если вы хотите работать в своем окружении

- Ubuntu 24.04 (Проект был разработан и протестирован на этой ОС)
- [ROS2 Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) 
- [Gazebo Harmonic](https://gazebosim.org/docs/harmonic/install/)
- [Nav2](https://docs.nav2.org/getting_started/index.html)
- [Open-RMF](https://github.com/open-rmf/rmf)
- [Зависимости для free_fleet](https://github.com/open-rmf/free_fleet#dependency-installation-source-build-and-setup) (Zenoh, CycloneDDS, zenoh-bridge, Python libraries)
- Python libraries: FastAPI, Uvicorn, Pydantic, ruamel.yaml
#### При наличии ошибок с зависимостями после запуска, попробуйте использовать `rosdep` с помощью команды 
```bash
cd ~/your_ws
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
```

# Шаги для создания вашей первой симуляции производства с помощью роботов в Rombus

1. Открыть корневую папку проекта в терминале и прописать команду `source /opt/ros/jazzy/setup.bash`
2. Открыть корневую папку проекта в терминале и прописать команду `colcon build`
3. Поместить вашу черно-белую карту для роботов в формате PNG в папку `src/test_building_maps/assets`
4. Прописать команду `source install/setup.bash` 
5. Запустить скрипт командой `ros2 run lab_bringup start_all_actions.py`
6. Выберите создание карты, и у вас откроется приложение [traffic-editor](documentation/Traffic-editor.md). С его помощью создайте карту, сохраните и закройте приложение. Дальше следуйте указаниям скрипта-меню
7. [Создайте робота(-ов)](documentation/Create_robot.md)
8. Запустите симуляцию 
9. Запустите отображение 3D мира с помощью `Gazebo`
10. Запустите [RMF-Web](documentation/RMF-Web.md) в отдельных терминалах 
11. Запустите [логику Open-RMF](documentation/Fleet_Adapter.md) (Рекомендуется предварительно дождаться полного запуска симуляции!)
12. \[Опционально\] Запустите отдельный [адаптер](documentation/Fleet_Adapter.md) с иными настройками

#### Вы уже можете пользоваться работой системы, но если Вы уже понимаете как работать с [OpenMES](), то можно попробовать работу полноценной системы производства.

12. Запустите транслятор точек для `OpenMES`, который позволит `OpenMes` получать точные координаты ваших рабочих станций
13. Запустите симуляцию работы производственной линии, которая будет выполнять шаги батчей, которые рассчитаны на работу роботов

## Поздравляю, вы создали первую симуляцию производства!

### В случае ошибок можете посмотреть логи в файлах по пути `your_workspace/install/lab_bringup/lib/logs`
