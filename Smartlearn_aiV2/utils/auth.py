import csv

USERS_CSV = "data/users.csv"


def authenticate(username, password):
    """
    Validates user credentials from CSV
    """
    with open(USERS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                row["username"] == username and
                row["password"] == password
            ):
                return {
                    "username": row["username"],
                    "role": row["role"]
                }
    return None
