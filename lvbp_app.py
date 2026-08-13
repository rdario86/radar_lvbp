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
        st.warning("❌ No se encontraron juegos en esta fecha.")
        return

    juego_lvbp = None
    for j in juegos:
        if "Caracas" in j['home_name'] or "Guaira" in j['home_name'] or "Magallanes" in j['home_name'] or "Lara" in j['home_name']:
            juego_lvbp = j
            break
    
    if not juego_lvbp:
        juego_lvbp = juegos[0]

    st.success(f"✅ **Juego encontrado:** {juego_lvbp['away_name']} ✈️ @ 🏠 {juego_lvbp['home_name']}")
    st.markdown("---")

    try:
        box = statsapi.boxscore_data(juego_lvbp['game_id'])
    except Exception as e:
        st.error(f"Error al extraer boxscore: {e}")
        return

    equipos = [
        ('away', juego_lvbp['away_name'], '✈️ Visitante'),
        ('home', juego_lvbp['home_name'], '🏠 Local')
    ]

    for lado, nombre_equipo, icono in equipos:
        st.markdown(f"## {icono}: {nombre_equipo}")
        
        # 1. BARRIDO DE LANZADORES
        pitchers_list = box.get(lado, {}).get('pitchers', [])
        st.markdown(f"### ⚾ Lanzadores ({len(pitchers_list)})")
        for pid in pitchers_list:
            p_key = f"ID{pid}"
            jugador = box.get(lado, {}).get('players', {}).get(p_key, {})
            nombre = jugador.get('person', {}).get('fullName', 'Desconocido')
            stats_p = jugador.get('stats', {}).get('pitching', {})
            
            with st.expander(f"Pitcher: {nombre}"):
                if stats_p:
                    st.write(f"- IP: {stats_p.get('inningsPitched', 'VACÍO')} | H: {stats_p.get('hits', 'VACÍO')} | BB: {stats_p.get('baseOnBalls', 'VACÍO')} | K: {stats_p.get('strikeOuts', 'VACÍO')}")
                else:
                    st.error("Sin datos.")

        # 2. BARRIDO DE BATEADORES (CORREGIDO)
        batters_list = box.get(lado, {}).get('batters', [])
        
        # Primero contamos cuántos bateadores reales hay para el título
        bateadores_reales = []
        for pid in batters_list:
            p_key = f"ID{pid}"
            jugador = box.get(lado, {}).get('players', {}).get(p_key, {})
            posicion = jugador.get('position', {}).get('abbreviation', '')
            if posicion != 'P': # Si NO es Pitcher, lo guardamos
                bateadores_reales.append(jugador)

        st.markdown(f"### 🏏 Bateadores Reales ({len(bateadores_reales)})")
        
        for jugador in bateadores_reales:
            nombre = jugador.get('person', {}).get('fullName', 'Desconocido')
            posicion = jugador.get('position', {}).get('abbreviation', 'N/A')
            stats_b = jugador.get('stats', {}).get('batting', {})
            
            with st.expander(f"{posicion} - {nombre}"):
                if stats_b:
                    st.write(f"- **Turnos (AB):** {stats_b.get('atBats', 'VACÍO')}")
                    st.write(f"- **Hits (H):** {stats_b.get('hits', 'VACÍO')}")
                    st.write(f"- **Ponches recibidos (SO):** {stats_b.get('strikeOuts', 'VACÍO')}")
                    st.write(f"- **Impulsadas (RBI):** {stats_b.get('rbi', 'VACÍO')}")
                else:
                    st.error("🚨 ALERTA: Sin estadísticas de bateo.")
if st.button("Ejecutar Prueba Completa LVBP", type="primary"):
    with st.spinner("Analizando pitcheo y bateo..."):
        probar_datos_lvbp()
