
	var $hamburger = $(".hamburger");

	$hamburger.on("click", function() {
		var $this = $(this);
		
		$this.toggleClass("open");
  })
  $('.nav-toggle').on('click', function(e) {
    $(this).toggleClass('nav-open');
    $(this).parent().children('.sidebar').toggleClass('active');
  });
  $('.user-nav-toggle').on('click', function(e) {
    $(this).toggleClass('active');
    $(this).parent().children('.user-menu').toggleClass('active');
  });
$('.navbar-toggler').on('click', function () {
  if (!$('header .navbar-collapse').hasClass('show')) {
    $('header').addClass('open-menu')

  }
  else {
    $('header').removeClass('open-menu')

  }
})
$('.products .fav').on('click', function (e) {
  $(e.target).attr('src', 'static/images/icons/heart-a.svg')
})



// click category or sub category
$('.sidebar .categories').on('click', function (e) {

  $(e.target).toggleClass('active')
})


$('.sidebar .colors').on('click', function (e) {

  $(e.target).parent().toggleClass('active')
})



// for filter

// 

/*Dropdown Menu*/
$('.sorting .dropdown').click(function () {
  $(this).attr('tabindex', 1).focus();
  $(this).toggleClass('active');
  $(this).find('.dropdown-menu').fadeToggle(300);
});
$('.sorting .dropdown').focusout(function () {
  $(this).removeClass('active');
  $(this).find('.dropdown-menu').slideUp(300);
});
$('.sorting .dropdown .dropdown-menu li').click(function () {
  $(this).parents('.dropdown').find('span').text($(this).text());
  $(this).parents('.dropdown').find('input').attr('value', $(this).attr('id'));
});
/*End Dropdown Menu*/



// for grid

$('.filter .shown .list').on('click', function (e) {
  $('.filter .shown >div').removeClass('active')
  $(this).addClass('active')
  $('.content .products ').addClass('list')

})
$('.filter .shown .grid').on('click', function (e) {
  $('.filter .shown >div').removeClass('active')
  $('.content .products ').removeClass('list')

  $(this).addClass('active')

})

// product count
$('.product-count .change-count').on('click', function (e) {
  if ($(e.target).attr('data-title') == 'minus') {
    $('.product-count .count input').val(+$('.product-count .count input').val() - 1)
    if (+$('.product-count .count input').val() < 1) {
      $('.product-count .count input').val(1)
    }

  }
  else if ($(e.target).attr('data-title') == 'plus') {
    $('.product-count .count input').val(+$('.product-count .count input').val() + 1)
    if (+$('.product-count .count input').val() > +$('.product-count .count input').attr('max')) {
      $('.product-count .count input').val($('.product-count .count input').attr('max'))
    }


  } else {
    return false;
  }
})

// desctiption tabs

$('.product-descriptions .desc-nav li ').on('click', function (e) {
  $('.product-descriptions .tabs .tab,.product-descriptions .desc-nav li ').removeClass('active')
  $(`.product-descriptions .tabs .tab[data-id='${$(e.target).attr('data-id')}'],.product-descriptions .desc-nav li[data-id='${$(e.target).attr('data-id')}']`).addClass('active')
})


// add comment

$('.rate-button .give-rate').on('click', function () {
  $('.add-comment').toggleClass('show')
})


// edit user infor
$('.edit-input').on('click', function (e) {
  $(e.target).parent().children('input').attr('disabled', false).focus()
})


// user pages

$('.account .user-menu .menu-item').on('click', function (e) {
  $('.account .user-menu .menu-item').removeClass('active')

  $(e.target).addClass('active')
  $(`.user-pages .user-page`).removeClass('active')
  $(`.user-pages .user-page[data-id='${$(e.target).attr('data-id')}']`).addClass('active')
})


// user oder page navs

$('.orders .order-nav li ').on('click', function (e) {
  $('.orders .order-nav li,.orders .order-tab').removeClass('active')
  $(`.orders .order-nav li[data-id='${$(e.target).attr('data-id')}'],.orders .order-tab[data-id='${$(e.target).attr('data-id')}']`).addClass('active')
})


// order page

$('.order-products .open-order-detail').on('click', function (e) {
  $(e.target).children('span').toggleClass('active')
$(e.target).parent().parent().parent().toggleClass('active')
})


// give star

$('.starRating span').click(function(){
  $(this).siblings().removeClass('active');
  $(this).addClass('active');
  $(this).parent().addClass('starRated');
  
  // Added for Demo
  let rating = $(this).index() + 1;
  $('#currentRating').html( "<small>Rating: <b>" + rating + "</b></small>" );
});