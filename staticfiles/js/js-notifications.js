// websocket

var socket = new WebSocket("ws://" + window.location.host + "/ws/new_order/");
socket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    createNotification(data)
};


// notification style


let id = 1; // counter for unique id for each notification

function createNotification(data) {
    const notificationContainer = document.querySelector(".notification-container");

    // if there are already 3 notifications displayed, remove the oldest one
    if (notificationContainer.childNodes.length === 4) {
        deleteNotification(notificationContainer.firstChild, notificationContainer)
    }

    // create a new notification element
    const notification = document.createElement("div");
    notification.classList.add("notification");
    notification.id = `notification-${id}`;
    id++;

    ///// navbar notifications:
    const navbarNotificationContainer = document.querySelector(".notification-navbar")
    let navbarNotificationCount = document.getElementById("navbarNotificationCount")
    let NotCountInt = parseInt(navbarNotificationCount.textContent);
    if (NotCountInt === 0) {
        const element = document.getElementById("zero-notifications-navbar");
        element.parentNode.removeChild(element);
    }
    navbarNotificationCount.textContent = (NotCountInt + 1).toString()
    const navbarNotification = document.createElement("a")
    let note = "";
    if (data.note !== "") {
        note = `<p style="margin-bottom: 5px;">Комментарий: ${data.note}</p>`
    }
    navbarNotification.innerHTML = `
    <a class="dropdown-item d-flex align-items-center" href="${location.protocol}//${location.host}/main/confirm-takeroom/${data.order_id}">
                                            <div class="me-3">
                                                <div class="bg-primary icon-circle">
                                                    <i class="far fa-clock fs-4 text-white"></i>
                                                </div>
                                            </div>
                                            <div>
                                                <span class="small text-gray-500">${data.time} (#${data.order_id})</span>
                                                <p style="margin-bottom: 5px;"><strong>ФИО:</strong> ${data.user_full_name} (${data.user_email})
                                                    <br><strong>Кабинет:</strong> ${data.room_name}</p>
                                                ` + note + `
                                            </div>
                                        </a>
    `
    navbarNotificationContainer.appendChild(navbarNotification);
    /////


    // add data to the notification
    notification.innerHTML = `<div class="card shadow" style="width: 350px;">
                        <div class="card-header" style="padding-top: 6px;padding-bottom: 5px;">
                            <p class="text-primary m-0 fw-bold" style="margin-bottom: 24px;font-size: 15px;padding-right: 0px;margin-right: 12px;">
                                <span style="background-color: rgb(255, 255, 255);">Новая заявка #${data.order_id}</span>
                                <a href="#"><i class="far fa-times-circle text-black-50 close-notification" style="position: absolute;right: 0;margin-right: 5px;font-size: 20px;"></i></a>
                            </p>
                        </div>
                        <div class="card-body" style="margin-bottom: -9px;padding-top: 10px;">
                            <div>
                                <p class="text-sm-start text-md-start text-lg-start text-xl-start text-xxl-start d-xxl-flex justify-content-xxl-start" style="font-size: 13px;margin-bottom: 5px;text-align: left;">Пользователь: ${data.user_full_name}
                                <br>Комната: ${data.room_name}
                                </p>
                                <p class="text-sm-start text-md-start text-lg-start text-xl-start text-xxl-start d-xxl-flex justify-content-xxl-start" style="font-size: 13px;margin-bottom: 5px;text-align: left;position: absolute;right: 15px;top: 45px;">${data.time}</p>
                                ${data.note ? `<p class="text-sm-start text-md-start text-lg-start text-xl-start text-xxl-start d-xxl-flex justify-content-xxl-start" style="font-size: 13px;margin-bottom: 5px;text-align: left;">Комментарий: ${data.note}</p>` : ""}
                            </div>
                            <hr style="margin-top: 8px;margin-bottom: 5px;">
                            <a href="${location.protocol}//${location.host}/main/confirm-takeroom/${data.order_id}" class="btn btn-primary" type="button" style="font-size: 11px;margin-right: 12px;">Открыть</a>
                            <a id="cancelOrder" class="btn btn-danger" type="button" style="font-size: 11px;">Отклонить</a>
                        </div>
                    </div>`

    // add the new notification to the container
    notificationContainer.appendChild(notification);

    // add event listener to remove the notification
    const removeBtn = notification.querySelector(".close-notification");
    removeBtn.addEventListener("click", function () {
        deleteNotification(notification, notificationContainer)
    });

    const rejectBtn = notification.querySelector(".btn-danger");
    rejectBtn.addEventListener("click", function () {
        var url = location.protocol + "//" + location.host + "/api/cancel-takeroom/" + data.order_id
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                console.log(response)
            }
        };
        xhr.send();
        deleteNotification(notification, notificationContainer)
        let navbarNotificationCount = document.getElementById("navbarNotificationCount")
        let NotCountInt = parseInt(navbarNotificationCount.textContent);
        NotCountInt = NotCountInt - 1;
        if(NotCountInt <= 0) {
            NotCountInt = 0
            let navbarZeroNotification = document.createElement("a")
            navbarZeroNotification.innerHTML = `<a id="zero-notifications-navbar" class="dropdown-item text-center small text-gray-500">Нет активных заявок</a>`
            navbarNotificationContainer.appendChild(navbarZeroNotification)
        }
        navbarNotificationCount.textContent = (NotCountInt).toString()
        deleteNotificationNavBar(navbarNotification, navbarNotificationContainer)
    });


    // remove the notification after 2 minutes
    setTimeout(function () {
        deleteNotification(notification, notificationContainer)
    }, 2 * 60 * 1000);


    // remove the notification in navbar after 5 minutes
    setTimeout(function () {
        let navbarNotificationCount = document.getElementById("navbarNotificationCount")
        let NotCountInt = parseInt(navbarNotificationCount.textContent);
        NotCountInt = NotCountInt - 1;
        if(NotCountInt <= 0) {
            NotCountInt = 0
            let navbarZeroNotification = document.createElement("a")
            navbarZeroNotification.innerHTML = `<a id="zero-notifications-navbar" class="dropdown-item text-center small text-gray-500">Нет активных заявок</a>`
            navbarNotificationContainer.appendChild(navbarZeroNotification)
        }
        navbarNotificationCount.textContent = (NotCountInt).toString()
        deleteNotificationNavBar(navbarNotification, navbarNotificationContainer)
    }, 5 * 60 * 1000);

    id++;
}

function deleteNotification(notification, notificationContainer) {
    try {
        notification.classList.add("fade-out");
        notification.style.opacity = '0'
        setTimeout(function () {
            notificationContainer.removeChild(notification);
        }, 200);
    } catch (e) {
        console.log("Уведомление уже было скрыто/удалено.")
    }
}

function deleteNotificationNavBar(notification, notificationContainer) {
    try {
            notificationContainer.removeChild(notification);
    } catch (e) {
        console.log("Уведомление уже было скрыто/удалено.")
    }
}