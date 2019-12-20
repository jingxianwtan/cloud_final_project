try {
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var recognition = new SpeechRecognition();
}
catch(e) {
    console.error(e);
}


var noteTextarea = $('#searchRequest');
var instructions = $('#recording-instructions');

var noteContent = '';

recognition.continuous = true;

recognition.onresult = function(event) {

    // event 是一个SpeechRecognitionEvent 对象
    // 保存了所有历史捕获对象
    // 我们只取当前的内容
    var current = event.resultIndex;

    // 获取此前所说话的记录
    var transcript = event.results[current][0].transcript;

    // 将当前记录添加到笔记内容中
    // 解决安卓设备的bug
    var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript);

    if(!mobileRepeatBug) {
        noteContent += transcript;
        noteTextarea.val(noteContent);
    }
};

recognition.onstart = function() {
    instructions.text('Recording Now');
}

recognition.onspeechend = function() {
    instructions.text('Finished Recording');
}

recognition.onerror = function(event) {
    if(event.error == 'no-speech') {
        instructions.text('speak again');
    };
}

function toggleVoice(e) {
    if (e.className == "ON") {
        e.className = "OFF";
        if (noteContent.length) {
            noteContent += ' ';
        }
        recognition.start();
    } else {
        e.className = "ON";
        recognition.stop();
    }
}

noteTextarea.on('input', function() {
    noteContent = $(this).val();
})

$('#submit').on('click', function(e) {
    recognition.stop();

    if(!noteContent.length) {
        instructions.text('Could not search empty input');
    }
    else {

        // 重置变量，更新界面
        noteContent = '';
        noteTextarea.val('');
    }

})
