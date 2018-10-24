// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function(){
    // 页面加载完毕，获取新闻列表
    getNewsList(1)

    // TODO 关注当前作者
    $(".focus").click(function () {
        var user_id = $(this).attr('data-userid')
        var params = {
            "action": "follow",
            "user_id": user_id
        }

        $.ajax({
            url: "/news/follow",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == "0") {
                    // 关注成功
                    var count = parseInt($(".follows b").html());
                    count++;
                    $(".follows b").html(count + "")
                    $(".focus").hide()
                    $(".focused").show()
                }else if (resp.errno == "4101"){
                    // 未登录，弹出登录框
                    $('.login_form_con').show();
                }else {
                    // 关注失败
                    alert(resp.errmsg)
                }
            }
        })
    })

    // TODO 取消关注当前作者
    $(".focused").click(function () {
        var user_id = $(this).attr('data-userid')
        var params = {
            "action": "unfollow",
            "user_id": user_id
        }

        $.ajax({
            url: "/news/follow",
            type: "post",
            contentType: "application/json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno == "0") {
                    // 取消关注成功
                    var count = parseInt($(".follows b").html());
                    count--;
                    $(".follows b").html(count + "")
                    $(".focus").show()
                    $(".focused").hide()
                }else if (resp.errno == "4101"){
                    // 未登录，弹出登录框
                    $('.login_form_con').show();
                }else {
                    // 取消关注失败
                    alert(resp.errmsg)
                }
            }
        })

    })
})

// TODO 获取新闻列表
function getNewsList(page) {
    // 使用正则切割问号后面的参数,得到的是字典
    var params = {
        "p": page,
        "user_id": $('.focus_other a').attr('data-userid')
    }

    $.get("/user_info/news_info", params, function (resp) {
        if (resp.errno == "0") {
            // 先清空原有的数据
            $(".article_list").html("");
            // 拼接数据
            for (var i = 0; i<resp.newsList.length; i++) {
                var news = resp.newsList[i];
                var html = '<li><a href="/news/'+ news.id +'" target="_blank">' + news.title + '</a><span>' + news.create_time + '</span></li>'
                // 添加数据
                $(".article_list").append(html)
            }
            // 设置页数和总页数
            $("#pagination").pagination("setPage", resp.currentPage, resp.totalPage);
        }else {
            alert(resp.errmsg)
        }
    })
}
