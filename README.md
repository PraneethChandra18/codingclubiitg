# codingclubiitg website 2019
To initialize the project, run the following commands:
1. sudo apt-get install python3-venv
2. python3 -m venv env (If not made a virtual environment before)
3. pip3 install -r requirements.txt
4. Whenever you start working on the project, type the command: $ source env/bin/activate
5. After working on the project, type the command: $ deactivate
6. We need a key and decoded text from webmaster to activate the emailing feature and these should be kept in the file mysite/key.py .
   Use cryptography.fernet for encryption and decryption
