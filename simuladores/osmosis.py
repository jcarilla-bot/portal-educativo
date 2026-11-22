"""Simulador didáctico. Entrada compatible con portal.py: mostrar_osmosis()."""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def _trayectoria(interior, exterior):
    # Dos compartimentos, V_inicial = 1 cada uno; solutos no permeables.
    # dV/dt = k * (n_in/V - n_out/(2-V)). Presiones iguales.
    tiempo = np.linspace(0, 10, 101)
    volumen = np.ones_like(tiempo)
    for i in range(1, len(tiempo)):
        anterior = volumen[i - 1]
        a, b = 1e-10, 2 - 1e-10
        # Euler implícito: raíz única, positiva y sin sobrepasar equilibrio.
        for _ in range(45):
            v = (a + b) / 2
            residuo = v - anterior - 0.15 * 0.1 * (
                interior / v - exterior / (2 - v)
            )
            if residuo > 0:
                b = v
            else:
                a = v
        volumen[i] = (a + b) / 2
    return tiempo, volumen


def _dibujo(v, interior, exterior, fase):
    fig, ax = plt.subplots(figsize=(5, 5))
    radio = np.cbrt(v)  # Volumen de esfera proporcional a r³, no a r².
    ax.set_facecolor('#f0f8ff')
    ax.add_patch(plt.Circle((0, 0), radio, fc='#fff0ec', ec='#a94442', lw=3))
    rng = np.random.default_rng(42)
    # Cada símbolo de soluto representa la misma cantidad; número constante.
    for dentro, cantidad in ((True, interior), (False, exterior)):
        n = int(round(cantidad * 60))
        puntos = []
        while len(puntos) < n:
            x, y = rng.uniform(-1.55, 1.55, 2)
            distancia = np.hypot(x, y)
            if (dentro and distancia < radio - .06) or (
                not dentro and distancia > radio + .06
            ):
                puntos.append((x, y))
        if puntos:
            xy = np.array(puntos)
            ax.scatter(xy[:, 0], xy[:, 1], c='#843bb5', s=24, marker='s', zorder=3)
    # Agua esquemática: trayectorias bidireccionales incluso en isotonicidad.
    for j in range(36):
        angulo = j * 2 * np.pi / 36
        progreso = (fase / 12 + j * .381966) % 1
        sentido = 1 if j % 2 else -1
        distancia = radio + sentido * (progreso - .5) * .65
        ax.scatter(distancia * np.cos(angulo), distancia * np.sin(angulo),
                   c='#168cdb', s=14, alpha=.8, zorder=4)
    diferencia = interior / v - exterior / (2 - v)
    if abs(diferencia) > 1e-4:
        entra = diferencia > 0
        for angulo in (0, np.pi / 2, np.pi, 3 * np.pi / 2):
            fuera = (radio + .28) * np.array([np.cos(angulo), np.sin(angulo)])
            dentro = (radio - .28) * np.array([np.cos(angulo), np.sin(angulo)])
            inicio, fin = (fuera, dentro) if entra else (dentro, fuera)
            ax.annotate('', xy=fin, xytext=inicio,
                        arrowprops=dict(arrowstyle='->', color='#086e52', lw=2.5),
                        zorder=5)
        texto = 'Flujo neto: entrada' if entra else 'Flujo neto: salida'
    else:
        texto = 'Sin flujo neto: intercambio en ambos sentidos'
    ax.set_title(texto, fontsize=10)
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    return fig


def mostrar_osmosis():
    st.title('💧 Simulador de ósmosis celular')
    st.write('Modifica las concentraciones iniciales y observa cómo cambia el volumen celular.')
    st.info('Modelo didáctico de una célula animal con membrana permeable al agua '
            'y solutos no permeables. El medio exterior es un compartimento finito.')
    col1, col2 = st.columns(2)
    with col1:
        interior = st.slider('Concentración intracelular (mol/L)',
                             0.0, 1.0, 0.3, 0.05, key='osm_in')
    with col2:
        exterior = st.slider('Concentración extracelular (mol/L)',
                             0.0, 1.0, 0.5, 0.05, key='osm_out')
    st.caption('Los deslizadores indican concentraciones iniciales de un soluto ideal '
               'que no se disocia (1 mol = 1 osmol). Cambiarlos reinicia el experimento.')
    parametros = (interior, exterior)
    if st.session_state.get('osm_parametros') != parametros:
        st.session_state.update(osm_parametros=parametros, osm_paso=0, osm_activa=False)
    diferencia = interior - exterior
    estado = 'isotónico' if abs(diferencia) < .001 else (
        'hipotónico' if diferencia > 0 else 'hipertónico')
    st.subheader(f'Medio inicialmente {estado}')
    st.write('El agua atraviesa la membrana en ambos sentidos. Las flechas verdes '
             'indican únicamente el flujo neto, hacia la mayor concentración osmótica actual.')
    tiempo, volumen = _trayectoria(interior, exterior)

    def iniciar():
        if st.session_state.osm_paso >= len(tiempo) - 1:
            st.session_state.osm_paso = 0
        st.session_state.osm_activa = True

    def detener():
        st.session_state.osm_activa = False

    def reiniciar():
        st.session_state.osm_paso = 0
        st.session_state.osm_activa = False

    b1, b2, b3 = st.columns(3)
    b1.button('▶ Iniciar / continuar', on_click=iniciar, key='osm_start')
    b2.button('⏸ Detener', on_click=detener, key='osm_stop')
    b3.button('↺ Reiniciar', on_click=reiniciar, key='osm_reset')

    @st.fragment(run_every=.2 if st.session_state.osm_activa else None)
    def escena():
        paso = st.session_state.osm_paso
        v = float(volumen[paso])
        c3, c4 = st.columns(2)
        with c3:
            st.subheader('Representación celular')
            fig = _dibujo(v, interior, exterior, paso)
            st.pyplot(fig)
            plt.close(fig)
            st.caption('Azul: agua · Violeta: solutos · Verde: flujo neto. '
                       'Trayectorias ilustrativas, no movimiento molecular real. '
                       'El espacio exterior del dibujo no está a escala de volumen.')
        with c4:
            st.subheader('Evolución del volumen')
            fig, ax = plt.subplots()
            ax.plot(tiempo, volumen, '--', color='lightgray', label='Predicción')
            ax.plot(tiempo[:paso + 1], volumen[:paso + 1], lw=3, label='Simulación')
            ax.scatter([tiempo[paso]], [v], color='#168cdb', zorder=4)
            ax.axhline(1, ls='--', color='gray')
            ax.set(xlabel='Tiempo (unidades arbitrarias)', ylabel='Volumen relativo',
                   xlim=(0, 10), ylim=(0, 2))
            ax.grid(True, alpha=.3)
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)
        m1, m2, m3 = st.columns(3)
        m1.metric('Volumen celular actual', f'{v:.2f}', f'{(v - 1) * 100:+.1f}%')
        m2.metric('Concentración interior actual', f'{interior / v:.3f} mol/L')
        m3.metric('Concentración exterior actual', f'{exterior / (2 - v):.3f} mol/L')
        st.metric('Volumen celular final (t = 10)', f'{volumen[-1]:.2f}',
                  f'{(volumen[-1] - 1) * 100:+.1f}%')
        st.caption(f'Tiempo: {tiempo[paso]:.1f} / 10. '
                   'El final del intervalo no implica que se haya alcanzado el equilibrio.')
        if st.session_state.osm_activa:
            if paso < len(tiempo) - 1:
                st.session_state.osm_paso = paso + 1
            else:
                st.session_state.osm_activa = False
                st.rerun()

    escena()
    with st.expander('Modelo y límites científicos'):
        st.write('Ambos compartimentos parten del mismo volumen relativo (1). '
                 'El volumen total es 2 y la cantidad de soluto de cada lado se conserva. '
                 'Al entrar agua, el interior se diluye y el exterior se concentra; '
                 'al salir, ocurre lo contrario. Se aplica dV/dt = '
                 '0,15 × (C_interior − C_exterior), en unidades arbitrarias, '
                 'con temperatura constante y sin diferencia de presión hidrostática. '
                 'El radio se calcula como la raíz cúbica del volumen relativo.')
        st.write('Es un modelo ideal, no una predicción de una célula real: '
                 'no incluye lisis, tensión de membrana, volumen de sólidos, '
                 'transporte de solutos ni regulación celular. Las partículas dibujadas '
                 'son símbolos: su tamaño y sus trayectorias no están a escala. '
                 'Con agua pura a un lado, el modelo puede tender a volúmenes extremos '
                 'sin representar los daños que sufriría una célula real.')


if __name__ == '__main__':
    mostrar_osmosis()
