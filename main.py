import DataHandler
import OddsMath

def main():
    handler = DataHandler.DataHandler()
    for filename in handler.list_files():
        print(filename)


if __name__ == "__main__":
    print("Running...")
    main()