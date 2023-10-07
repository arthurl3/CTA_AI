import views
from config import Config

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = views.create_ui()
    Config.app = app
    app.mainloop()

