import subprocess
import os

processes = {}
def menu(answer):

    if processes.get(answer) != None:
        input('Уже выполняется\n' \
        '<Нажмите кнопку чтобы продолжить>\n'\
        ' ')
        return 0

    elif answer == 1:
        commands_chain = (
            "source /opt/ros/jazzy/setup.bash && "
            "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp && "
            "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/turtlebot3_simulations/turtlebot3_gazebo/models && "
            "ros2 launch main_simulation multi_sim_launch.py"
        )
        process = subprocess.Popen([
            'gnome-terminal', '--', 
            'bash', '-c', f"{commands_chain}; exec bash"
        ])

        processes[answer] = process
        input('Симуляция запущена\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0

    elif answer == 2:
        process = subprocess.Popen([
            'gnome-terminal', '--',
            'gz', 'sim', '-g'
        ])

        processes[answer] = process
        input('Gazebo запущен\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
    

    elif answer == 3:
        map_name = input('Введите название карты: ')
        server_uri = input('Введите адрес (default: ws://localhost:8000/_internal): ')
        config_name = input('Введите название конфига для адаптера (default: turtlebot3_fleet_config.yaml): ')
        graph = input('Введите название файла графов (default: 0.yaml): ')

        process = subprocess.Popen([
            'gnome-terminal', '--',
            'ros2', 'launch', 'lab_bringup', 'multi_real_launch.py', f'map_name:={map_name}',
            f'server_uri:={server_uri}', f'config_name:={config_name}', f'graph:={graph}'
        ])

        return 0






def main():

    start_zenohd = subprocess.Popen([
        'gnome-terminal', '--', 'zenohd'
    ])

    while True:
        answer = input('[1] - Запустить  симуляцию\n' \
        '[2] - Запустить Gazebo\n' \
        '[3] - Запустить логику RMF (Адаптер, заглушки погрузчиков/разгрузчиков, внутренние мозги RMF)\n' \
        '[4] - Создать новую карту (Переработать старую)\n' \
        '[5] - Добавить робота\n' \
        '[6] - Запустить отдельный адаптер\n' \
        '[7] - Закрыть все\n' \
        'Ваш ответ: ')

        try:
            if menu(int(answer)) == 1:
                break
            else:
                os.system('clear')
        except:
            input('Неверное число\n' \
            '<Нажмите кнопку чтобы продолжить>')
            os.system('clear')

    start_zenohd.terminate()

if __name__ == "__main__":
    main()