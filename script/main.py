from conn import conn
import json

cursor = conn.cursor()

with open('json/allCharsUpdated.json', 'r', encoding='utf-8') as file:
    dadosCharacters = json.load(file)

with open('json/allLocations.json', 'r', encoding='utf-8') as file:
    dadosLocations = json.load(file)

with open('json/allEpisodesUpdated.json', 'r', encoding='utf-8') as file:
    dadosEpisodes = json.load(file)

print("Dados carregados do JSON:")

# SCRIPT TO POPULATE DATABASE WITH allCharsUpdated.json
cursor.execute("""
        CREATE TABLE IF NOT EXISTS personagens (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            status VARCHAR(50),
            species VARCHAR(50),               
            type VARCHAR(50),
            gender VARCHAR(10),
            image VARCHAR(255)
        );
    """
)

for personagem in dadosCharacters:
    cursor.execute("""
    INSERT INTO personagens (
        id, name, status, species, type, gender, image
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        personagem['id'],
        personagem['name'],
        personagem['status'],
        personagem['species'],
        personagem['type'],
        personagem['gender'],
        personagem['image'],
    )
)

# SCRIPT TO POPULATE DATABASE WITH allLocations.json
cursor.execute("""
        CREATE TABLE IF NOT EXISTS location (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(50),
            dimension VARCHAR(100),
            residents_count INTEGER
        );
    """
)

for location in dadosLocations:
    cursor.execute("""
    INSERT INTO location (
        id, name, type, dimension, residents_count
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        location['id'],
        location['name'],
        location['type'],
        location['dimension'],
        len(location['residents'])
    )
)

# SCRIPT TO POPULATE DATABASE WITH allEpisodesUpdated.json
cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            air_date VARCHAR(50),
            episode VARCHAR(100)
        );
    """
)

for episodes in dadosEpisodes:
    cursor.execute("""
    INSERT INTO episodes (
        id, name, air_date, episode
    )
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        episodes['id'],
        episodes['name'],
        episodes['air_date'],
        episodes['episode']
    )
)

conn.commit()

if conn:
    print("Conexão bem-sucedida.")
else:
    print("Falha na conexão com o banco de dados.")