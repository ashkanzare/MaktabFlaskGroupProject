function openSearch() {
  $("#search_bar_container").css('display', 'block');
  $('.navbar').css('filter', 'blur(3px)')
  $('#main-body').css('filter', 'blur(3px)')
}

function closeSearch() {
  $("#search_bar_container").css('display', 'none');
  $("#search_result").html('')
  $('.navbar').css('filter', 'none')
  $('#main-body').css('filter', 'none')
}

function search(url) {
        const container = document.getElementById('search_result');
        container.innerHTML = ''
        let text = $("#search_bar").val()
        if (text.length >= 1) {
        $.get(url + text, function(data, status) {
            for (let post of data['results']) {
                  const card = document.createElement('div');
                  let post_image = post.image;
                  if ( post_image === "") {
                      post_image = 'media/posts/post_public/post.jpg'
                  }
                  card.classList = 'card-body';
                  const content = `
                    <div class="shadow text-right mt-2 row bg-white justify-content-between rounded" style="min-width: 25%">
                    <div class="mt-2 col-2 mb-2" style="max-width: 10rem"><img class="card-img-top cover" style="height: 5rem; width: auto;" src=${'static/' + post_image} alt="Post image"></div>
                      <div class="text-center col-8 mt-4">
                            <h3 class="card-title">${post.title}</h3>
                      </div>
                      <div class="text-center col-2 mt-4">
                            <p class="mt-2 mb-4">نویسنده:<span class="mr-2"><a href="#">${post.author.username}</a></span></p>
                      </div>
                    </div>  
                  `;

                  container.innerHTML += content;}
            });}
    }

