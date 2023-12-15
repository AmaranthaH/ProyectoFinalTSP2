#El programa se encuentra limitado a 1 página por letra del abecedario en los archivos descargados, por lo mismo puede faltar información, pero esta se puede agregar manualmente a la lista de anime, para solucionar eso.

#El programa no tiene nada guardado antes de usarse, entonces, cuando se agrega un anime, primero se debe actualizar, para cargar la base de datos y poder tener opciones en la búsqueda.

#Por falta de tiempo no está implementada la función  "login" bien hecho, por lo que no se puede aislar de buena forma los datos de un usuario de otro, pero si se puede especificar en la base de datos y que datos le pertenecen a que usuario, esto mediante el uso de la id para guardar, eliminar datos y ver datos, siendo este caso para ver la lista de animes, que solicita el id Personal para ver una lista, pero no pudiendo estar limitado a solo es usuario. 

#Otra cosa que no está bien implementada es el agregado a la lista personal los datos obtenidos de la red, lo mismo, por falta de tiempo y el problema del "login" mencionado antes, pero si se puede cargar, ver y buscar esta información, es decir, si está guardada y es manipulable, pero, siendo la única deficiencia que no se puede agregar a la lista de animes personal.

En la sección de buscar animes, una vez cargada la información, como se vaya escribiendo en el input, se muestran solo los animes que vayan de acuerdo a la escritura de lo que se está buscando.

Instalar 
    SQLAlchemy
    flask-sqlalchemy
    flask_login
    Blueprint
    render_template
    redirect
    url_for
    jsonify
    os
    hashlib (incluida a la versión de Python que se esté utilizando)

Instrucciones 
    Ejecutar
    python -m venv .venv
     .venv\Scripts\activate
        (hacer el procedimiento para conectarse a github)
     git clone (repositorio)
     pip install -r requeriments.txt