from fastapi.testclient import TestClient
from sqlmodel import Session, Field, SQLModel, create_engine,select

from fastapi_todo_app.main import app, get_session, Todo, User

# from fastapi_todo_app.settings import settings

from fastapi_todo_app import settings


def test_get_todos():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}



# def test_write_main():
#     client = TestClient(app=app)
#     response = client.post("/todos/", json={"content": "buy bread"})
#     assert response.status_code == 200
#     assert response.json() == {"content": "buy bread"}





def test_write_main():

    connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")

    engine = create_engine(
        connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

    SQLModel.metadata.create_all(engine)  

    with Session(engine) as session:  

        def get_session_override():  
                return session  

        app.dependency_overrides[get_session] = get_session_override 

        client = TestClient(app=app)

        todo_content = "buy bread"

        response = client.post("/todos/",
            json={"content": todo_content, "is_done":False}
        )

        data = response.json()

        assert response.status_code == 200
        # assert data["is_done"] == False
        # assert data["content"] == todo_content

# def test_read_list_main():

#     connection_string = str(settings.TEST_DATABASE_URL).replace(
#     "postgresql", "postgresql+psycopg")

#     engine = create_engine(
#         connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)

#     SQLModel.metadata.create_all(engine)  

#     with Session(engine) as session:  

#         def get_session_override():  
#                 return session  

#         app.dependency_overrides[get_session] = get_session_override 
#         client = TestClient(app=app)

#         response = client.get("/todos/")
#         assert response.status_code == 200
