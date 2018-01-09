import os
from distutils.core import setup



def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

setup(name='simple_upload',
      version='1.0',
      packages=['simple_upload'],
      package_data=package_data("simple_upload", ["templates", "migrations"]),
      ) 
 
