from setuptools import setup, find_packages

setup(name='clisupport',
      version='0.1.0',
      description='Tools for support team',
      url='https://github.com/khanhphamhong/clisupport',
      author='Khanh Pham Hong',
      author_email='me@khanhphamhong.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['cx_Oracle', 'requests','PrettyTable'],
      entry_points={
          'console_scripts': [
              'clisupport = clisupport.clisupport:main'
          ]
      },
      platforms=['Linux', 'Darwin'],)