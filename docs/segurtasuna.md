# Segurtasuna

PyJangela-k Django-ren babesak erabiltzen ditu, eta ez du babes-geruza propiorik gehitzen.
Dokumentu honek azaltzen du non eta nola aplikatzen den babes bakoitza proiektu honetan.
Kodean, puntu horiek euskarazko iruzkinekin markatuta daude (adib. `# XSS saihestu: ...`), defentsan erraz aurkitzeko.

| Arriskua | Babesa | Non |
|---|---|---|
| Pasahitzak lapurtzea | Hash-a (PBKDF2), inoiz ez testu arrunta | `ErabiltzaileaManager` |
| Baimenik gabeko sarbidea | Saioa + rola, dekoratzailearekin | `decorators.py` |
| XSS | Autoescape (txantiloiak) eta `textContent` (JS) | `templates/`, `menua.js` |
| CSRF | `CsrfViewMiddleware` + `{% csrf_token %}` | `settings.py`, formularioak |
| SQL injection | ORM-a (kontsulta parametrizatuak) | `services/`, `forms.py` |
| Sekretuak errepoan | `.env` (Git-etik kanpo) | `settings.py` |

## Autentifikazioa

- Saioa **emailarekin** hasten da, Django-ren `LoginView`-arekin eta formulario propio batekin
  ([`forms.py`](../web/jangela/presentation/forms.py), `SaioaHasiForm`).
- Pasahitzak **hash** moduan gordetzen dira (1. araua): `set_password()` erabiltzen da beti.
- Erabiltzaile **inaktiboek** (`is_active = False`) ezin dute saioa hasi (19. araua). Django-k
  berak blokeatzen ditu, eta formularioak mezu argia ematen du pasahitza zuzena bada.
- **Logout-ak POST soilik** onartzen du (`LogoutView`), CSRF tokenarekin: esteka batek ezin du saioa itxi.

## Baimenak (rolak)

Bista bakoitzak behar dituen rolak adierazten ditu:

```python
@rola_behar(Rola.IKASLEA, Rola.IRAKASLEA, Rola.SUKALDEA)
def menua_kontsultatu(request):
```

[`rola_behar`](../web/jangela/presentation/decorators.py) dekoratzaileak `login_required` barne hartzen du:

- saiorik gabe → login orrira birbideratzen du;
- beste rol batekin → **403** (`PermissionDenied`).

Laravel-eko rol-middleware-aren baliokidea da, baina bista bakoitzean, eta horrela argi ikusten da nork sar daitekeen.

**Jabetza**: erabiltzaile bakoitzak bere datuak soilik ikusi eta aldatzen ditu (erreserbak, ordainketak).
Zerbitzuan egiaztatzen da, kontsultan bertan erabiltzailea iragaziz:

```python
get_object_or_404(ErreserbaModel, pk=pk, erabiltzailea=request.user)
```

Horrela, beste erabiltzaile baten id-a asmatzen duenak 404 jasotzen du (ez du jakingo existitzen den).
*Erreserba eta ordainketen issue-etan aplikatuko da ([#13](https://github.com/lopezibon-dev/pyjangela/issues/13), [#15](https://github.com/lopezibon-dev/pyjangela/issues/15)).*

`/admin/` kontu tekniko batentzat da (superuser-a), garapen-tresna gisa: ez ditu domeinuko arauak aplikatzen.

## XSS

- **Txantiloiak**: Django-ren autoescape-a aktibo dago beti. Erabiltzailearen datuekin **ez da inoiz `|safe` erabiltzen**.
- **JavaScript**: zerbitzaritik datorren testua `textContent`-rekin idazten da, inoiz ez `innerHTML`-rekin
  ([`menua.js`](../web/jangela/presentation/static/js/menua.js)):

  ```javascript
  txartela.querySelector('.deskribapena').textContent = menua.deskribapena;
  ```

  Horrela, menu baten deskribapenak `<script>` badu ere, testu gisa erakusten da.
- **JSON**: `JsonResponse`-k `Content-Type: application/json` bidaltzen du, eta nabigatzaileak ez du HTML gisa interpretatzen.
  Edukia `textContent`-rekin txertatzen da (goian).

## CSRF

- `CsrfViewMiddleware` aktibo dago, eta POST formulario guztiek `{% csrf_token %}` daramate.
- Datuak aldatzen dituzten ekintzak **POST** bidez bakarrik egiten dira. Adibidez, menua ezabatzeak (UC17)
  GET-ean berrespen-orria erakusten du, eta POST-ean ezabatzen du.
- `fetch` bidezko eskaerentzat, [`base.html`](../web/jangela/presentation/templates/base.html)-k tokena
  `<meta name="csrf-token">`-n uzten du, `X-CSRFToken` goiburuan bidaltzeko. Gaur egungo `fetch` bakarra
  GET da (`/menua/json/`, `@require_GET`), eta ez du ezer aldatzen.
- `XFrameOptionsMiddleware`-k clickjacking-a saihesten du (orria ezin da beste gune baten `<iframe>`-ean kargatu).

## SQL injection

Kontsulta guztiak **ORM**-arekin egiten dira; Django-k parametrizatzen ditu. Ez dago SQL gordinik.

```python
MenuaModel.objects.filter(menua_data=data)
```

## Sarreren balidazioa

- **Formularioak** (`forms.py`): eremu motak eta derrigorrezkoak. Zerbitzuak `cleaned_data` soilik jasotzen du.
- **JSON bistak**: parametroak esplizituki balidatzen dira. Adibidez, `?data=` okerra bada → **400** eta errore-mezua JSON-ean.
- **Datu-basea**: `UniqueConstraint` eta `CheckConstraint` azken babes gisa ([uml-diagrama.md](uml-diagrama.md#arauak-ereduan)).

Xehetasun gehiago: [arkitektura.md](arkitektura.md#non-balidatzen-da-zer).

## Konfigurazioa eta sekretuak

- Errepoa **publikoa** da: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` eta DBko kredentzialak `.env`-etik irakurtzen dira
  (`python-dotenv`), eta `.env` ez dago Git-en. Txantiloia: [`web/.env.example`](../web/.env.example).
- `DEBUG`-ek **`False`** du lehenetsita: `.env`-ean `DEBUG=True` ez badago, ez da errore-xehetasunik erakusten.
- Demo datuak (`seed_demo`) **asmatuak** dira: ez dago benetako daturik errepoan.
- Ekoizpenean (Docker), Apache-k zerbitzatzen du aplikazioa `DEBUG=False`-rekin. Ikus [instalazioa.md](instalazioa.md).
