function showNotification(res, status) {
    Swal.fire({
        // `${status}`,
        // `${res.message}`,
        // `${res.status}`,
        title: status,
        text: res.message,
        icon: res.status,
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        confirmButtonText: 'باشه'
    }).then(result => {
        if (result.isConfirmed) {
            if (res.callBack) {
                res.callBack()
            }
        }
    });
}

$(function () {
    $('marquee').mouseover(function () {
        $(this).attr('scrollamount', 0);
    }).mouseout(function () {
        $(this).attr('scrollamount', 5);
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
