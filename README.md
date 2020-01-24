# README

Proyecto para generar archivos con formato GTFS-RT con python

# Configuración

## Configuración de python

El proyecto ha sido usado con python 3.7 por lo que se recomienda usar esa versión. Además, es muy aconsejable generar un entorno virtual para la ejecución del proyecto

```
    # crear entorno virtual, se puede usar el parámetro --python para referencia una versión específica de python
    virtualenv venv --python /usr/bin/python3

    # activar entorno virtual
    source venv/bin/activate
```

## Instalación de dependencias

Las dependencias se encuentran en el archivo `requirements.txt` y se pueden instalar directamente con el comando `pip install requirements.txt`. 

# Ejecución

para generar y leer un archivo gtfs-rt con datos de posición de vehículos debe ejecutar el archivo `python build_proto.py`.
