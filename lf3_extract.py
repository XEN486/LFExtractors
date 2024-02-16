from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os, tarfile, io

KEY = b'\x44\xee\x33\x41\x4a\x56\x48\xe1\x5e\x1c\x7e\x15\x85\xb1\x07\x38'

def decrypt_lf3(path):
    with open(path, 'rb') as f:
        # read the IV (stored in the first 16 bytes)
        IV = f.read(16)

        # create a cipher using AES with our key, a CTR with our IV and the default backend
        cipher = Cipher(algorithms.AES(KEY), modes.CTR(IV), backend=default_backend())

        # read the encrypted data
        ENC_DATA = f.read()

        # decrypt the data
        decryptor = cipher.decryptor()
        DEC_DATA = decryptor.update(ENC_DATA) + decryptor.finalize()

    # return the data
    return DEC_DATA

def extract_lf3(path):
    # get filename
    filename = os.path.splitext(os.path.basename(path))[0]
    
    # we decrypt our LF3 file into a tar
    print('Decrypting...')
    tar_data = decrypt_lf3(path)
        
    # say that we are extracting
    print('Extracting...')
    # create destination folder if it doesn't already exist
    if not os.path.exists(filename):
        os.makedirs(filename)
    
    # this is stupid but I can't think of a better way other than writing files
    with tarfile.open(fileobj=io.BytesIO(tar_data)) as tar:
        tar.extractall(filename)

def main():
    extract_lf3(str(input('Enter the path of the LF3 file: ')))

if __name__ == '__main__':
    main()
        
    
