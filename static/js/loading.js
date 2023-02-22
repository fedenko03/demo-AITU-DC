const spinner = document.getElementById('loading-spinner');

window.onload = function () {
    spinner.style.display = 'none';
    document.body.classList.remove('loading');
};

document.addEventListener('DOMContentLoaded', () => {
    spinner.style.display = 'block';
    document.body.classList.add('loading');
});



