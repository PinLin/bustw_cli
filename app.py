from views.main_view import MainView


def main():
    try:
        MainView().main()
    except EOFError:
        print()
        print("Bye!")
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
