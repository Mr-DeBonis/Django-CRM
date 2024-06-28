# Installation

1. Use Python 3.11
2. Install mysql
3. Run
```
pip install -r requirements.txt
```

# Database migration

1. After creating a model, run:
`python manage.py makemigrations`
2. To load to DB: 
`python manage.py migrate`