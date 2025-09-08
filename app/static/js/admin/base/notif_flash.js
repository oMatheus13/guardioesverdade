document.addEventListener('DOMContentLoaded', function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    toastElList.forEach(function(toastEl, index) {
        var toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000 + (index * 1500) // Atraso incremental
        });
        toast.show();
    });
});