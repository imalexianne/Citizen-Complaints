
$(document).ready(function () {
  // Province → District
  $('#id_province').change(function () {
    var provinceId = $(this).val();
    $.get('/ajax/get-districts/', { province_id: provinceId }, function (data) {
      var districtSelect = $('#id_district');
      districtSelect.empty();
      districtSelect.append('<option value="">---------</option>');
      $.each(data, function (index, item) {
        districtSelect.append(new Option(item.name, item.id));
      });
      $('#id_sector, #id_cell, #id_village').empty().append('<option value="">---------</option>');
    });
  });

  // District → Sector
  $('#id_district').change(function () {
    var districtId = $(this).val();
    $.get('/ajax/get-sectors/', { district_id: districtId }, function (data) {
      var sectorSelect = $('#id_sector');
      sectorSelect.empty();
      sectorSelect.append('<option value="">---------</option>');
      $.each(data, function (index, item) {
        sectorSelect.append(new Option(item.name, item.id));
      });
      $('#id_cell, #id_village').empty().append('<option value="">---------</option>');
    });
  });

  // Sector → Cell
  $('#id_sector').change(function () {
    var sectorId = $(this).val();
    $.get('/ajax/get-cells/', { sector_id: sectorId }, function (data) {
      var cellSelect = $('#id_cell');
      cellSelect.empty();
      cellSelect.append('<option value="">---------</option>');
      $.each(data, function (index, item) {
        cellSelect.append(new Option(item.name, item.id));
      });
      $('#id_village').empty().append('<option value="">---------</option>');
    });
  });

  // Cell → Village
  $('#id_cell').change(function () {
    var cellId = $(this).val();
    $.get('/ajax/get-villages/', { cell_id: cellId }, function (data) {
      var villageSelect = $('#id_village');
      villageSelect.empty();
      villageSelect.append('<option value="">---------</option>');
      $.each(data, function (index, item) {
        villageSelect.append(new Option(item.name, item.id));
      });
    });
  });
});
