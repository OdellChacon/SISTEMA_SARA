# Sistema SARA

Sistema web de control de asistencia docente, horarios y asignación de aulas para la **UPTAIET** (Universidad Politécnica Territorial Agroindustrial del Estado Táchira).

## El problema

La planificación de horarios y aulas se armaba a mano cada período, y la asistencia de los docentes se controlaba en papel. No había una forma rápida de ver qué clases se dieron y cuáles no.

## Qué hace

- **Docentes:** registro de docentes y administradores, con autenticación propia.
- **Materias y aulas:** catálogo de materias y aulas disponibles.
- **Clases y horarios:** asignación de docente, materia, aula y bloque horario, con vista de calendario.
- **Asistencia:** registro de asistencia por clase y listado de incumplimientos.
- **Dashboard:** resumen general y configuración del sistema.

## Stack

- **Backend:** Python, Django
- **Base de datos:** PostgreSQL (configurada por `DATABASE_URL`)
- **Frontend:** plantillas de Django, TailwindCSS (crispy-tailwind), JavaScript
- **Despliegue:** Procfile listo para plataformas tipo Heroku/Render

## Estructura

```
SARA/        configuración del proyecto
dashboard/   panel principal y configuración
docentes/    docentes, administradores y autenticación
materias/    materias
aulas/       aulas
clases/      clases, calendario, asistencias e incumplimientos
```

## Correr en local

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # define DATABASE_URL
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

Desarrollado por [Odell Chacón](https://github.com/OdellChacon).
