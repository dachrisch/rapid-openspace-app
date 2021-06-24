
var addColumn = function (location_id, location_name) {
    console.log('add location ' + location_name);
    var th_loc_id = 'loc_' + location_id
    var column = $('<th class="location" id="'+th_loc_id+'">' + location_name + '</th>')
    var close_button = $('<button id="close_'+th_loc_id+'" type="button" class="close" data-target="#'+th_loc_id+'" data-dismiss="alert"><span class="float-right"><i class="fa fa-remove"></i></span></button>')
    close_button.appendTo(column)
    column.appendTo('#marketplace_locations')
    $('.close').on('click', function(e){
        e.stopPropagation();
        var $target = $(this).parents('.location');
        console.log('remove location ' + $target[0].id)
        $target.hide('slow', function(){
            $target.remove();
            deleteLocation($target[0].id.replace('loc_', ''))
        });
    });
};

var addRow = function (timeslot_id, timeslot_start, timeslot_duration) {
    console.log('add timeslot ' + timeslot_start);
    var tr_slot_id = 'loc_' + timeslot_id
    var row = $('<tr><td class="timeslot" id="'+tr_slot_id+'">' + timeslot_start + '</td></tr>')
    row.appendTo('#marketplace_timeslots')
}
var deleteLocation = function (location_id){
    let rapidos_id = $('#rapidos_id').val()
    let url = `/api/rapidos/${rapidos_id}/locations/${location_id}`
    $.ajax({
      type: "DELETE",
      url: url,
      success: function(res) {
        console.log('deleted location ' +location_id)
      },
      contentType: "application/json",
      dataType: "json"
    });
};
var createLocation = function (rapidos_id, location_name){
    let url = `/api/rapidos/${rapidos_id}/locations`
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify({'name' : location_name}),
      success: function(res) {
        addColumn(res['id'], res['name'])
        console.log('created location ' + res['name'] +', ' + res['id'])
      },
      contentType: "application/json",
      dataType: "json"
    });
}

var createTimeslot = function (rapidos_id, timeslot_start, timeslot_duration){

    addRow(rapidos_id, timeslot_start, timeslot_duration)
}

$('#add_location_button').click(function() {
    let s_location = $('#session_location').val()
    let rapidos_id = $('#rapidos_id').val()

    createLocation(rapidos_id, s_location)
});

$('#add_timeslot_button').click(function() {
    let timeslot_start = $('#timeslot_start_time').val()
    let timeslot_duration = $('#timeslot_duration').val()
    let rapidos_id = $('#rapidos_id').val()

    createTimeslot(rapidos_id, timeslot_start, timeslot_duration)
});
