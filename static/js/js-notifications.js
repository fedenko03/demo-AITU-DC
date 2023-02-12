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
    if (notificationContainer.childNodes.length === 3) {
        deleteNotification(notificationContainer.firstChild, notificationContainer)
    }

    // create a new notification element
    const notification = document.createElement("div");
    notification.classList.add("notification");
    notification.id = `notification-${id}`;
    id++;

    // add data to the notification
    notification.innerHTML = `
    <div class="card bg-light shadow-sm">
        <div class="card-body px-4 py-5 px-md-5" style="margin-top: -20px;padding-bottom: 55px;margin-bottom: -35px;width: 450px;">
            <div class="bs-icon-lg d-flex justify-content-center align-items-center mb-3 bs-icon" style="top: 1rem;right: 1rem;position: absolute;">
            <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-x fs-1 text-muted close-notification" style="margin-bottom: 3px; cursor: pointer;">
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>
                </svg></div>
          
            <p style="display: flex; justify-content: flex-start"> ${data.time}</p>            
            <h6 class="fs-4 fw-bold text-primary card-title"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 16 16" class="bi bi-exclamation-circle fs-2 text-primary" style="padding-bottom: 0px;margin-bottom: 3px;">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"></path>
                    <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"></path>
                </svg>&nbsp;Новая заявка #${data.order_id}!</h6>
                
            <p class="text-muted card-text mb-4">Пользователь: <b>${data.user_full_name}</b>
            <br>Комната: <b>${data.room_name}</b>
            ${data.note ? `<br>Комментарий: ${data.note}` : ""}
            </p>
            <a href="${location.protocol}//${location.host}/main/confirm-takeroom/${data.order_id}" class="btn btn-primary shadow" type="button">Открыть</a>
            <button id="cancelOrder" class="btn btn-danger shadow" type="button">Отклонить</button>
        </div>
    </div>
  `;

    // add the new notification to the container
    notificationContainer.appendChild(notification);

    // add event listener to remove the notification
    const removeBtn = notification.querySelector(".close-notification");
    removeBtn.addEventListener("click", function () {
        deleteNotification(notification, notificationContainer)
    });

    const rejectBtn = notification.querySelector(".btn-danger");
    rejectBtn.addEventListener("click", function () {
        var url = location.protocol + "//" + location.host + "/main/cancel-takeroom/" + data.order_id
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
    });


    // remove the notification after 2 minutes
    setTimeout(function () {
        deleteNotification(notification, notificationContainer)
    }, 1 * 60 * 1000);

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