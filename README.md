# Setup

cd backend

python -m venv venv

# Dependencies

pip install -r requirements.txt

pip freeze > requirements.txt

- when adding packages

# Running server (separate terminal)

./venv/Scripts/Activate.ps1

- activates venv

uvicorn main:app --reload

- runs server

deactivate

- closes venv
