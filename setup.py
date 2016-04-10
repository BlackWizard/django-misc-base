from setuptools import setup, find_packages

setup(
    name='django-misc-base',
    version='1.0.1',
    description='Base miscellaneous packages for django.',
    long_description=open('README.md').read(),
    author='BlackWizard',
    author_email='BlackWizard@mail.ru',
    url='http://github.com/BlackWizard/django-misc-base',
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires=['django-nginx-filter-image', ],
    zip_safe=False,
)
