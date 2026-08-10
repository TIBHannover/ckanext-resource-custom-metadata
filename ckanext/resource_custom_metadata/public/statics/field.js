$(document).ready(function(){

  /* 
    Material/Material combination autocomplete
  */
  let materials = [
          {value : "Aluminium" , data: "Aluminium"},
          {value : "Kupfer" , data: "Kupfer"},
          {value : "Stahl" , data: "Stahl"},
          {value : "Titan" , data: "Titan"},
          {value : "Titan_Pulver" , data: "Titan_Pulver"}
        ];
  $('.input-material_combination_').autocomplete({lookup:materials});

  /* 
    data types autocomplete
  */
    let dataTypes = [
      {value : "Mech.-Eigenschaften" , data: "Mech.-Eigenschaften"},
      {value : "Phys.-Eigenschaften" , data: "Phys.-Eigenschaften"}
    ];
  $('.input-data_type_').autocomplete({lookup:dataTypes});

  
  /* 
    surface prepration autocomplete
  */
    let surfaces = [
      {value : "Oberflächenbehandlung" , data: "Oberflächenbehandlung"},
      {value : "Buersten" , data: "Buersten"},
      {value : "Chemisch" , data: "Chemisch"},
      {value : "Plasma" , data: "Plasma"},
      {value : "Schleifen" , data: "Schleifen"},
      {value : "Unbehandelt" , data: "Unbehandelt"}
    ];
  $('.input-surface_preparation_').autocomplete({lookup:surfaces});


   /* 
    Atmosphere autocomplete
  */
    let atmospheres = [
      {value : "Ar" , data: "Ar"},
      {value : "Ar-Silan" , data: "Ar-Silan"},
      {value : "H2" , data: "H2"},
      {value : "H2-Silan" , data: "H2-Silan"},
      {value : "Schleifen" , data: "Schleifen"},
      {value : "Normal-O2" , data: "Normal-O2"}
    ];
  $('.input-atmosphere_').autocomplete({lookup:atmospheres});

  const autocompleteLookups = {
    material_combination_: materials,
    data_type_: dataTypes,
    surface_preparation_: surfaces,
    atmosphere_: atmospheres
  };

  function addMetadataRow(group) {
    const $group = $(group);
    const template = $group.find('template[data-metadata-row-template]')[0];
    const index = parseInt($group.attr('data-next-index'), 10);
    const inputName = $group.attr('data-input-name');
    const html = template.innerHTML.replace(/__INDEX__/g, String(index));
    const $row = $(html);

    $group.find('[data-metadata-rows]').append($row);
    $group.attr('data-next-index', index + 1);

    if (autocompleteLookups[inputName]) {
      $row.find('.input-' + inputName).autocomplete({
        lookup: autocompleteLookups[inputName]
      });
    }

    // Keep resource choices already used by another row unavailable.
    $row.find('.resource-box').each(function () {
      const resource = this;
      $('.resource-box:checked').each(function () {
        if ($(this).val() === $(resource).val() &&
            $(this).attr('field_name') === $(resource).attr('field_name')) {
          $(resource).parent().hide();
        }
      });
    });
  }

  $(document).on('click', '[data-add-metadata-row]', function () {
    addMetadataRow($(this).closest('[data-metadata-field-group]'));
  });
});
