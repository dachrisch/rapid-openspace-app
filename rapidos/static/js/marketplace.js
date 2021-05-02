var addPanel = function (location_name, location_id){
    console.log('addPanel  ' + location_name)
    var myCol = $('<div class="col-sm-3 col-md-3 pb-2"></div>');
    var myPanel = $('<div class="card card-outline-info" id="'+location_name+'Panel"><div class="card-block"><div class="card-title"><span>Location #'+location_name+'</span><button type="button" class="close" data-target="#'+location_name+'Panel" data-dismiss="alert"><span class="float-right"><i class="fa fa-remove"></i></span></button></div><p>'+location_id+' </p><img src="/static/images/placeholder.svg" class="rounded rounded-circle"></div></div>');
    myPanel.appendTo(myCol);
    myCol.appendTo('#contentPanel');
    $('.close').on('click', function(e){
      e.stopPropagation();
          var $target = $(this).parents('.col-sm-3');
          $target.hide('slow', function(){
            $target.remove();
          });
    });
};

var createLocation = function (rapidos_id, location_name){
    let url = `/api/rapidos/${rapidos_id}/locations`
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify({'name' : location_name}),
      success: function(res) {
        addPanel(res['name'], res['id'])

        console.log(res)
      },
      contentType: "application/json",
      dataType: "json"
    });
}

$('#add_session_button').click(function() {
    let s_location = $('#session_location').val()
    let rapidos_id = $('#rapidos_id').val()

    createLocation(rapidos_id, s_location)
});
