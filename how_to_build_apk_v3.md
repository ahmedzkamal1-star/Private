## الطريقة الثانية: الأتمتة الكاملة عبر GitHub (الأسهل)

لقد قمت بإضافة نظام "GitHub Actions" لمشروعك. هذا يعني أن GitHub سيقوم ببناء التطبيق لك آلياً في كل مرة ترفع فيها تحديثاً للموبايل.

### خطوات الحصول على التطبيق من GitHub:
1. ارفع كود الموبايل إلى GitHub (عبر `git push`).
2. افتح مستودعك (Repository) على صفحة GitHub في المتصفح.
3. اضغط على التبويب **Actions** في الأعلى.
4. ستجد عملية بناء جارية باسم **Build Android APK**. انتظر حتى تنتهي (يتحول اللون للأخضر).
5. اضغط على اسم العملية، ثم انزل للأسفل لتجد قسم **Artifacts**.
6. ستجد ملف الـ APK جاهزاً للتحميل هناك!

---

## الطريقة الأولى: استخدام Google Colab (للتحكم اليدوي)
...

إليك الخطوات بالتفصيل:

### 1. تجهيز الملفات
1. قم بضغط مجلد `mobile_app` الذي أنشأناه إلى ملف بصيغة `.zip` واسمه `mobile_app.zip`.
2. افتح [Google Colab](https://colab.research.google.com/).

---

### 2. الكود البرمجي (داخل Colab)
قم بإنشاء خلايا كود (Code Cells) وضع فيها الأوامر التالية بالترتيب:

#### الكود المصحح والنهائي (Ultra-Robust Version)
```python
# --- كود بناء التطبيق "النسخة الاحترافية 2026" - إصلاح الشامل ---
import os
import shutil
from google.colab import files

# 1. تحديث وتثبيت كافة الأدوات (بما في ذلك libtool المسبب للخطأ)
print("1️⃣ جارٍ تجهيز بيئة العمل (تثبيت libtool والأدوات الأساسية)...")
!sudo apt-get update > /dev/null
!sudo apt-get install -y build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev openjdk-17-jdk unzip zip libtinfo5 libtool pkg-config autoconf automake libltdl-dev libffi-dev --fix-missing > /dev/null
!pip install buildozer cython==0.29.33 > /dev/null

# 2. رفع ملف الكود
print("\n2️⃣ يرجى رفع ملف mobile_app.zip الآن:")
uploaded = files.upload()

# 3. فك الضغط والتنظيف الذكي للمجلدات
if os.path.exists('work_dir'): shutil.rmtree('work_dir')
os.makedirs('work_dir')
!unzip -o mobile_app.zip -d work_dir > /dev/null

# البحث عن ملف main.py داخل المجلدات لضبط المسار تلقائياً
target_path = 'work_dir'
for root, dirs, files_in_dir in os.walk('work_dir'):
    if 'main.py' in files_in_dir:
        target_path = root
        break
%cd {target_path}
print(f"تم الانتقال للمجلد الصحيح: {os.getcwd()}")

# 4. إعادة كتابة ملف buildozer.spec لضمان خلوه من الأخطاء
print("\n3️⃣ جارٍ كتابة ملف الضبط الذهبي...")
spec_content = """
[app]
title = منصة الدحيح الآمنة
package.name = aldahid_secure
package.domain = com.ahmedzkamal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,cryptography,pyjnius,android
orientation = portrait
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.release_artifact = apk
android.debug_artifact = apk
[buildozer]
log_level = 2
warn_on_root = 1
"""
with open('buildozer.spec', 'w', encoding='utf-8') as f:
    f.write(spec_content)

# 5. البدء في البناء مع تجاوز كل العقبات
print("\n4️⃣ بدأت عملية صناعة الـ APK... (20 دقيقة)")
!yes | buildozer -v android debug
```

---

### 3. تحميل التطبيق النهائي
بعد انتهاء العملية بنجاح، ستجد ملف الـ APK داخل مجلد اسمه `bin` في القائمة الجانبية للملفات في Colab.
- قم بتحميله على هاتفك وتثبيته.

---

### 💡 ملاحظات هامة:
- **المتطلبات (Requirements):** تأكد أن سطر `requirements` في ملف `buildozer.spec` يحتوي على:
  `python3,kivy==2.3.0,kivymd==1.2.0,requests,cryptography,pyjnius,android`
- **الأذونات (Permissions):** تأكد من إضافة:
  `android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE`
- **التشفير:** بما أننا نستخدم مكتبة `cryptography` و `pyjnius` للأمان، يجب أن تكون موجودة في المتطلبات كما ذكرت بالأعلى.

**إذا واجهت أي رسالة خطأ أثناء البناء في Colab، انسخها لي وسأخبرك بالحل فوراً!** 🚀
