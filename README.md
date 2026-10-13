# ميزان — برنامج المحاسبة وإدارة المحلات

برنامج محاسبة عربي لويندوز، بيشتغل بدون إنترنت، وبيخدم أكتر من 14 مجال عمل: ميني ماركت، مطاعم، ورش خياطة، موبايلات وكمبيوتر، صيدليات، وغيرها.

## ⬇️ تحميل البرنامج

**[تحميل ميزان لويندوز (Mizan-Setup.exe)](https://github.com/Akyedgam3/mizan-updates/releases/latest/download/Mizan-Setup.exe)**

1. نزّل الملف وشغّله، وكمّل خطوات التنصيب.
2. أول ما يفتح البرنامج بيطلعلك **بصمة الجهاز**. ابعتها للبائع أو للوكيل.
3. بيوصلك **مفتاح التفعيل**، الصقه بشاشة التفعيل وبلّش شغل.

> إذا ويندوز طلّع رسالة "Windows protected your PC" اكبس **More info** وبعدين **Run anyway**.

## 📞 للاشتراك أو لتصير وكيل

واتساب: **+963 968 037 609** — **+963 980 072 891**

---

ملف `feed.txt` هون هو قائمة حالة التراخيص الموقّعة، البرنامج بيقراه ليتحقق من الاشتراك ومن التحديثات. لا تعدّله يدوياً، بينطلع من لوحة الإدارة.

---

## 🛠️ ملاحظات الصيانة (لصاحب المشروع)

- **الموقع:** https://akyedgam3.github.io/mizan-updates/ (GitHub Pages من فرع `main`، المجلد الرئيسي).
- **تعديل الصفحات:** عدّل الملفات في `tools/pages/` وبعدين شغّل `python3 tools/build_site.py`. لا تعدّل `index.html` وأخواتها مباشرة لأنها بتنولّد.
- **التصميم والحركات:** `assets/css/site.css` و `assets/js/site.js`. الأيقونات من Lucide بملف واحد `assets/img/icons.svg`.
- **الفيديوهات:** `media/` (كل فيديو أقل من 100MB). صورة الغلاف من نفس الاسم `.jpg`.
- **ملف التنصيب:** بينرفع كـ Release باسم ثابت `Mizan-Setup.exe`، فرابط `releases/latest/download/Mizan-Setup.exe` بيضل شغّال مع كل نسخة.
- **`feed.txt`:** قائمة حالة التراخيص وإعلان التحديثات، بتنطلع موقّعة من لوحة الإدارة (`npm run admin` بمشروع البرنامج). البرنامج بيقراها من:
  - `https://raw.githubusercontent.com/Akyedgam3/mizan-updates/main/feed.txt`
  - احتياطي: `https://cdn.jsdelivr.net/gh/Akyedgam3/mizan-updates@main/feed.txt`
- **لما تشتري دومين:** حطه بـ Settings ← Pages ← Custom domain، وعدّل `SITE` بـ `tools/build_site.py` و `base` بـ `tools/pages/404.html` (بيصير `/`).
