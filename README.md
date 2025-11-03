# File structure:
``` bash
(.venv) artin@g15:~/customic-task$ tree
.
├── Dockerfile
├── README.md
├── bruno-customic-api # Bruno files for testing API
│   ├── Get detail of task by id.bru
│   ├── Get list of all mockups.bru
│   ├── Making mockup.bru
│   └── bruno.json
├── compose.yaml # Docker compose file
├── customic # Django startproject files
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── media # Created mockups pictures will be stored here
│   └── mockups
├── mockups_api # Django startapp files
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_mockuptask_task_id.py
│   │   ├── 0003_rename_task_font_mockuptask_font_and_more.py
│   │   ├── 0004_alter_mockuptask_task_id.py
│   │   ├── 0005_rename_shirt_colors_mockuptask_shirt_color_and_more.py
│   │   ├── 0006_mockuptask_results.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── serializer.py
│   ├── tasks.py # Celery task
│   ├── tests # Some unit tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_task.py
│   └── views.py
├── requirements.txt
├── static
│   ├── fonts # Fonts for making mockups with custom fonts
│   │   ├── Froke.otf
│   │   └── Lemynotes.ttf
│   └── images # 4 base tshirt images for making mockups
│       ├── black.png
│       ├── blue.png
│       ├── white.png
│       └── yellow.png
└── task.pdf
```

# مراحل انجام تسک ها و توضیحات

## Swagger

در ابتدا می‌خواهم بگویم که این اولین تجربه استفاده من از swagger بود

ظاهرا برای استفاده از swagger در django ما دو کتابخانه اصلی داریم

drf-yasg و drf-spectacular که اولی برای نسخه دو ساخته شده و spectacular برای نسخه سه

من از drf-spectacular استفاده کردم که برای نسخه سه ساخته شده.

## models.py

در اینجا دو model تعریف شده است.

اولی MockupTask که اطلاعات تسک های celery در آن قرار دارد و Mockup که در آن اطلاعات مربوط به Mockup های ساخته شده قرار دارد.

## serializer.py

در این فایل serializer برای endpoint ها ساخته شده.

برای تمیز بودن کدها و راحت بودن کار با swagger سریالایزرها برای Body و Response های endpoint های مختلف به صورت جدا تعریف شده است.

## views.py

در این‌جا سه view اصلی که قرار است از آن‌ها استفاده شود، ساخته شده‌اند.

- اولین MockupTaskGenerateView است که برای ساخت mockup ها استفاده می‌شود
در کلاس آن از دکوراتور extend_schema استفاده شده است که بتوان در swagger از Json Body برای دادن اطلاعات اولیه برای ساخت mockup ها استفاده کرد

این کلاس دارای یک متد post است
در آن ابتدا اطلاعات مورد نیاز برای ساخت mockup گرفته می‌شود و یک مدل MockupTask ساخته می‌شود و اطلاعات تسک در آن ذخیره می‌شود و وضعیت آن به PENDING تغییر پیدا میکند

سپس این اطلاعات به تابع make_mockup_image داده می‌شود که یک تسک celery است که بعدا مراحل ساخت آن توضیح داده می‌شود

سپس Response مناسب به کاربر داده می‌شود

- دومین view کلاس MockupTaskDetailView است که ارث‌بری شده از RetrieveAPIView
نحوه کار آن ساده است
تمام mockup های ساخته شده را لود میکند و سپس بر اساس task_id که به آن داده می‌شود وضعیت تسک خواسته شده را به عنوان Response برمیگرداند

- سومین view MockupListView است 

در ابتدا من اجرای pagination و search رو بلد نبودم برای همین سرچ کردم و ظاهرا django کلاس ListAPIView را دارد که با استفاده از آن اجرای این ۲ مورد راحت است برای همین این view را چایلد ListAPIView قرار دادم

سرچ فیلد ها را مشخص کردم

بعد از ساخت به یک مشکلی خوردم آن هم این بود که وقتی از pagination استفاده میشد در Response اطلاعات اضافه داده میشد برای همین مجبور به ساخت کلاس MakePagination شدم تا در آن Response خودم را بسازم که در آن فقط data خواسته شده است و اطلاعات اضافه مثل شماره صفحه قرار ندارد

##  tasks.py

من قبلا تجربه کار با کتابخونه Pillow رو برای کار با تصویر داشتم برای همین برای چاپ متن روی تصویر از این کتابخونه استفاده کردم.

در ابتدای تابع make_mockup_image ما با استفاده از task_id مدل MockupTask مورد نظر خود را میگیریم.

بعد اطلاعات مورد نیاز برای چاپ را در متغیر های مربوطه ذخیر میکنیم

در صورتی که shirt_color به ما داده نشده بود تمام لباس های موجود در static/images رو به عنوان لباسی که قرار است mockup آن ساخته شود وارد میکنیم

بعد سراغ فونت میرویم و سعی میکنیم فونتی که کاربر داده را از لیست فونت های static/fonts انتخاب کنیم در صورت بروز مشکل از فونت پیش فرض PIL استفاده می‌شود

سپس روی تمام لباس ها لوپ زده می‌شود و لباس ها تولید می‌شود

برای تولید لباس ها چند نکته رعایت شده است

اول اینکه در صورتی که رنگ متن لباس داده نشده باشد بر اساس میزان روشن یا تیره بودن لباس رنگ سفید یا سیاه برای چاپ متن روی لباس انتخاب می‌شود

این کار از طریق بررسی رنگ وسط تصویر (که رنگ تقریبی لباس است) انجام می‌شود رنگ پیکسل پیدا می‌شود سپس به تابع calculate_good_text_color داده می‌شود در آنجا با توجه به فرمول داده شده میزان روشنایی آن پیکسل تشخیص داده می‌شود و بر اساس آن رنگ سیاه یا سفید برای چاپ انتخاب می‌شود

نکته بعدی این است که موقعیت چاپ بر اساس سایز عکس به صورت تقریبی انتخاب می‌شود

در آخر تابع مدل Mockup از لباس ساخته می‌شود اطلاعات مورد نیاز در آن ذخیره می‌شود و text_color ریست می‌شود

دلیل ریست کردن این است که اگر کاربر رنگ متن را نداده باشد و مثلا لباس اول سفید باشد text_color سیاه می‌شود و اگر مثلا لباس بعدی سیاه باشد تابع در ابتدا چک میکند که متغیر text_color چه مقداری دارد و اینگونه می‌بیند که text_color رنگ داشته و به اشتباه میفتد برای اینکار در آخر تابع ریست می‌شود

بعد از این مرحله اطلاعات مربوط به مدل MockupTask آپدیت می‌شود.

حال به بخش celery میرسیم

من قبلا با celery کار نکرده بودم و اولین بار بود که از ان استفاده میکردم

ظاهرا برای انجام تسک ها به صورت async celery دو تابع اصلی دارد

delay() و apply_async() که نحوه کار آنها مثل هم است و فرق اصلی آنها این است که apply_async() دارای option های بیشتری است و کنترل بیشتری به ما میدهد

من در view از delay() استفاده کردم چون نیازی به option های apply_async() نمی‌دیدم

ظاهرا با استفاده از دکوراتور @shared_task()
می‌شود یک تابع را به عنوان تسک celery رجیستر کرد که بتوان از delay() استفاده کرد بخاطر همین من از این روی تابع ساخت عکسم استفاده کردم


## urls.py

در این فایل من url های مربوط به API و همچنین url های مربوط به swagger را تنظیم کردم

## settings.py

در این فایل تنظیمات Django آورده شده

همچنین بعضی آدرس های مهم مثل فایل های font و عکس خام تی شرت ها و تنظیمات DRF, Pagination

## نوشتن unit test

من نوشتن unit test و با django.test بلد نبودم اما رفتم نگاه کردم
ظاهراً ۲ تا class خیلی مهم داره.

* TestCase و SimpleTestCase
فرقشون تو این هست که TestCase به DB دسترسی داره و میشه باهاش model ها رو تست کرد

من صرفا برای مثال ۲ تا تست برای تسک celery نوشتم که تابع calculate_good_text_color رو تست میکنه
این کار برای این بود که صرفا با SimpleTestCase کار کرده باشم

۱ تست هم برای MockupTask model نوشتم
برای اینکه با TestCaes کار کرده باشم
در حین کار با TestCase فهمدیم که ما یک سری اسم های از پیش تعریف شده برای method های کلاس TestCase داریم مثلا
setUp که همیشه اول هر تست قبل از بقیه method ها اجرا می‌شود.

## افزودن احراز هویت

این کار هم برای من کاملا جدید بود و تا به حال انجام نداده بودم

مثل اینکه برای انجام این کار چند راه است اما JWT یکی از بهترین روش هاست

برای انجام این کار از کتابخونه djangorestframework-simplejwt استفاده شده

در فایل settings.py 
‍‍‍```python
'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
),
```
را در تنظیمات DRF اضافه کردم

سپس در url.py
``` python
path("api/token/", TokenObtainPairView.as_view()),
path("api/token/refresh/", TokenRefreshView.as_view()),
```
را اضافه کردم تا ادرس های ساخت توکن و رفرش کردن ان را اضافه کرده باشم

سپس در بخش تنظیمات swagger در فایل settings.py
تنظیمات authorization رو انجام دادم

ظاهرا برای اعمال permision برای دسترسی به یک view صرفا کافیست permission_classes آن کلاس را مشخص کنید و من این کار را کردم.

# Docker

## compose.yaml

برای تنظیم و اجرای پروژه توسط داکر ۳ تا سرویس اصلی تنظیم کردم

اولی وب است که مربوط به اجرای وب سرور پایتون است که در آن قبل از اجرای سرور migration های مربوط به مدل ها انجام می‌شود

دومین سرویس ردیس است که برای اجرای celery مورد نیاز است

و آخرین سرویس celery worker

## Dockerfile

در این فایل پیش نیاز های مروبوط به کتابخانه Pillow نصب می‌شود و سپس کتابخانه های مورد نیاز با کمک requirements.txt نصب می‌شود و سپس سرور اجرا می‌شود


## اجرای پروژه توسط داکر

برای اجرای پروژه توسط داکر کافیست از دستور زیر استفاده کنید

‍‍``` bash
docker compose up --build
```

سپس به ادرس ***http://127.0.0.1:8000*** بروید
