$(function() {
    // Topic Fetch
    if ($('.fetch-topic').length) {
        $('.fetch-topic').on('click', function(e) {
            e.preventDefault();
            url = $(this).attr('href');

            $.ajax({
                url: url,
                type: 'post'
            }).done(function(data) {
                if (data.result == 1) {
                    window.location.reload();
                }
            });
        });
    }

    // List page selected
    if ($('table.table').length &&
        $('table input[type="checkbox"]').length) {
        var maincheck = $('table.table th input[type="checkbox"]');
        var listchecks = $('table.table td input[type="checkbox"]');
        var imbutton = $('.im.btn');

        maincheck.on('change', function() {
            listchecks.prop('checked', maincheck.prop('checked'));
            if (maincheck.prop('checked')) {
                imbutton.addClass('show');
            } else {
                imbutton.removeClass('show');
            }
        });

        listchecks.on('change', function() {
            if ($('table.table td input:checked').length) {
                imbutton.addClass('show');
            } else {
                imbutton.removeClass('show');
            }
        });

        imbutton.on('click', function(e) {
            e.preventDefault();
            var button = e.target;
            var checked = $('table.table td input:checked');

            weibo_ids = [];
            for (var i = 0; i < checked.length; i++) {
                weibo_ids.push(checked[i].value);
            }

            e.target.href += weibo_ids.join(',');
            window.location.href = e.target.href;
        });
    }
});
