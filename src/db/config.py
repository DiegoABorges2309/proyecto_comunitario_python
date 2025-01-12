TORTOISE_ORM = {
    "connections": {
        "default": "mysql://root:230904@localhost:3306/service"
    },
    "apps": {
        "models": {
            "models": ["src.db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}