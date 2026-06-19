cmake_minimum_required(VERSION 3.5)
project(test_building_maps)

find_package(ament_cmake REQUIRED)

# 1. Находим исходные файлы карт
file(GLOB MAP_FILES "maps/*.building.yaml")

# Создаем директории для генерации
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/maps)
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/worlds)

# Список для отслеживания всех сгенерированных файлов
set(GENERATED_OUTPUTS)

# 2. Описываем правила генерации для каждой карты
foreach(MAP_FILE ${MAP_FILES})
  get_filename_component(MAP_NAME ${MAP_FILE} NAME_WE)
  
  file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/maps/${MAP_NAME})

  set(OUTPUT_WORLD "${CMAKE_CURRENT_BINARY_DIR}/worlds/${MAP_NAME}.world")
  # Замените 'floor_name' на имя вашего этажа, если rmf генерирует конкретный файл, 
  # либо оставьте общую директорию под управление CMake targets
  
  # Очередь сборки: генерация мира и сеток на этапе компиляции
  add_custom_command(
    OUTPUT ${OUTPUT_WORLD}
    COMMAND ros2 run rmf_building_map_tools building_map_generator gazebo 
            ${MAP_FILE} ${OUTPUT_WORLD} ${CMAKE_CURRENT_BINARY_DIR}/maps/${MAP_NAME}
    COMMAND ros2 run rmf_building_map_tools building_map_generator nav 
            ${MAP_FILE} ${CMAKE_CURRENT_BINARY_DIR}/maps/${MAP_NAME}/nav_graphs
    DEPENDS ${MAP_FILE}
    COMMENT "Generating Open-RMF worlds and maps for ${MAP_NAME}"
  )
  
  list(APPEND GENERATED_OUTPUTS ${OUTPUT_WORLD})

  get_filename_component(MAP_ABSOLUTE_PATH ${MAP_FILE} ABSOLUTE)
  install(
    FILES ${MAP_ABSOLUTE_PATH}
    DESTINATION share/${PROJECT_NAME}/maps/${MAP_NAME}
  )
endforeach()

# Создаем общую цель сборки, чтобы colcon знал, что нужно запустить генерацию
add_custom_target(${PROJECT_NAME}_generate_maps ALL DEPENDS ${GENERATED_OUTPUTS})

# 4. Экспортируем сгенерированные результаты
install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/maps/
  DESTINATION share/${PROJECT_NAME}/maps
)

install(
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

install(DIRECTORY assets DESTINATION share/${PROJECT_NAME})
install(DIRECTORY assets DESTINATION share/${PROJECT_NAME}/maps)
install(DIRECTORY configs DESTINATION share/${PROJECT_NAME})

ament_package()
