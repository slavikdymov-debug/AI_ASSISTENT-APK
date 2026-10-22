[app]

# --- Идентификация приложения ---
title = AI Assistant 3D
package.name = aiassistant3d
package.domain = org.crafterok

# --- Что берём в APK ---
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,json
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__,.venv,venv,tests
source.exclude_patterns = admin_reset.py,test_db.py,config.example.py,*.md,*.txt,*.log,.gitignore,buildozer.spec

# --- Версия ---
version = 1.0.0

# --- Зависимости Python ---
# kivy       — UI
# pg8000     — чистый Python-драйвер Postgres (без C-расширений, работает на Android)
# openssl    — нужен для ssl в pg8000 (без него TLS к Neon не заработает)
# pyjnius    — требуется p4a для доступа к Java (ставится автоматически, но укажем явно)
requirements = python3,kivy==2.3.0,pg8000,openssl,pyjnius,android

# --- Ориентация / экран ---
orientation = portrait
fullscreen = 0

# --- Android SDK/NDK ---
# 25b — стабильная версия, не имеет проблемы с libwebp, как r28c
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# --- Архитектуры ---
android.archs = arm64-v8a,armeabi-v7a

# --- Разрешения ---
# INTERNET обязателен: без него pg8000 не откроет сокет к Neon
android.permissions = INTERNET

# --- Прочее ---
android.accept_sdk_license = True
android.allow_backup = True
android.wakelock = True
android.debug_artifact = apk
android.release_artifact = aab

# --- python-for-android ---
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
