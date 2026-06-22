cmake_minimum_required(VERSION 3.8)
project(lab_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(PROGRAMS scripts/start_all_actions.py DESTINATION lib/${PROJECT_NAME})
install(FILES
  scripts/update_config.py
  scripts/updater_fleet_robots.py
  scripts/update_gazebo_world.py
  scripts/add_robot.py
  scripts/update_arms.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
