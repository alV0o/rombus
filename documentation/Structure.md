# Структура проекта

Изначально структура в ROS2 делится на папки **src** (исходники), **build** (папка для ускорения сборки), **install** (папка с собранными файлами). Внутри себя они содержат [**пакеты**](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html) с [нодами](https://stepik.org/lesson/1597035/step/1?unit=1618661), [launch-файлами](https://stepik.org/lesson/1505350/step/1?unit=1525496) и т.д.

## src
1. Пакет [`free_fleet`](https://github.com/open-rmf/free_fleet) содержит классы для удобного взаимодействия с типами данных из ROS2
2. Пакет [`free_fleet_adapter`](https://github.com/open-rmf/free_fleet)
	- `action.py` — абстрактный класс для обработки [`action`](https://stepik.org/lesson/1505348/step/1?unit=1525494) роботом
	- `robot_adapter.py` — абстрактный класс адаптера  для одного `turtlebot3`
	- `nav2_robot_adapter.py` — реализация адаптера `robot_adapter` с учетом особенностей `Nav2`
	- `fleet_adapter.py` — полноценный [адаптер](documentation/Fleet_Adapter.md) для флота роботов с гибкой настройкой (sim_time, server_uri, config_path, nav_graph_path)
	- `fleet_adapter.launch.xml` — удобный launch-файл для запуска `fleet_adapter.py`
3. Пакет `free_fleet_examples`
	- Папка `config` — содержит три подпапки `fleet`, `template`, `zenoh`, которые содержат конфигурационные файлы для работы программы. `template` - содержит шаблоны [`fleet_config`](https://osrf.github.io/ros2multirobotbook/integration_fleets_adapter_tutorial.html#2-update-the-configyaml-file), `fleet` содержит файлы, которые являются по шаблону заполненными конфигурационными файлами, а `zenoh` содержит файл конфигурации для [Zenoh](https://github.com/eclipse-zenoh/zenoh?tab=readme-ov-file#configuration-options)
	- Папка `launch` — содержит файлы `rmf_common.launch.xml`, `nav2_unique_multi_tb3_simulation_fleet_adapter.launch.xml` и `turtlebot3_world_rmf_common.launch.xml`. Первый запускает все необходимые ноды от Open-RMF, второй запускает `fleet_adapter.launch.xml` с конфигурациями, а третий запускает сам `rmf_common.launch.xml`, но с конфигурациями
4. Пакет `lab_bringup`
	- `multi_real_launch.py` — launch-файл для запуска "мозгов" Open-RMF, адаптера, заглушек для погрузчика/разгрузчика
	- `add_robot.py` — скрипт для добавления робота в конфигурационный файл для симуляции и `fleet_config`.
	- `update_arms.py` — скрипт для добавления погрузчиков/разгрузчиков в конфигурационный файл исходя из графов путей карты
	- `update_config.py` — скрипт для расчета [конфигурационного файла](https://github.com/ros-navigation/navigation2/tree/main/nav2_map_server#map-server-1) для `Nav2` исходя из данных из `*.building.yaml` файла карты
	- `update_gazebo_world.py` — скрипт для добавления необходимых плагинов в разметку файла карты `*.world`
	- `updater_fleet_robots.py` — скрипт для изменения данных о роботах и координатах в файлах `fleet_config`
	- `start_all_actions.py` — самый главный скрипт, который запускает меню, а также позволяет пользователю легко использовать все доступные скрипты и launch файлы для работы с Rombus
5. Пакет `main_simulation`
	- Папка `mocks` — содержит файлы `arm_mock_dispenser.cpp` и `arm_mock_ingestor.cpp`, которые выполняют роль заглушек для погрузчика и разгрузчика, слушая топики от Open-RMF
	- `arms_launch.py` — launch-файл для запуска заглушек погрузчика/загрузчика с помощью конфигурационного файла `mocks.yaml`
	- `rviz_launch.py` — launch-файл для настроенного запуска [RViz](https://stepik.org/lesson/1612393/step/1?unit=1634192) с помощью конфигурационного файла из папки `rviz`
	- `tb3_simulation_launch.py` — launch-файл для запуска робота `turtlebot3` с множеством конфигураций
	- `multi_sim_launch.py` — launch-файл для запуска всей симуляции. Он запускает заглушки, всех роботов, исходя из конфигурационного файла своей карты и сервер `Gazebo` для корректной 3D симуляции роботов в пространстве
	- Папка `params` — содержит файлы [`nav2_params`](https://docs.nav2.org/configuration/index.html), которые сконфигурированы с разной допустимой скоростью для роботов
6. Пакет `mes_rmf_adapter`
	- `adapter_2.py` — скрипт, который является адаптером между `Open-RMF` и `OpenMES`. Он делает API запрос к MES системе и просматривает все шаги и ищет, которые сейчас должны наступить. Если среди них есть шаг с нужной инструкцией, то он его переводит в понятный для `Open-RMF` формат и отправляет задачу на доставку для роботов
	- `mock_server.py` — скрипт заглушка, который симулирует инструкцию от `OpenMES`
	- `translator_coords.py` — скрипт, который поднимает небольшой API сервер, для того, чтобы `OpenMES` мог обращаться и забирать точки погрузки и разгрузки для нужной карты, а также получать все названия карт
	- `utils.py` — скрипт, который содержит метод поиска  точек погрузки и разгрузки
7. Пакет `test_building_maps`
	- Папка `assets` — содержит PNG изображения карты
	- Папка `configs/template` — содержит шаблон для [конфигурационного файла](https://github.com/ros-navigation/navigation2/tree/main/nav2_map_server#map-server-1) для `Nav2`
	- Папка `maps` — содержит `*.building.yaml` файл для карты, который содержит все необходимые данные о карте, созданной в [`traffic-editor`](documentation/Traffic-editor.md)
	- `CMakeLists.txt` — содержится во многих пакетах для копирования папок в `install`, но в этом пакете он производит также дополнительное выполнение скриптов сборки мира на базе карты для `Gazebo` с помощью , а также формирование файлов графов `nav_graphs` для карты с помощью [`building_map_generator`](https://osrf.github.io/ros2multirobotbook/simulation.html#building-map-generator)
## install
### В основном содержит то же самое, что и src, но есть отличия:
#### (Практически все файлы находятся в подпапке `<package>/share/<package>`)
1. Пакет `free_fleet_examples`
	- Папка `config` — в подпапке `fleet` изменяются значения только внутри **install**, а не **src**
2. Пакет `main_simulation`
	- Папка `config` — внутри находятся все файлы конфигурации роботов для конкретной карты в файлах `*_robot_config.yaml`, а также файл `mocks.yaml` для погрузчиков и разгрузчиков
3. Пакет `lab_bringup`
	- Папка `logs` (**Находится не в share, а в lib**) — внутри содержит файлы `*.log`, которые хранят логи всех процессов, запущенных с помощью `start_all_actions.py`. С их помощью можно точно посмотреть проблему, где она произошла и почему
4. Пакет `test_building_maps`
	- Папка `configs` — содержит конфигурационные файлы `Nav2` для каждой карты
	- Папка `worlds` — содержит все `*.world` файлы, которые нужны для работы `Gazebo`.
	- Папка `maps` — содержит подпапки каждой карты, внутри которой лежат `*.building.yaml`, а также папка с этажом и графами путей
## Вне src и install
1. Папки`documentation` и `screenshots` — содержит всю документацию, которую вы читали
2. файлы `Dockerfile` и `docker-compose.yml` — позволяют собрать папку в Docker-контейнер для запуска без скачивания зависимостей на свой ПК