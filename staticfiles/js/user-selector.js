if(document.getElementById('selectroom')) {
    document.getElementById('room').value = document.getElementById('selectroom').options[0].value;

    $(document).ready(function () {
        $('#selectroom').change(function () {
            var value = $(this).val();
            document.getElementById('room').value = value;
            console.log("выбран кабинет " + value);
        });
    });

    $(document).ready(function () {
        $('.js-select2').select2({
            placeholder: "Выберите кабинет",
            maximumSelectionLength: 2,
            language: "ru"
        });
    });
}

