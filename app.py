import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os
import json
from PIL import Image
import unicodedata

# Configuración de la página
st.set_page_config(page_title="Entrenamiento Juan", page_icon="💪", layout="centered")

# --- FUNCIÓN DE VOZ DESACTIVADA (para evitar errores) ---
def hablar(texto):
    # Esta función está desactivada para garantizar el despliegue en la nube
    # En futuras versiones añadiremos una solución de voz ligera
    pass

# --- FUNCIÓN PARA MOSTRAR IMAGEN (MAPA DE NOMBRES) ---
def mostrar_imagen_ejercicio(nombre_desde_csv):
    mapa_nombres = {
        "Plancha frontal (desde pies)": "plancha_frontal",
        "plancha_frontal": "plancha_frontal",
        "plancha_frontal_desde_pies": "plancha_frontal",
        "Plancha lateral": "plancha_lateral",
        "Puente de glúteos": "puente_de_gluteos",
        "Puente de glúteos una pierna": "puente_de_gluteos_una_pierna",
        "Bird-Dog": "bird_dog",
        "Superman estático": "superman_estatico",
        "TRX Remo": "trx_remo",
        "TRX Remo con rotación": "trx_remo_con_rotacion",
        "TRX Remo una mano": "trx_remo_a_una_mano",
        "TRX Curl de bíceps": "trx_curl_de_biceps",
        "TRX Curl isométrico": "trx_curl_isometrico",
        "TRX Flexión diamante": "trx_flexion_diamante",
        "TRX Sentadilla asistida": "trx_sentadilla_asistida",
        "TRX Zancada asistida": "trx_zancada_asistida",
        "TRX Sentadilla búlgara asistida": "trx_sentadilla_bulgara_asistida",
        "Flexión estándar": "flexion_estandar",
        "Flexión inclinada silla": "flexion_inclinada_silla",
        "Flexión con apertura": "flexion_con_apertura",
        "Flexión diamante": "flexion_diamante",
        "Fondos en silla": "fondos_en_silla",
        "Dominada australiana": "dominada_australiana",
        "Colgado isométrico": "colgado_isometrico",
        "Remo invertido barra baja": "remo_invertido_barra_baja",
    }
    nombre_archivo = mapa_nombres.get(nombre_desde_csv, nombre_desde_csv)
    nombre_archivo = nombre_archivo.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
    
    extensiones = [".png", ".jpg", ".jpeg", ".gif"]
    carpeta = "imagenes"
    
    if not os.path.exists(carpeta):
        st.error(f"❌ La carpeta `{carpeta}/` no existe.")
        return False
    
    for ext in extensiones:
        ruta = os.path.join(carpeta, f"{nombre_archivo}{ext}")
        if os.path.exists(ruta):
            try:
                img = Image.open(ruta)
                st.image(img, caption=nombre_archivo, use_container_width=True)
                return True
            except:
                pass
    
    st.markdown(f"[Ver en YouTube](https://www.youtube.com/results?search_query={nombre_archivo.replace('_', '+')}+ejercicio)")
    return False

# --- FUNCIÓN PARA CARGAR Y GUARDAR MODIFICACIONES ---
def cargar_modificaciones():
    if os.path.exists("modificaciones.json"):
        with open("modificaciones.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_modificaciones(mods):
    with open("modificaciones.json", "w", encoding="utf-8") as f:
        json.dump(mods, f, indent=2, ensure_ascii=False)

# Cargar ejercicios
@st.cache_data
def cargar_ejercicios():
    df = pd.read_csv("ejercicios.csv")
    def normalizar_dia(nombre):
        nombre = nombre.strip()
        variantes = {
            'lunes': 'Lunes', 'martes': 'Martes', 'miercoles': 'Miercoles',
            'miércoles': 'Miercoles', 'jueves': 'Jueves', 'viernes': 'Viernes',
            'sabado': 'Sabado', 'sábado': 'Sabado', 'domingo': 'Domingo'
        }
        return variantes.get(nombre.lower(), nombre)
    df['dia'] = df['dia'].apply(normalizar_dia)
    return df

df_ejercicios = cargar_ejercicios()

# Mapeo de días
dias_semana = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sabado",
    "Sunday": "Domingo"
}

# --- SELECTOR DE DÍA ---
st.sidebar.title("📅 Configuración")

modo_dia = st.sidebar.radio(
    "Selecciona el modo:",
    ["📆 Día real (automático)", "📝 Día manual (elige tú)"],
    index=0
)

if modo_dia == "📆 Día real (automático)":
    hoy = datetime.now().strftime("%A")
    hoy_es = dias_semana.get(hoy, "Lunes")
else:
    dias_semana_lista = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    hoy_es = st.sidebar.selectbox("Elige el día que quieres entrenar:", dias_semana_lista, index=0)

st.sidebar.success(f"📅 Día: {hoy_es}")

# --- DÍAS DE CARDIO ---
dias_cardio = ["Martes", "Jueves", "Sabado", "Domingo"]

# Título
st.title("💪 Entrenamiento Personalizado")

# Menú
menu = st.radio(
    "Elige una opción:",
    ["🏋️ Entrenar", "📊 Historial", "⚙️ Ajustes"],
    index=0,
    horizontal=True
)

# --- ENTRENAR ---
if menu == "🏋️ Entrenar":
    st.header(f"🏋️ Entrenamiento de {hoy_es}")

    if hoy_es in dias_cardio:
        # --- CARDIO ---
        st.info("🔄 Hoy es día de cardio.")
        if hoy_es == "Sabado":
            st.success("🏃 Sábado: Caminata rápida o trote progresivo (50-60 min)")
        elif hoy_es == "Domingo":
            st.success("🧘 Domingo: Descanso activo (20 min)")
        else:
            st.success("🏃 Cardio: Caminata rápida (40 min)")

        st.divider()
        st.subheader("📍 Cardio con GPS")

        if "cardio_activo" not in st.session_state:
            st.session_state.cardio_activo = False
            st.session_state.tiempo_inicio = None
            st.session_state.tiempo_transcurrido = 0
            st.session_state.distancia = 0.0
            st.session_state.velocidad = 0.0

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if not st.session_state.cardio_activo and st.button("▶️ Iniciar cardio", type="primary", use_container_width=True):
                st.session_state.cardio_activo = True
                st.session_state.tiempo_inicio = datetime.now()
                st.rerun()
        with col2:
            if st.session_state.cardio_activo and st.button("⏹️ Finalizar", type="primary", use_container_width=True):
                st.session_state.cardio_activo = False
                if st.session_state.tiempo_inicio:
                    delta = datetime.now() - st.session_state.tiempo_inicio
                    st.session_state.tiempo_transcurrido = int(delta.total_seconds())
                st.rerun()
        with col3:
            if st.button("🔄 Reiniciar", use_container_width=True):
                st.session_state.cardio_activo = False
                st.session_state.tiempo_transcurrido = 0
                st.session_state.distancia = 0.0
                st.rerun()

        if st.session_state.cardio_activo:
            delta = datetime.now() - st.session_state.tiempo_inicio
            segundos = int(delta.total_seconds())
            minutos = segundos // 60
            segs = segundos % 60
            col_tiempo, col_distancia, col_velocidad = st.columns(3)
            with col_tiempo:
                st.metric("⏱️ Tiempo", f"{minutos:02d}:{segs:02d}")
            with col_distancia:
                st.metric("📏 Distancia", f"{st.session_state.distancia:.2f} km")
            with col_velocidad:
                st.metric("⚡ Velocidad", f"{st.session_state.velocidad:.1f} km/h")

            st.components.v1.html("""
                <script>
                    var lastLat=null, lastLon=null, distancia=0, velocidad=0, lastTime=null;
                    function toRad(d){return d*Math.PI/180;}
                    function calcDist(lat1,lon1,lat2,lon2){
                        var R=6371, dLat=toRad(lat2-lat1), dLon=toRad(lon2-lon1);
                        var a=Math.sin(dLat/2)*Math.sin(dLat/2)+Math.cos(toRad(lat1))*Math.cos(toRad(lat2))*Math.sin(dLon/2)*Math.sin(dLon/2);
                        return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));
                    }
                    function actualizar(){
                        if(navigator.geolocation){
                            navigator.geolocation.getCurrentPosition(function(p){
                                var lat=p.coords.latitude, lon=p.coords.longitude, acc=p.coords.accuracy;
                                if(acc<50 && lastLat!==null && lastLon!==null){
                                    var d=calcDist(lastLat,lastLon,lat,lon);
                                    if(d>0.01){ distancia+=d; var now=new Date().getTime(); if(lastTime!==null){ var h=(now-lastTime)/3600000; if(h>0) velocidad=d/h;} lastTime=now; }
                                }
                                lastLat=lat; lastLon=lon;
                                window.parent.postMessage({distancia:distancia, velocidad:velocidad}, '*');
                            }, function(){}, {enableHighAccuracy:true, timeout:10000, maximumAge:2000});
                        }
                    }
                    setInterval(actualizar, 2000);
                    actualizar();
                </script>
            """, height=50)
            st.info("🟢 GPS activo...")
            time.sleep(1)
            st.rerun()

        elif st.session_state.tiempo_transcurrido > 0:
            minutos = st.session_state.tiempo_transcurrido // 60
            segs = st.session_state.tiempo_transcurrido % 60
            st.success(f"✅ Cardio completado: {minutos:02d}:{segs:02d}")
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("📏 Distancia", f"{st.session_state.distancia:.2f} km")
            with col_res2:
                st.metric("⚡ Velocidad", f"{st.session_state.velocidad:.1f} km/h")

            if st.button("💾 Guardar registro"):
                st.success("✅ Registro guardado")
                st.session_state.tiempo_transcurrido = 0
                st.session_state.distancia = 0.0
                st.rerun()
        else:
            st.info("📍 Pulsa 'Iniciar cardio' para comenzar.")

    else:
        # --- FUERZA ---
        ejercicios_hoy = df_ejercicios[df_ejercicios["dia"] == hoy_es]
        
        if ejercicios_hoy.empty:
            st.warning(f"No hay ejercicios programados para {hoy_es}.")
        else:
            # --- CARGAR MODIFICACIONES GUARDADAS ---
            modificaciones = cargar_modificaciones()
            clave_dia = f"{hoy_es}_{datetime.now().strftime('%Y%m%d')}"
            
            # --- MOSTRAR PLAN COMPLETO DEL DÍA ---
            st.subheader("📋 Plan completo del día")
            
            ejercicios_lista = ejercicios_hoy.to_dict('records')
            
            if clave_dia in modificaciones:
                for i, ej in enumerate(ejercicios_lista):
                    if i < len(modificaciones[clave_dia]):
                        mod = modificaciones[clave_dia][i]
                        ej['ejercicio'] = mod.get('ejercicio', ej['ejercicio'])
                        ej['series'] = mod.get('series', ej['series'])
                        if ej['tipo'] == 'tiempo':
                            ej['tiempo_segundos'] = mod.get('tiempo_segundos', ej['tiempo_segundos'])
                        else:
                            ej['repeticiones'] = mod.get('repeticiones', ej['repeticiones'])
            
            for i, row in enumerate(ejercicios_lista):
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{row['ejercicio']}**")
                        st.caption(f"{row['musculo']}")
                    with col2:
                        if row["tipo"] == "tiempo":
                            st.write(f"⏱️ {row['series']} x {row['tiempo_segundos']}s")
                        else:
                            st.write(f"🔄 {row['series']} x {row['repeticiones']}")
                    with col3:
                        if st.button("✏️", key=f"edit_{i}"):
                            st.session_state.editando = i
                            st.rerun()
                    with col4:
                        if st.button("🗑️", key=f"del_{i}"):
                            ejercicios_lista.pop(i)
                            mods = modificaciones.get(clave_dia, [])
                            if i < len(mods):
                                mods.pop(i)
                            modificaciones[clave_dia] = mods
                            guardar_modificaciones(modificaciones)
                            st.rerun()
                
                if 'editando' in st.session_state and st.session_state.editando == i:
                    with st.expander(f"✏️ Modificando: {row['ejercicio']}", expanded=True):
                        nuevo_nombre = st.text_input("Nombre del ejercicio:", value=row['ejercicio'], key=f"nombre_{i}")
                        nuevas_series = st.number_input("Series:", min_value=1, max_value=10, value=int(row['series']), key=f"series_{i}")
                        
                        if row["tipo"] == "tiempo":
                            nuevo_tiempo = st.number_input("Tiempo (segundos):", min_value=5, max_value=120, value=int(row['tiempo_segundos']), key=f"tiempo_{i}")
                        else:
                            nuevas_repeticiones = st.number_input("Repeticiones:", min_value=1, max_value=50, value=int(row['repeticiones']), key=f"reps_{i}")
                        
                        col_guardar, col_cancelar = st.columns(2)
                        with col_guardar:
                            if st.button("✅ Guardar cambios", key=f"save_{i}"):
                                row['ejercicio'] = nuevo_nombre
                                row['series'] = nuevas_series
                                if row["tipo"] == "tiempo":
                                    row['tiempo_segundos'] = nuevo_tiempo
                                else:
                                    row['repeticiones'] = nuevas_repeticiones
                                
                                mods = modificaciones.get(clave_dia, [])
                                while len(mods) <= i:
                                    mods.append({})
                                mods[i] = {
                                    'ejercicio': nuevo_nombre,
                                    'series': nuevas_series,
                                    'tiempo_segundos': row.get('tiempo_segundos', 0),
                                    'repeticiones': row.get('repeticiones', 0)
                                }
                                modificaciones[clave_dia] = mods
                                guardar_modificaciones(modificaciones)
                                del st.session_state.editando
                                st.rerun()
                        with col_cancelar:
                            if st.button("❌ Cancelar", key=f"cancel_{i}"):
                                del st.session_state.editando
                                st.rerun()
            
            if st.button("➕ Añadir ejercicio al final", use_container_width=True):
                nuevo_ej = {
                    'ejercicio': 'Nuevo ejercicio',
                    'musculo': 'Personalizado',
                    'tipo': 'repeticiones',
                    'series': 3,
                    'repeticiones': 10,
                    'tiempo_segundos': 0,
                    'nota': 'Ejercicio añadido por el usuario'
                }
                ejercicios_lista.append(nuevo_ej)
                mods = modificaciones.get(clave_dia, [])
                mods.append({
                    'ejercicio': 'Nuevo ejercicio',
                    'series': 3,
                    'repeticiones': 10,
                    'tiempo_segundos': 0
                })
                modificaciones[clave_dia] = mods
                guardar_modificaciones(modificaciones)
                st.rerun()
            
            st.divider()
            if st.button("▶️ Comenzar entrenamiento", type="primary", use_container_width=True):
                st.session_state.entrenando = True
                st.session_state.ejercicio_actual = 0
                st.session_state.ejercicios_lista = ejercicios_lista
                st.session_state.completados = []
                st.session_state.voz_reproducida = False
                st.rerun()

            if "entrenando" in st.session_state and st.session_state.entrenando:
                ejercicios = st.session_state.ejercicios_lista
                idx = st.session_state.ejercicio_actual
                
                if idx < len(ejercicios):
                    row = ejercicios[idx]
                    
                    st.progress((idx) / len(ejercicios))
                    st.caption(f"Ejercicio {idx + 1} de {len(ejercicios)}")
                    
                    st.subheader(f"📍 {row['ejercicio']}")
                    
                    mostrar_imagen_ejercicio(row['ejercicio'])
                    
                    st.write(f"**Músculo:** {row['musculo']}")
                    
                    if row["tipo"] == "tiempo":
                        st.write(f"⏱️ **{row['series']} series de {row['tiempo_segundos']} segundos**")
                    else:
                        st.write(f"🔄 **{row['series']} series de {row['repeticiones']} repeticiones**")
                    
                    st.caption(f"📝 {row['nota']}")
                    
                    if row["tipo"] == "tiempo":
                        if "temporizador_activo" not in st.session_state:
                            st.session_state.temporizador_activo = False
                            st.session_state.tiempo_restante = 0
                        
                        col_timer1, col_timer2 = st.columns([2, 1])
                        with col_timer1:
                            if not st.session_state.temporizador_activo:
                                if st.button(f"⏱️ Iniciar temporizador ({row['tiempo_segundos']}s)", use_container_width=True):
                                    st.session_state.temporizador_activo = True
                                    st.session_state.tiempo_restante = row['tiempo_segundos']
                                    st.rerun()
                            else:
                                placeholder = st.empty()
                                for t in range(st.session_state.tiempo_restante, 0, -1):
                                    placeholder.metric("⏱️ Tiempo restante", f"{t}s")
                                    time.sleep(1)
                                placeholder.metric("⏱️ Tiempo restante", "¡TIEMPO!")
                                st.session_state.temporizador_activo = False
                                st.session_state.tiempo_restante = 0
                                st.rerun()
                        
                        with col_timer2:
                            if st.button("✅ Hecho", type="primary", use_container_width=True):
                                st.session_state.completados.append(row['ejercicio'])
                                st.session_state.ejercicio_actual += 1
                                st.session_state.voz_reproducida = False
                                st.rerun()
                    else:
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("✅ Serie completada", type="primary", use_container_width=True):
                                st.session_state.completados.append(row['ejercicio'])
                                st.session_state.ejercicio_actual += 1
                                st.session_state.voz_reproducida = False
                                st.rerun()
                        with col2:
                            if st.button("⏭️ Saltar", use_container_width=True):
                                st.session_state.ejercicio_actual += 1
                                st.session_state.voz_reproducida = False
                                st.rerun()
                    
                    if st.button("🚪 Salir del entrenamiento", use_container_width=True):
                        st.session_state.entrenando = False
                        st.rerun()
                
                else:
                    st.success("🎉 ¡Entrenamiento completado!")
                    st.write(f"✅ Has completado {len(st.session_state.completados)} ejercicios.")
                    
                    st.divider()
                    st.subheader("📝 ¿Cómo ha ido?")
                    col_facil, col_normal, col_dificil = st.columns(3)
                    with col_facil:
                        if st.button("😊 Fácil", use_container_width=True):
                            st.success("¡Subiremos la dificultad!")
                            st.session_state.entrenando = False
                            st.rerun()
                    with col_normal:
                        if st.button("🙂 Normal", use_container_width=True):
                            st.info("Mantendremos la dificultad.")
                            st.session_state.entrenando = False
                            st.rerun()
                    with col_dificil:
                        if st.button("😰 Difícil", use_container_width=True):
                            st.warning("Bajaremos la dificultad.")
                            st.session_state.entrenando = False
                            st.rerun()

# --- HISTORIAL ---
elif menu == "📊 Historial":
    st.header("📊 Historial")
    st.info("Próximamente en la app nativa.")

# --- AJUSTES ---
elif menu == "⚙️ Ajustes":
    st.header("⚙️ Ajustes")
    st.info("Próximamente en la app nativa.")