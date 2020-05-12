(function () {
	'use strict';
	// iPad and iPod detection	
	var isiPad = function () {
		return (navigator.platform.indexOf("iPad") != -1);
	};

	var isiPhone = function () {
		return (
			(navigator.platform.indexOf("<i></i>Phone") != -1) ||
			(navigator.platform.indexOf("iPod") != -1)
		);
	};

	var functionFactory = (cssSelector, endpoint, key)=>{
		return function(){
			$.ajax({
				type: 'GET',
				url: endpoint,
				dataType: 'json',
				headers: {
					'Content-Type': 'application/json',
					"Access-Control-Allow-Origin": "*"
				},
				success: function (data ) {
					console.log(data[key]);
					$(cssSelector).html(data[key])
				}
			})
		}}
		var getDay22 = () => {
			for (let index = 1; index < 4; index++) {
				$.ajax({
					type: 'GET',
					url: 'http://127.0.0.1:5000/api/users/2/journeys/2/days/'+index+'/',
					dataType: 'json',
					headers: {
						'Content-Type': 'application/json',
						"Access-Control-Allow-Origin": "*"
					},
					success: function (data) {
						console.log(data);
						console.log('.date22' + index);

						$('.date22'+index).html(data['date']);
						$('.desc22'+index).html(data['description']);
					},
				})
			}
		}

	var functionFactoryChangeUserOnClick = (cssSelector, endpoint, key)=>{
		return function(){
			$(cssSelector).click(function() {
				$.ajax({
					type: 'PUT',
					url: endpoint,
					dataType: 'json',
					headers: {
						'Content-Type': 'application/json',
						"Access-Control-Allow-Origin": "*"
					},
					success: function (data ) {
						console.log(data[key]);
						$(cssSelector).html(data[key])
					}
				})
			}
		)
	}}


	var functionFactoryEditOnClick = (cssSelector, endpoint, key)=>{
		return function(){
			$(cssSelector).click(function() {
				$.ajax({
					type: 'GET',
					url: endpoint,
					dataType: 'json',
					headers: {
						'Content-Type': 'application/json',
						"Access-Control-Allow-Origin": "*"
					},
					success: function (data ) {
						alert("user changed");
					}
				})
			}
		)
	}}

	var functionFactoryDeleteOnClick = (cssSelector, endpoint)=>{
		return function(){
			$(cssSelector).click(function() {
				$.ajax({
					type: 'DELETE',
					url: endpoint,
					dataType: 'json',
					headers: {
						'Content-Type': 'application/json',
						"Access-Control-Allow-Origin": "*"
					},
					success: function (data ) {
						alert("User deleted succesfully");
					}
				})
			}
		)
	}}

	
	var daysFromJourneyFunction = functionFactory('.user2', 'http://127.0.0.1:5000/api/users/2/', 'username');
	var imagesFromDayFunction = functionFactory('.user2', 'http://127.0.0.1:5000/api/users/1/journeys/1/days/2/images/', 'username');
	var journeysFromUserFunction = functionFactory('.user2', 'http://127.0.0.1:5000/api/users/2/journeys', 'username');
	var user1LoadFunction = functionFactory('.user2', 'http://127.0.0.1:5000/api/users/2/', 'username');
	var journeySingleLoadFunction = functionFactory('.journey1', 'http://127.0.0.1:5000/api/users/1/journeys/1/', 'title');
	var daySingleLoadFunction = functionFactory('.day1', 'http://127.0.0.1:5000/api/users/1/journeys/1/days/1/', 'title');
	var imageSingleLoadFunction = functionFactory('.day1', 'http://127.0.0.1:5000/api/users/1/journeys/1/days/1/images/1', 'title'); 
	var editUser2 = functionFactoryEditOnClick('.edituser2', 'http://127.0.0.1:5000/api/users/2/', 'title'); 
	var deleteUser2 = functionFactoryDeleteOnClick('.deleteuser2', 'http://127.0.0.1:5000/api/users/2/'); 
	var editDay1 = functionFactoryEditOnClick('.editday', 'http://127.0.0.1:5000/api/users/1/journeys/1/days/1/', 'title'); 
	var deleteDay = functionFactoryDeleteOnClick('.deleteday', 'http://127.0.0.1:5000/api/users/1/journeys/1/days/1/', 'title'); 
	var changeUser2 = functionFactoryChangeUserOnClick('.changeuser1', 'http://127.0.0.1:5000/api/users/2/', 'username'); 
	var journey2user2day2 =  functionFactory('.date1', 'http://127.0.0.1:5000/api/users/2/journeys/2/days/2', 'date');
	

	// Click outside of offcanvass
	var mobileMenuOutsideClick = function () {
		$(document).click(function (e) {
			var container = $("#fh5co-offcanvas, .js-fh5co-close-offcanvas");
			if (!container.is(e.target) && container.has(e.target).length === 0) {
				if ($('#fh5co-offcanvas').hasClass('animated fadeInLeft')) {
					$('#fh5co-offcanvas').addClass('animated fadeOutLeft');
					setTimeout(function () {
						$('#fh5co-offcanvas').css('display', 'none');
						$('#fh5co-offcanvas').removeClass('animated fadeOutLeft fadeInLeft');
					}, 1000);
					$('.js-fh5co-nav-toggle').removeClass('active');
				}
			}
		});

		$('body').on('click', '.js-fh5co-close-offcanvas', function (event) {
			$('#fh5co-offcanvas').addClass('animated fadeOutLeft');
			setTimeout(function () {
				$('#fh5co-offcanvas').css('display', 'none');
				$('#fh5co-offcanvas').removeClass('animated fadeOutLeft fadeInLeft');
			}, 1000);
			$('.js-fh5co-nav-toggle').removeClass('active');
			event.preventDefault();
		});
	};

	// Burger Menu
	var burgerMenu = function () {

		$('body').on('click', '.js-fh5co-nav-toggle', function (event) {
			var $this = $(this);
			$('#fh5co-offcanvas').css('display', 'block');
			setTimeout(function () {
				$('#fh5co-offcanvas').addClass('animated fadeInLeft');
			}, 100);
			// $('body').toggleClass('fh5co-overflow offcanvas-visible');
			$this.toggleClass('active');
			event.preventDefault();
		});
	};

	var scrolledWindow = function () {

		$(window).scroll(function () {
			var header = $('#fh5co-header'),
				scrlTop = $(this).scrollTop();
			$('#fh5co-home .flexslider .fh5co-overlay').css({
				'opacity': (.5) + (scrlTop / 2000)
			});

			if ($('body').hasClass('offcanvas-visible')) {
				$('body').removeClass('offcanvas-visible');
				$('.js-fh5co-nav-toggle').removeClass('active');
			}
		});

		$(window).resize(function () {
			if ($('body').hasClass('offcanvas-visible')) {
				$('body').removeClass('offcanvas-visible');
				$('.js-fh5co-nav-toggle').removeClass('active');
			}
		});
	};

	// Page Nav
	var clickMenu = function () {
		var topVal = ($(window).width() < 769) ? 0 : 58;

		$(window).resize(function () {
			topVal = ($(window).width() < 769) ? 0 : 58;
		});

		if ($(this).attr('href') != "#") {
			$('#fh5co-main-nav a:not([class="external"]), #fh5co-offcanvas a:not([class="external"])').click(function (event) {
				var section = $(this).data('nav-section');

				if ($('div[data-section="' + section + '"]').length) {
					$('html, body').animate({
						scrollTop: $('div[data-section="' + section + '"]').offset().top - topVal
					}, 500);
				}
				event.preventDefault();
			});
		}
	};

	var contentWayPoint = function () {
		var i = 0;
		$('.animate-box').waypoint(function (direction) {
			if (direction === 'down' && !$(this.element).hasClass('animated')) {
				i++;
				$(this.element).addClass('item-animate');
				setTimeout(function () {
					$('body .animate-box.item-animate').each(function (k) {
						var el = $(this);
						setTimeout(function () {
							el.addClass('fadeInUp animated');
							el.removeClass('item-animate');
						}, k * 200, 'easeInOutExpo');
					});
				}, 100);
			}
		}, {
			offset: '85%'
		});
	};

	// Document on load.
	$(function () {
		mobileMenuOutsideClick();
		burgerMenu();
		scrolledWindow();
		user1LoadFunction();
		// journeySingleLoadFunction();
		// journey2user2day2();
		getDay22();
		// changeUser();
		// deleteDay();
		// Animations
		contentWayPoint();
	});
}());