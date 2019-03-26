import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='datamax_printer',
    version='0.1.1',
    author='Michael Blättler',
    author_email='michael.blaettler@innetag.ch',
    description='Controll a datamax o\'neil labelprinter using DPL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/inNETMonitoring/datamax-python-adapter',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries'
    ]
)
