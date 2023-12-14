#El program se encuentra limitado a 1 pagina por letra del abecedario, por lo mismo puede faltal informacion, pero esta se puede agregar manualmente a las lista de anime, para solucionar eso

El programa no tiene nada guardado antes de usarse entonces, cuando se agrega un anime, primero se debe actualizar, para cargar la base de datos y poder tener opciones en la busqueda.

Por falta de tiempo no esta implementado login bien hecho, por lo que no se puede aislar de buena forma los datos de un usuario de otro, pero si se puede especificar en la base de datos y que datos le pertenecen a que usuario usuario, esto mediante el uso de la id para guardar, eliminar datos y ver datos, siendo este caso para ver la lista de animes, que solicita el id Personal para ver una lista, pero no pudiendo estar limitado a solo es usuario.

Otra cosa que no esta bien imprementada es el agregado a la lista personal los datos obtenidos de la red, lo mismo, por falta de tiempo, pero si se puede cargar, ver y buscar esta informacion, es decir, si esta guardada y es manipulable, pero, siendo la unica deficiencia que no se puede agregar a la lista de animes personal

En la seccion de buscar animes, una vez cargada la información, como se vaya escribiendo en el input se mostran solo los animes que vayan deacuerdo a la escritura de lo que se esta buscando

instalar 
    SQLAlchemy
    flask-sqlalchemy
    flask_login
    Blueprint
    render_template
    redirect
    url_for
    jsonify
    os
    hashlib (inculada a la versión de Python que estás utilizando)

Instrucciones 
    Ejecutar
    python -m venv .venv
     .venv\Scripts\activate
        (hacer el prodimiento para conectarse a github)
     git clone (repositorio)
     pip install -r requeriments.txt