
    function doDelete(id, url) {
        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                $('#' + id).css('display', 'none')
            }
        })
    }

    function deActivate(id, url) {
        $.ajax({
            url: url,
            type: "GET",
            success: function (response) {
                let icon = $('#active-' + id)
                let span = $('#span-' + id)
                if (icon.hasClass('fa-eye')) {
                    icon.removeAttr('class', 'fa-eye')
                    icon.attr('class', 'm-2 fa fa-eye-slash')
                    span.html('غیرفعال')
                } else {
                    icon.removeAttr('class', 'fa-eye-slash')
                    icon.attr('class', 'm-2 fa fa-eye')
                    span.html('فعال')
                }
            }
        })
    }

