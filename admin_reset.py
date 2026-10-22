# -*- coding: utf-8 -*-
"""
Административная утилита сброса паролей AI Assistant 3D.
Позволяет задать новый пароль ЛЮБОМУ пользователю.

Запуск:
    python admin_reset.py                        # интерактивный режим
    python admin_reset.py CrafterOk.Ivan newpass # из аргументов
"""
import sys
import getpass
import db


# ============================================================
# НАСТРОЙКИ ПО УМОЛЧАНИЮ
# ============================================================
DEFAULT_PASSWORD = "admin123"   # если нажать Enter при вводе нового пароля


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def print_header():
    print("=" * 60)
    print("  🔐 Административный сброс пароля — AI Assistant 3D")
    print("=" * 60)


def list_users(users: dict):
    """Печатает список всех пользователей с их ролями."""
    print("\n📋 Пользователи в базе:")
    print(f"  {'#':<3} {'Логин':<28} {'Имя':<22} {'Роль':<10}")
    print("  " + "-" * 65)
    for i, (login, u) in enumerate(users.items(), 1):
        name = u.get("full_name", "")[:20]
        role = u.get("role", "")
        print(f"  {i:<3} {login:<28} {name:<22} {role:<10}")
    print()


def choose_user(users: dict) -> str:
    """Интерактивный выбор пользователя: по номеру или по логину."""
    list_users(users)

    while True:
        raw = input("Введите НОМЕР пользователя или ЛОГИН (Enter — отмена): ").strip()
        if not raw:
            return ""

        # По номеру
        if raw.isdigit():
            idx = int(raw) - 1
            logins = list(users.keys())
            if 0 <= idx < len(logins):
                return logins[idx]
            print("❌ Нет пользователя с таким номером.")
            continue

        # По логину
        if raw in users:
            return raw
        print(f"❌ Пользователь '{raw}' не найден. Попробуйте снова.")


def choose_password() -> str:
    """Ввод нового пароля (скрыто, с подтверждением)."""
    while True:
        p1 = getpass.getpass("Новый пароль (Enter — admin123): ").strip()
        if not p1:
            p1 = DEFAULT_PASSWORD
            print(f"ℹ️  Использован пароль по умолчанию: {DEFAULT_PASSWORD}")
            return p1

        if len(p1) < 4:
            print("❌ Пароль должен быть минимум 4 символа.")
            continue

        p2 = getpass.getpass("Повторите пароль: ").strip()
        if p1 != p2:
            print("❌ Пароли не совпадают. Попробуйте снова.")
            continue

        return p1


def reset_password(username: str, new_password: str) -> bool:
    """Меняет пароль пользователя. Возвращает True при успехе."""
    try:
        new_hash = db.hash_password(new_password)

        # Пробуем через функцию из db.py (если есть)
        if hasattr(db, "update_password"):
            db.update_password(username, new_hash)
        else:
            # Резервный путь — напрямую через SQL
            conn = db.get_connection()
            try:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE users SET password_hash = %s WHERE username = %s",
                    (new_hash, username),
                )
                conn.commit()
            finally:
                conn.close()

        return True
    except Exception as e:
        print(f"❌ Ошибка записи в базу: {e}")
        return False


# ============================================================
# ОСНОВНАЯ ЛОГИКА
# ============================================================

def main():
    print_header()

    # 1. Подключаемся и читаем список пользователей
    try:
        users = db.load_users()
    except Exception as e:
        print(f"❌ Не удалось подключиться к базе Neon:\n   {e}")
        print("\n💡 Проверьте, что переменная DATABASE_URL задана и пароль верный.")
        return 1

    if not users:
        print("⚠️  В таблице users нет ни одной записи.")
        return 1

    # 2. Если передан логин и пароль в аргументах — сбрасываем без интерактива
    if len(sys.argv) >= 3:
        username = sys.argv[1].strip()
        new_password = sys.argv[2].strip()

        if username not in users:
            print(f"❌ Пользователь '{username}' не найден.")
            print("Доступные логины:", ", ".join(users.keys()))
            return 1

        if len(new_password) < 4:
            print("❌ Пароль должен быть минимум 4 символа.")
            return 1

        if reset_password(username, new_password):
            print(f"✅ Пароль для '{username}' изменён на: {new_password}")
            return 0
        return 1

    # 3. Иначе — интерактивный режим
    username = choose_user(users)
    if not username:
        print("Отменено.")
        return 0

    u = users[username]
    print(f"\n🎯 Выбран пользователь: {username} ({u.get('full_name','')}, {u.get('role','')})")

    new_password = choose_password()
    if not new_password:
        print("Отменено.")
        return 0

    if reset_password(username, new_password):
        print(f"\n✅ Готово! Пароль для '{username}' теперь: {new_password}")
        print("   Запустите main.py и войдите с новым паролем.")
        return 0
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nОтменено пользователем.")
        sys.exit(130)

#python admin_reset.py