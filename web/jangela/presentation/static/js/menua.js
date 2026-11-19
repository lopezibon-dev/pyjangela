// Menua kontsultatu (UC05/UC11): datepicker-a (jQuery UI) + fetch (promesak).
// Laravel-eko menua.js-tik egokitua: $.ajax ordez fetch.
document.addEventListener('DOMContentLoaded', function () {
  const $input = $('#menua_data');
  const url = $input.data('url');
  const OTORDUAK = ['GOSARIA', 'BAZKARIA', 'AFARIA'];
  let azkenData = $input.val(); // Orria gaurko menuekin dator (zerbitzaritik)

  // Datepicker-a euskaraz, astelehenetik hasita
  $input.datepicker({
    dateFormat: 'yy-mm-dd',
    firstDay: 1,
    dayNamesMin: ['Ig', 'Al', 'Ar', 'Az', 'Og', 'Or', 'La'],
    monthNames: [
      'Urtarrila', 'Otsaila', 'Martxoa', 'Apirila', 'Maiatza', 'Ekaina',
      'Uztaila', 'Abuztua', 'Iraila', 'Urria', 'Azaroa', 'Abendua'
    ],
    onSelect: kudeatuDataAldaketa
  });

  // Eskuz idatzitako data (formatua zerbitzarian balidatzen da)
  $input.on('change', function () {
    kudeatuDataAldaketa($input.val());
  });

  $('#aurrekoa').on('click', function () { mugituEguna(-1); });
  $('#hurrengoa').on('click', function () { mugituEguna(1); });

  function mugituEguna(egunak) {
    // Data okerra bada, gaurtik abiatu
    const data = $input.datepicker('getDate') || new Date();
    data.setDate(data.getDate() + egunak);
    $input.datepicker('setDate', data);
    kudeatuDataAldaketa($input.val());
  }

  function kudeatuDataAldaketa(dataTestua) {
    // Eskaera errepikatuak saihestu
    if (dataTestua === azkenData) return;
    azkenData = dataTestua;
    lortuMenuak(dataTestua);
  }

  function lortuMenuak(dataTestua) {
    ezkutatu('#errorea');
    erakutsi('#kargatzen');

    // Asinkronia: fetch + promise (orria birkargatu gabe)
    fetch(url + '?data=' + encodeURIComponent(dataTestua), {
      headers: { 'Accept': 'application/json' }
    })
      .then(function (response) {
        // Erroreen kudeaketa: HTTP erroreak (adib. 400 data okerra)
        if (!response.ok) {
          return response.json()
            .catch(function () { return {}; })
            .then(function (json) {
              throw new Error(json.errorea || 'Errorea menuak kargatzean (' + response.status + ').');
            });
        }
        return response.json();
      })
      .then(function (json) {
        $input.removeClass('is-invalid');
        erakutsi('#menuak');
        eguneratuMenuak(json.menuak);
      })
      .catch(function (errorea) {
        // Erroreen kudeaketa: sare-erroreak (fetch-ek TypeError jaurtitzen du)
        const mezua = errorea instanceof TypeError
          ? 'Ezin izan da zerbitzariarekin konektatu.'
          : errorea.message;
        $input.addClass('is-invalid');
        // Aurreko dataren menuak ez erakutsi errorearekin batera
        ezkutatu('#menuak');
        ezkutatu('#menurik-ez');
        erakutsiErrorea(mezua);
        azkenData = null; // Berriro saiatu ahal izateko
      })
      .finally(function () {
        ezkutatu('#kargatzen');
      });
  }

  function eguneratuMenuak(menuak) {
    let menurikEz = true;
    OTORDUAK.forEach(function (mota) {
      const menua = menuak[mota];
      const txartela = document.getElementById(mota.toLowerCase());
      // XSS saihestu: textContent (inoiz ez innerHTML)
      txartela.querySelector('.deskribapena').textContent = menua ? menua.deskribapena : 'Ez dago menurik';
      txartela.querySelector('.beganoa').textContent = menua ? menua.aukera_beganoa : '-';
      if (menua) menurikEz = false;
    });
    if (menurikEz) erakutsi('#menurik-ez'); else ezkutatu('#menurik-ez');
  }

  function erakutsiErrorea(mezua) {
    // XSS saihestu: textContent
    document.getElementById('errorea').textContent = mezua;
    erakutsi('#errorea');
  }

  function erakutsi(hautatzailea) { $(hautatzailea).removeClass('d-none'); }
  function ezkutatu(hautatzailea) { $(hautatzailea).addClass('d-none'); }
});
