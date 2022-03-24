document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message == ""){
        return
    }
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
    $('#text-input-container .emoji-wysiwyg-editor').empty()
    $("#chat-log-container").animate({ scrollTop: $('#chat-log-container').prop("scrollHeight") }, 1000);

};