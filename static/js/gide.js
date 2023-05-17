var mode = 1;
var step = 1;
var last_step = 6;

const button1 = document.getElementById('mode1');
const button2 = document.getElementById('mode2');
const button3 = document.getElementById('mode3');

function hideAllElems() {
    document.getElementById('mc-text1').style.display = 'none';
    document.getElementById('mc-text2').style.display = 'none';
    document.getElementById('image1-step').style.display = 'none';
    document.getElementById('image2-step').style.display = 'none';
    document.getElementById('image3-step').style.display = 'none';
}

function Mode1() { // Как взять ключ
    mode = 1;
    button1.className = 'modal-button active-button';
    button2.className = 'modal-button';
    button3.className = 'modal-button';
    last_step = 6;
    m1_s1();
}

function m1_s1() {
    step = 1;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 1';
    document.getElementById('mc-text1').textContent = 'Выберите действие “Взять ключ” на главной странице.';
    document.getElementById('image1-step').src = staticUrl + 'img/' + 'gide/1/step1.png';
    document.getElementById('image1-step').style.height = '280px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button inactive';
    document.getElementById('next-btn').className = 'step-button';
    document.getElementById('prev-btn').onclick = m1_s1;
    document.getElementById('next-btn').onclick = m1_s2;
}

function m1_s2() {
    step = 2;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 2';
    document.getElementById('mc-text1').textContent = 'Выберите нужный кабинет, используя поиск либо интерактивную карту университета.';
    document.getElementById('mc-text2').textContent = 'Чтобы перейти к следующему шагу, нажмите кнопку “Далее” внизу экрана.';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/1/step2-1.png';
    document.getElementById('image2-step').src =  staticUrl + 'img/' + 'gide/1/step2-2.png';
    document.getElementById('image3-step').src =  staticUrl + 'img/' + 'gide/1/step2-3.png';

    document.getElementById('image1-step').style.height = '170px';
    document.getElementById('image2-step').style.height = '170px';
    document.getElementById('image3-step').style.height = '120px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('mc-text2').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';
    document.getElementById('image2-step').style.display = 'block';
    document.getElementById('image3-step').style.display = 'block';


    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button';
    document.getElementById('prev-btn').onclick = m1_s1;
    document.getElementById('next-btn').onclick = m1_s3;
}

function m1_s3() {
    step = 3;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 3';
    document.getElementById('mc-text1').textContent = 'Попросите пользователя отсканировать QR-код через своё устройство для подтверждения взятия ключа.';
    document.getElementById('mc-text2').textContent = 'Также вы можете ввести данные пользователя вручную, нажав на кнопку “Ввести данные вручную”';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/1/step3.png';

    document.getElementById('image1-step').style.height = '250px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('mc-text2').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').onclick = m1_s2;
    document.getElementById('next-btn').onclick = m1_s4;
}

function m1_s4() {
    step = 4;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 4';
    document.getElementById('mc-text1').textContent = 'Если вы выбрали “Ввести данные вручную”, то следующий шаг - заполнить все поля и нажать кнопку “Подтвердить”';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/1/step4.png';

    document.getElementById('image1-step').style.height = '290px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').onclick = m1_s3;
    document.getElementById('next-btn').onclick = m1_s5;
}

function m1_s5() {
    step = 5;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 5';
    document.getElementById('mc-text1').textContent = 'Если пользователь подтвердил заявку по QR  ИЛИ администратор вручную ввел все данные и нажал кнопку “Подтвердить”, то в случае успеха появится следующее окно:';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/1/step5.png';

    document.getElementById('image1-step').style.height = '290px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';


    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button';
    document.getElementById('prev-btn').onclick = m1_s4;
    document.getElementById('next-btn').onclick = m1_s6;
}

function m1_s6() {
    step = 6;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 6';
    document.getElementById('mc-text1').textContent = 'Если возникла ошибка, то будет показано следующее:';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/1/step6.png';

    document.getElementById('image1-step').style.height = '290px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button inactive';
    document.getElementById('prev-btn').onclick = m1_s5;
    document.getElementById('next-btn').onclick = m1_s6;
}

///////////////////////

function Mode2() { // Как вернуть ключ
    mode = 2;
    button1.className = 'modal-button';
    button2.className = 'modal-button active-button';
    button3.className = 'modal-button';
    last_step = 3;
    m2_s1();
}

function m2_s1() {
    step = 1;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 1';
    document.getElementById('mc-text1').textContent = 'Выберите действие Вернуть ключ” на главной странице.';
    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/2/step1.png';
    document.getElementById('image1-step').style.height = '280px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button inactive';
    document.getElementById('next-btn').className = 'step-button';
    document.getElementById('prev-btn').onclick = m2_s1;
    document.getElementById('next-btn').onclick = m2_s2;
}

function m2_s2() {
    step = 2;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 2';
    document.getElementById('mc-text1').textContent = 'Попросите пользователя отсканировать QR-код через своё устройство, либо нажмите кнопку “Показать все заявки”';
    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/2/step2.png';
    document.getElementById('image1-step').style.height = '280px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button';

    document.getElementById('prev-btn').onclick = m2_s1;
    document.getElementById('next-btn').onclick = m2_s3;
}

function m2_s3() {
    step = 3;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 3';
    document.getElementById('mc-text1').textContent = 'После появления окна с занятыми кабинетами, выберите  тот, ключ от которого нужно вернуть. Для этого нажмите кнопку “Вернуть ключ” и подтвердите возврат.';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/2/step3-1.png';
    document.getElementById('image2-step').src =  staticUrl + 'img/' + 'gide/2/step3-2.png';

    document.getElementById('image1-step').style.height = '260px';
    document.getElementById('image2-step').style.height = '150px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';
    document.getElementById('image2-step').style.display = 'block';


    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button inactive';

    document.getElementById('prev-btn').onclick = m2_s2;
    document.getElementById('next-btn').onclick = m2_s3;
}


function Mode3() { // Как забронировать кабинет
    mode = 3;
    button1.className = 'modal-button';
    button2.className = 'modal-button';
    button3.className = 'modal-button active-button';
    last_step = 3;
    m3_s1();
}

function m3_s1() {
    step = 1;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 1';
    document.getElementById('mc-text1').textContent = 'Перейдите на страницу с кабинетами. Выберите нужный кабинет, у которого есть расписание. Выберите свободную ячейку и нажмите “Забронировать”. Затем нажмите “Далее”.';
    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/3/step1.png';
    document.getElementById('image1-step').style.height = '320px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button inactive';
    document.getElementById('next-btn').className = 'step-button';
    document.getElementById('prev-btn').onclick = m3_s1;
    document.getElementById('next-btn').onclick = m3_s2;
}

function m3_s2() {
    step = 2;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 2';
    document.getElementById('mc-text1').textContent = `Для подтверждения бронирования, попросите пользователя отсканировать QR-код со своего устройства. Пользователь может сразу взять ключ, если ключ находится у охраны и до начала занятия осталось менее 30 минут `;
    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/3/step2.png';
    document.getElementById('image1-step').style.height = '280px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';

    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button';

    document.getElementById('prev-btn').onclick = m3_s1;
    document.getElementById('next-btn').onclick = m3_s3;
}

function m3_s3() {
    step = 3;
    hideAllElems();
    document.getElementById('mc-step').textContent = 'Шаг 3';
    document.getElementById('mc-text1').textContent = 'После сканирования  QR-кода появится соответствующее сообщение с успехом (рис.1) или с ошибкой (рис.2)';

    document.getElementById('image1-step').src =  staticUrl + 'img/' + 'gide/3/step3-1.png';
    document.getElementById('image2-step').src =  staticUrl + 'img/' + 'gide/3/step3-2.png';

    document.getElementById('image1-step').style.height = '260px';
    document.getElementById('image2-step').style.height = '260px';

    document.getElementById('mc-text1').style.display = 'block';
    document.getElementById('image1-step').style.display = 'block';
    document.getElementById('image2-step').style.display = 'block';


    document.getElementById('prev-btn').className = 'step-button';
    document.getElementById('next-btn').className = 'step-button inactive';

    document.getElementById('prev-btn').onclick = m3_s2;
    document.getElementById('next-btn').onclick = m3_s3;
}

function hideModalGide() {
    document.getElementById('modal-window').style.display = 'none';
}

function showModalGide() {
    document.getElementById('modal-window').style.display = 'flex';
}

Mode1();