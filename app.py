import streamlit as st
import base64
from io import BytesIO
import pandas as pd

from scrape import scrape_x


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="X Scraper",
    layout="centered"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    
    .st-key-kofi_button a {
        background-color: #8b5cf6 !important;
        color: white !important;
        border: none !important;
    }

    .st-key-kofi_button a:hover {
        background-color: #7c3aed !important;
        color: white !important;
    }

    .st-key-progreso {
        border: 2px solid #22c55e !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    .st-key-resultado {
        border: 2px solid #8b5cf6 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "scraping_iniciado" not in st.session_state:
    st.session_state.scraping_iniciado = False

if "scraping_completado" not in st.session_state:
    st.session_state.scraping_completado = False

if "reset_solicitado" not in st.session_state:
    st.session_state.reset_solicitado = False

if "cuenta" not in st.session_state:
    st.session_state.cuenta = None

if "fecha_inicio" not in st.session_state:
    st.session_state.fecha_inicio = None

if "fecha_final" not in st.session_state:
    st.session_state.fecha_final = None

# ============================================================
# RESULTADO DEL SCRAPING
# ============================================================
#
# ESTE ES EL CAMBIO FUNDAMENTAL:
#
# El DataFrame se guarda aquí y sobrevive a los reruns
# de Streamlit.
#

if "df" not in st.session_state:
    st.session_state.df = None

if "progreso" not in st.session_state:
    st.session_state.progreso = {}

if "scraping_error" not in st.session_state:
    st.session_state.scraping_error = None


# ============================================================
# BOTÓN DE MÚSICA
# ============================================================

musica = st.sidebar.toggle(
    "🔊 Música",
    value=True
)

if musica:

    try:

        with open("musica.mp3", "rb") as f:
            audio_bytes = f.read()

        audio_base64 = base64.b64encode(
            audio_bytes
        ).decode()

        st.markdown(
            f"""
            <audio autoplay loop>
                <source
                    src="data:audio/mp3;base64,{audio_base64}"
                    type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

    except FileNotFoundError:

        st.sidebar.warning(
            "No se encontró musica.mp3."
        )


# ============================================================
# CONTENEDOR PRINCIPAL
# ============================================================
#
# Volvemos deliberadamente a la configuración anterior.
#
# La interfaz inicial puede permanecer visible mientras
# aparece la interfaz del scraping.
#

main_container = st.empty()


# ============================================================
# RESET
# ============================================================

def reset_app():

    st.session_state.scraping_iniciado = False

    st.session_state.scraping_completado = False

    st.session_state.reset_solicitado = False

    st.session_state.cuenta = None

    st.session_state.fecha_inicio = None

    st.session_state.fecha_final = None

    st.session_state.df = None

    st.session_state.progreso = {}

    st.session_state.scraping_error = None


# ============================================================
# EJECUTAR SCRAPING
# ============================================================

def ejecutar_scraping():

    with main_container.container():

        col_izquierda, col_derecha = st.columns(
            [0.42, 0.58]
        )


        # ====================================================
        # COLUMNA IZQUIERDA
        # ====================================================

        with col_izquierda:

            st.image(
                "logo.png",
                width=300
            )

            st.title(
                "X Scraper (by Nico)"
            )

            st.text_input(
                "Usuario de X",
                value=st.session_state.cuenta,
                disabled=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.date_input(
                    "Fecha inicial",
                    value=st.session_state.fecha_inicio,
                    disabled=True
                )

            with col2:

                st.date_input(
                    "Fecha final",
                    value=st.session_state.fecha_final,
                    disabled=True
                )


        # ====================================================
        # COLUMNA DERECHA
        # ====================================================

        with col_derecha:

            with st.container(
                border=True,
                key="progreso"
            ):

                progress_container = st.empty()

                progress_bar = st.progress(0)

                progress_text = st.empty()

                total_dias = (
                    st.session_state.fecha_final
                    - st.session_state.fecha_inicio
                ).days + 1

                progreso = st.session_state.progreso


                # ============================================
                # CALLBACK DE PROGRESO
                # ============================================

                def actualizar_progreso(
                    fecha,
                    total
                ):

                    progreso[fecha] = total

                    st.session_state.progreso = progreso

                    dias_completados = len(
                        progreso
                    )

                    progreso_barra = min(
                        dias_completados / total_dias,
                        1.0
                    )

                    progress_bar.progress(
                        progreso_barra
                    )

                    progress_text.markdown(
                        f"**{dias_completados} of "
                        f"{total_dias} days completed**"
                    )

                    texto = "### Progress\n\n"

                    for dia in sorted(progreso):

                        cantidad = progreso[dia]

                        texto += (
                            f"✓ **{dia}** — "
                            f"{cantidad} tweets accumulated\n\n"
                        )

                    progress_container.markdown(
                        texto
                    )


                # ============================================
                # SCRAPING
                # ============================================

                # IMPORTANTE:
                #
                # scrape_x() solamente se ejecuta si df todavía
                # no existe.
                #
                # Si Streamlit hace un rerun por cualquier motivo
                # mientras ya existe el resultado, no se vuelve
                # a ejecutar el parser.
                #

                if st.session_state.df is None:

                    try:

                        with st.spinner(
                            f"Scraping "
                            f"@{st.session_state.cuenta} "
                            f"from "
                            f"{st.session_state.fecha_inicio} "
                            f"to "
                            f"{st.session_state.fecha_final}..."
                        ):

                            df = scrape_x(
                                st.session_state.cuenta,
                                str(
                                    st.session_state.fecha_inicio
                                ),
                                str(
                                    st.session_state.fecha_final
                                ),
                                progress_callback=(
                                    actualizar_progreso
                                )
                            )


                        # ====================================
                        # GUARDAR RESULTADO
                        # ====================================

                        st.session_state.df = df

                        st.session_state.scraping_completado = True

                        st.session_state.scraping_error = None

                        st.success(
                            "✓ Scraping completed"
                        )


                    except Exception as e:

                        st.session_state.scraping_error = str(e)

                        st.session_state.scraping_completado = False

                        st.error(
                            "❌ An error occurred during the scraping process."
                        )

                        st.exception(e)

                        return

                else:

                    # ========================================
                    # RESULTADO YA EXISTENTE
                    # ========================================
                    #
                    # Si hubo un rerun, simplemente mostramos
                    # que el resultado ya está disponible.
                    #
                    # NO ejecutamos scrape_x().
                    #

                    st.success(
                        "✓ Scraping completed"
                    )


            # =================================================
            # RESULTADO
            # =================================================

            df = st.session_state.df

            if df is None:

                return


            # =================================================
            # EXCEL
            # =================================================

            excel_buffer = BytesIO()

            df_excel = df.rename(
                columns={
                    "texto": "text"
                }
            )

            df_excel.to_excel(
                excel_buffer,
                index=False,
                engine="openpyxl"
            )

            excel_buffer.seek(0)


            # =================================================
            # RESULTADO
            # =================================================

            with st.container(
                border=True,
                key="resultado"
            ):

                st.markdown(
                    "### Results"
                )

                st.markdown(
                    f"""
                    **Account:** @{st.session_state.cuenta}  
                    **Period:** {st.session_state.fecha_inicio} – {st.session_state.fecha_final}  
                    **Days processed:** {total_dias}  
                    **Tweets found:** {len(df)}
                    """
                )


                # =================================================
                # TABLA RESUMEN POR DÍA
                # =================================================

                dias = sorted(
                    st.session_state.progreso.keys()
                )

                tweets_por_dia = {
                    str(dia): st.session_state.progreso[dia]
                    for dia in dias
                }

                tabla_diaria = pd.DataFrame(
                    [tweets_por_dia],
                    index=["Tweets found per day"]
                )

                st.dataframe(
                    tabla_diaria,
                    width="stretch"
                )


                # =================================================
                # TABLA COMPLETA DE TWEETS
                # =================================================

                st.dataframe(
                    df,
                    width="stretch"
                )


                # =================================================
                # BOTONES
                # =================================================

                col_boton1, col_boton2 = st.columns(2)

                with col_boton1:

                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_buffer,
                        file_name=(
                            f"{st.session_state.cuenta}_"
                            f"{st.session_state.fecha_inicio}_"
                            f"{st.session_state.fecha_final}.xlsx"
                        ),
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                        use_container_width=True
                    )

                with col_boton2:

                    if st.button(
                        "🔄 New Scraping",
                        type="secondary",
                        use_container_width=True
                    ):

                        reset_app()

                        st.rerun()

# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

def mostrar_interfaz_inicial():

    with main_container.container():

        st.image(
            "logo.png",
            width=220
        )

        st.title(
            "X Scraper (by Nico)"
        )

        cuenta = st.text_input(
            "X user (with or without @)",
            placeholder="@Reuters"
        )

        col1, col2 = st.columns(2)

        with col1:

            fecha_inicio = st.date_input(
                "Initial date"
            )

        with col2:

            fecha_final = st.date_input(
                "Final date"
            )


        # ====================================================
        # VALIDACIÓN DE FECHAS
        # ====================================================

        if fecha_final < fecha_inicio:

            st.error(
                "The final date must be equal to or later than "
                "the initial date."
            )

            return


        # ====================================================
        # LIMPIAR USUARIO
        # ====================================================

        cuenta = (
            cuenta
            .strip()
            .lstrip("@")
        )


        # ====================================================
        # BOTÓN
        # ====================================================

        if st.button(
            "🔎 Start Scraping",
            type="primary"
        ):

            if not cuenta:

                st.error(
                    "Please enter an X user before starting the scraping."
                )

                return


            # ================================================
            # GUARDAR PARÁMETROS
            # ================================================

            st.session_state.cuenta = cuenta

            st.session_state.fecha_inicio = fecha_inicio

            st.session_state.fecha_final = fecha_final


            # ================================================
            # LIMPIAR RESULTADO ANTERIOR
            # ================================================

            st.session_state.df = None

            st.session_state.progreso = {}

            st.session_state.scraping_error = None

            st.session_state.scraping_completado = False

            st.session_state.scraping_iniciado = True

            st.rerun()

        # ====================================================
        # APOYAR EL PROYECTO
        # ====================================================

        with st.container(key="kofi_button"):

            st.link_button(
                "☕ Support X Scraper",
                "https://ko-fi.com/nicohouse97",
                type="primary"
            )



# ============================================================
# CONTROL PRINCIPAL
# ============================================================
#
# Si todavía no se ha iniciado ningún scraping:
#
#     → mostramos la interfaz inicial.
#
# Si ya se inició:
#
#     → mostramos la interfaz de scraping.
#
# Esto vuelve deliberadamente al comportamiento visual
# anterior que aceptamos.
#

if not st.session_state.scraping_iniciado:

    mostrar_interfaz_inicial()

else:

    ejecutar_scraping()