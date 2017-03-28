from setuptools import setup
setup(
    name='PedalPi - Physical',
    packages=[
        'physical',
        'physical/navigation',
        'physical/sevensegments'
    ],
    test_suite='test',
    install_requires=['gpiozero'],
)
