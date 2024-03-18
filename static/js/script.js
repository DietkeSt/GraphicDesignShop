$(document).ready(function(){
    $('.add-to-basket').click(function(){
        var productId = $(this).data('value');
        var quantity = $(this).data('quantity');

        $.ajax({
            type: 'POST',
            url: '{% url "store_basket:add_to_basket" %}',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                'product_id': productId,
                'quantity': quantity,
            },
            success: function(response) {
                // Update basket quantity display
                $('#basket-qty').text(response.basket_total);
            },
            error: function(xhr, errmsg, err) {
                console.log("Error adding item to basket: " + errmsg);
            }
        });
    });
});