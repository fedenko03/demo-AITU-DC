PinLockButton = document.getElementById("PinLockButton")

PinLockButton.addEventListener("click", function () {
    PinLockCodeElem = document.getElementById("PinLockCode")
    PinLockCode = PinLockCodeElem.value
    const pattern = /^\d{4,10}$/; // regular expression to match only digits and limit length
    const isValid = pattern.test(PinLockCode); // check if input matches the pattern
    if (isValid) {
        document.getElementById("errorPinLock").textContent = "";
        return  window.location.href = `${location.protocol}//${location.host}/main/pinlock/${PinLockCode}`;
    } else {
        const errorMessage = "PIN-код должен содержать от 4 до 10 цифр.";
        document.getElementById("errorPinLock").textContent = errorMessage; // display error message
        return false; // input is invalid
    }
})