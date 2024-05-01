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
        window.location.reload();
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
        window.location.reload();
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

  // Toggle visibility of contact form
  function toggleContactForm() {
    var contactFormSection = $('#order-contact-form');
    contactFormSection.toggle();
  }

  // Function to scroll to the contact form section
  function scrollToContactForm() {
    var contactFormSection = $('#order-contact-form');
    $('html, body').animate({
        scrollTop: contactFormSection.offset().top
    }, 500);
  } 

  // Add click event listener to "Problem with order" button to toggle contact form
  $(document).on('click', '.problem-with-order-button', function(e) {
    e.preventDefault();
    toggleContactForm();
    scrollToContactForm();
  });

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

  // Change event for radio buttons to update visual stars
  $('.star-rating input[type="radio"]').change(function() {
    var rating = $(this).val();
    $(this).closest('.star-rating').find('.star').each(function(index) {
        if (index < rating) {
            $(this).text('★').css('color', 'gold');  // Filled star
        } else {
            $(this).text('☆').css('color', 'gray');  // Empty star
        }
    });
    $(this).closest('.star-rating').data('rating', rating);
  });

  // Click event to submit review
  $('.leave-review-btn').click(function() {
    var container = $(this).closest('.star-rating');
    var rating = container.data('rating');
    var productID = $(this).data('product-id');
    
    if (!rating) {
        alert('Please select a rating before submitting your review.');
        return;
    }
    
    var url = '/submit-review/' + productID + '/';
    console.log("Submitting to URL: ", url);
    
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'rating': rating,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'action': 'post'
        },
        success: function(response) {
            alert('Thank you for your review!');
        },
        error: function(xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText);  // Provides more detail about the error
          alert('Error submitting review: ' + errmsg);
        }
      });
    });

});

// Function to get CSRF token
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