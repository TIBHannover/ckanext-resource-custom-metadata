$(document).ready(function(){

    /**
     * Add new metadata input field for material combination
     * 
     */
     $('#material_comb_box_1').show();
     $('#mat_comb').click(function(){
       let all_visible = false;
       for(let i=1; i <= $('.material-comb-box').length; i++){
         if ($('#material_comb_box_' + i).is(':hidden')){
           $('#material_comb_box_' + i).fadeIn();
           all_visible = true;
           break;
         }
       }
       if(!all_visible){
         $(this).hide();
       }
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
});