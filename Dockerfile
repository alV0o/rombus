FROM osrf/ros:jazzy-desktop-full
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    curl \
    gnupg \
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-nav2-bringup \
    ros-jazzy-rmf-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    ros-jazzy-rosbag2 \
    python3-colcon-common-extensions \
    python3-ruamel.yaml \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages rosbags pycdr2 eclipse-zenoh nudged fastapi pydantic uvicorn

RUN mkdir -p /etc/apt/keyrings \
    && curl -L https://download.eclipse.org/zenoh/debian-repo/zenoh-public-key | gpg --dearmor --yes --output /etc/apt/keyrings/zenoh-public-key.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/zenoh-public-key.gpg] https://download.eclipse.org/zenoh/debian-repo/ /" | tee -a /etc/apt/sources.list > /dev/null \
    && apt-get update \
    && cd /tmp \
    && apt-get download zenoh zenohd zenoh-plugin-rest zenoh-plugin-storage-manager \
    && dpkg --unpack *.deb \
    && rm -f /var/lib/dpkg/info/zenohd.postinst \
    && dpkg --configure -a \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*


COPY ./src /tmp/src_for_analysis

# 3. Обновляем rosdep и автоматически ставим ВСЕ зависимости (RMF, Nav2, Gazebo и т.д.)
# Благодаря этому шагу огромный ручной список ros-jazzy-* больше не нужен!
RUN rosdep update && apt-get update && \
    rosdep install --from-paths /tmp/src_for_analysis --ignore-src -y -r --rosdistro jazzy \
    && rm -rf /tmp/src_for_analysis \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
