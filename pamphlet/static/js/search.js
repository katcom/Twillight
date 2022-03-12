
$("#search-btn").on('click',function(e){
    var form = $("#search-bar-form")
    var actionUrl = form.attr('action')

    $.ajax(
        {
            type:"POST",
            url:actionUrl,
            data:form.serialize(),
            success:function(data){
                console.log(data)
                display_serach_result(data)
            },
            error:function(result){
                console.log(result.responseText)
            }

        }
    )
})
function display_serach_result(data){
    data_dict ={result:data}
    console.log(data_dict)
    var tpl = $("#single-user-box").html()
    var template = Handlebars.compile(tpl)
    var html = template(data_dict)
    $("#search-result-container").html(html)
}
