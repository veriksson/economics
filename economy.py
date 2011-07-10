# -*- coding: utf-8 -*-

from collections import namedtuple
import csv
import datetime
from categories import categories

Transaction = namedtuple("Transaction", ["date", "note", "category", "amount"])

def contains(note, strings):
    for s in strings:
        if s in note: return True
    return False

def find_category(note):
    note = note.lower()
    if contains(note, categories["mat"]):
        return "Mat"
    if contains(note,categories["alkohol"]):
        return "Alkohol"
    if contains(note, categories["spel"]):
        return "Spel"
    if contains(note, categories["lön"]):
        return "Lön"
    return "Okänd"

def parse_csv(name):
    reader = csv.reader(open(name, "rb"), delimiter=",", quoting = csv.QUOTE_NONNUMERIC)
    return reader

def make_transactions(reader, transactions = None):
    if transactions is None:
        transactions = []

    first = True
    for row in reader:
        if first:
            first = False
            continue

        if row is None: continue

        try:
            date, note, category, amount, _ = row
            date = parse_to_date(date)

            if category == "":
                category = find_category(note)
            transactions.append(
                Transaction(date, note, category, amount))
        except Exception, e:
            pass
    return transactions

def get_amount(transactions):
    for transaction in transactions:
        yield transaction.amount

def parse_to_date(date):
    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    return dt

def get_first_and_last(transactions):
    first = max(transactions, key=lambda x: x.date)
    last = min(transactions, key=lambda x: x.date)
    return first, last

def find_by_category(category, transactions):
    return [transaction for transaction in transactions 
            if transaction.category == category]

def list_categories(transactions):
    return set([t.category for t in transactions])

def produce_months(transactions):
    from itertools import groupby
    sgkey = lambda x: (x.date.year, x.date.month)
    st = sorted(transactions, key = sgkey)
    groups = groupby(st, key = sgkey)
    months = []
    for group in groups:
        months.append(Month(group[0], [t for t in group[1]]))
    return months

class Month(object):
    def __init__(self, date, transactions):
        self.date = datetime.datetime(date[0], date[1], 1)
        self.transactions = transactions

    def income(self):
        return sum(t.amount for t in self.transactions if t.amount >= 0)

    def expenses(self):
        return sum(t.amount for t in self.transactions if t.amount < 0)

    def net(self):
        return sum(t.amount for t in self.transactions)

def write_to_file(months, filename="out.csv"):
    writer = csv.writer(open(filename, "wb"), delimiter = ",")
    writer.writerows([[x.date, x.income(), x.expenses(), x.net()] for x in months])


if __name__ == "__main__":
    import sys
    script, csv_file = sys.argv
    reader = parse_csv(csv_file)
    transactions = make_transactions(reader)
    months = produce_months(transactions)
    write_to_file(months, "a:/out.csv")
