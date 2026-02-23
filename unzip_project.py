import zipfile
import os

# المعرف الصحيح للملف
zip_name = 'Al-Dahih_Final_Update.zip'
extract_dir = '.' 

if os.path.exists(zip_name):
    print(f"📦 جاري فتح {zip_name}...")
    try:
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("✅ تم فك الضغط بنجاح! جميع الملفات تم تحديثها.")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء فك الضغط: {e}")
else:
    print(f"❌ خطأ: الملف '{zip_name}' غير موجود في هذا المجلد.")
    print("يرجى التأكد من رفع الملف أولاً إلى PythonAnywhere.")
