import subprocess
import os
import shutil
import update_config
import updater_fleet_robots
import update_gazebo_world
import add_robot
import signal
import time
import sys
from mes_rmf_adapter import update_arms

processes = {}
log_files = {}
def menu(answer):

    if processes.get(answer) != None:
        process = processes[answer]

        if process.poll() is None:
            input('Уже выполняется\n' \
            '<Нажмите кнопку чтобы продолжить>\n'\
            ' ')
            return 0
        else:
            del processes[answer]
            if answer in log_files:
                log_files[answer].close()
                del log_files[answer]

    if answer == 1:
        map_name = input('Введите название карты для симуляции: ')

        update_arms.main(map_name)

        commands_chain = (
            "source /opt/ros/jazzy/setup.bash && "
            "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp && "
            "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:~/turtlebot3_simulations/turtlebot3_gazebo/models && "
            "stdbuf -oL -eL ros2 launch main_simulation multi_sim_launch.py"
        )

        log_file = open("../logs/process_1_simulation.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen(
            ['bash', '-c', f"{commands_chain}; exec bash"],
            stdout=log_file,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            preexec_fn=os.setsid,
            text=True,
        )   
        time.sleep(1)

        process.stdin.write(f"{map_name}\n")
        process.stdin.flush()

        processes[answer] = process
        input('Симуляция запущена (Логи в process_1_simulation.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0

    elif answer == 2:
        log_file = open("../logs/process_2_gazebo.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen(
            ['gz', 'sim', '-g'],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            bufsize=0
        )

        processes[answer] = process
        input('Gazebo запущен (Логи в process_2_gazebo.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
    

    elif answer == 3:
        map_name = input('Введите название карты: ')

        updater_fleet_robots.main(map_name)

        server_uri = input('Введите адрес (default: ws://localhost:8000/_internal): ')
        config_name = input('Введите название конфига для адаптера (default: turtlebot3_fleet_config.yaml): ')
        graph = input('Введите название файла графов (default: 0.yaml): ')

        log_file = open("../logs/process_3_rmf.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen([
            'stdbuf', '-oL', '-eL',
            'ros2', 'launch', 'lab_bringup', 'multi_real_launch.py', 
            f'map_name:={map_name}', f'server_uri:={server_uri}', 
            f'config_name:={config_name}', f'graph:={graph}'
        ], stdout=log_file, stderr=subprocess.STDOUT, bufsize=0)


        processes[answer] = process
        input('RMF Запущен (Логи в process_3_rmf.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0

    elif answer == 4:

        log_file = open("../logs/traffic-editor.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen(
            ['traffic-editor'],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            bufsize=0)
        process.wait()

        print('Началась пересборка...')
     
        ws_path = os.path.expanduser('~/test_ws')

        colcon_process = subprocess.Popen([
            'colcon', 'build', '--packages-select', 'test_building_maps'
        ], cwd=ws_path)
        colcon_process.wait()

        print('Пересборка закончилась')
        map_name=input('Введите название карты: ')
        update_config.main(map_name)
        update_gazebo_world.main(map_name)

        input('Карта создана\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0

    elif answer == 5:
        map_name = input('Введите название карты: ')
        add_robot.main(map_name)
        input('Робот создан\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
    
    elif answer == 6:

        map_name = input('Введите название карты: ')
        server_uri = input('Введите адрес (default: ws://localhost:8000/_internal): ')
        config_name = input('Введите название конфига для адаптера (default: turtlebot3_fleet_config.yaml): ')
        graph = input('Введите название файла графов (default: 0.yaml): ')

        commands_chain = (
            "source ~/test_ws/install/setup.bash && "
            "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp && "
            "export ROS_DOMAIN_ID=55 && "
            f"stdbuf -oL -eL ros2 launch free_fleet_examples nav2_unique_multi_tb3_simulation_fleet_adapter.launch.xml  server_uri:={server_uri} map_name:={map_name} config_name:={config_name} graph:={graph}"
        )
        
        log_file = open("../logs/process_6_adapter.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen(
            ['bash', '-c', commands_chain],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            bufsize=0,
            preexec_fn=os.setsid # Важно для цепочек команд
        )

        processes[answer] = process
        input('Адаптер запущен (Логи в process_6_adapter.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
    
    elif answer == 7:

        current_script_path = os.path.abspath(__file__)

        # 2. Поднимаемся на 4 уровня вверх:
        # scripts -> lab_bringup -> src -> test_ws
        current_dir = current_script_path
        for _ in range(4):
            current_dir = os.path.dirname(current_dir)

        workspace_root = current_dir
        target_script = os.path.join(
            workspace_root,
            "src",
            "mes_rmf_adapter",
            "mes_rmf_adapter",
            "translator_coords.py",
        )

        if not os.path.exists(target_script):
            print(f"[Ошибка] Файл не найден по пути: {target_script}")
            return 1

        log_file = open("../logs/process_7_translator.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        process = subprocess.Popen(
            [sys.executable, os.path.basename(target_script)],
            cwd=os.path.dirname(target_script),
            stdout=log_file,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )

        processes[answer] = process
        input('Транслятор запущен (Логи в process_7_translator.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
    
    elif answer == 8:
        log_file = open("../logs/process_8_sim_mes_system.log", "w", encoding="utf-8")
        log_files[answer] = log_file

        commands_chain = (
            "export ROS_DOMAIN_ID=55 && "
            f"stdbuf -oL -eL ros2 run mes_rmf_adapter adapter"
        )

        process = subprocess.Popen(
            ['bash', '-c', commands_chain],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            bufsize=0,
            stdin=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        time.sleep(1)

        id_work_order = input('Введите ID заказа: ')

        process.stdin.write(f"{id_work_order}\n")
        process.stdin.flush()

        processes[answer] = process
        input('Симуляция выполнения MES системы (Логи в process_8_sim_mes_system.log)\n' \
        '<Нажмите кнопку чтобы продолжить>\n'
        ' ')
        return 0
        


    elif answer in(9, 0):
        for ans, proc in list(processes.items()):
            try:
                # Если процесс запускался через bash -c (блоки 1 и 6), 
                # нужно убить всю группу процессов, иначе bash умрет, а ROS-ноды останутся жить.
                if ans in (1, 6, 8):
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
                
                proc.wait(timeout=3)
            except Exception:
                # Если мягко не закрылся — убиваем принудительно
                try:
                    if ans in (1, 6, 8):
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    else:
                        proc.kill()
                except:
                    pass
            
            # Закрываем дескриптор файла лога
            if ans in log_files:
                log_files[ans].close()
                del log_files[ans]
                
        processes.clear()
        
        if answer == 9:
            input('Все процессы успешно остановлены\n<Нажмите кнопку чтобы продолжить>\n ')
            return 0
        return 1





def main(log_clear):

    os.makedirs("../logs", exist_ok=True)
    log_file = open("../logs/zenohd.log", "w", encoding="utf-8")

    start_zenohd = subprocess.Popen(
        ['zenohd'],
        stdout=log_file,
        stderr=subprocess.STDOUT,
        bufsize=0)
    
    while True:
        answer = input('[1] - Запустить  симуляцию\n' \
        '[2] - Запустить Gazebo\n' \
        '[3] - Запустить логику RMF (Адаптер, заглушки погрузчиков/разгрузчиков, внутренние мозги RMF)\n' \
        '[4] - Создать новую карту (Переработать старую)\n' \
        '[5] - Добавить робота\n' \
        '[6] - Запустить отдельный адаптер\n' \
        '[7] - Запустить транслятор точек для OpenMES\n' \
        '[8] - Запустить симуляцию выполнения MES системы\n' \
        '[9] - Закрыть все\n' \
        '[0] - Выйти\n' \
        'Ваш ответ: ')

        try:
            if menu(int(answer)) == 1:
                break
            else:
                if log_clear == 0:
                    os.system('clear')
        except Exception as e:
            input(f'[ОШИБКА]: {e}\n' \
            '<Нажмите кнопку чтобы продолжить>')
            if log_clear == 0:
                os.system('clear')


    start_zenohd.terminate()
    log_file.close()


if __name__ == "__main__":
    while True:
        log_clear = int(input('Очищать логи? Да [0] | Нет [1]\n'))
        if log_clear == 0 or log_clear ==1:
            break

    main(log_clear)