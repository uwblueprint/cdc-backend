from config import config


def main():
    if "dev" in config.get("app-env"):
        # Print out sample config for dev environments
        print("tornado port:", config.get("tornado.port"))
        print("tornado debug:", config.get("tornado.debug"))
        print("postgres hostname:", config.get("postgres.hostname"))
        print("postgres database:", config.get("postgres.database"))
        print("postgres user:", config.get("postgres.user"))


if __name__ == "__main__":
    main()
