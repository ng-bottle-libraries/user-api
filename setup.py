from setuptools import setup
from namespace_user_api import __version__

if __name__ == '__main__':
    setup(name='namespace_user_api', version=__version__,
          author='Samuel Marks', license='MIT', py_modules=['namespace_user_api'],
          test_suite='tests')
