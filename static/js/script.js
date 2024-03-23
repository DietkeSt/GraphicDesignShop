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
  
// Remove Alert message after 5 seconds
$(document).ready(function() {
  setTimeout(function() {
    $('.alert').fadeOut('slow', function() {
      $(this).remove();
    });
  }, 5000);
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