console.log("JavaScript loaded...")

$('.like').on('click', function(event){
  event.preventDefault();
  var element = $(this);
  $.ajax({
    url: '/like_cat/',
    method: 'GET',
    data: {cat_id: element.attr('data-id')},
    success: function(response){
      element.html('Likes: ' + response);
    }
  })
})
