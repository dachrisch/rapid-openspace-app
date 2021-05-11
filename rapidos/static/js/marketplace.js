
var addColumn = function (location_name, location_id) {
    console.log('add location ' + location_name);
    var th_loc_id = 'loc_' + location_id
    var column = $('<th class="location" id="'+th_loc_id+'">' + location_name + '</th>')
    var close_button = $('<button type="button" class="close" data-target="#'+th_loc_id+'" data-dismiss="alert"><span class="float-right"><i class="fa fa-remove"></i></span></button>')
    close_button.appendTo(column)
    column.appendTo('#marketplace_locations')
    $('.close').on('click', function(e){
        e.stopPropagation();
        var $target = $(this).parents('.location');
        console.log('remove location ' + $target[0].id)
        $target.hide('slow', function(){
            $target.remove();
            deleteLocation($target[0].id)
        });
    });
};
var deleteLocation = function (location_id){
        console.log('deleted location ' +location_id)
};
var createLocation = function (rapidos_id, location_name){
    let url = `/api/rapidos/${rapidos_id}/locations`
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify({'name' : location_name}),
      success: function(res) {
        addColumn(res['name'], res['id'])
        console.log('created location ' + res['name'] +', ' + res['id'])
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
