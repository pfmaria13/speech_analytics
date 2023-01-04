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