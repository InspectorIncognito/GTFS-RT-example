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

## Descarga de compilador protoc

Descargar y descomprimir el compilador desde [aquí](https://github.com/protocolbuffers/protobuf/releases) y elegir la versión y variante según el sistema operativo desde donde se ejecutará el comando.

La carpeta debe ser renombrada a `protoc` y puesta en la raíz del proyecto.


# Ejecución

El primer paso corresponde a compilar el archivo `gtfs-realtime.proto`, esto se realiza con el comando

```
    protoc\bin\protoc.exe -I=. --python_out=output\ gtfs-realtime.proto
```

La expresión `protoc/bin/protoc.exe` es para windows, para otros sistemas operativos revisar la carpeta protoc. Además, los parámetros corresponden a: 

1. `-I` corresponde a la dirección donde se encuentra el archivo gtfs-realtime.proto 
2. `--python_out` es la dirección donde se generará el archivo gtfs_realtime_pb2.py.

Lo anterior genera el archivo `output\gtfs_realtime_pb2.py` que permitirá definir el archivo GTFS-RT.


