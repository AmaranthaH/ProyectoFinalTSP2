from flask import Blueprint, render_template, redirect, url_for,jsonify
from flask import request
from .models import db, Persona, PersonaSesion,BibliotecaGeneralAnime,ListaAnime

import requests
import os
import hashlib

from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/formulario')
def formulario():
    return render_template('formulario.html')

@main.route('/iniciar_sesion')
def sesion():
    return render_template('iniciar_Sesion.html')

@main.route('/sesionRe')
def RegresarSession():
    return render_template('Sesion_abierta.html')

@main.route('/borrar_de_lista')
def eliminar_L():
    return render_template('borrar.html')

@main.route('/GuardadoM')
def GuardadManual():
    return render_template('guardado_manual.html')

@main.route('/submit_form', methods=['POST'])  ## Metodo para registrar a las personas
def submit_form():

    email = request.form.get('email')
    nickname = request.form.get('nickname')
    contrasena = request.form.get('contrasena')

    # Verificar si el nickname ya existe en la base de datos
    persona_existente = Persona.query.filter_by(email=email).first()

    if persona_existente:
        # El email ya está registrado, mostrar la página de ya_registrado
        return render_template('ya_existe.html')

    else:
        # El nickname no está registrado, agregar la nueva persona a la base de datos
        # Generar salt
        salt = os.urandom(16)
        # Hash de la contraseña con el salt
        contrasena_salted = contrasena.encode('utf-8') + salt
        contrasena_hash = hashlib.pbkdf2_hmac('sha256', contrasena_salted, salt, 100000).hex()

        nueva_persona = Persona(email=email, nickname=nickname, contrasena=contrasena_hash)
        db.session.add(nueva_persona)
        db.session.commit()

        sesion_nueva_persona = PersonaSesion(user_id=nueva_persona.id, contrasena_hash=contrasena_hash, salt=salt)
        db.session.add(sesion_nueva_persona)
        db.session.commit()

        # Redirigir a la página de éxito
        return redirect(url_for('main.exito'))


@main.route('/ver_registros')
def ver_registros():
    personas = Persona.query.all()
    return render_template('ver_registros.html', personas=personas)

@main.route('/exito')
def exito():
    return render_template('exito.html')


@main.route('/Sesion_on', methods=['POST'])
def Sesion_On():
    email = request.form.get('email')
    contrasena = request.form.get('contrasena')

    # Verificar si el email existe en la base de datos
    persona_existente = Persona.query.filter_by(email=email).first()

    if persona_existente:
        # Persona encontrada, obtener su id
        user_id = persona_existente.id

        # Buscar la instancia de PersonaSesion basándote en el user_id
        sesion_persona_existente = PersonaSesion.query.filter_by(user_id=user_id).first()

        if sesion_persona_existente:
            # Contraseña almacenada y salt de la PersonaSesion
            contrasena_hash = sesion_persona_existente.contrasena_hash
            salt = sesion_persona_existente.salt

            # Verificar la contraseña ingresada con la almacenada
            contrasena_salted = contrasena.encode('utf-8') + salt
            contrasena_ingresada_hash = hashlib.pbkdf2_hmac('sha256', contrasena_salted, salt, 100000).hex()

            if contrasena_ingresada_hash == contrasena_hash:
                # Contraseña correcta, redirigir a la página de éxito
                return render_template('Sesion_abierta.html')
            else:
                # Contraseña incorrecta, manejar esto como desees
                return render_template('ya_existe.html')
        else:
            # No se encontró una instancia de PersonaSesion para el usuario
            return render_template('ya_existe.html')

    else:
        # Persona no encontrada, manejar como desees
        return render_template('ya_existe.html')

@main.route('/BuscarAnime')
def BA():
    return render_template('BuscarAnime.html')

####################################################
@main.route('/scrap_anime_data', methods=['GET'])
def scrap_anime_data():
    url_base = 'https://myanimelist.net/anime.php?letter={}'
    abecedario = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_paginas = 1

    for letra in abecedario:
        for pagina_actual in range(1, max_paginas + 1):
            url = f'{url_base.format(letra)}&show={(pagina_actual - 1) * 50}'
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            tabla = soup.select_one('#content > div.js-categories-seasonal.js-block-list.list')

            if tabla:
                datos_animes = []

                for fila in tabla.find_all('tr'):
                    celdas = fila.find_all('td')

                    if len(celdas) >= 2:
                        nombre_bruto = celdas[1].get_text(strip=True)
                        nombre_sin_add = nombre_bruto.split('add')[0].strip()
                        episodios = celdas[3].get_text(strip=True)

                        # Verificar si el anime ya existe en la base de datos
                        if not BibliotecaGeneralAnime.query.filter_by(nombre=nombre_sin_add).first():
                            # Si no existe, agregar el nuevo anime
                            nuevo_anime = BibliotecaGeneralAnime(nombre=nombre_sin_add, capitulos=episodios)
                            db.session.add(nuevo_anime)
                            db.session.commit()

                            print(f'Nuevo anime agregado: {nombre_sin_add} - Capítulos: {episodios}')

                print(f'Datos guardados en "resultados_anime_{letra}_pagina_{pagina_actual}.txt"')

            else:
                print(f'No se encontró la tabla en la página {letra}, {pagina_actual}. Fin del scraping.')
                break

    return jsonify({'message': 'Web scraping completado'})


def parse_anime_info(anime_info):
    parts = anime_info.split('\t')
    nombre_anime = parts[0].split(': ')[1]
    capitulos_anime = parts[1].split(': ')[1]

    return nombre_anime, capitulos_anime


@main.route('/resultados_busqueda', methods=['POST'])
def resultados_busqueda():
    search_query = request.form.get('searchQuery')

    # Realizar la búsqueda en la base de datos
    resultados = BibliotecaGeneralAnime.query.filter(BibliotecaGeneralAnime.nombre.ilike(f'%{search_query}%')).all()

    # Excluir la primera instancia de la búsqueda
    resultados_sin_primera_instancia = resultados[1:]

    resultados_json = [{'nombre': anime.nombre, 'capitulos': anime.capitulos} for anime in resultados_sin_primera_instancia]

    return jsonify(resultados_json)

# ... (código anterior)

@main.route('/registrar_anime_m', methods=['POST'])
def registro_manual():
    nombre_anime = request.form.get('nombre')
    capitulos_anime = request.form.get('capitulos')
    id_persona = request.form.get('id')

    # Verificar si el anime ya existe en la base de datos
    if not ListaAnime.query.filter_by(nombre=nombre_anime).first():
        # Si no existe, agregar el nuevo anime
        nuevo_anime = ListaAnime(nombre=nombre_anime, capitulos=capitulos_anime, persona_id=id_persona, biblioteca_id=id_persona)
        db.session.add(nuevo_anime)
        db.session.commit()

        return render_template('exito_manual.html', nombre_anime=nombre_anime, capitulos_anime=capitulos_anime)
    else:
        # El anime ya existe, manejar esto como desees
        return render_template('error.html', nombre_anime=nombre_anime)
    
@main.route('/eliminar_anime_m', methods=['POST'])
def eliminar_manual():
    nombre_anime = request.form.get('nombre')
    id_persona = request.form.get('id')

    # Buscar el anime en la base de datos
    anime_a_eliminar = ListaAnime.query.filter_by(nombre=nombre_anime, persona_id=id_persona).first()

    if anime_a_eliminar:
        # Si existe, eliminar el anime
        db.session.delete(anime_a_eliminar)
        db.session.commit()

        return render_template('exito_manual.html', operacion='eliminado', nombre_anime=nombre_anime)
    else:
        # El anime no existe, manejar esto como desees
        return render_template('error.html', operacion='eliminar', nombre_anime=nombre_anime)



    
@main.route('/ver_lista_anime', methods=['GET'])
def ver_lista_anime():
    # Obtener el ID del parámetro de la solicitud
    persona_id = request.args.get('persona_id')

    # Filtrar la lista de animes por el ID de la persona
    animes = ListaAnime.query.filter_by(persona_id=persona_id).all()

    # Crear una lista con los datos filtrados
    anime_list = [{'nombre': anime.nombre, 'capitulos': anime.capitulos} for anime in animes]

    return jsonify(anime_list)

