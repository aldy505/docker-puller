generate_requirements:
    pip freeze > requirements.txt

dev:
    python3 -m uvicorn main:app --reload