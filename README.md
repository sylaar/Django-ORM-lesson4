# Карта покемонов

скрин

### Краткое описание

Небольшой сайт-помошник для игры в Pokemon GO.

В игре необходимо находить и собирать покемонов.  
Данный сайт помогает отображать и фильтровать нужныъ покемонов которые доступны в определенный момент времени. Также есть страница с описанием и эволюциями конкретного покемона.

### **Клонирование репозитория**
```bash
git clone https://github.com/sylaar/Django-ORM-lesson4.git
cd pokemon_map
```

### **Создание виртуального окружения**
```bash
python -m venv .venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows
```

### **Установка зависимостей**
```bash
pip install -r requirements.txt
```

### **Настройка `.env`**
Создаём файл `.env` 
```
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
```
### **Запуск проекта**
Применение миграций
```
python manage.py migrate
```
Запуск сервера
```
python manage.py runserver
```
