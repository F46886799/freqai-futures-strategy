# پروژه استراتژی (Strategy Project)

پروژه Python با پشتیبانی Docker و WSL2

## 🚀 نصب و راه‌اندازی سریع

### گزینه ۱: Windows (PowerShell)

```powershell
# ایجاد محیط مجازی
python -m venv .venv

# فعال‌سازی محیط مجازی
.\.venv\Scripts\Activate.ps1

# نصب بسته‌ها
pip install -r requirements.txt

# اجرای برنامه
python src/main.py
```

### گزینه ۲: WSL2

```bash
# ایجاد محیط مجازی
python3 -m venv .venv

# فعال‌سازی محیط مجازی
source .venv/bin/activate

# نصب بسته‌ها
pip install -r requirements.txt

# اجرای برنامه
python src/main.py
```

### گزینه ۳: Docker

```bash
# ساخت و اجرا با Docker Compose
docker-compose up --build

# اجرا در background
docker-compose up -d

# توقف
docker-compose down
```

## 📁 ساختار پروژه

```
strategy/
├── src/                  # کدهای اصلی
│   ├── __init__.py
│   └── main.py          # نقطه شروع برنامه
├── tests/               # تست‌ها
│   ├── __init__.py
│   └── test_main.py
├── scripts/             # اسکریپت‌های کمکی
│   ├── setup.sh
│   └── run.sh
├── .env.example         # نمونه متغیرهای محیطی
├── .gitignore
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🧪 تست

```bash
# اجرای تست‌ها
pytest

# تست با coverage
pytest --cov=src tests/
```

## 🔧 متغیرهای محیطی

فایل `.env.example` را به `.env` کپی کنید:

```bash
cp .env.example .env
```

## 📝 پیش‌نیازها

- Python 3.10+
- Docker Desktop
- WSL2 (برای Windows)
- Git
