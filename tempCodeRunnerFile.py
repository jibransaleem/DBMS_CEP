@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
