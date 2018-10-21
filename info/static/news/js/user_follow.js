function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {

    $(".focused").click(function () {
        // TODO 取消关注当前新闻作者
        var user_id = $(this).attr('data-userid');
        var params = {
            "action": "unfollow",
            "user_id": user_id
        }

        $.ajax({
            url: "/user_info/follow_info",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == "0") {
                    // 取消关注成
                   window.location.reload()
                }
                else {
                    // 取消关注失败
                    alert(resp.errmsg)
                }
            }
        })

    })

})