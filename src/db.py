import mysql.connector
from typing import Tuple
from datetime import datetime

DB_NAME = 'finapp'
conn = mysql.connector.connect(host="localhost", user='root', password='new_password', database=DB_NAME)

def create_table():
    sql = f"""
    CREATE TABLE `{DB_NAME}`.`user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(45) UNIQUE NOT NULL,
    `first_name` VARCHAR(45) NOT NULL,
    `last_name` VARCHAR(45) NOT NULL,
    `date_of_birth` DATETIME NOT NULL,
    `member_since` DATETIME NOT NULL,
    `phone_number` VARCHAR(20) NOT NULL,
    `email` VARCHAR(45) NOT NULL,
    `address` VARCHAR(100) NULL,
    `password` VARCHAR(45) NOT NULL,
    `balance` DECIMAL(10) NOT NULL,
    PRIMARY KEY (`id`));
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def seed_db():
    """seed = inserting database with some fake initial data to play around with."""
    add_user("john.wick", "John", "Wick", "12/12/1990", "(201) 323-7654", "john.wick@gmail.com", "1138 Continental Blvd, New York, NY 10001", "testing!",0)
    add_user("marty.byrd", "Marty", "Byrd", "01/01/1988", "(312) 515-1111", "marty.byrd@gmail.com", "4211 Osage Beach Pkwy, Osage Beach, MO 65065", "testing!", 100)

def add_user(username: str, first_name: str, last_name: str, date_of_birth: str, phone_number: str, email: str, address: str, password: str, balance: str):
    """FYI the date format used is dd/mm/yyyy. Feel free to try changing it.
    """
    sql = f"""INSERT INTO `{DB_NAME}`.`user` (`username`, `first_name`, `last_name`, `date_of_birth`, `member_since`, `phone_number`, `email`, `address`, `password`, `balance`) VALUES ('{username}', '{first_name}', '{last_name}', STR_TO_DATE('{date_of_birth}', '%d/%m/%Y'), STR_TO_DATE('{datetime.now().strftime('%d/%m/%Y')}', '%d/%m/%Y'), '{phone_number}', '{email}', '{address}', '{password}', {balance});"""
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def update_account_balance(id: int, amount: float) -> int:
    sql = f"""UPDATE `{DB_NAME}`.`user` SET balance = balance+{amount} where id = {id};"""
    cur = conn.cursor()
    cur.execute(sql)
    # Read the updated balance
    cur.execute(f"""SELECT balance FROM `{DB_NAME}`.`user` WHERE id = {id};""")
    updated_balance = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return updated_balance

def check_account_balance(id: int) -> int:
    sql = f"""SELECT balance FROM `{DB_NAME}`.`user` where id = {id};"""
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    return result[0]

def get_user_name(id: int) -> Tuple[str, str]:
    sql = f"""SELECT first_name, last_name FROM `{DB_NAME}`.`user` where id = {id};"""
    cur = conn.cursor()
    cur.execute(sql)
    
    for row in cur:
        print(row)
        return row
    return -1

def validate_login(username: str, password: str) -> int:
    sql = f"""SELECT id FROM `{DB_NAME}`.`user` where username = '{username}' and password = '{password}';"""
    cur = conn.cursor()
    cur.execute(sql)
    
    for row in cur:
        return row[0]
    return -1