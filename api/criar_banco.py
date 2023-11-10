import sqlite3

connection = sqlite3.connect('dev.db')
cursor = connection.cursor()

criar_tabela_script = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id TEXT PRIMARY KEY, nome TEXT,estrelas REAL, diaria REAL, cidade TEXT)"

criar_hotel_script = "INSERT INTO hoteis VALUES ('alpha', 'Alpha Hotel', 4.3, 343.30, 'São Paulo')"

cursor.execute(criar_tabela_script)
cursor.execute(criar_hotel_script)

connection.commit()
connection.close()