INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bookshelf',
    'relationship_app',
]


# make a backup first
cp LibraryProject/settings.py LibraryProject/settings.py.bak

# insert 'bookshelf', after the line that starts INSTALLED_APPS =
python - <<'PY'
from pathlib import Path
p = Path('LibraryProject/settings.py')
s = p.read_text()
s = s.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [\n    'bookshelf',")
p.write_text(s)
print('Inserted bookshelf into INSTALLED_APPS (backup at LibraryProject/settings.py.bak)')

ALLOWED_HOSTS = ['*']

