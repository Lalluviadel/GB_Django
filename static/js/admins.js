function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

window.addEventListener('load', (e) => {
    $('#update_cat_catcher').on('click', '#update_cat_btn', (e) => {
        let t_href = e.target;
        $.ajax({
            type: 'POST',
            headers: {'X-CSRF-TOKEN': csrftoken},
            url: '/admins/categories/delete/' + t_href.name + '/',
            success: (data) => {
                if (data) {
                    $('.table-responsive').html(data.result)
                }
            },
        });
        e.preventDefault();
    });

    $('#update_prod_catcher').on('click', '#update_prod_btn', (e) => {
        let t_href = e.target;
        $.ajax({
            type: 'POST',
            headers: {'X-CSRF-TOKEN': csrftoken},
            url: '/admins/products/delete/' + t_href.name + '/',
            success: (data) => {
                if (data) {
                    $('.table-responsive').html(data.result)
                }
            },
        });
        e.preventDefault();
    });

    $('#update_users_catcher').on('click', '#update_user_btn', (e) => {
        let t_href = e.target;
        $.ajax({
            type: 'POST',
            headers: {'X-CSRF-TOKEN': csrftoken},
            url: '/admins/users-delete/' + t_href.name + '/',
            success: (data) => {
                if (data) {
                    $('.table-responsive').html(data.result)
                }
            },
        });
        e.preventDefault();
    });

    $('#give_me_a_crown').on('click', '#give_me_a_crown_btn', (e) => {
        let t_href = e.target;
        console.log(t_href.name);
        $.ajax({
            type: 'POST',
            headers: {'X-CSRF-TOKEN': csrftoken},
            url: '/admins/users-is-staff/' + t_href.name + '/',
            success: (data) => {
                if (data) {
                    $('.table-responsive').html(data.result)
                }
            },
        });
        e.preventDefault();
    });
})