
function like_dislike(post, user, value, url) {
    let post_data = {
        'post': post,
        'user': user,
        'value': value,
    }
    $.get(url, post_data, function (data, status) {
        let like = $('#like')
        let dislike = $('#dislike')
        if (value === 'like') {
            if (like.css('color') !== 'rgb(0, 128, 0)') {
                like.css('color', 'green')
                dislike.css('color', 'black')
            } else {
                like.css('color', 'black')
            }
        } else {
            if (dislike.css('color') !== "rgb(255, 0, 0)") {
                dislike.css('color', 'red')
                like.css('color', 'black')
            } else {
                dislike.css('color', 'black')
            }
        }
        $('#post-like').html(String(data['likes']).replace(/[0-9]/g, c => String.fromCharCode(c.charCodeAt(0) + 1728)))
        $('#post-dislike').html(String(data['dislikes']).replace(/[0-9]/g, c => String.fromCharCode(c.charCodeAt(0) + 1728)))

    });
}
