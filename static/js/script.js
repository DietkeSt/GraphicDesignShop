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
    var offset = 128; 
    $('html, body').animate({
        scrollTop: contactFormSection.offset().top - offset
    }, 500);
  } 

  // Function to adjust padding based on hash
  function adjustPaddingForHash() {
    // Array of section IDs that require dynamic padding
    const sections = ['contact-form-section', 'services-section'];

    // Loop through each section
    sections.forEach(sectionId => {
        const section = $('#' + sectionId);
        // Check if the current hash matches the section ID
        if (window.location.hash === '#' + sectionId) {
            section.css('padding-top', '8em'); // Adds padding when navigated to
        } else {
            section.css('padding-top', '0'); // Removes padding otherwise
        }
    });
  }

  // Call adjustPaddingForHash on load and on hash change
  adjustPaddingForHash();
  $(window).on('hashchange', adjustPaddingForHash);

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

  // Listen for changes on the address dropdown and update address fields
  $('#addressSelect').change(function() {
    var addressId = $(this).val();
    if (addressId) {
        // Fetch address details from the server
        $.ajax({
            type: 'GET',
            url: `/account/get-address-details/${addressId}/`,
            success: function(data) {
                $('#full_name').val(data.full_name);
                $('#phone').val(data.phone);
                $('#address_line').val(data.address_line);
                $('#address_line2').val(data.address_line2 || '');
                $('#town_city').val(data.town_city);
                $('#postcode').val(data.postcode);
                $('#country').val(data.country);
            },
            error: function(error) {
                console.log('Error fetching address details:', error);
            }
        });
    }
  });

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

  // Toggle review form visibility on clicking 'Leave a review'
  $(document).on('click', '.open-review-btn', function() {
    var productID = $(this).data('product-id');
    var reviewForm = $('.star-rating[data-product-id="' + productID + '"]');
    // Toggle visibility
    reviewForm.toggle();
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
            container.hide();
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

        var full_name = document.getElementById("full_name").value;
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phone").value;
        var address_line = document.getElementById("address_line").value;
        var address_line2 = document.getElementById("address_line2").value;
        var town_city = document.getElementById("town_city").value;
        var country = document.getElementById("country").value;
        var postcode = document.getElementById("postcode").value;
        var buyer_note = document.getElementById("buyer_note").value;

        $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:8000/orders/add/',
            data: {
                order_key: clientSecret,
                full_name: full_name,
                email: email,
                phone: phone,
                address_line: address_line,
                address_line2: address_line2,
                town_city: town_city,
                country: country,
                postcode: postcode,
                buyer_note: buyer_note,
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
                                line1: address_line,
                                line2: address_line2,
                                city: town_city,
                                country: country,
                                postal_code: postcode
                            },
                            name: full_name,
                            email: email,
                            phone: phone
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