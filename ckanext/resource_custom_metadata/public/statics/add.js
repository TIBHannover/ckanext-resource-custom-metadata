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


    /**
     * click the select all checkbox
     * 
     */
     $('.select-all-resources').click(function(){
        let id = $(this).attr('id');
        field_name_box_and_id = $(this).attr('id').split('select-all-resources-')[1];
        let checkBoxes = $('.resource-checkbox-input-' + field_name_box_and_id);
        for(let i=0; i < checkBoxes.length; i++){
            if($(checkBoxes[i]).is(':visible')){
              if($(checkBoxes[i]).prop('checked') == !($(this).prop('checked'))){
                  $(checkBoxes[i]).click();
              }
            }
        }
    });


     /**
     * hide a resource from other modals when the resource is chosen for one metadata in a modal
     * 
     */

      let resources =  $('.resource-box');
      for(let i=0; i < resources.length; i++){
        if($(resources[i]).prop('checked') == true){
          $(".resource-box[value=" + $(resources[i]).val() + "]").parent().hide();
        }
      }
      for(let i=0; i < resources.length; i++){
        if($(resources[i]).prop('checked') == true){          
          $(resources[i]).parent().show();  
        }
      }

      $('.resource-box').click(function(){
          let resources_checkbox = $('.resource-box');
          for(let i=0; i < resources_checkbox.length; i++){
              if($(resources_checkbox[i]).val() ===  $(this).val() && $(resources_checkbox[i]).attr('field_name') ===  $(this).attr('field_name')){
                if($(this).prop('checked') == true){
                  $(resources_checkbox[i]).parent().hide();    
                }
                else{
                  $(resources_checkbox[i]).parent().show();
                }
              }
          }

          if($(this).prop('checked') == true){
            $(this).parent().show();          
          }
          
      });

});