import peewee as pw
import sqlite3 as lite
import sqlalchemy as sql

db = pw.MySQLDatabase('johnydb', user='john', passwd='megajohny')

class Book(pw.Model):
    author = pw.CharField()
    title = pw.TextField()

    class Meta:
        database = db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()
for book in Book.filter(author="me"):
    print(book.title)