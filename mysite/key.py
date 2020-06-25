from cryptography.fernet import Fernet

key = b'LIfDFgoWBgTXGMAsAPDFth2uMO7Uk1mWJnrzDCNoJSo='
f = Fernet(key)

decode = f.decrypt(b'gAAAAABep-zrKwHtq6JyyBjfX_LVSrSqZj4wO09icivmk2lzYdVIt52DtxLmzepLzUW0TEZXbVOnh9oLI8q1lDkZznlsxA1qKg==').decode()
