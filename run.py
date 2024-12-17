from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8080) # Launch built-in web server and run this Flask webapp, debug=True

    


    