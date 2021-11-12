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
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

window.addEventListener('load', () => {
    $('.product_add').on('click', 'button[type="button"]', (e) => {
        let t_href = e.target;
        let page_id = t_href.name;
        $.ajax({
            type: 'POST',
            headers: { 'X-CSRF-TOKEN': csrftoken}, // этот работает наконец
            url: '/baskets/add/' + t_href.name + '/',
            data: {'page_id': page_id},
            success: (data) => {
                if (data) {
                    $('.product_items').html(data.result)
                }
            },
            error:function(error){
                console.log(error);}
        });
        e.preventDefault();
    });

    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target;
        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: (data) => {
                if (data) {
                    $('.basket_list').html(data.result)
                }
            },
        });
        e.preventDefault();
    });

    // $('.manager_detail').on('click', 'button[type="button"]', (e) => {
    //     $(document).on('click', '.manager_detail', (e) =>{

    $('.product_view').on('click', 'button[class="btn btn-primary"]', (e) => {
            let t_href = e.target;
            let product_id = t_href.name;
            $.ajax({
                url: '/products/modal/' + product_id + '/',
                success: (data) => {
                    if (data) {
                        $('.product_viewer').html(data.result)
                }
            },
        });
        e.preventDefault();
    });

    $('.send_to_proceed').on('click', 'button[type="button"]', (e) => {
        let t_href = e.target;
        $.ajax({
            type: 'POST',
            url: '/orders/forming_complete/' + t_href.name + '/',
            success: (data) => {
            if (data) {
                $('.text-center').html(data)
                }
            },
        });
        e.preventDefault();
    });

    if ($("#random").length > 0){
        setInterval(function() {
        document.getElementById("random").innerHTML = Math.floor
        (Math.random() * 2) + 1;}, 2000);
    }
});
