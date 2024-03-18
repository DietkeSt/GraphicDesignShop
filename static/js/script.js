$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url "basket:add_to_basket" %}',
        data: {
            product_id: $('#add-button').val(),
            productqty: $('#select option: selected').text(),
            csrfmiddlewaretoken: "{{csrf_token}}",
            action: 'post'
        },
        success: function (json) {
            document.getElementById('basket-qty').innerHTML = json.qty
        },
        error: function (xhr, errmsg, err) {}
    });
})
    