import statsapi
import json

def probar_datos_lvbp():
    # Fecha en plena temporada regular de la LVBP pasada
    FECHA_PRUEBA = "2025-12-15" 
    
    print(f"🔍 Viajando en el tiempo a la fecha: {FECHA_PRUEBA}...")

    # sportId=17 es el código que usa MLB para agrupar las Ligas de Invierno (LVBP, LIDOM, LMP, etc.)
    try:
        juegos = statsapi.schedule(date=FECHA_PRUEBA, sportId=17) 
    except Exception as e:
        print(f"Error conectando a la API: {e}")
        return

    if not juegos:
        print("❌ No se encontraron juegos de Ligas de Invierno en esta fecha.")
        return

    # Buscar un juego específico de la LVBP (por nombre de equipo)
    juego_lvbp = None
    for j in juegos:
        # Filtramos buscando equipos venezolanos populares
        if "Caracas" in j['home_name'] or "Guaira" in j['home_name'] or "Magallanes" in j['home_name'] or "Lara" in j['home_name']:
            juego_lvbp = j
            break
    
    if not juego_lvbp:
        print("⚠️ No encontré a Leones, Tiburones, Magallanes o Cardenales. Tomando el primer juego de invierno disponible...")
        juego_lvbp = juegos[0]

    print(f"\n✅ Juego encontrado: {juego_lvbp['away_name']} ✈️  @ 🏠 {juego_lvbp['home_name']}")
    print(f"ID del Juego: {juego_lvbp['game_id']}")
    print("-" * 50)

    print("📥 Extrayendo Boxscore para ver el nivel de detalle...")
    try:
        box = statsapi.boxscore_data(juego_lvbp['game_id'])
    except Exception as e:
        print(f"Error al extraer boxscore: {e}")
        return

    # Revisar la profundidad de los datos de pitcheo del equipo local
    pitchers_local = box.get('home', {}).get('pitchers', [])
    print(f"\n⚾ Lanzadores utilizados por {juego_lvbp['home_name']} ({len(pitchers_local)} en total):")
    
    for pid in pitchers_local:
        p_key = f"ID{pid}"
        jugador = box.get('home', {}).get('players', {}).get(p_key, {})
        nombre = jugador.get('person', {}).get('fullName', 'Desconocido')
        stats_pitcheo = jugador.get('stats', {}).get('pitching', {})
        
        print(f"\n👉 {nombre}:")
        if stats_pitcheo:
            print(f"   - Innings Lanzados: {stats_pitcheo.get('inningsPitched', 'VACÍO')}")
            print(f"   - Hits Permitidos: {stats_pitcheo.get('hits', 'VACÍO')}")
            print(f"   - Ponches (K): {stats_pitcheo.get('strikeOuts', 'VACÍO')}")
            print(f"   - Pitcheos Totales: {stats_pitcheo.get('pitchesThrown', 'VACÍO')}")
            print(f"   - Strikes: {stats_pitcheo.get('strikes', 'VACÍO')}")
        else:
            print("   [!] 🚨 ALERTA: Sin estadísticas de pitcheo registradas en la API.")

if __name__ == "__main__":
    probar_datos_lvbp()