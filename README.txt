To use the project execute these lines:

.venv\Scripts\activate
python.exe -m pip install --upgrade pip
pip install fastapi uvicorn

uvicorn main:app --reload - to execute API main.py


For tests:
pip install pytest
pytest - for use tests in test_gestor_tarefas.py

pip install httpx - for API tests

pip install pytest-cov
pytest --cov to use pytest with % of tested code lines


for Web:
pip install jinja2