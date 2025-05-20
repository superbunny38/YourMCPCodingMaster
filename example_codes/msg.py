from utils import create_random_message

def main():
    """
    Main function to demonstrate the use of the create_random_message function.
    """
    name = "Ch"
    message = create_random_message(name)
    print(message)

if __name__ == "__main__":
    main()