[app]
title = AI Assistant 3D
package.name = aiassistant3d
package.domain = org.crafterok

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*

version = 1.0.0
requirements = python3,kivy,pg8000

orientation = portrait
fullscreen = 0

# Разрешения (нужен интернет для БД и API)
android.permissions = INTERNET

# Архитектуры процессоров
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Версия Android API
android.api = 31
android.minapi = 21

# Ориентация
android.wakelock = True
