window.addEventListener('load', () => {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = []
    let price_arr = []
    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val())
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseInt($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity').val());
        _sum = parseInt($('.orderitems-' + i + '-price').text().replace(',', '.'));
        _price = _sum / _quantity;

        quantity_arr[i] = _quantity
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0
        }
    }

    $('.table').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value)
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            price_obj = '.orderitems-' + orderitem_num.toString() + '-price';
            cost = orderitem_quantity * price_arr[orderitem_num]
            $(price_obj).html(cost.toString() + ',00 руб');
            orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
    });

    $('.formset_row').formset({
        addText: '<i class="fa fa-plus"></i> Добавить продукт',
        deleteText: '<i class="fa fa-trash"></i> удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummerUpdate(price_arr[orderitem_num], delta_quantity)
        delta_quantity = 0;
        delta_cost = 0;
        quantity_arr[orderitem_num] = 0;
    }

    function orderSummerUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity
        if (isNaN(delta_cost)) {
            delta_cost = 0;
        }
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));

        if (!isNaN(delta_quantity)) {
            order_total_quantity = order_total_quantity + delta_quantity;
            $('.order_total_quantity').html(order_total_quantity.toString())
        }
        $('.order_total_cost').html(order_total_price.toString() + ',00');
    }

    $(document).on('change', '.order_form select', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
        let orderitem_product_pk = target.options[target.selectedIndex].value;
        if (orderitem_product_pk) {
            $.ajax({
                url: '/orders/product/' + orderitem_product_pk + '/price/',
                success: function (data) {
                    if (data.price) {
                        price_arr[orderitem_num] = parseFloat(data.price)
                        if (isNaN(quantity_arr[orderitem_num])) {
                            quantity_arr[orderitem_num] = 0;
                        }
                        let price_html = '<span class="orderitems-' + orderitem_num + '-price">' + '0 руб' + '</span> ';
                        let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html);
                    }
                }
            });
        }
    });
});
