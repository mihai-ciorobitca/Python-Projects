from package import functions

if __name__ == "__main__":
    print("""
          1. Alarm
          2. Encrypt
          3. Decrypt
          4. QR
          5. Detect movement
          6. Screenshot
        """)
    user_input = input("Run program: ")
    if user_input == "1":
        functions.alarm()
    elif user_input == "2":
        functions.encrypt()
    elif user_input == "3":
        functions.decrypt()
    elif user_input == "4":
        functions.qr()
    elif user_input == "5":
        functions.detect_movement()
    elif user_input == "6":
        functions.screenshot()
    else:
        print("Invalid option")