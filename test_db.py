# -*- coding: utf-8 -*-
"""Проверка подключения к Neon."""

import db

print("🔌 Проверка подключения к Neon...")

# 1. Создаём тестового пользователя
db.upsert_user({
    "username": "CrafterOk.Owner",
    "password_hash": "test_hash",
    "full_name": "Владелец",
    "role": "owner",
    "schedule": "Пн-Пт 10:00-19:00",
    "pay_type": "fixed",
    "pay_rate": 100000,
    "language": "ru",
    "tasks": [],
    "pay_history": [],
})
print("✅ Пользователь создан")

# 2. Читаем обратно
users = db.load_users()
print(f"👥 Пользователей в БД: {len(users)}")
print(f"   Найден: {list(users.keys())}")

# 3. Создаём категорию и товар
db.upsert_category("Тест")
db.add_product("Тест", "Ваза", 500, "vase.gcode")
cats = db.load_categories()
print(f"📦 Категорий: {len(cats)}")

# 4. Пишем в чат
db.add_message("общий", "CrafterOk.Owner", "owner", "Привет из теста!")
msgs = db.load_messages("общий")
print(f"💬 Сообщений: {len(msgs)}")

print("\n🎉 Всё работает! Neon подключён.")