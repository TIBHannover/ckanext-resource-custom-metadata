$(document).ready(function(){

    /**
     * remove a field box
     * 
     */
    $('.box-remove-anchor').click(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        field_name_box = $(this).attr('id').split('remove_')[0];
        // hide the field box
        $('#' + field_name_box + id).fadeOut(); 
        
        // unselect the checkboxes
        field_name = $(this).attr('id').split('box_remove_')[0];
        let checkBoxes = $('.resource-checkbox-input-' + field_name + id);
        for(let i=0; i < checkBoxes.length; i++){
            if($(checkBoxes[i]).prop('checked') == true){
              $(checkBoxes[i]).click();
            }
        }
        
        // unselect the select-all 
        if($('#select-all-resources-' + field_name + id).prop('checked') == true){
          $('#select-all-resources-' + field_name + id).click();
        }

        $('#' + field_name + id).val('');
        
    });

});