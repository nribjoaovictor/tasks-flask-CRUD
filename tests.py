import pytest
import requests

#pytest tests.py -v

#CRUD
BASE_URL = "http://127.0.0.1:5000"
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json() #corpo do retorno
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json["id"]) 
#===================================================================================================== test session starts ======================================================================================================
#platform win32 -- Python 3.11.4, pytest-7.4.3, pluggy-1.6.0 -- C:\Program Files\Python311\python.exe
#cachedir: .pytest_cache
#rootdir: C:\Users\Notebook\tasks-flask-CRUD
#collected 1 item                                                                                                                                                                                                                

#tests.py::test_create_task PASSED                                                                                                                                                                                         [100%]

#====================================================================================================== 1 passed in 0.24s =======================================================================================================

def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json

def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json["id"]

#===================================================================================================== test session starts ======================================================================================================
#platform win32 -- Python 3.11.4, pytest-7.4.3, pluggy-1.6.0 -- C:\Program Files\Python311\python.exe
#cachedir: .pytest_cache
#rootdir: C:\Users\Notebook\tasks-flask-CRUD
#collected 3 items                                                                                                                                                                                                               

#tests.py::test_create_task PASSED                                                                                                                                                                                         [ 33%]
#tests.py::test_get_tasks PASSED                                                                                                                                                                                           [ 66%]
#tests.py::test_get_task PASSED                                                                                                                                                                                            [100%]

#====================================================================================================== 3 passed in 0.19s =======================================================================================================

def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "This task has been updated",
            "title": "Updated Task"
        }
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        #nova requisição a tarefa especifica
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]

def test_delete_task(): 
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404

