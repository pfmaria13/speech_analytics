function start() {
    self.location.href='audio/withoutstart';
}
function stop() {
   self.location.href='withoutstop'
}

//function start2() {
//    var button = document.getElementsByName('mybtn1');
//    var text = document.getElementsByName('record');
//    if ( button.getAttribute('data-show') === "false") {
//        text.innerText = "ЗАКОНЧИТЬ ЗАПИСЬ";
//        button.setAttribute('data-show', "true");
//        self.location.href='audio/withoutstart';
//    }
//    else {
//        self.location.href='withoutstop';
//    }
//}

function fun1() {
    var rad=document.getElementsByName('state-d');
    for (var i=0;i<rad.length; i++) {
      if (rad[i].checked) {
          if (i==0) {
              self.location.href='without'
          };
          if (i==1) {
              self.location.href='mine'
          };
          if (i==2) {
              self.location.href='ready'
          };
      };
    };
}
$(".btn.third").click(function(){
  $(this).prop('disabled',true)
});