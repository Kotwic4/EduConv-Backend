# API
  ## model
      /model
  method: POST
  data: keras layers in json
  
  json format: 
```
{
    "dataset":"dataset_name",
    "layers":[
                {
                    "layer_name":layername,"args":{arg_name:arg_value,...
                },
                ...
             ]
}
```
 returns: model_id

    /model/<model_id>/train
    
   method: POST
   required JSON (might be empty)
   returns: nothing important
  
  trains model previously sent to /model and saves results locally
  
    /model/<model_id>/<filename>
    
  method: GET
  
  returns: file with given filename from model files
  
  ## datasets
  
    /data
    
  method: GET
  
  returns: list of supported datasets (e.g. \["mnist","cifar-10"]) 
  
    /data/<dataset>/<image_id>
  
  method: GET
  
  returns: json map representing image from dataset
  
    /data/<dataset>/bitmaps/<image_id>
    
  method: GET
  
  returns: image as jpg file