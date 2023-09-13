import uvicorn
from fastapi import FastAPI

from db.base import engine
from db.tables import Base
from routers import booking

import to_sql, to_df


app = FastAPI()

app.include_router(booking.bookings)
app.include_router(booking.stats)


@app.get("/")
def root():
    return {"message": "Hello ROOT !!!"}


if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    to_sql.import_data()
    uvicorn.run("main:app", port=8000, reload=True)
