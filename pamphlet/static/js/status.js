
function setupLikeButtons(){
    console.log("found dis form:"+$(".dislike-post-form").length)
    $(".dislike-post-form").each(function(){
        console.log('set dislike')
        var btn = $(this).siblings('.like-button')
        
        $(this).on('submit',function(e){
            e.preventDefault()
            var form = $(this)
            var actionUrl = form.attr('action')
            console.log("called delete")
            console.log("data:")
            
            console.log(form.serialize())
            $.ajax(
                {
                    type:'post',
                    url:actionUrl,
                    data:form.serialize(),
                    success:function(data){
                        //alert("Dislike Successfully!")
                        set_to_dislike_btn(btn)
                        console.log('dislike')
                    },
                    error:function(result){
                        alert('something wrong,see console')
                        console.log(result.responseText)
                    }
        
                }
            )
        })
    })
    console.log("found like form:"+$(".dislike-post-form").length)

    $(".like-post-form").each(function(){
        $(this).on('submit',function(e){
            e.preventDefault()
            var form = $(this)
            var actionUrl = form.attr('action')
            console.log("called")
            var btn = $(this).siblings('.like-button')
            console.log(form.serialize())
            $.ajax(
                {
                    type:"POST",
                    url:actionUrl,
                    data:form.serialize(),
                    success:function(data){
                        set_to_like_btn(btn)                        
                    },
                    error:function(result){
                        alert('something wrong,see console')
                        console.log(result.responseText)                    }
        
                }
            )
        })
    })
    console.log("found like btn:"+$(".like-button").length)

    $('.like-button').each(function(){
        console.log('set like btn')
        $(this).unbind().on('click',function(e){
            var btn = e.currentTarget
            
            if ($(btn).attr('is_liked') == 'true'){
                var form = $(btn).siblings('.dislike-post-form')[0]
                console.log('found dis like')
            }else{
                var form = $(btn).siblings('.like-post-form')[0]
                console.log('found  like,go to post form')

            }
    
            $(form).children('input[type=submit]').trigger('click')
            //console.log('submit form')
        })
    }) 
}

function toggleLike(pk){
    console.log(this)
}

function set_to_dislike_btn(btn){
    console.log('change el:')
    console.log(btn)
    $(btn).attr('is_liked','false')
    $(btn).find('.heart-logo').removeClass('font-color-red fa-solid')
    $(btn).find('.heart-logo').addClass('fa-regular')
    count = parseInt($(btn).find('.likes-count').text())
    if(!isNaN(count)){
        $(btn).find('.likes-count').text(count-1)
    }
}
function set_to_like_btn(btn){
    console.log('change el:')
    console.log(btn)
    $(btn).attr('is_liked','true')
    $(btn).find('.heart-logo').removeClass('fa-regular')
    $(btn).find('.heart-logo').addClass('font-color-red fa-solid')

    count = parseInt($(btn).find('.likes-count').text())
    console.log('count:'+count)
    if(!isNaN(count)){
        $(btn).find('.likes-count').text(count+1)
    }
}

function set_delete_status_btn(){
    $('.delete-status-btn').each(function(){
        console.log('find delete btn')
        console.log(this)
        $(this).on('click',function(e){
            var btn = e.currentTarget;
            console.log('click delete btn')
            
            $(btn).siblings('.delete-status-form').find("input[type='submit']").trigger('click')
        })
    })
    set_delete_status_form()
}
function set_delete_status_form(){
    
    $('.delete-status-form').each(function(){
        $(this).on('submit',function(e){
            e.preventDefault()
            var form = $(this)
            var actionUrl = form.attr('action')
            is_confirmed = confirm('Do you want to delete this status?')
            if(is_confirmed){
    
                $.ajax({
                    type:"POST",
                    url:actionUrl,
                    data:form.serialize(),
                    success:function(data){
                        alert('Status Deleted!')
                        window.location.reload()                    
                    },
                    error:function(result){
                        alert('something wrong,see console')
                        console.log(result.responseText) 
                    }                   
                })
            }
        })
    })
}
function remove_delete_status_button(){
    $('.delete-status-btn').each(function(){
        $(this).remove()
    })
}