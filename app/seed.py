from faker import Faker

import seed_database

DATA_SIZE = 50


def gen_users() -> list[tuple]:
    """ user_name, user_gender, user_birthdate, user_addr """
    values = [(
        f"{fake.first_name()} {fake.middle_name()} {fake.last_name()}",
        fake.pybool(),  # False == М, True == Ж
        fake.date_of_birth(),
        fake.address())
        for _ in range(DATA_SIZE)]
    return values


def gen_phones() -> list[tuple]:
    """ user_id, phone_type, phone_num """
    values = [(
        _ + 1,
        fake.pybool(),  # False == Городской, True == Мобильный
        "".join(filter(str.isdigit, fake.phone_number())))
        for _ in range(DATA_SIZE)]
    return values


def gen_emails() -> list[tuple]:
    """ user_id, email_type, email_addr """
    values = [(
        _ + 1,
        fake.pybool(),  # False == Личная, True == Рабочая
        fake.email())
        for _ in range(DATA_SIZE)]
    return values


def insert_data(table_name, column_names, values: list[tuple]) -> None:
    try:
        placeholders = ("%s, " * len(values[0])).rstrip(", ")
        insert_query = (f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders}); """)
        with conn.cursor() as cursor:
            cursor.executemany(insert_query, values)
        conn.commit()
        print(f'INFO:     Insertion into table "{table_name}" successful')
    except Exception as _ex:
        print(f'INFO:     Error while inserting into "{table_name}": {_ex}')


if __name__ == "__main__":
    try:
        conn = seed_database.get_connection()
        fake = Faker(locale="ru_RU")

        insert_data(
            table_name="users",
            column_names="user_name, user_gender, user_birthdate, user_addr",
            values=gen_users())
        insert_data(
            table_name="phones",
            column_names="user_id, phone_type, phone_num",
            values=gen_phones())
        insert_data(
            table_name="emails",
            column_names="user_id, email_type, email_addr",
            values=gen_emails())
    finally:
        if conn:
            conn.close()
        print("INFO:     PostgreSQL connection closed")
