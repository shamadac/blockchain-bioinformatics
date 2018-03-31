# -*- coding: utf-8 -*-

import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from django.core.files import File

def encrypt(key, file: 'File'):
    chunksize = 64 * 1024
   
    name = file.name.rsplit(".")[0]
    outputFile = os.getcwd() + "/DockerMarket/dockers/" + name + ".docker"
    
    filesize = str(file.size).zfill(16)
    
    IV = ''
    IV = os.urandom(16)
    
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    
    with open(outputFile, 'wb') as outfile:
        outfile.write(bytes(filesize, encoding = 'utf-8'))
        outfile.write(IV)
        
        for chunk in file.chunks(chunksize):
            
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - (len(chunk) % 16))
            
            outfile.write(encryptor.encrypt(chunk))


def decrypt(key, filename, reviewer: 'Reviewer'):
    chunksize = 64 * 1024
    filename_split = filename.rsplit(".")
    name, extension = filename_split[0], filename_split[1]
    outputFile = name + " (Reviewed_" + reviewer.initials + ")." + extension
    filename = "ms/" + name + ".thesis"
    
    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
    
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        
        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                
                if len(chunk) == 0:
                    break
                
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(bytes(password, encoding='utf-8'))
    return hasher.digest()

def cipher(operation, key, file, reviewer: 'Reviewer' = ""):
    if operation == 'encrypt':
        encrypt(key, file)
        print("Docker encrypted.")
    elif operation == 'decrypt':
        decrypt(key, file, reviewer)
        print("Manuscript body decrypted.")