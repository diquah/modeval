from setuptools import setup, find_packages


def read_desc():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='modeval',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version='1.0',
    license='MIT',
    description='Pure Python math evaluater without using eval() and no dependencies.',
    author='Ruby Cookinson',
    long_description=read_desc(),
    long_description_content_type='text/markdown',
    url='https://github.com/rubycookinson/modeval',
    download_url='https://github.com/rubycookinson/modeval/archive/refs/tags/0.1.tar.gz',
    keywords=['eval', 'expression', 'parser', 'math', 'string', 'modular'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
