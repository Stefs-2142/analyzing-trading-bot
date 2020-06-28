from model import DbUtils


def main():
    db = DbUtils()
    users = db.getUsers()
    for user in users:
        print(user)


if __name__ == "__main__":
    main()
