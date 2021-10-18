setInterval(function() {
    document.getElementById("random").innerHTML = Math.floor
    (Math.random() * 2) + 1;}, 2000);


window.onload = () => {
    $('.basket_list').on('click', 'input[type="number"]', (e) => {
        let t_href = e.target;
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
    //
    // $('.manager_detail').on('click', 'button[type="button"]', (e) => {
    //     $(document).on('click', '.manager_detail', (e) =>{

    $('.product_view').on('click', 'button[type="button"]', (e) => {
            let t_href = e.target;
            let product_id = t_href.name;
            $.ajax({
                url: '/products/modal/' + product_id + '/',
                success: (data) => {
                    if (data) {
                        $('.product_viewer').html(data)
                }
            },
        });
        e.preventDefault();
    });

    $('.product_add').on('click', 'button[type="button"]', (e) => {
        let t_href = e.target;
        let page_id = t_href.value;

        var csrf = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrf},
            url: '/baskets/add/' + t_href.name + '/',
            data: {'page_id': page_id},
            // success: (data) => {
                // if (data) {
                //     $('.product_items').html(data.result)
                // }
            // },
        });
        e.preventDefault();
    });
};