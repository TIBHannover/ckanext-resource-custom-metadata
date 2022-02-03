$(document).ready(function(){
    /**
     * Add new metadata input field for material combination
     * 
     */
     $('#material_combination_box_1').show();
     $('#mat_comb').click(function(){
       let all_visible = false;
       for(let i=1; i <= $('.material-comb-box').length; i++){
         if ($('#material_combination_box_' + i).is(':hidden')){
           $('#material_combination_box_' + i).fadeIn();
           all_visible = true;
           break;
         }
       }
      //  if(!all_visible){
      //    $(this).hide();
      //  }
     });

     /**
     * Add new metadata input field for surface preparation
     * 
     */
      $('#surface_preparation_box_1').show();
      $('#surface_preparation_new').click(function(){
        let all_visible = false;
        for(let i=1; i <= $('.surface-preparation-box').length; i++){
          if ($('#surface_preparation_box_' + i).is(':hidden')){
            $('#surface_preparation_box_' + i).fadeIn();
            all_visible = true;
            break;
          }
        }
        if(!all_visible){
          $(this).hide();
        }
      });

      /**
     * Add new metadata input field for Atmosphere
     * 
     */
       $('#atmosphere_box_1').show();
       $('#atmosphere_new').click(function(){
         let all_visible = false;
         for(let i=1; i <= $('.atmosphere-box').length; i++){
           if ($('#atmosphere_box_' + i).is(':hidden')){
             $('#atmosphere_box_' + i).fadeIn();
             all_visible = true;
             break;
           }
         }
         if(!all_visible){
           $(this).hide();
         }
       });

       /**
     * Add new metadata input field for Data Type
     * 
     */
        $('#data_type_box_1').show();
        $('#data_type_new').click(function(){
          let all_visible = false;
          for(let i=1; i <= $('.data-type-box').length; i++){
            if ($('#data_type_box_' + i).is(':hidden')){
              $('#data_type_box_' + i).fadeIn();
              all_visible = true;
              break;
            }
          }
          if(!all_visible){
            $(this).hide();
          }
        });

     /**
     * Add new metadata input field for Analysis Method
     * 
     */
      $('#analysis_method_box_1').show();
      $('#analysis_method_new').click(function(){
        let all_visible = false;
        for(let i=1; i <= $('.analysis-method-box').length; i++){
          if ($('#analysis_method_box_' + i).is(':hidden')){
            $('#analysis_method_box_' + i).fadeIn();
            all_visible = true;
            break;
          }
        }
        if(!all_visible){
          $(this).hide();
        }
      });
});