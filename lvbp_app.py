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
