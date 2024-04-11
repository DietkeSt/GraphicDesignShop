// Add Item to basket
$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
    var url = $(this).data('url');
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
            window.location.reload();
        },
        error: function (xhr, errmsg, err) {}
    });
})

// Delete Item from basket
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    var url = $(this).data('delete-url');
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        productid: $(this).data('index'),
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        action: 'post'
      },
      success: function (json) {
        $('.product-item[data-index="' + prodid + '"]').remove();
        document.getElementById("subtotal").innerHTML = json.subtotal;
        document.getElementById("basket-qty").innerHTML = json.qty
      },
      error: function (xhr, errmsg, err) {}
    });
  })

  // Update Item in basket
  $(document).on('click', '.update-button', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    var url = $(this).data('update-url');
    $.ajax({
      type: 'POST',
      url: url,
      data: {
        productid: $(this).data('index'),
        productqty: $('#select' + prodid + ' option:selected').val(),
        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        action: 'post'
      },
      success: function (json) {
        document.getElementById("basket-qty").innerHTML = json.qty
        document.getElementById("subtotal").innerHTML = json.subtotal
      },
      error: function (xhr, errmsg, err) {}
    });
  })
  
$(document).ready(function() {

  // Array of paths to highlight the addresses card
  var highlightAddressPaths = [
    '/account/addresses/',
    '/account/add_address/'
  ];

  // Remove Alert message after 5 seconds
  setTimeout(function() {
    $('.alert').fadeOut('slow', function() {
      $(this).remove();
    });
  }, 5000);

  // Highlight Order section
  if (window.location.pathname === '/account/dashboard/') {
    $('#ordersCard').addClass('highlighted');
  }

  // Highlight Addresses section
  if (highlightAddressPaths.includes(window.location.pathname)) {
      $('#addressesCard').addClass('highlighted');
  }

  // Highlight Profile section
  if (window.location.pathname === '/account/profile/edit/') {
    $('#profileCard').addClass('highlighted');
  }

  // Highlight Wishlist section
  if (window.location.pathname === '/account/wishlist/') {
    $('#wishlistCard').addClass('highlighted');
  }

});

// Function to display the selected filename
function displayFileName(input) {
  const fileNameElement = document.getElementById('file-name');
  if (input.files.length > 0) {
      fileNameElement.textContent = input.files[0].name;
  } else {
      fileNameElement.textContent = '';
  }
}

// Function to submit and reset the address form
function submitForm() {
  var form = document.getElementsByName('address_form')[0];
  form.submit(); // Submit the form
  form.reset();  // Reset all form data
  return false; // Prevent page refresh
}

// Initialize Stripe if the payment form exists
if ($('#payment-form').length > 0) {
  var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
  var elements = stripe.elements();

  var style = {
      base: {
          color: "#000",
          lineHeight: '2.4',
          fontSize: '16px',
          "::placeholder": {
              color: "#aab7c4"
          }
      },
      invalid: {
          color: "#fa755a",
          iconColor: "#fa755a"
      }
  };

  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  card.on('change', ({error}) => {
      let displayError = document.getElementById('card-errors');
      if (error) {
          displayError.textContent = error.message;
          $('#card-errors').addClass('alert alert-info');
      } else {
          displayError.textContent = '';
          $('#card-errors').removeClass('alert alert-info');
      }
  });

  // Get the client secret from the submit button data attribute
  var submitButton = document.getElementById('submit');
  var clientSecret = submitButton.getAttribute('data-secret');

  // Handle form submission for payment
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();

        var custName = document.getElementById("custName").value;
        var custAdd = document.getElementById("custAdd").value;
        var custAdd2 = document.getElementById("custAdd2").value;
        var postCode = document.getElementById("postCode").value;

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/orders/add/',
            data: {
                order_key: clientSecret,
                csrfmiddlewaretoken: CSRF_TOKEN,
                action: "post",
            },
            success: function(json) {
                console.log(json.success)

                stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            address: {
                                line1: custAdd,
                                line2: custAdd2
                            },
                            name: custName
                        },
                    }
                }).then(function(result) {
                    if (result.error) {
                        console.log(result.error.message);
                        // Show error to your customer (e.g., insufficient funds)
                        $('#card-errors').text(result.error.message).addClass('alert alert-danger');
                    } else {
                        // The payment has been processed!
                        if (result.paymentIntent.status === 'succeeded') {
                            console.log('Payment succeeded');
                            // Redirect to success page or update UI
                            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
                        }
                    }
                });

            },
            error: function(xhr, errmsg, err) {},
        });
    });
}