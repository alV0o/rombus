from setuptools import find_packages, setup

package_name = 'mes_rmf_adapter'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alvo',
    maintainer_email='alvo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'task_server = mes_rmf_adapter.adapter:main',
            'mock_server = mes_rmf_adapter.mock_server:main',
            'adapter = mes_rmf_adapter.adapter_2:main',
            'start_adapter = mes_rmf_adapter.start_adapter:main'
        ],
    },
)
