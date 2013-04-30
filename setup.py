from distutils.core import setup

setup(
    name='python-propellor',
    version='0.1.0',
    description='Pretty progress and load indicators',
    author='Thomas Einsporn',
    author_email='mbarkhau@gmail.com',
    long_description=open("README.md", 'r').read(),
    license="BSD",
    url="https://github.com/pixelkaiser/python-propeller",
    download_url="https://bitbucket.org/nexttuesday/django-rpc/",
    packages=[ 'propeller' ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries'
    ],
)

