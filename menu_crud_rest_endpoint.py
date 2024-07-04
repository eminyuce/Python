from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

# Database Configuration
DATABASE_URL = "mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Menu(Base):
    __tablename__ = "Menus"

    Id = Column(Integer, primary_key=True, index=True)
    ParentId = Column(Integer, default=0, nullable=False)
    Name = Column(String(255), nullable=False)
    CreatedDate = Column(DateTime, default=datetime.utcnow, nullable=False)
    UpdatedDate = Column(DateTime, default=datetime.utcnow, nullable=False)
    IsActive = Column(Boolean, nullable=False)
    Position = Column(Integer, nullable=False)
    Description = Column(String, nullable=True)
    ImageState = Column(Boolean, nullable=True)
    MainPage = Column(Boolean, nullable=True)
    LinkIsActive = Column(Boolean, nullable=True)
    Link = Column(String(500), nullable=True)
    MainImageId = Column(Integer, nullable=True)
    MenuLink = Column(String(500), nullable=False)
    PageTheme = Column(String(50), nullable=True)
    Lang = Column(Integer, nullable=False)
    MetaKeywords = Column(String(1000), nullable=True)
    AddUserId = Column(String(100), nullable=True)
    UpdateUserId = Column(String(100), nullable=True)

class MenuCreate(BaseModel):
    ParentId: int
    Name: str
    IsActive: bool
    Position: int
    Description: Optional[str] = None
    ImageState: Optional[bool] = None
    MainPage: Optional[bool] = None
    LinkIsActive: Optional[bool] = None
    Link: Optional[str] = None
    MainImageId: Optional[int] = None
    MenuLink: str
    PageTheme: Optional[str] = None
    Lang: int
    MetaKeywords: Optional[str] = None
    AddUserId: Optional[str] = None
    UpdateUserId: Optional[str] = None

class MenuUpdate(BaseModel):
    ParentId: Optional[int] = None
    Name: Optional[str] = None
    IsActive: Optional[bool] = None
    Position: Optional[int] = None
    Description: Optional[str] = None
    ImageState: Optional[bool] = None
    MainPage: Optional[bool] = None
    LinkIsActive: Optional[bool] = None
    Link: Optional[str] = None
    MainImageId: Optional[int] = None
    MenuLink: Optional[str] = None
    PageTheme: Optional[str] = None
    Lang: Optional[int] = None
    MetaKeywords: Optional[str] = None
    AddUserId: Optional[str] = None
    UpdateUserId: Optional[str] = None

class MenuResponse(BaseModel):
    Id: int
    ParentId: int
    Name: str
    CreatedDate: datetime
    UpdatedDate: datetime
    IsActive: bool
    Position: int
    Description: Optional[str] = None
    ImageState: Optional[bool] = None
    MainPage: Optional[bool] = None
    LinkIsActive: Optional[bool] = None
    Link: Optional[str] = None
    MainImageId: Optional[int] = None
    MenuLink: str
    PageTheme: Optional[str] = None
    Lang: int
    MetaKeywords: Optional[str] = None
    AddUserId: Optional[str] = None
    UpdateUserId: Optional[str] = None

    class Config:
        orm_mode = True

class MenuRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_menu(self, menu_id: int):
        return self.db.query(Menu).filter(Menu.Id == menu_id).first()

    def get_menus(self, skip: int = 0, limit: int = 100):
        return self.db.query(Menu).offset(skip).limit(limit).all()

    def create_menu(self, menu: MenuCreate):
        db_menu = Menu(**menu.dict(), CreatedDate=datetime.utcnow(), UpdatedDate=datetime.utcnow())
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return db_menu

    def update_menu(self, menu_id: int, menu: MenuUpdate):
        db_menu = self.db.query(Menu).filter(Menu.Id == menu_id).first()
        if db_menu:
            update_data = menu.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_menu, key, value)
            db_menu.UpdatedDate = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_menu)
            return db_menu
        return None

    def delete_menu(self, menu_id: int):
        db_menu = self.db.query(Menu).filter(Menu.Id == menu_id).first()
        if db_menu:
            self.db.delete(db_menu)
            self.db.commit()
            return db_menu
        return None

class MenuService:
    def __init__(self, db: Session):
        self.repository = MenuRepository(db)

    def get_menu(self, menu_id: int):
        return self.repository.get_menu(menu_id)

    def get_menus(self, skip: int = 0, limit: int = 100):
        return self.repository.get_menus(skip=skip, limit=limit)

    def create_menu(self, menu: MenuCreate):
        return self.repository.create_menu(menu)

    def update_menu(self, menu_id: int, menu: MenuUpdate):
        return self.repository.update_menu(menu_id, menu)

    def delete_menu(self, menu_id: int):
        return self.repository.delete_menu(menu_id)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/menus/", response_model=MenuResponse)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    service = MenuService(db)
    return service.create_menu(menu)

@app.get("/menus/", response_model=List[MenuResponse])
def read_menus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = MenuService(db)
    return service.get_menus(skip=skip, limit=limit)

@app.get("/menus/{menu_id}", response_model=MenuResponse)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    db_menu = service.get_menu(menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@app.put("/menus/{menu_id}", response_model=MenuResponse)
def update_menu(menu_id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    service = MenuService(db)
    db_menu = service.update_menu(menu_id, menu)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

@app.delete("/menus/{menu_id}", response_model=MenuResponse)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    service = MenuService(db)
    db_menu = service.delete_menu(menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
