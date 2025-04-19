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

# SCRIPT TO POPULATE DATABASE WITH allLocations.json
cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(50),
            dimension VARCHAR(100),
            residents_count INTEGER
        );
    """
            )

for locations in dadosLocations:
    cursor.execute("""
    INSERT INTO locations (
        id, name, type, dimension, residents_count
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        locations['id'],
        locations['name'],
        locations['type'],
        locations['dimension'],
        len(locations['residents'])
    )
    )

# SCRIPT TO POPULATE DATABASE WITH allCharsUpdated.json
cursor.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            status VARCHAR(50),
            species VARCHAR(50),               
            type VARCHAR(50),
            gender VARCHAR(10),
            image VARCHAR(255),
            origin_id INT,
            location_id INT,
            FOREIGN KEY (origin_id) REFERENCES locations(id),
            FOREIGN KEY (location_id) REFERENCES locations(id)
        );
    """
            )
            
def extract_id_of_the_url(url):
    if url:
        partes = url.strip('/').split('/')
        if partes and partes[-1].isdigit():
            return int(partes[-1])
    return None

print('cheguei aqui ')

for characters in dadosCharacters:
    origin_id = extract_id_of_the_url(characters['origin']['url'])
    location_id = extract_id_of_the_url(characters['location']['url'])

    cursor.execute("""
    INSERT INTO characters (
        id, name, status, species, type, gender, image, origin_id, location_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        characters['id'],
        characters['name'],
        characters['status'],
        characters['species'],
        characters['type'],
        characters['gender'],
        characters['image'],
        origin_id,
        location_id
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters_episodes (
        episode_id INT,
        character_id INT,
        PRIMARY KEY (episode_id, character_id),
        FOREIGN KEY (episode_id) REFERENCES episodes(id),
        FOREIGN KEY (character_id) REFERENCES characters(id)
    )
""")

for episode in dadosEpisodes:
    episode_id = episode['id']
    for character_url in episode['characters']:
        character_id = int(character_url.split(
            '/')[-1]) 

        cursor.execute("""
            INSERT INTO characters_episodes (
                episode_id, character_id
            )
            VALUES (%s, %s)
            ON CONFLICT (episode_id, character_id) DO NOTHING
        """, (
            episode_id,
            character_id
        )
        )

conn.commit()

if conn:
    print("Conexão bem-sucedida.")
else:
    print("Falha na conexão com o banco de dados.")