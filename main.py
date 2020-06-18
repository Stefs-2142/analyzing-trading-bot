from model import DbUtils

import settings


def main():
    db = DbUtils()
    users = db.getUsers()
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
