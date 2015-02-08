$(document).ready(function(){
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var $update = $("#update");
  var $result = $("#result");
  var $folding = $(".folding");

  socket.on('update', function(msg) {
    $result.html(msg);
  });

  socket.on('detail', function(ret) {
    var $link = $("#" + ret.id);
    $link.siblings("div.content").removeClass("hidden");
    $link.siblings("div.content").html(ret.data);
    $link.siblings("a.folding").removeClass("hidden");
  });

  $update.click(function(){
    socket.emit('update');
  });

  function _folding(obj){
    $(obj).addClass("hidden");
    $(obj).siblings("div.content").addClass("hidden");
  }

  function _link_click(obj){
    var path = $(obj).attr("path");
    var id = $(obj).attr("id");
    socket.emit('detail', path, id);
  }

  link_click = _link_click;
  folding = _folding;
});
