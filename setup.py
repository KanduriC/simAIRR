from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='simAIRR',
    version='0.1',
    packages=find_packages(exclude=["tests", "test.*"]),
    url='',
    license='MIT',
    author='Chakravarthi Kanduri',
    author_email='chakra.kanduri@gmail.com',
    description='',
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['sim_airr=simAIRR.simairr_cli.simairr_cli:execute']})

