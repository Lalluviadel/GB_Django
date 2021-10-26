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


window.onload = () => {
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

    $('.product_view').on('click', 'button[type="button"]', (e) => {
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



    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;

    let quantity_arr = []
    let price_arr = []

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())


    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;


    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseInt($('.orderitems-' + i + '-price').text().replace(',' , '.'));

        // console.log(_quantity)
        // console.log(_price)
        quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price;

        } else {
            price_arr[i] = 0
        }
    }

    $('.order_form').on('click', 'input[type=number]', (e) => {
        let target = e.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        }
    });


    $('.order_form').on('click', 'input[type=checkbox]', (e) => {
        let target = e.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        }else{
            delta_quantity = quantity_arr[orderitem_num];
        }
         orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    });


    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    function  deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    }

    function orderSummerUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_quantity').html(order_total_quantity.toString())
        $('.order_total_cost').html(order_total_price.toString() + ',00');

    }

};




