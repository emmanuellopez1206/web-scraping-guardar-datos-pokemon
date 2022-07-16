import requests
from bs4 import BeautifulSoup
import psycopg2

connection = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "Vicky120600*",
    database = "test",
    port = "5432"
)
connection.autocommit = True

def web_scraping_insertar_datos():

    url = "https://pokemondb.net/pokedex/all"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    rows = soup.find("table", attrs={"id":"pokedex"}).find("tbody").find_all("tr")
    
    cursor = connection.cursor()
    for row in rows:
        names = row.find_all("td")[1].get_text()
        names_correct = names.replace("'",'"')
        types = row.find_all("td")[2].get_text()
        total = row.find_all("td")[3].get_text()
        hp = row.find_all("td")[4].get_text()
        attack = row.find_all("td")[5].get_text()
        defense = row.find_all("td")[6].get_text()
        sp_attack = row.find_all("td")[7].get_text()
        sp_defense = row.find_all("td")[8].get_text()
        speed = row.find_all("td")[9].get_text()

        query = f""" INSERT INTO pokemones (name,type,total,hp,atack,defense,sp_attack,sp_defense,speed) values ('{names_correct}','{types}',{total},{hp},{attack},{defense},{sp_attack},{sp_defense},{speed})"""
        cursor.execute(query)
    cursor.close()

def crear_tabla():
    cursor = connection.cursor()
    query = "CREATE TABLE pokemones(name varchar(255),type varchar(255),total int8, hp int8, atack int8, defense int8, sp_attack int8, sp_defense int8, speed int8)"
    try:
        cursor.execute(query)
    except:
        print("La tabla ya está creada")
    cursor.close()  
    
if __name__ == "__main__":
    crear_tabla()
    web_scraping_insertar_datos()