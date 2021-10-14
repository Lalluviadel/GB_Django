window.onload = () => {
    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target;
        console.log(t_href.name);
        console.log(t_href.value);
        // var csrf = $('meta[name="csrf-token"]').attr('content');
        $.ajax({
            // headers: {'X-CSRFToken': csrf},

            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: (data) => {
                if (data) {
                    $('.basket_list').html(data.result)
                }
            },
        });
        e.preventDefault();
    });


    $('.product_add').on('click', 'button[type="button"]', (e) => {
        let t_href = e.target;
        console.log(t_href.name)

        var csrf = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrf},
            url: '/baskets/add/' + t_href.name + '/',
            success: (data) => {
                if (data) {
                    $('.product_items').html(data.result)
                }
            },
        });
        e.preventDefault();
    });
};