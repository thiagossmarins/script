from conn import conn;
import json;

cursor = conn.cursor();

with open('json/allCharsUpdated.json', 'r', encoding='utf-8') as file:
    dados = json.load(file);

print("Dados carregados do JSON:");
print(json.dumps(dados, indent=4, ensure_ascii=False));

cursor.execute("""
        CREATE TABLE IF NOT EXISTS personagens (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            status VARCHAR(50),
            species VARCHAR(50),
            type VARCHAR(50),
            gender VARCHAR(10),
            origin_name VARCHAR(100),
            location_name VARCHAR(100),
            location_url VARCHAR(255),
            image_url VARCHAR(255),
            episode_urls TEXT[],  -- Array de URLs para episódios
            character_url VARCHAR(255),
            created TIMESTAMP
        );
    """
)

for personagem in dados:
  cursor.execute("""
    INSERT INTO personagens (
        id, name, status, species, type, gender,
        origin_name, location_name, location_url, 
        image_url, episode_urls, character_url, created
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """, (
        personagem['id'],
        personagem['name'],
        personagem['status'],
        personagem['species'],
        personagem['type'],
        personagem['gender'],
        personagem['origin']['name'],
        personagem['location']['name'],
        personagem['location']['url'],
        personagem['image'],
        personagem['episode'],
        personagem['url'],
        personagem['created']
    )
  )

  conn.commit()

  # Fechar o cursor e a conexão
  # cursor.close()
  # conn.close()

else:
    print("Falha na conexão com o banco de dados.")