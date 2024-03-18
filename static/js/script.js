$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    var url = $(this).data('url');
    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            productid: $('#add-button').val(),
            productqty: $('#select option:selected').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            action: 'post'
        },
        success: function (json) {
            console.log(json);
            document.getElementById('basket-qty').innerHTML = json.qty
        },
        error: function (xhr, errmsg, err) {}
    });
})
    