from artsyml_app import create_app
#from artsyml import ArtsyML
#print(dir(ArtsyML))
app = create_app()

if __name__ == '__main__':
    app.run(debug = True)
    