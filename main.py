import fastapi
import models
from database import session,engine
import database_models
from sqlalchemy.orm import Session

database_models.base.metadata.create_all(bind=engine)
app = fastapi.FastAPI()
@app.get("/")
def greet():
    return "Hello, World!"



def init_db():
    db=session()
    for product in products:
        db.add(database_models.product(id=product.id, name=product.name, description=product.description, price=product.price))
    db.commit()
    

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
@app.get("/getallproducts")
def get_all_products(db:Session = fastapi.Depends(get_db)):
    return db.query(database_models.product).all()

@app.get("/getproduct/{id}")
def get_product(id: int,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        return db_product
    return 'No Item Found'


@app.post("/addproduct")
def add_product(product:models.product,db:Session = fastapi.Depends(get_db)):
    db.add(database_models.product(id=product.id, name=product.name, description=product.description, price=product.price))
    db.commit() 
    return {"message": "Product added successfully"}

@app.put("/updateproduct/{id}")
def update(id: int, product: models.product,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        return {"message": "Product updated successfully"}
    return {"message": "Product not found"}

@app.delete("/deleteproduct/{id}")
def delete_product(id: int,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}