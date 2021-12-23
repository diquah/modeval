from setuptools import setup, find_packages


def read_desc():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='modeval',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='0.1',
    license='MIT',
    description='Pure Python math evaluater without using eval() and no dependencies.',
    author='Ruby Cookinson',
    long_description=read_desc(),
    url='https://github.com/rubycookinson/modeval',
    download_url='https://github.com/rubycookinson/modeval/archive/refs/tags/0.1.tar.gz',
    keywords=['eval', 'expression', 'parser', 'math', 'string'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
