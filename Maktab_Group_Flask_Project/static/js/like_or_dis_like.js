
               function like_dislike(post,user,value,url) {
                   let pk = $(this).attr('value');
                   $.ajax({
                       type: 'GET',
                       url: url,
                       data: {
                           'post': post,
                           'user': user,
                           'value': value,
                       },

               //         success: function () {
               //                  let btnLike = document.querySelector('#like')
               //              let btnDisLike = document.querySelector('#dislike')
               //              btnDisLike.addEventListener('click',() =>btnDisLike.style.backgroundColor ='#cc3333')
               //              btnLike.addEventListener('click',()=>btnLike.style.backgroundColor ='#4bb544')
               // }

                   });
                            }

