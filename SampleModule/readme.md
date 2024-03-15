# Install these modules first

wheel - for building the whl file will be uploaded on PyPi.org
twine - for upoading
setuptools - for setting up

Install modules
```bash
pip install setuptools, wheel, twine
```

# Commands to execute

Create build file
```bash
python setup.py sdist bdist_wheel
```

# Local testing

Install your module locally
```bash
pip install .\dist\your_module_name-0.1-py3-none-any.whl
```

Create a pythonscript and import your module
```bash
from your_modul_name import Class1, my_function1, myfunction2

c = Class1()
c.first_method()

my_function1()
myfunction2()
```

# Uploading on PyPi.org

Make sure you have your PyPi token in file .pypirc
located in C://Users//{your user}

The file should contain
[pypi]
```bash
username = __token__
password = TOKEN
```

Upload using twine
```bash
twine upload */dist
```

# Use your module globaly

Install your module using pip and enjoy :)