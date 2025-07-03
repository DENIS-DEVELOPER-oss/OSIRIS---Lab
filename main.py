from app import app

if __name__ == '__main__':
    # La aplicación se ejecuta en modo debug en puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
