import os
import glob
import csv
import sqlite3


def main():
    get_db()


def get_db():
    for csvFile in glob.glob('data/*.csv'):
        file_name = os.path.basename(csvFile)
        with open(csvFile, mode='r', encoding='utf-8') as file_table:
            reader = csv.DictReader(file_table)  # Não vai ler csv com delimiter='\t'
            fields = tuple(reader.fieldnames)
            con = sqlite3.connect('data/novedejulho.db')
            cur = con.cursor()
            cur.execute(f"CREATE TABLE '{file_name}' {fields};")
            reader_2 = csv.reader(file_table)  # Não vai ler csv com delimiter='\t'
            for i in reader_2:
                i = tuple(i)
                cur.execute(f"INSERT INTO '{file_name}' VALUES {i};")
            con.commit()
    con.close()


if __name__ == '__main__':
    main()
