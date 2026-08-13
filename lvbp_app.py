import streamlit as st
import statsapi

st.set_page_config(page_title="Auditoría LVBP", page_icon="🔍")

st.title("🔍 Prueba de Datos: LVBP vs MLB API")
st.markdown("Verificando si la base de datos tiene la profundidad necesaria...")
st.markdown("---")

def probar_datos_lvbp():
    FECHA_PRUEBA = "2025-12-15" 
    
    st.info(f"⏳ Viajando en el tiempo a la fecha: **{FECHA_PRUEBA}**...")

    try:
        juegos = statsapi.schedule(date=FECHA_PRUEBA, sportId=17) 
    except Exception as e:
        st.error(f"Error conectando a la API: {e}")
        return

    if not juegos:
        st.warning("❌ No se encontraron juegos de Ligas de Invierno en esta fecha.")
        return

    juego_lvbp = None
    for j in juegos:
        if "Caracas" in j['home_name'] or "Guaira" in j['home_name'] or "Magallanes" in j['home_name'] or "Lara" in j['home_name']:
            juego_lvbp = j
            break
    
    if not juego_lvbp:
        st.warning("⚠️ No encontré a Leones, Tiburones, Magallanes o Cardenales. Tomando el primer juego disponible...")
        juego_lvbp = juegos[0]

    st.success(f"✅ **Juego encontrado:** {juego_lvbp['away_name']} ✈️ @ 🏠 {juego_lvbp['home_name']}")
    st.caption(f"ID del Juego: {juego_lvbp['game_id']}")
    st.markdown("---")

    st.write("📥 Extrayendo Boxscore para ambos equipos...")
    try:
        box = statsapi.boxscore_data(juego_lvbp['game_id'])
    except Exception as e:
        st.error(f"Error al extraer boxscore: {e}")
        return

    # Creamos una lista para evaluar tanto al Visitante como al Local
    equipos = [
        ('away', juego_lvbp['away_name'], '✈️ Visitante'),
        ('home', juego_lvbp['home_name'], '🏠 Local')
    ]

    # Hacemos el barrido para ambos lados
    for lado, nombre_equipo, icono in equipos:
        pitchers_list = box.get(lado, {}).get('pitchers', [])
        st.markdown(f"### {icono}: {nombre_equipo} ({len(pitchers_list)} lanzadores)")
        
        for pid in pitchers_list:
            p_key = f"ID{pid}"
            jugador = box.get(lado, {}).get('players', {}).get(p_key, {})
            nombre = jugador.get('person', {}).get('fullName', 'Desconocido')
            stats_pitcheo = jugador.get('stats', {}).get('pitching', {})
            
            with st.expander(f"👉 {nombre}"):
                if stats_pitcheo:
                    st.write(f"- **Innings Lanzados:** {stats_pitcheo.get('inningsPitched', 'VACÍO')}")
                    st.write(f"- **Hits Permitidos:** {stats_pitcheo.get('hits', 'VACÍO')}")
                    st.write(f"- **Boletos (BB):** {stats_pitcheo.get('baseOnBalls', 'VACÍO')} 🎯") # <--- AQUI ESTÁN LOS BOLETOS
                    st.write(f"- **Ponches (K):** {stats_pitcheo.get('strikeOuts', 'VACÍO')}")
                    st.write(f"- **Pitcheos Totales:** {stats_pitcheo.get('pitchesThrown', 'VACÍO')}")
                    st.write(f"- **Strikes:** {stats_pitcheo.get('strikes', 'VACÍO')}")
                else:
                    st.error("🚨 ALERTA: Sin estadísticas de pitcheo registradas en la API para este jugador.")

if st.button("Ejecutar Prueba LVBP", type="primary"):
    with st.spinner("Conectando con los servidores de MLB..."):
        probar_datos_lvbp()
