import fastapi
import models
from database import session,engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

database_models.base.metadata.create_all(bind=engine)
app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
@app.get("/products")
def get_all_products(db:Session = fastapi.Depends(get_db)):
    return db.query(database_models.product).all()

@app.get("/products/{id}")
def get_product(id: int,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        return db_product
    return 'No Item Found'


@app.post("/products")
def add_product(product:models.product,db:Session = fastapi.Depends(get_db)):
    db.add(database_models.product(id=product.id, name=product.name, description=product.description, price=product.price))
    db.commit() 
    return {"message": "Product added successfully"}

@app.put("/products/{id}")
def update(id: int, product: models.product,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db.commit()
        return {"message": "Product updated successfully"}
    return {"message": "Product not found"}

@app.delete("/products/{id}")
def delete_product(id: int,db:Session = fastapi.Depends(get_db)):
    db_product=db.query(database_models.product).filter(database_models.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}