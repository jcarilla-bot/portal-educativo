"""Modelo didáctico de dos poblaciones: presas y depredadores."""
import io
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def simular(n0, p0, r, capacidad, ataque, mortalidad, duracion,
            reduccion=0.0, momento=30.0, paso=0.02):
    """Lotka-Volterra con crecimiento logístico de las presas, RK4.

    N'=rN(1-N/K)-aNP; P'=e*aNP-mP, e=0.1.
    Las poblaciones son abundancias continuas, no individuos discretos.
    """
    # Incluir exactamente el instante del cambio evita integrar a través de él.
    t = np.arange(0.0, duracion, paso)
    t = np.unique(np.append(t, [duracion, momento] if 0 < momento < duracion else [duracion]))
    y = np.empty((len(t), 2))
    y[0] = n0, p0

    def derivada(z, k):
        n, p = z
        consumo = ataque * n * p
        return np.array([r * n * (1 - n / k) - consumo,
                         .1 * consumo - mortalidad * p])

    for i in range(len(t) - 1):
        h = t[i + 1] - t[i]
        k = capacidad * (1 - reduccion) if t[i] >= momento else capacidad
        z = y[i]
        d1 = derivada(z, k)
        d2 = derivada(z + h * d1 / 2, k)
        d3 = derivada(z + h * d2 / 2, k)
        d4 = derivada(z + h * d3, k)
        y[i + 1] = np.maximum(0, z + h * (d1 + 2*d2 + 2*d3 + d4) / 6)
    return t, y


def mostrar_ecosistemas():
    st.title('🌿 Dinámica de ecosistemas')
    st.write('Explora cómo se relacionan una población de presas y una de depredadores '
             'y qué ocurre cuando disminuyen los recursos del hábitat.')
    st.info('Modelo de dos poblaciones en un sistema cerrado. Los recursos limitan '
            'el crecimiento de las presas; los depredadores dependen de ellas. '
            'El tiempo se expresa en unidades arbitrarias.')
    with st.expander('Configura el experimento', expanded=True):
        a, b = st.columns(2)
        with a:
            n0 = st.slider('Presas iniciales', 0, 1000, 200, 10, key='eco_n')
            r = st.slider('Tasa de crecimiento de las presas', .1, 1.0, .6, .05, key='eco_r')
            capacidad = st.slider('Capacidad de carga del hábitat (K)', 100, 1000, 500, 25, key='eco_k')
            ataque = st.slider('Coeficiente de depredación (a)', .001, .020, .005, .001,
                               format='%.3f', key='eco_a')
        with b:
            p0 = st.slider('Depredadores iniciales', 0, 100, 20, 5, key='eco_p')
            mortalidad = st.slider('Tasa de mortalidad de depredadores', .05, .8, .2, .05,
                                   key='eco_m')
            duracion = st.slider('Duración del experimento', 20, 120, 60, 10, key='eco_d')
        perturbacion = st.checkbox('Simular pérdida de recursos del hábitat', key='eco_evento')
        reduccion, momento = 0.0, duracion / 2
        if perturbacion:
            c, d = st.columns(2)
            reduccion = c.slider('Reducción de la capacidad de carga (%)', 10, 75, 50, 5,
                                 key='eco_reduccion') / 100
            momento = d.slider('Momento de la pérdida de recursos', 1, duracion - 1,
                               min(30, duracion - 1), key=f'eco_momento_{duracion}')
            st.caption('El cambio reduce K de forma permanente. No elimina animales '
                       'instantáneamente: cambia el crecimiento posterior de las presas.')
    t, y = simular(n0, p0, r, capacidad, ataque, mortalidad, duracion, reduccion, momento)
    # Mostrar una serie ligera, incluyendo el instante exacto de la perturbación.
    indices = np.unique(np.append(np.arange(0, len(t), 5), [len(t)-1, np.argmin(abs(t-momento))]))
    t, y = t[indices], y[indices]
    st.subheader('Evolución de las poblaciones')
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(t, y[:, 0], color='#25834b', lw=2.5, label='Presas')
    ax.plot(t, y[:, 1], color='#b54825', lw=2.5, label='Depredadores')
    k_t = np.where(t >= momento, capacidad * (1-reduccion), capacidad)
    ax.step(t, k_t, where='post', color='#808080', ls='--', label='Capacidad de carga K')
    if perturbacion:
        ax.axvline(momento, ls=':', color='#7546aa', label='Pérdida de recursos')
    ax.set(xlabel='Tiempo (unidades arbitrarias)', ylabel='Abundancia poblacional',
           xlim=(0, duracion), ylim=(0, None))
    ax.grid(alpha=.2)
    ax.legend()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption('K es el límite de las presas en ausencia de depredación, '
               'no una tercera población. Los valores decimales son abundancias del modelo.')
    instante = st.slider('Explora un instante de la simulación', 0, duracion,
                         min(10, duracion), key=f'eco_t_{duracion}')
    n, p = [np.interp(instante, t, y[:, j]) for j in (0, 1)]
    c1, c2, c3 = st.columns(3)
    c1.metric('Presas en el instante elegido', f'{n:.1f}')
    c2.metric('Depredadores en el instante elegido', f'{p:.1f}')
    c3.metric('Capacidad de carga actual', f'{capacidad * (1-reduccion if instante >= momento else 1):.0f}')
    with st.expander('Relación entre las dos poblaciones'):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(y[:, 0], y[:, 1], color='#4768a7')
        ax.scatter(y[0, 0], y[0, 1], label='Inicio', color='green', zorder=3)
        ax.scatter(y[-1, 0], y[-1, 1], label='Final', color='red', zorder=3)
        ax.set(xlabel='Presas', ylabel='Depredadores', xlim=(0, None), ylim=(0, None))
        ax.legend()
        ax.grid(alpha=.2)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.write('Cada punto de la curva representa las dos abundancias en un mismo '
                 'instante. Una espiral indica oscilaciones de amplitud cambiante; '
                 'no todas las combinaciones producen ciclos.')
    datos = io.StringIO()
    np.savetxt(datos, np.column_stack((t, y, k_t)), delimiter=',',
               header='tiempo,presas,depredadores,capacidad_carga', comments='', fmt='%.6f')
    st.download_button('Descargar datos (CSV)', datos.getvalue(),
                       file_name='dinamica_ecosistemas.csv', mime='text/csv')
    with st.expander('Investiga: tres experimentos para comparar'):
        st.markdown('1. Pon los depredadores iniciales a **0**. ¿Hacia qué valor tienden las presas?\n'
                    '2. Mantén los demás controles y aumenta los depredadores iniciales. '
                    '¿Qué población cambia primero?\n'
                    '3. Activa una pérdida del **50 %** de K. Predice el efecto y compara las curvas.')
        st.write('Cambia una sola variable cada vez. Anota la hipótesis, los valores '
                 'utilizados y las evidencias de la gráfica.')
    with st.expander('Modelo científico y limitaciones'):
        st.latex(r'\frac{dN}{dt}=rN\left(1-\frac{N}{K}\right)-aNP')
        st.latex(r'\frac{dP}{dt}=e\,aNP-mP')
        st.write('N: presas; P: depredadores; r: crecimiento de presas; K: capacidad '
                 'de carga; a: coeficiente de encuentro y consumo; m: mortalidad '
                 'de depredadores. Se fija e = 0,1 como factor de conversión de '
                 'presas consumidas en nuevos depredadores, no como eficiencia energética medida.')
        st.write('Es una simplificación de Lotka–Volterra con crecimiento logístico. '
                 'Supone mezcla homogénea, depredación proporcional a N×P, ausencia '
                 'de migraciones y de otras especies, y parámetros constantes salvo K '
                 'en la perturbación. No incluye edades, refugios, saciedad ni azar. '
                 'Una abundancia muy pequeña no equivale a una extinción real: '
                 'el modelo es continuo y no representa individuos discretos.')
