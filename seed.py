from database import SessionLocal
import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

excuses = [
    # Душные (dumb)
    {"text": "Задержка общественного транспорта", "category": "dumb"},
    {"text": "Проспал(а)", "category": "dumb"},
    {"text": "Интернет пропал", "category": "dumb"},
    {"text": "Спину защемило", "category": "dumb"},
    {"text": "Пробки на дороге", "category": "dumb"},
    # Средние (medium)
    {"text": "Застрял(а) в лифте", "category": "medium"},
    {"text": "Было плохое самочувствие", "category": "medium"},
    {"text": "Ребенок заболел", "category": "medium"},
    {"text": "Ждал(а) курьера с важным заказом, а он перепутал адрес", "category": "medium"},
    # Креативные (creative)
    {"text": "Помогал(а) бабушке перейти дорогу, она оказалась гадалкой и сделала мне бесплатный расклад. Её последнее предсказание: 'Ты опоздаешь'", "category": "creative"},
    {"text": "Пытался(ась) доказать, что Земля плоская, и прыгал(а), пытаясь заставить большую черепаху чихнуть.", "category": "creative"},
    {"text": "Был(а) уверен(а), что умею останавливать время.", "category": "creative"},
    # Сверхкреативные (super_creative)
    {"text": "Увидел(а) странную точку в небе и позвонил(а) в научное издание, чтобы зафиксировать пришествие НЛО", "category": "super_creative"},
    {"text": "Меня похитили инопланетяне, но я сбежал(а) и вернулся(ась) с сувениром (проставиться перед коллегами)", "category": "super_creative"}
]

for e in excuses:
    db.add(models.Excuse(text=e["text"], category=e["category"]))

db.commit()
print("База данных заполнена отмазками!")
db.close()
