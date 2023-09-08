from app import create_app
from app.config import Config


app = create_app(Config)


if __name__ == "__main__":
    import bjoern

    HOST = Config.HOST
    PORT = Config.PORT

    app.logger.info(f"Run <{app.name}> on http://{HOST}:{PORT}")
    bjoern.run(app, host=HOST, port=PORT)