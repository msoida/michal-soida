from michalsoida import app
from michalsoida.settings import host, port, debug

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
