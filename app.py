from Maktab_Group_Flask_Project.__init__ import create_app

app = create_app()

if __name__ == '__main__':
    import os

    os.system('flask init-db')
    app.run()
