from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='purplship-server.manager',
      version='2021.7.7',
      description='Multi-carrier shipping API Shipments manager module',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/purplship/purplship-server',
      author='purplship',
      author_email='danielk.developer@gmail.com',
      license='Apache License Version 2.0',
      packages=find_packages("."),
      install_requires=[
            'purplship-server.core',
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
      ],
      zip_safe=False
)
