import subprocess


def print_by_less(article: str):
    try:
        less = subprocess.Popen("less", stdin=subprocess.PIPE)
        less.stdin.write(article.encode("utf-8"))
        less.stdin.close()
        less.wait()

    except FileNotFoundError:
        print(article)
