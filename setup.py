from setuptools import setup, find_packages

setup(
    name='component_recognizer',
    version='0.1',
    author='afomin',
    company='afomin',
    author_email='alexanderfomin1992@mail.ru',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'component_recognizer= component_recognizer.start_processing:main',
            'camera_calibration= component_recognizer.camera_calibration:main',
        ],
    },
    package_data={
        'component_recognizer': ['pcb_images/*', ],
        'camera_calibration': ['calib_images/*', 'calibration', ]
    },
)
