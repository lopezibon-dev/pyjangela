# PyJangela — CLAUDE.md (fuente única de contexto)

> Este es el **único documento de contexto** del proyecto. Lo leen Claude Code y todos los chats del proyecto de claude.ai.
> Si otro documento lo contradice, **prevalece CLAUDE.md**. Cuando cambie, se vuelve a subir a las fuentes del proyecto.

## Objetivo y alcance
Proyecto educativo: migrar la aplicación web Ikastetxeko Jangela (comedor de un centro educativo) de Laravel/PHP a Python/Django.
Debe cumplir las rúbricas de evaluación (`docs-internos/ebaluazioa.md`).
Se mantienen los requisitos y los casos de uso web documentados (UC01–UC20). **No inventar flujos, requisitos, entidades, reglas, tablas ni APIs que no estén documentados.**

## Tecnologías
- Python + Django; MySQL 8.4.
- Proyecto Django en `web/`, configuración en `config/` y una única app: `jangela`.
- Frontend responsive: HTML/CSS/Bootstrap 5 (CDN)/JavaScript. Asincronía con `fetch` + promises; jQuery solo para el datepicker.
- Configuración con variables de entorno desde `.env` (`python-dotenv`): `SECRET_KEY`, `DEBUG` y la BD (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`). Plantilla en `.env.example`.

## Entornos y despliegue
- Desarrollo: sin Docker. `runserver`, MySQL local y Python local. Sin Apache ni XAMPP.
- Producción/MVP (más adelante): Docker Compose con dos contenedores, `web` (Apache + mod_wsgi + Django) y `db` (MySQL 8). No usar Gunicorn. `DB_HOST=db` en Docker y `localhost` en local.
- CI con GitHub Actions: previsto, sin definir todavía.
- Gestión: GitHub Projects (Kanban) + issues. El diagrama de Gantt (Mermaid) se generará al final, a partir de los issues reales.

## Principios de trabajo
- **Sin overengineering**: usar la solución más simple que funcione. Prioridad: claridad educativa y rapidez de desarrollo.
- Aplicar buenas prácticas (SRP, código legible, funciones cortas) solo mientras no añadan complejidad. **La simplicidad tiene prioridad.**
- El objetivo son las rúbricas: el código tiene que poder explicarse fácilmente en la defensa.
- No añadir capas, patrones, frameworks, apps Django ni abstracciones sin preguntar antes.
- No cambiar las reglas de negocio por cambiar de tecnología.
- **Respetar lo ya decidido** ("Decisiones tomadas"). No mover ni rehacer código que funciona; si algo parece mejorable, proponerlo primero.
- Si hay dudas, incoherencias o una decisión no trivial: **preguntar antes de actuar**. `docs-internos/` puede tener información desfasada.

## Idioma y nombres
- Comunicación con el usuario: en **castellano**.
- Carpetas y módulos técnicos: en inglés (`services/`, `dto/`, `views.py`). Lo que impone Django se deja como está.
- Clases, entidades, atributos y métodos de dominio: en **euskera**, por ejemplo `lortuEgunekoMenuak`. Entidades en singular.
- Se combinan con términos en inglés cuando es lo habitual:
  - sufijos técnicos: `MenuaService`, `ErabiltzaileaForm`
  - operaciones CRUD y términos universales: `update`, `delete`, `create`, `list`
- Comentarios y docstrings: en euskera, breves.
- Commits, PR, issues y todo lo de Git/GitHub: en euskera.
- La documentación del repo (`docs/`): en euskera, en Markdown; diagramas en Mermaid.

## Arquitectura (aplanada)
Flujo: **view (`presentation/`) → servicio (`application/services/`) → modelo ORM**.
- **No se usa el patrón Repository**, ni contratos con `Protocol`, ni entidades de dominio aparte: el ORM de Django hace ese papel, y los modelos ORM son las entidades.
- **No DDD, no agregados, no aggregate roots.**
- Los servicios contienen la lógica de negocio y usan el ORM directamente. Usan `with transaction.atomic():` cuando un caso de uso necesita atomicidad (por ejemplo, la regla 21). Sin Unit of Work ni abstracciones transaccionales propias.
- Las views son finas: reciben la petición, validan con el Form, llaman al servicio y renderizan la plantilla o devuelven JSON.
- **DTO**: el Django Form hace de DTO de entrada. En `application/dto/` solo van `@dataclass` sencillas para lecturas ricas (joins, por ejemplo `ErreserbaInfoDto`), y solo cuando un caso de uso lo necesite. No crear un DTO si basta con un parámetro simple.
- Plantillas: un único `base.html` (menú Bootstrap condicional según público/rol) y carpetas `ikaslea/`, `irakaslea/` y `sukaldea/`.
- **Dashboard según el rol, no según `egoiliarra`**: IKASLEA → dashboard de IKASLEA (sea residente o no); IRAKASLEA → el suyo; SUKALDEA → el suyo.
- **Profila (UC03)**: enlace en el menú de todos los roles; la misma página para todos.
- **Menua (UC05/UC11)**: enlace "Menua" en el menú de todos los roles; la misma página de consulta para todos (SUKALDEA también, además de su CRUD "Menuak").
- `rola_behar(*rolak)` acepta uno o varios roles.
- **Menú de IKASLEA**: un bloque IKASLEA con los enlaces comunes (Menua, Ordainketak, Profila) y, dentro, `{% if user.ikaslea.egoiliarra %}` para lo excluyente: el residente ve su IkasturtekoErreserba (UC20); el no residente ve las reservas puntuales (UC08–UC10).
- Control de acceso por rol: con decoradores en las views (el equivalente al middleware de rol de Laravel).

### Estructura de carpetas
```text
pyjangela/                 # Git-en erroa
├── .gitignore
├── CLAUDE.md
├── README.md
├── docs/                  # errepoko dokumentazioa (euskaraz)
├── docs-internos/         # ez da Git-era igotzen (garapen-egunkaria.md, egoera.md, ...)
└── web/
    ├── manage.py
    ├── requirements.txt
    ├── .env               # ez da Git-era igotzen
    ├── .env.example
    ├── jangela.bat        # karpeta-egitura birsortzeko; ez da Git-era igotzen
    ├── config/            # settings.py, urls.py, asgi.py, wsgi.py
    └── jangela/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py      # ORM modeloak inportatzen ditu
        ├── migrations/
        ├── domain/
        │   └── enums/     # Enum puruak (str, Enum), bat fitxategiko
        ├── application/
        │   ├── services/  # negozio-logika (ORM zuzenean)
        │   └── dto/       # irakurketa aberatsetarako @dataclass-ak soilik
        ├── infrastructure/
        │   └── persistence/
        │       └── models/  # ORM modeloak, bat fitxategiko + choices.py
        ├── management/
        │   └── commands/  # seed_demo.py
        └── presentation/
            ├── views.py   # edo views/ikaslea.py, views/sukaldea.py, ...
            ├── forms.py
            ├── urls.py
            ├── static/    # js/menua.js, css/
            └── templates/ # TEMPLATES["DIRS"]-en gehituta
                ├── base.html
                ├── ikaslea/
                ├── irakaslea/
                └── sukaldea/
```

## Decisiones tomadas (ya implementadas: no cambiar sin preguntar)
- **Usuario**: `ErabiltzaileaModel` hereda de `AbstractUser`. `AUTH_USER_MODEL = "jangela.ErabiltzaileaModel"`. Login por email (`USERNAME_FIELD = "email"`).
  - Mapeo dominio → Django: `izena→first_name`, `abizenak→last_name`, `aktiboa→is_active`, `sortze_data→date_joined`, `pasahitza_hash→password`.
  - El superuser es una cuenta técnica (solo para `/admin/`). `is_staff`/`is_superuser` y `rola` son ejes independientes: no existe un rol `ADMIN`.
- **Claves primarias**: `id` automático de Django en todos los modelos.
- **Enums**: `Enum` puros `(str, Enum)` en `domain/enums/`, uno por archivo, como fuente única de valores. Los modelos **no usan `TextChoices`**: generan los `choices` con `enum_choices()` de `infrastructure/persistence/models/choices.py`.
- **Modelos ORM**: en `infrastructure/persistence/models/`, uno por archivo. `jangela/models.py` los importa explícitamente para que Django genere las migraciones.
- **Relaciones**: las 0..1 son `OneToOneField`. `on_delete`: `PROTECT` en todas las relaciones (`Ikaslea`, `IkasturtekoErreserba`, `Erreserba` y `Ordainketa`).
- `zenbatekoa`: `DecimalField(max_digits=8, decimal_places=2)`.
- `UrtekoErreserba` se renombró a `IkasturtekoErreserba`: es una reserva permanente para todo el curso (ni mensual ni semanal). El cobro está en `Ordainketa`.
- Settings: `TIME_ZONE = "Europe/Madrid"`, `USE_TZ = True`, `LANGUAGE_CODE = "eu"`.
- El admin de Django no aplica las reglas de dominio: es una herramienta de desarrollo.
- **Parámetros de negocio** (horas límite, precios): constantes en `settings.py`, no en la BD (no hay entidad de configuración).

## Dominio
Entidades: `Erabiltzailea`, `Ikaslea`, `IkasturtekoErreserba`, `Erreserba`, `Ordainketa`, `Menua`.

Enumeraciones:
- `Rola`: `IKASLEA`, `IRAKASLEA`, `SUKALDEA`.
- `OtorduMota`: `GOSARIA`, `BAZKARIA`, `AFARIA`.
- `ErreserbaEgoera`: `AKTIBOA`, `EZEZTATUA`.
- `OrdainketaEgoera`: `ORDAINTZEKE`, `ORDAINDUTA`.
- `OrdainketaMota`: `HILEKOA`, `ALDIZKAKOA`.

### Relaciones
`Erabiltzailea`–`Ikaslea`; `Ikaslea`–`IkasturtekoErreserba`; `Erabiltzailea`–`Erreserba`; `Erabiltzailea`–`Ordainketa`; `Erreserba`–`Ordainketa`. `Menua` no tiene ninguna relación directa.
`Ikaslea`–`IkasturtekoErreserba` es 1:0..1: opcional desde `Ikaslea` y obligatoria desde `IkasturtekoErreserba` (en Mermaid: `||--o|`).

### Reglas de negocio
1. Email único; las contraseñas se guardan como hash.
2. Cada usuario tiene un único rol.
3. Un usuario con rol `IKASLEA` tiene un registro `Ikaslea`; los demás roles no.
4. Solo los estudiantes residentes (`egoiliarra = true`) pueden tener `IkasturtekoErreserba`.
5. Una reserva se crea o se cancela al menos 24 horas antes de la hora límite del tipo de comida. Las horas límite son parámetros configurados por la administración, en `settings.py` (`ORDU_MUGAK`: `GOSARIA` 08:00, `BAZKARIA` 13:00, `AFARIA` 20:00).
6. Comensales del día = reservas anuales aplicables + reservas puntuales activas. Solo cuentan los usuarios activos (`aktiboa = true`): los inactivos ya no participan en el centro.
7. Todo pago pertenece a un usuario.
8. `ALDIZKAKOA` requiere `erreserba_id`; `HILEKOA` no requiere reserva (`erreserba_id = NULL`).
9. `ORDAINDUTA` requiere fecha de pago; `ORDAINTZEKE` requiere que la fecha de pago sea nula.
10. Todo pago tiene fecha de creación.
11. Solo hay un menú por cada combinación de fecha y tipo de comida.
12. Los alumnos residentes (`egoiliarra = true`) personalizan su `IkasturtekoErreserba` y no hacen reservas puntuales. El resto de usuarios que reservan (`IKASLEA` no residente, `IRAKASLEA`) solo hacen reservas puntuales.
13. `IkasturtekoErreserba` configura la agenda semanal por conjunción: las `OtorduMota` marcadas se aplican a los días marcados (día ∧ comida). Se usan 10 booleanos: `gosaria`, `bazkaria`, `afaria`, `astelehena`, `asteartea`, `asteazkena`, `osteguna`, `ostirala`, `larunbata`, `igandea`. No se permiten combinaciones que necesiten 21 booleanos (una celda día×comida independiente).
14. El plazo de 24 horas (regla 5) se aplica solo a las reservas puntuales. Modificar `IkasturtekoErreserba` no tiene plazo ni versionado en el MVP.
15. La vigencia de `IkasturtekoErreserba` es implícita (por ejemplo, el curso de septiembre a junio). No hay campo de año ni histórico.
16. Los usuarios pueden indicar su preferencia por el menú vegano con `Erabiltzailea.beganoa` (booleano), sea cual sea su rol.
17. Cada `Menua` tiene `deskribapena` (menú estándar) y `aukera_beganoa` (menú vegano). Las dos son obligatorias y siempre tienen texto; `aukera_beganoa` puede coincidir con `deskribapena`.
18. UC14 muestra, por día y `OtorduMota`, el total de comensales y cuántos tienen preferencia vegana. Es la suma de las reservas puntuales activas (vía `Erabiltzailea.beganoa`) y las reservas anuales aplicables (vía `Ikaslea` → `Erabiltzailea.beganoa`). Solo usuarios activos (regla 6). UC13 reutiliza el mismo cálculo para la fecha de hoy.
19. Un `Erabiltzailea` con `aktiboa = false` no puede iniciar sesión.
20. Procesar pagos queda fuera del MVP: al crear una reserva se genera un `Ordainketa` `ALDIZKAKOA` en estado `ORDAINTZEKE`; el paso a `ORDAINDUTA` no se detalla. El importe sale del precio del tipo de comida, en `settings.py` (`PREZIOAK`: `GOSARIA` 4,00 €, `BAZKARIA` 8,00 €, `AFARIA` 8,00 €).
21. Al cancelar una reserva puntual (UC09), su `Erreserba` pasa a `EZEZTATUA` y se elimina el `Ordainketa` asociado (dentro de `transaction.atomic()`). En el MVP ese pago siempre está en `ORDAINTZEKE` (regla 20).
22. Un usuario no puede tener dos reservas puntuales `AKTIBOA` para la misma fecha y `OtorduMota` (sí puede volver a reservar una que canceló). Se comprueba dos veces: en el servicio (mensaje claro al usuario) y en la BD con una restricción única, como guarda final (también ante peticiones simultáneas).

### Casos de uso web
- **Todos los roles**: UC03 ver perfil (la misma página para todos; incluye la preferencia de menú vegano). Solo lectura.
- **Consultar menú (UC05/UC11)**: una sola página de solo lectura (`/menua/`, datepicker + `fetch`) para todos los roles: IKASLEA, IRAKASLEA y también SUKALDEA. Sin sesión no se entra.
- **Estudiantes residentes**: UC01 login (carga el dashboard de IKASLEA), UC02 logout, UC03 ver perfil, UC04 consultar pagos, UC05 consultar menú (estándar y vegano), UC20 ver y editar su `IkasturtekoErreserba` (reglas 12–15: 10 booleanos, sin plazo ni versionado). Si todavía no tiene `IkasturtekoErreserba`, el formulario sale con todos los campos marcados por defecto y el registro se crea al guardar.
- **Otros usuarios** (estudiantes no residentes / profesores): UC06 login (el IKASLEA no residente carga el dashboard de IKASLEA; el IRAKASLEA, el de IRAKASLEA), UC07 logout, UC03 ver perfil, UC08 crear reserva, UC09 cancelar reserva, UC10 ver mis reservas, UC11 consultar menú (estándar y vegano), UC12 consultar pagos.
- **Personal de cocina**: UC13 ver comensales del día (dashboard: `/sukaldea/dashboard`), UC14 ver estadísticas de los próximos días (`/sukaldea/estatistikak`, con selector de fecha), UC15 crear menú (descripción estándar y vegana, las dos obligatorias), UC16 actualizar menú (ídem), UC17 eliminar menú, UC18 login (carga el dashboard de SUKALDEA), UC19 logout, UC03 ver perfil.
- UC13 y UC14 comparten la lógica de cálculo de comensales: UC13 la aplica a hoy, en el dashboard; UC14 a cualquier fecha, con un selector (widget de jQuery), en su propia página.

## Validación (aplicar en todos los issues)
- **Entrada**: usar Django Forms, o validación explícita en las views que devuelven JSON. Las plantillas usan autoescape: no usar nunca `|safe` con datos del usuario. Las llamadas con `fetch` también envían el token CSRF (cabecera `X-CSRFToken`).
- **Negocio**: las reglas y la comprobación de propiedad (cada usuario solo ve y edita lo suyo) van en el servicio. Por ejemplo, `get_object_or_404(Modelo, pk=pk, erabiltzailea=request.user)`.
- **Datos**: usar el ORM. Poner restricciones (`unique`, FK) solo cuando la regla lo exija. SQL raw solo si es imprescindible, y siempre parametrizado.
- Señalar con comentarios en euskera los puntos que se evalúan, para encontrarlos rápido en la defensa. Por ejemplo:
  - `# Sarreren balidazioa (formularioa)`
  - `# XSS saihestu: autoescape / ihes egitea`
  - `# SQL injection saihestu: ORM / parametrizazioa`
  - `# Negozio-araua: erabiltzaileak bere datuak soilik`
  - en JS: `// Asinkronia: fetch + promise`

## Proyecto Laravel de referencia (`C:\dev\jangela\web`)
- No analizarlo entero. Consultar solo archivos concretos cuando un issue lo indique (por ejemplo, `resources/js/menua.js` y su CSS en UC05/UC11).
- Ignorar los agregados, lo de DDD y los repositorios. Allí no existe el menú vegano.
- En `menua.js`: sustituir `$.ajax`/XHR por `fetch` + promises, pero mantener el datepicker de jQuery.

## Datos demo
- Referencia de Laravel: `docs-internos/sql-laravel/` (esquema, inserts y actualización de fechas). No se ejecutan: solo sirven como referencia para los datos demo.
- Los datos demo se generan con el comando `python manage.py seed_demo`: fechas relativas a hoy, idempotente (borra y vuelve a crear), y solo datos ficticios (el repo es público).
- Cuando llegue ese issue, proponer qué datos extra merece la pena añadir y esperar la aprobación del usuario.

## Flujo git y GitHub
- Un issue = una rama `tipo/N-descripcion` (feat, fix, chore, docs), creada desde `main` actualizado.
- Al empezar un issue, pasar su tarjeta a *In Progress* en el Project.
- Commits pequeños y con un mensaje claro (en euskera).
- Al terminar: push de la rama y PR con `Closes #N`.
- **Nunca hacer push ni merge a `main`**: el merge (rebase/fast-forward) lo hace el usuario.

## Al final de cada sesión
1. Actualizar `docs-internos/egoera.md`: Estado actual, Decisiones, Pendiente.
2. Proponer una entrada para `docs-internos/garapen-egunkaria.md` (fuera del repo, por ahora), imitando el idioma y el estilo de las entradas existentes. Añadirla solo cuando el usuario la apruebe.
3. Si ha cambiado CLAUDE.md, recordar al usuario que lo vuelva a subir a las fuentes del proyecto de claude.ai.