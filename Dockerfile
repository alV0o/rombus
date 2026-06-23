FROM osrf/ros:jazzy-desktop
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    curl \
    ros-jazzy-rmf-fleet-adapter \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*


RUN curl --proto '=https' --tlsv1.2 -sSf https://zenoh.io | sh

WORKDIR /ros2_ws
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
