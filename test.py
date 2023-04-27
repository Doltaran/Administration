from peewee import *
import sys
import os
from random import randint
from datetime import datetime, timedelta
import pytest

db = SqliteDatabase('my_database.db')

class Client(Model):
    name = CharField()
    city = CharField()
    address = CharField()

    class Meta:
        database = db

class Order(Model):
    client = ForeignKeyField(Client, backref='orders')
    date = DateField()
    amount = DecimalField()
    description = TextField()

    class Meta:
        database = db

def init_database():
    if os.path.exists('my_database.db'):
        os.remove('my_database.db')
    db.create_tables([Client, Order])

def fill_database():
    names = ['John', 'Alice', 'Bob', 'Mary', 'Peter', 'Olivia', 'James', 'Emma', 'Tom', 'Lucy']
    cities = ['New York', 'London', 'Paris', 'Tokyo', 'Moscow', 'Berlin', 'Madrid', 'Sydney', 'Beijing', 'Toronto']
    for i in range(10):
        client = Client.create(name=names[randint(0, 9)], city=cities[randint(0, 9)], address='Address ' + str(i+1))
        for j in range(5):
            order = Order.create(client=client, date=datetime.now()-timedelta(days=randint(0, 365)),
                                 amount=randint(100, 10000), description='Description ' + str(j+1))

def show_table(table_name):
    if table_name == 'clients':
        for client in Client.select():
            print(client.name, client.city, client.address, sep='\t')
    elif table_name == 'orders':
        for order in Order.select():
            print(order.client.name, order.date, order.amount, order.description, sep='\t')

def test_init_database():
    init_database()
    assert os.path.exists('my_database.db')

def test_database_columns():
    columns = set(('name','id', 'city', 'address'))
    assert set(Client._meta.fields.keys()) == columns
    columns = set(('client','id', 'date', 'amount', 'description'))
    assert set(Order._meta.fields.keys()) == columns

def test_fill_database():
    fill_database()
    assert Client.select().count() >= 10
    assert Order.select().count() >= 50

def show_table(table_name):
    if table_name == 'clients':
        for client in Client.select():
            print(client.name, client.city, client.address, sep='\t')
    elif table_name == 'orders':
        for order in Order.select():
            print(order.client.name, order.date, order.amount, order.description, sep='\t')

def main():
    if len(sys.argv) == 1:
        print('Usage: python main.py [init | fill | show [tablename]]')
    elif sys.argv[1] == 'init':
        init_database()
        print('Database created')
    elif sys.argv[1] == 'fill':
        fill_database()
        print('Database filled with test data')
    elif sys.argv[1] == 'show':
        if len(sys.argv) == 2:
            print('Usage: python main.py show [tablename]')
        elif sys.argv[2] == 'clients':
            show_table('clients')
        elif sys.argv[2] == 'orders':
            show_table('orders')
        else:
            print('Unknown table name')
    else:
        print('Unknown command')

if __name__ == '__main__':
    main()
