import sys

from views.main_view import MainView


def main():
    # 讀取外部參數
    choice = sys.argv.copy()
    choice.pop(0)

    try:
        MainView().main(choice)
    except EOFError:
        print()
        print("Bye!")
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
