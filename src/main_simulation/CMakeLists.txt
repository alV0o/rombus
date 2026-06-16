cmake_minimum_required(VERSION 3.8)
project(main_simulation)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rmf_ingestor_msgs REQUIRED)
find_package(rmf_dispenser_msgs REQUIRED)

add_executable(arm_mock_ingestor mocks/arm_mock_ingestor.cpp)
add_executable(arm_mock_dispenser mocks/arm_mock_dispenser.cpp)

ament_target_dependencies(arm_mock_ingestor rclcpp rmf_ingestor_msgs)
ament_target_dependencies(arm_mock_dispenser rclcpp rmf_dispenser_msgs)

install(TARGETS arm_mock_ingestor DESTINATION lib/${PROJECT_NAME})
install(TARGETS arm_mock_dispenser DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY rviz DESTINATION share/${PROJECT_NAME})
install(DIRECTORY params DESTINATION share/${PROJECT_NAME})
install(DIRECTORY config DESTINATION share/${PROJECT_NAME})
install(DIRECTORY coords DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
