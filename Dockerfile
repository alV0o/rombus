FROM osrf/ros:jazzy-desktop-full
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ros-jazzy-rmf-dev \
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    python3-colcon-common-extensions \
    python3-ruamel.yaml \
    && rm -rf /var/lib/apt/lists/*

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


WORKDIR /ros2_ws
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
