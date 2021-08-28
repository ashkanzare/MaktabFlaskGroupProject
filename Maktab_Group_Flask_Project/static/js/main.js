
function search(url, url_static) {
        const container = document.getElementById('search_result');

        container.innerHTML = ''
        let text = $("#search_bar").val()
        if (text.length >= 1) {
        $.get(url + text, function(data, status) {
            if (data['results'].length >= 1) {
            for (let post of data['results']) {
                  const card = document.createElement('div');
                  let post_image = post.image;
                  if ( post_image === "") {
                      post_image = 'media/posts/post-default/post.jpg'
                  }
                  card.classList = 'card-body';
                  const content = `
                    <div class="search-results shadow text-right mt-2 row bg-white justify-content-between rounded" onclick="window.location='/post/${post._id.$oid}';" style="min-width: 25%">
                    <div class="mt-2 col-2 mb-2 phone-image" style="max-width: 10rem"><img class="card-img-top cover" style="height: 5rem; width: auto;" src=${url_static + post_image} alt="Post image"></div>
                      <div class="text-center col-8 mt-4">
                            <h3 class="card-title phone-title">${post.title}</h3>
                      </div>
                      <div class="text-center col-2 mt-4 ml-2">
               
                            <a class="writer-link" href="/user-profile/${post.author}">${post.author}</a>
                      </div>
                    </div>  
                  `;

                  container.innerHTML += content;}
            }
          else {
              container.innerHTML += "<h3 class='text-white'>نتیجه ای یافت نشد...</h3>"
            }
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

function comment(url1, url2) {
    let comment = $('#comment')
    let comment_text = comment.val()
    $.post(url1, {'comment_content': comment_text}, function(data, status) {
            let counter_elem = $('#comment-counter')

            let counter = Number(counter_elem.html())
            console.log(counter_elem);
            console.log(counter);
            let real_time_counter = $('#comment-count-realtime')

            let num = Number(real_time_counter.html().replace(/[٠-٩]/g, d => "٠١٢٣٤٥٦٧٨٩".indexOf(d)).replace(/[۰-۹]/g, d => "۰۱۲۳۴۵۶۷۸۹".indexOf(d)))
            real_time_counter.html(String(num+1).replace(/[0-9]/g, c => String.fromCharCode(c.charCodeAt(0) + 1728)))
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
            const top_3_section = document.getElementById('top-3-comments');
            section.innerHTML = ''
            top_3_section.innerHTML = ''
            let more_comments = `
                <div class="text-center mb-4">
                    <button class="bg-white" onclick="more_comments('${url}')" id="more_comment" style="border: none;outline: none; width: 50px; height: 50px; border-radius: 50%"><i class="fa fa-plus bg-white" aria-hidden="true"></i></button>
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
                            
                            <div class="col-5" style="font-weight: bolder"><i class="fa fa-user-circle-o ml-1" aria-hidden="true"></i><a class="username" href="/user-profile/${comment.user.username}">${comment.user.username}</a></div>
                            <div class="col-7">${comment.comment}</div>
                        </div>    
                    </div>
                    <div class="col-3"><p style="font-size: 60%; font-weight: lighter" class="mt-1">${ get_time_diff(date, data['time']) }</p></div>
                    </div>
                  `;

                  section.innerHTML += content;}


            for (let comment of data['top_3'].reverse()) {

                      const content = `
                            <li style="font-weight: bolder">
                                <i class="fa fa-user-circle-o" aria-hidden="true"></i>
                                <a class="username" href="/user-profile/${comment.user.username}">${comment.user.username}</a>
                                
                                <ul class="comment-ul">
                                    <li class="mr-3" style="font-weight: lighter">${comment.comment}</li>
                                </ul>

                            </li>
                      `;

                      top_3_section.innerHTML += content;}
            if (data['result'].length === 0 ) {
                let content = `
                    <div class="d-flex mt-3">
                        <div class="ml-3 text-secondary">بدون کامنت</div>
                        <span id="comment-count-realtime" class="d-none">0</span>

                    </div>`
                top_3_section.innerHTML += content
            }
            });

}

function check_input() {
	 document.getElementById('comment-btn').disabled = document.getElementById("comment").value === "";
}

let i = 0;
let txt = 'به وبسایت ما خوش اومدی!!';
let speed = 50;

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("welcome").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}

function copy() {
  let copyText = 'maktabblog.com';
  navigator.clipboard.writeText(copyText);
}

$(document).ready(function(){
  $("#copy_click").hover(function(){
    $(this).html("کلیک کن تا لینک کپی شه!")
    }, function(){
    $(this).html("دریافت لینک دعوت");
  });
});


/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */

function openNav() {

  document.getElementById("mySidebar").style.height = "50%";
}

function closeNav() {
  document.getElementById("mySidebar").style.height = "0%";
}

function openSearch() {
  document.getElementById("mySearchbar").style.height = "75%";
}

function closeSearch() {
  document.getElementById("mySearchbar").style.height = "0%";
}

function get_sub(id) {
    let ul = $(`#${id} > li > i`)
    if (ul.css('transform') === 'none') {
        $(`#${id} > ul`).removeAttr('class', 'd-none').attr('class', 'd-flex')
        ul.css('transform', 'rotate(180deg)')

    }
    else {
        $(`#${id} > ul`).attr('class', 'd-none');
         ul.css('transform', 'none')
}}

let count = 0;
function json_loop(array, ul_name, url_for) {
    for (let category of array) {
        count += 1
        let ul = $('<ul/>')
        let li = $('<li/>').attr('class', 'd-flex').css('top', '5%')
        ul.attr('class', 'mt-2 d-flex ')
        li.html(`<a class="category_a d-flex justify-content-start" href="${url_for}${category._id.$oid}">${category.name}</a>`)
        const myArr = category.path.split("/");
        ul.attr('class', `d-none level-${myArr.length}`)
        ul.attr('id', `${Math.random().toString(36).substr(2, 5)}`)
        ul.append(li)
        ul_name.append(ul)
        if ('children' in category) {
                let i = $('<i/>').attr('class', 'fa fa-caret-right arrow pt-2 pl-3').attr('onclick', `get_sub("${ul.attr('id')}")`)
                li.append(i)
                json_loop(category.children, ul, url_for)
                }

    }
    return ul_name
}
