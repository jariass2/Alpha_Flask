USERS

admin
admin123

usuario
usuario123

-------
brew install mdbtools
-------
He añadido un sistema de API con autenticación por token. Aquí está cómo usarlo:

Primero, necesitas obtener un token API:
bash

# Iniciar sesión y obtener un token
curl -X POST http://localhost:5001/api/token \
     -H "Cookie: session=tu_session_id"
Una vez tengas el token, puedes ejecutar la secuencia desde cualquier lugar:
bash

# Ejecutar la secuencia
curl -X POST http://localhost:5001/api/ejecutar_secuencia \
     -H "X-API-Token: tu_token_aqui"
Características del sistema API:

Autenticación segura mediante tokens
Los tokens son únicos y generados aleatoriamente
Cada token está asociado a un usuario
Los tokens pueden ser revocados si es necesario
Las respuestas son en formato JSON
Manejo de errores adecuado
Para mayor seguridad, recomiendo:

Usar HTTPS en producción
Rotar los tokens periódicamente
Implementar rate limiting
Almacenar los tokens en una base de datos
Añadir expiración a los tokens

------
El endpoint para ejecutar la secuencia es:

Code

POST http://localhost:5001/api/ejecutar_secuencia
Necesitas incluir el token en el header de la petición. Aquí tienes un ejemplo completo de cómo hacer la llamada con curl:

bash

curl -X POST http://localhost:5001/api/ejecutar_secuencia \
     -H "X-API-Token: tu_token_aqui"
O si estás usando Python con requests:

python

import requests

url = "http://localhost:5001/api/ejecutar_secuencia"
headers = {
    "X-API-Token": "tu_token_aqui"
}

response = requests.post(url, headers=headers)
print(response.json())
La respuesta será un JSON con los resultados de la ejecución de cada script:

json
CopyInsert
[
    {
        "script": "script1.py",
        "output": "resultado del script 1",
        "status": "success"
    },
    {
        "script": "script2.py",
        "output": "resultado del script 2",
        "status": "success"
    },
    {
        "script": "script3.py",
        "output": "resultado del script 3",
        "status": "success"
    }
]

------
He implementado un sistema completo de gestión de usuarios con las siguientes características:

Backend:
Almacenamiento persistente de usuarios en users.json
Endpoints para CRUD de usuarios:
GET /admin/users: Listar usuarios
POST /admin/users: Crear usuario
PUT /admin/users/<username>: Actualizar usuario
DELETE /admin/users/<username>: Eliminar usuario
Validaciones de seguridad:
Solo admin puede gestionar usuarios
No se puede eliminar el usuario admin
No se puede eliminar el propio usuario