import os
import glob
import csv
import sqlite3


def get_db():
    for csvFile in glob.glob('data/*.csv'):
        file_name = os.path.basename(csvFile)
        with open(csvFile, mode='r', encoding='utf-8') as file_table:
            reader = csv.DictReader(file_table)
            fields = tuple(reader.fieldnames)
            con = sqlite3.connect('data/novedejulho.db')
            cur = con.cursor()
            cur.execute(f"CREATE TABLE '{file_name}' {fields};")
            reader_2 = csv.reader(file_table)
            for i in reader_2:
                i[5] = i[5].replace("'", "")
                i = tuple(i)
                cur.execute(f"INSERT INTO '{file_name}' VALUES {i};")
            con.commit()
    con.close()


if __name__ == '__main__':
    get_db()
