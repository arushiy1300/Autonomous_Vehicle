from setuptools import setup

package_name = 'encoder_odometry'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name,
            ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='qtpi',
    maintainer_email='qtpi@todo.todo',
    description='Encoder Odometry',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odom_node = encoder_odometry.odom_node:main',
        ],
    },
)
