import sys
reload(sys)
sys.setdefaultencoding('utf8')
from src.scripts.auto_log_in import log_in
import sys


def main():
    log_in()


if __name__ == "__main__":
    main()