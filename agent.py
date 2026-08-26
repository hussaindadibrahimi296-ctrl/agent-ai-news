from database import test_database


def main():
    print("================================")
    print("AI News Agent")
    print("================================")

    try:
        if test_database():
            print("PostgreSQL: OK")
        else:
            print("PostgreSQL: FAILED")

    except Exception as error:
        print(f"Database error: {error}")


if __name__ == "__main__":
    main()
