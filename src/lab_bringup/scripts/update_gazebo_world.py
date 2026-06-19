import xml.etree.ElementTree as ElementTree
import os
from ament_index_python import get_package_share_directory


def main(map_name, world_dir=None):
    if world_dir is None:
        world_dir = get_package_share_directory('test_building_maps')
    world_path = os.path.join(world_dir, 'worlds', f'{map_name}.world')

    
    try:
        with open(world_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if lines[0].startswith('<?xml'):
            return
        tree = ElementTree.parse(world_path)
        root = tree.getroot()

        world = root.find('world')

        if world is not None:
            plugin_imu = ElementTree.Element(
                'plugin',
                filename='gz-sim-imu-system',
                name='gz::sim::systems::Imu'
            )

            plugin_sensors = ElementTree.Element(
                'plugin',
                filename='gz-sim-sensors-system',
                name='gz::sim::systems::Sensors'
            )

            render_engine = ElementTree.SubElement(plugin_sensors, 'render_engine')
            render_engine.text='ogre2'

            world.insert(0, plugin_imu)
            world.insert(0, plugin_sensors)


            if hasattr(ElementTree, "indent"): #отступы
                ElementTree.indent(tree, space="  ", level=0)

            tree.write(
                world_path,
                encoding='utf-8',
                xml_declaration=True, 
                short_empty_elements=False
            )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    map_name = input('Input map name: ')
    main(map_name)