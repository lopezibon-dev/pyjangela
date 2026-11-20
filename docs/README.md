# PyJangela — Dokumentazioa

Ikastetxeko jangela kudeatzeko aplikazioaren diseinua, arkitektura eta instalazioa.
Proiektuaren aurkezpena [erroko README-an](../README.md) dago.

## Diseinua eta arkitektura

| Dokumentua | Edukia |
|---|---|
| [Arkitektura](arkitektura.md) | Geruzak, MVC/MVT-rekin duten lotura eta non balidatzen den zer |
| [UML diagrama](uml-diagrama.md) | Domeinuko entitateak, enumak eta erlazioak |
| [Erabilera-kasuak](erabilera-kasuak.md) | UC01–UC20 rolaren arabera, bakoitza bere issue-arekin |
| [Segurtasuna](segurtasuna.md) | Autentifikazioa, rolak, XSS, CSRF, SQL injection eta sekretuak |

## Instalazioa eta garapena

| Dokumentua | Edukia |
|---|---|
| [Instalazioa](instalazioa.md) | Instalazio klasikoa (`runserver`) eta Docker bidezkoa (Apache + MySQL) |
| [Garapen-plana (Gantt)](garapen-plana-gantt.md) | Milestone eta issue-en denbora-estimazioa |

## Irakurtzeko ordena gomendatua

1. [Erabilera-kasuak](erabilera-kasuak.md): aplikazioak **zer** egiten duen.
2. [UML diagrama](uml-diagrama.md): **zein** datu kudeatzen dituen.
3. [Arkitektura](arkitektura.md): **nola** dagoen antolatuta kodea.
4. [Segurtasuna](segurtasuna.md): **nola** babesten den.
