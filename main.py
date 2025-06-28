import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="API de Videojuegos",
    description="Una API sencilla para consultar información sobre videojuegos.",
    version="1.0.0"
)

# --- Modelo de datos para un Videojuego ---
class Videojuego(BaseModel):
    id: int
    titulo: str
    ano_salida: int
    generos: List[str]
    plataformas: List[str]
    desarrollador: str
    descripcion_corta: str

# --- Base de datos en memoria (nuestros videojuegos) ---
# Hemos agregado los que pediste y algunos más que encajan en los géneros.
db_videojuegos = [
    Videojuego(
        id=1,
        titulo="Hollow Knight",
        ano_salida=2017,
        generos=["Metroidvania", "Acción", "Aventura"],
        plataformas=["PC", "Nintendo Switch", "PlayStation", "Xbox One"],
        desarrollador="Team Cherry",
        descripcion_corta="Un épico metroidvania dibujado a mano sobre un caballero silencioso en un reino en ruinas."
    ),
    Videojuego(
        id=2,
        titulo="The Binding of Isaac: Rebirth", # Usamos Rebirth como base, ya que Repentance es una expansión
        ano_salida=2014,
        generos=["Roguelike", "Acción", "Disparos"],
        plataformas=["PC", "Nintendo Switch", "PlayStation", "Xbox", "iOS"],
        desarrollador="Edmund McMillen, Nicalis, Inc.",
        descripcion_corta="Un roguelike de disparos con elementos de mazmorras y un alto nivel de rejugabilidad."
    ),
    Videojuego(
        id=3,
        titulo="Subnautica",
        ano_salida=2018,
        generos=["Supervivencia", "Aventura", "Exploración"],
        plataformas=["PC", "PlayStation", "Xbox", "Nintendo Switch"],
        desarrollador="Unknown Worlds Entertainment",
        descripcion_corta="Explora un vasto océano alienígena y construye bases para sobrevivir."
    ),
    Videojuego(
        id=4,
        titulo="Subnautica: Below Zero",
        ano_salida=2021,
        generos=["Supervivencia", "Aventura", "Exploración"],
        plataformas=["PC", "PlayStation", "Xbox", "Nintendo Switch"],
        desarrollador="Unknown Worlds Entertainment",
        descripcion_corta="Regresa al planeta 4546B para investigar una estación de investigación en un entorno ártico."
    ),
    Videojuego(
        id=5,
        titulo="Minecraft",
        ano_salida=2011,
        generos=["Sandbox", "Supervivencia", "Construcción", "Aventura"],
        plataformas=["PC", "Móviles", "Consolas"],
        desarrollador="Mojang Studios",
        descripcion_corta="Un juego de construcción y aventura de mundo abierto donde puedes crear casi cualquier cosa."
    ),
    # Recomendación basada en "Metroidvania" y "Acción"
    Videojuego(
        id=6,
        titulo="Ori and the Blind Forest",
        ano_salida=2015,
        generos=["Metroidvania", "Plataformas", "Aventura"],
        plataformas=["PC", "Xbox One", "Nintendo Switch"],
        desarrollador="Moon Studios",
        descripcion_corta="Un plataformas de aventura visualmente impresionante con una historia emotiva."
    ),
    # Recomendación basada en "Roguelike" y "Disparos"
    Videojuego(
        id=7,
        titulo="Hades",
        ano_salida=2020,
        generos=["Roguelike", "Acción", "Hack and Slash"],
        plataformas=["PC", "Nintendo Switch", "PlayStation", "Xbox"],
        desarrollador="Supergiant Games",
        descripcion_corta="Un roguelike de acción rápida con una rica narrativa mitológica griega y un estilo artístico único."
    ),
    # Recomendación basada en "Supervivencia" y "Exploración"
    Videojuego(
        id=8,
        titulo="Terraria",
        ano_salida=2011,
        generos=["Sandbox", "Aventura", "Supervivencia", "RPG"],
        plataformas=["PC", "Móviles", "Consolas"],
        desarrollador="Re-Logic",
        descripcion_corta="Un juego de sandbox 2D con un énfasis en la exploración, la construcción y el combate."
    ),
    # Recomendación basada en "Construcción" y "Sandbox"
    Videojuego(
        id=9,
        titulo="Satisfactory",
        ano_salida=2019,
        generos=["Construcción", "Estrategia", "Simulación"],
        plataformas=["PC"],
        desarrollador="Coffee Stain Studios",
        descripcion_corta="Construye fábricas masivas en un planeta alienígena en primera persona."
    ),
    # Recomendación variada (acción/RPG)
    Videojuego(
        id=10,
        titulo="Stardew Valley",
        ano_salida=2016,
        generos=["Simulación", "RPG", "Vida"],
        plataformas=["PC", "Móviles", "Consolas"],
        desarrollador="ConcernedApe",
        descripcion_corta="Crea la granja de tus sueños, explora cuevas y forma relaciones en un acogedor juego de simulación."
    )
]

# --- Endpoints de la API ---

@app.get("/videojuegos", response_model=List[Videojuego], summary="Obtener todos los videojuegos")
async def get_all_videojuegos():
    """
    Retorna una lista de todos los videojuegos disponibles en la API.
    """
    return db_videojuegos

@app.get("/videojuegos/{videojuego_id}", response_model=Videojuego, summary="Obtener un videojuego por ID")
async def get_videojuego(videojuego_id: int):
    """
    Retorna un videojuego específico usando su ID.
    Si el ID no existe, devuelve un error 404.
    """
    for juego in db_videojuegos:
        if juego.id == videojuego_id:
            return juego
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")

@app.get("/videojuegos/buscar", response_model=List[Videojuego], summary="Buscar videojuegos por título o género")
async def search_videojuegos(
        q: Optional[str] = None,
        genero: Optional[str] = None,
        ano: Optional[int] = None
):
    """
    Busca videojuegos por título (parcial), género o año de salida.
    Puedes combinar los parámetros de búsqueda.
    """
    results = db_videojuegos
    if q:
        results = [juego for juego in results if q.lower() in juego.titulo.lower() or q.lower() in juego.descripcion_corta.lower()]
    if genero:
        results = [juego for juego in results if genero.lower() in [g.lower() for g in juego.generos]]
    if ano:
        results = [juego for juego in results if juego.ano_salida == ano]

    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron videojuegos con esos criterios de búsqueda")

    return results

@app.post("/videojuegos/", response_model=Videojuego, status_code=201, summary="Agregar un nuevo videojuego")
async def create_videojuego(videojuego: Videojuego):
    """
    Agrega un nuevo videojuego a la lista.
    El ID del videojuego debe ser único.
    """
    for juego in db_videojuegos:
        if juego.id == videojuego.id:
            raise HTTPException(status_code=400, detail="Ya existe un videojuego con ese ID")
    db_videojuegos.append(videojuego)
    return videojuego

@app.put("/videojuegos/{videojuego_id}", response_model=Videojuego, summary="Actualizar un videojuego existente")
async def update_videojuego(videojuego_id: int, updated_videojuego: Videojuego):
    """
    Actualiza la información de un videojuego existente por su ID.
    """
    for index, juego in enumerate(db_videojuegos):
        if juego.id == videojuego_id:
            db_videojuegos[index] = updated_videojuego
            return updated_videojuego
    raise HTTPException(status_code=404, detail="Videojuego no encontrado")

@app.delete("/videojuegos/{videojuego_id}", status_code=204, summary="Eliminar un videojuego")
async def delete_videojuego(videojuego_id: int):
    """
    Elimina un videojuego de la lista por su ID.
    """
    global db_videojuegos # Necesario para modificar la lista global
    initial_len = len(db_videojuegos)
    db_videojuegos = [juego for juego in db_videojuegos if juego.id != videojuego_id]
    if len(db_videojuegos) == initial_len:
        raise HTTPException(status_code=404, detail="Videojuego no encontrado")
    return {"message": "Videojuego eliminado exitosamente"}

# --- Nuevos Endpoints para Géneros y Plataformas ---

@app.get("/generos", response_model=List[str], summary="Obtener una lista de géneros únicos")
async def get_unique_generos():
    """
    Retorna una lista de todos los géneros únicos presentes en la base de datos de videojuegos.
    Ideal para llenar selects o filtros en interfaces de usuario.
    """
    unique_generos = set() # Usamos un set para asegurar la unicidad
    for juego in db_videojuegos:
        for genero in juego.generos:
            unique_generos.add(genero)
    return sorted(list(unique_generos)) # Convertimos a lista y ordenamos alfabéticamente

@app.get("/plataformas", response_model=List[str], summary="Obtener una lista de plataformas únicas")
async def get_unique_plataformas():
    """
    Retorna una lista de todas las plataformas únicas presentes en la base de datos de videojuegos.
    Ideal para llenar selects o filtros en interfaces de usuario.
    """
    unique_plataformas = set() # Usamos un set para asegurar la unicidad
    for juego in db_videojuegos:
        for plataforma in juego.plataformas:
            unique_plataformas.add(plataforma)
    return sorted(list(unique_plataformas))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)