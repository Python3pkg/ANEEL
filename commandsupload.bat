"C:\Program Files (x86)\Python35-32\python.exe" setup.py sdist
"C:\Program Files (x86)\Python35-32\python.exe" setup.py bdist_wheel
"C:\Program Files (x86)\Python35-32\python.exe" setup.py register
"C:\Program Files (x86)\Python35-32\Scripts\twine.exe" upload dist/*