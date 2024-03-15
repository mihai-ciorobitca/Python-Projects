from stegano.lsb import hide, reveal
from PIL import Image

class Encryptor:
    def __init__(self):
        pass
    
    def encrypt(self,
                input_filename: str,
                message: str)->None:
        encrypted_image = hide(input_filename, message)
        encrypted_image.save("output.png")
    
    def decrypt(self, input_filename: str)->str:
        try:
            return reveal(input_filename)
        except:
            return "No message found"