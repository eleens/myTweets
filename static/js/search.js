/**
 * Created by yutingting on 2017/1/16.
 */

$('#search-form').submit(function (e) {
    $.post('/search/',$(this).serialize(),function (data) {
        $('.tweets').html(data);
    });
    e.preventDefault();
});