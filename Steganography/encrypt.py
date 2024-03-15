from encryptor import Encryptor

e = Encryptor()

message = input("Enter a message to encrypt: ")
input_filename = input("Enter filename to encrypt: ")
e.encrypt(input_filename=input_filename,
          message=message)