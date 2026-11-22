"""Primera práctica del laboratorio: comparación de modelos celulares."""
import streamlit as st
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"


def mostrar_laboratorio():
    st.title('🔬 Laboratorio virtual')
    st.subheader('Práctica 1 · Comparamos células animales y vegetales')
    st.write('Observa, identifica estructuras y utiliza las evidencias para justificar tus respuestas.')
    st.info('Son ilustraciones didácticas tridimensionales de una célula animal y una célula vegetal fotosintética, '
            'no fotografías al microscopio. Los colores y tamaños no están a escala '
            'y se representan estructuras seleccionadas.')
    st.markdown('**1. Observa y compara**')
    a, b = st.columns(2)
    for columna, vegetal, nombre in [(a, False, 'Muestra A'), (b, True, 'Muestra B')]:
        with columna:
            st.subheader(nombre)
            imagen = "celula_vegetal.png" if vegetal else "celula_animal.png"
            st.image(str(ASSETS / imagen), width="stretch")
    st.write('Anota qué estructuras comparten las muestras y cuáles aparecen solo en B. '
             'Los mismos números identifican las mismas estructuras en ambas ilustraciones.')
    with st.expander('Consultar la clave de estructuras'):
        st.write('1. Pared celular · 2. Membrana plasmática · 3. Núcleo · '
                 '4. Vacuola central · 5. Cloroplasto · 6. Citoplasma.')
        st.caption('La pared vegetal está por fuera de la membrana plasmática. '
                   'El interior de la vacuola no forma parte del citosol.')
    st.markdown('**2. Comprueba tus conclusiones**')
    preguntas = [
        ('¿Qué muestra representa una célula vegetal fotosintética?',
         ['Muestra A', 'Muestra B', 'Las dos'], 'Muestra B',
         'B presenta pared celular, cloroplastos y una gran vacuola central.'),
        ('¿Qué estructura señala el número 3?',
         ['Núcleo', 'Vacuola central', 'Pared celular'], 'Núcleo',
         'El núcleo está presente en las dos células eucariotas representadas.'),
        ('¿Qué estructura regula el intercambio de sustancias con el medio?',
         ['Pared celular', 'Membrana plasmática', 'Cloroplasto'], 'Membrana plasmática',
         'La membrana plasmática tiene permeabilidad selectiva y aparece en ambas células.'),
        ('¿Todas las células de una planta tienen cloroplastos?',
         ['Sí, todas', 'No; por ejemplo, muchas células de las raíces no los tienen'],
         'No; por ejemplo, muchas células de las raíces no los tienen',
         'Los cloroplastos son característicos de tejidos fotosintéticos, no de todas las células vegetales.'),
        ('¿Qué estructura corresponde al número 4 en B?',
         ['Núcleo', 'Vacuola central', 'Cloroplasto'], 'Vacuola central',
         'La vacuola central contiene savia vacuolar y contribuye a la turgencia celular.')
    ]
    with st.form('lab_celulas'):
        respuestas = [st.radio(p, opciones, index=None, key=f'lab_q{i}')
                      for i, (p, opciones, _, _) in enumerate(preguntas)]
        enviada = st.form_submit_button('Corregir respuestas')
    if enviada:
        if any(r is None for r in respuestas):
            st.warning('Responde todas las preguntas antes de corregir.')
        else:
            aciertos = sum(r == p[2] for r, p in zip(respuestas, preguntas))
            st.success(f'Resultado: {aciertos} de {len(preguntas)} respuestas correctas.')
            for i, (respuesta, (_, _, correcta, explicacion)) in enumerate(zip(respuestas, preguntas), 1):
                if respuesta == correcta:
                    st.success(f'{i}. Correcto. {explicacion}')
                else:
                    st.error(f'{i}. Revisa tu respuesta. {explicacion}')
    st.markdown('**3. Del esquema al microscopio**')
    st.write('En una preparación de epidermis de cebolla puedes distinguir las paredes celulares; '
             'el núcleo suele verse mejor con tinción. La epidermis del bulbo normalmente '
             'no presenta cloroplastos. En una hoja de una planta acuática, como Elodea, '
             'sí pueden observarse cloroplastos. No todos los orgánulos de un esquema '
             'se distinguen con un microscopio óptico escolar.')
    st.text_area('Conclusión: explica dos semejanzas y dos diferencias entre las muestras.',
                 key='lab_conclusion', height=120)
    st.caption('La conclusión es de respuesta abierta y no se corrige automáticamente. '
               'Las respuestas se mantienen durante la sesión; no se guardan en un registro permanente.')
