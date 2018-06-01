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
___
    /model/<model_id>/train
    
method: POST
required JSON (might be empty)
optional arguments:
   - epochs - number of epochs
   - batch_size
   
returns: nothing important
trains model previously sent to /model and saves results locally
___
  
    /model/<model_id>/<filename>
    
  method: GET
  returns: file with given filename from model files

___
    /model/info/<model_no>
  method: GET
  returns: json with model info. You may expect following fields in json:
  - "dataset"  (value is dataset name)
  - "epochs_learnt"
  - "epochs_to_learn"

  ## datasets
  
    /data
    
  method: GET
  returns: list of supported datasets (e.g. \["mnist","cifar-10"]) 
___
    /data/<dataset>/info
  method: GET
  returns: json with dataset info. You may expect following fields in json:
 - "name"
 - "train_images_count"
 - "test_images_count"
 - "img_width" (in pixels)
 - "img_height" (in_pixels)
 - "img_depth"
 - "labels" (json_array with strings)
  ___
    /data/<dataset>/<image_id>
  
  method: GET
  returns: json map representing image from dataset
  ___
    /data/<dataset>/bitmaps/<image_id>
    
  method: GET
  returns: image as jpg file