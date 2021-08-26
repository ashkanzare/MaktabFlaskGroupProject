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

function search(url, url_static) {
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
                    <div class="mt-2 col-2 mb-2" style="max-width: 10rem"><img class="card-img-top cover" style="height: 5rem; width: auto;" src=${url_static + post_image} alt="Post image"></div>
                      <div class="text-center col-8 mt-4">
                            <h3 class="card-title">${post.title}</h3>
                      </div>
                      <div class="text-center col-2 mt-4 ml-2">
                            <p class="mt-2 mb-4 ">نویسنده:<span class="mr-2"><a href="#">${post.author.username}</a></span></p>
                      </div>
                    </div>  
                  `;

                  container.innerHTML += content;}
            });}
    }

function sum_up_text(text_list) {
    let init_text = '';
    for (let text of text_list) {
        if (text.innerText !== undefined) {
            init_text += ' ' + text.innerText
        }
    }
    return init_text
}
function parse(text1, text2) {
    let content_1 =  sum_up_text($.parseHTML(text1))
    let content_2 =  sum_up_text($.parseHTML(text2))
    $('#new_1').html(content_1.substring(0,200) + '...')
    $('#new_2').html(content_2.substring(0,200) + '...')
}

function convertNumber(fromNum) {
    let persianNums = '۰١۲۳۴۵۶۷۸۹';
    return persianNums.indexOf(fromNum);
}

function comment(url1, url2) {
    let comment = $('#comment')
    let comment_text = comment.val()
    $.post(url1, {'comment_content': comment_text}, function(data, status) {
            let counter_elem = $('#comment-counter')
            let counter = Number(counter_elem.html())
            show_comments(url2, counter)
          });
    comment.val('')
}

function get_time_diff( datetime1, datetime2 )
{

    let diff = datetime2 - datetime1;
    console.log(datetime1, datetime2)
    let years = Math.floor(diff / 1000 / 60 / (60 * 24 * 30 * 12));
    let months = Math.floor(diff / 1000 / 60 / (60 * 24 * 30));
    let days = Math.floor(diff / 1000 / 60 / (60 * 24));
    let hour = Math.floor(diff / 1000 / 60 / (60));
    let minute = Math.floor(diff / 1000 / 60 );
    let seconds = Math.floor(diff / 1000 );

    if (years !== 0) {
        return `${years} سال پیش`
    }
    else if (months !== 0) {
        return `${months} ماه پیش`
    }
    else if (days !== 0) {
        return `${days} روز پیش`
    }
    else if (hour !== 0) {
        return `${hour} ساعت پیش`
    }
    else if (minute !== 0) {
        return `${minute} دقیقه پیش`
    }
    else if (seconds !== 0) {
        return `${seconds} ثانیه پیش`
    }
    else {
        return `   الان    `
    }

}




function more_comments(url) {
    let counter_elem = $('#comment-counter')
    let counter = Number(counter_elem.html()) + 1
    counter_elem.html(counter)
    show_comments(url, counter)

}

function show_comments(url, counter) {
    $.get(url, {'counter': counter}, function(data, status) {
            const section = document.getElementById('comment-section');
            section.innerHTML = ''
            let more_comments = `
                <div class="text-center mb-4">
                    <button class="bg-white" onclick="more_comments('${url}')" id="more_comment" style="outline: none; width: 50px; height: 50px; border-radius: 50%"><i class="fa fa-plus bg-white" aria-hidden="true"></i></button>
                </div>
            `
            if (data['result'].length !== data['max']) {
                section.innerHTML += more_comments;
            }
            for (let comment of data['result'].reverse()) {
                  let date = Number(comment.date);
                  const content = `
                
                <div class="row">
                    <div class="col-9" style="width: 80%">
                        <div class="row">
                            <div class="col-4" style="font-weight: bolder">${comment.user.username}</div>
                            <div class="col-8">${comment.comment}</div>
                        </div>    
                    </div>
                    <div class="bg-succes col-3"><p style="font-size: 60%; font-weight: lighter" class="mt-1">${ get_time_diff(date, data['time']) }</p></div>
                    </div>
                  `;

                  section.innerHTML += content;}
            });

}


