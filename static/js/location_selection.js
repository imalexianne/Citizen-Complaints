

function showStep(step) {
    document.querySelectorAll('.form-part').forEach(part => part.classList.remove('active'));
    document.getElementById('step' + step).classList.add('active');
}


function showStep(step) {
    document.querySelectorAll('.form-part').forEach(part => part.classList.remove('active'));
    document.getElementById('step' + step).classList.add('active');
}

$(function () {
    $('#province').change(function () {
        let provinceID = $(this).val();
        $.get('/ajax/get-districts/', { province_id: provinceID }, function (data) {
            $('#district').html('<option value="">Select District</option>');
            data.forEach(d => $('#district').append(`<option value="${d.id}">${d.name}</option>`));
            $('#sector, #cell, #village').html('<option value="">Select</option>');
        });
    });

    $('#district').change(function () {
        let districtID = $(this).val();
        $.get('/ajax/get-sectors/', { district_id: districtID }, function (data) {
            $('#sector').html('<option value="">Select Sector</option>');
            data.forEach(s => $('#sector').append(`<option value="${s.id}">${s.name}</option>`));
            $('#cell, #village').html('<option value="">Select</option>');
        });
    });

    $('#sector').change(function () {
        let sectorID = $(this).val();
        $.get('/ajax/get-cells/', { sector_id: sectorID }, function (data) {
            $('#cell').html('<option value="">Select Cell</option>');
            data.forEach(c => $('#cell').append(`<option value="${c.id}">${c.name}</option>`));
            $('#village').html('<option value="">Select</option>');
        });
    });

    $('#cell').change(function () {
        let cellID = $(this).val();
        $.get('/ajax/get-villages/', { cell_id: cellID }, function (data) {
            $('#village').html('<option value="">Select Village</option>');
            data.forEach(v => $('#village').append(`<option value="${v.id}">${v.name}</option>`));
        });
    });
});

