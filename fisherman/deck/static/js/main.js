$(function() {
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
});
