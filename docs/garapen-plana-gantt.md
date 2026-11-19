# PyJangela — Garapen-plana (Gantt)

Garapenaren denbora-estimazioa, milestone eta issue-en arabera antolatuta.
Estimazio bat da: ez du zertan bete. Garapenaren egoera GitHub Projects-eko issue-en egoeran jarraitzen da.

```mermaid
gantt
    title PyJangela — Garapen-plana (estimazioa)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m

    section Analisia
    Analisia eta diseinua (Laravel → Django)          :an, 2026-11-05, 2d

    section Oinarria
    #3 Proiektuaren hasierako konfigurazioa            :i3, after an, 1d
    #4 seed_demo minimoa                                :i4, after i3, 1d
    #5 base.html responsive                             :i5, after i4, 1d
    #6 Login/logout eta rolaren araberako dashboarda    :i6, after i5, 1d
    Oinarria                                            :milestone, m1, after i6, 0d

    section Menuak
    #11 Menuen CRUDa (UC15–UC17)                        :i11, after i6, 1d
    #12 Menua kontsultatu, fetch (UC05/UC11)            :i12, after i11, 1d
    Menuak                                              :milestone, m2, after i12, 0d

    section Erreserbak
    #13 Erreserba puntualak (UC08–UC10)                 :i13, after i12, 2d
    #14 Ikasturteko erreserba (UC20)                    :i14, after i13, 1d
    Erreserbak                                          :milestone, m3, after i14, 0d

    section Profila, ordainketak eta komensalak
    #15 Profila eta ordainketak (UC03, UC04/UC12)       :i15, after i14, 1d
    #16 Komensalak eta estatistikak (UC13/UC14)         :i16, after i15, 1d
    MVP                                                 :milestone, m4, after i16, 0d

    section Itxiera
    Dokumentazioa (docs/)                               :dk, after i16, 1d
    Docker (web + db)                                   :dc, after i16, 1d
    CI (GitHub Actions)                                 :ci, after dc, 1d
    Azken frogak                                        :fr, after dc, 1d
```
