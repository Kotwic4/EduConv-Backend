# API
  ## model
    /model
  method: POST
  
  data: keras layers in json
  
  json format: 
{"layers":[{"layer_name":layername,"args":{arg_name:arg_balue,...},...]}

 returns: model_id

    /model/<model_id>/<train>
    
  method: POST
  
  no data required
  
  returns: nothing important
  
  trains model previously sent to /model and saves results locally
  
    /model/<model_id>/<filename>
    
  method: GET
  
  returns: file with given filename from model files
  
  ## datasets
  
    /data/<dataset>/<image_id>
  
  method: GET
  
  returns: json map representing image from dataset
  
    /data/<dataset>/bitmaps/<image_id>
    
  method: GET
  
  returns: image as jpg file