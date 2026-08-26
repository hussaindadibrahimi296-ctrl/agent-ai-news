from database import init_database, test_database


def main():
    print("================================")
    print("AI News Agent")
    print("================================")

    try:
        if test_database():
            print("PostgreSQL connection: OK")

            init_database()

            print("Database initialization: OK")
            print("All tables are ready.")

        else:
            print("PostgreSQL connection: FAILED")

    except Exception as error:
        print(f"Database error: {error}")


if __name__ == "__main__":
    main()
