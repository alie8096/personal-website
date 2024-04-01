from blog import app, db
from blog.routes import create_user
if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     create_user()
        
    app.run(debug=True)