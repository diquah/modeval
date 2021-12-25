from setuptools import setup, find_packages

VERSION = '1.3'


def read_desc():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='modeval',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version=VERSION,
    license='MIT',
    description='Pure Python modular math evaluater without using built-in eval() and no dependencies.',
    author='Diquah',
    long_description=read_desc(),
    long_description_content_type='text/markdown',
    url='https://github.com/diquah/modeval',
    download_url=f'https://github.com/diquah/modeval/archive/refs/tags/v{VERSION}.tar.gz',
    keywords=['eval', 'expression', 'parser', 'math', 'string', 'modular'],
    install_requires=[],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.10',
    ],
)
