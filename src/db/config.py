TORTOISE_ORM = {
    "connections": {
        "default": "mysql://root:230904@localhost:3306/hola"
    },
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],  # Incluye "aerich.models"
            "default_connection": "default",
        }
    },
}