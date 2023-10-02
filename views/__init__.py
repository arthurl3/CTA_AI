from .app import App

app = None

def create_ui():
    global app
    app = App()
    return app
