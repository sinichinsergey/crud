CREATE TABLE users (
    user_id         integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_name       varchar(50),
    user_gender     boolean,  -- False = М, True = Ж
    user_birthdate  date,
    user_addr       varchar(100)
);

CREATE TABLE phones (
    phone_id    integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id     integer NOT NULL,
    phone_type  boolean,  -- False = Городской, True = Мобильный
    phone_num   varchar(11)
);

CREATE TABLE emails (
    email_id    integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id     integer NOT NULL,
    email_type  boolean,  -- False = Личная, True = Рабочая
    email_addr  varchar(100)
);