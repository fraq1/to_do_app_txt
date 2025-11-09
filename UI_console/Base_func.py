class Command:
    OPEN = '1'
    READ_TODAY = '2'
    WRITE_TODAY = '3'
    CLOSE = '4'


print("Hello! This is to-do-app!\nPlease chose option:")
print("1 - chose day to open.\n2 - open to do list for today.\n3 - write task for today.\n4 - close app")
command = input()
while command != Command.CLOSE:
    match command:
        case Command.OPEN:
            print(1)
            command = input()
        case Command.READ_TODAY:
            print(2)
            command = input()
        case Command.WRITE_TODAY:
            print(3)
            command = input()