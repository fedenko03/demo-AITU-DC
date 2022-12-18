step1 = document.getElementById('step1');
step2a = document.getElementById('step2a');
step2b = document.getElementById('step2b');
step3a = document.getElementById('step3a');
step4a = document.getElementById('step4a');
step5a = document.getElementById('step5a');

document.getElementById('btn_step1a').addEventListener('click', function () {
    if (!step1.classList.contains('hidden_step')) {
        step1.classList.add('hidden_step');
        step2a.classList.remove('hidden_step');
        document.querySelector('#btn_step1a').disabled = true
        document.querySelector('#btn_step1b').disabled = true
    }
});

document.getElementById('btn_step2a').addEventListener('click', function () {
    if (!step2a.classList.contains('hidden_step')) {
        step2a.classList.add('hidden_step');
        step3a.classList.remove('hidden_step');
        document.querySelector('#btn_step2a').disabled = true;
        data.room = document.querySelector('#chosedroom_confirm').innerText;
    }
});

document.getElementById('btn_step3a').addEventListener('click', function () {
    if (!step3a.classList.contains('hidden_step')) {
        step3a.classList.add('hidden_step');
        step4a.classList.remove('hidden_step');
    }
});

document.getElementById('btn_step4a').addEventListener('click', function () {
    if (!step4a.classList.contains('hidden_step')) {
        step4a.classList.add('hidden_step');
        step5a.classList.remove('hidden_step');
        document.querySelector('#btn_step4a').disabled = true;
        data.fullname = document.querySelector('#fullname_step4').value;

        let user = "";
        
        if (document.getElementById('professor').checked) {
            data.status = "professor";
            user = "Преподаватель";
        } else if(document.getElementById('student').checked) {
            data.status = "student";
            user = "Студент";
        } else {
            data.status = "other";
            user = "Пользователь";
        }

        document.querySelector('#total_steps').innerHTML = user + " " + data.fullname + " взял ключ от кабинета " + data.room;
        document.querySelector('#date_steps').innerHTML = new Date().toLocaleString();
    }
});

function check_filled() {
    if (document.getElementById("fullname_step4").value != '') {
        document.querySelector('#btn_step4a').disabled = false;
    } else {
        document.querySelector('#btn_step4a').disabled = true;
    }
}
