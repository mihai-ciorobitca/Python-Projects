from encryptor import Encryptor

e = Encryptor()

input_filename = input("Enter filename: ")
message = e.encrypt(input_filename=input_filename)
print(message)