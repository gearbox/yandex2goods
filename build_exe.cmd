rem Needs pyinstaller package
rem Use 'pip install pyinstaller'
rem You have to have Python/Scripts in your OS Path ENV variable

python pyinstaller -w -F -i static\favicon.ico xls_to_xml.py
