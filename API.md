# API
  ## scheme
  ### create new scheme
  #### url
  ```
  /scheme
  ```
  #### method
  POST
  #### body
  ```
  {
    "layers":[
      {
        "layer_name":layername,
        "args":{
          arg_name:arg_balue,
          ...
        }
      },
      ...
    ]
  }
  ```
  #### returns
  ```
  {
      "id":schema_id
      "scheme_json":input.json (as it was sent)
    },
  ```
  ### get all schema
  #### url
  ```
  /scheme/<schema_id>
  ```
  #### method
  GET

  #### returns
  ```
  {
      "id":schema_id
      "scheme_json":input.json (as it was sent)
    },
  ```
  ### get all schema
  #### url
  ```
  /scheme
  ```
  #### method
  GET
  
  #### returns
  ```
  [
    {
      "id":schema_id
      "scheme_json":input.json (as it was sent)
    },
    ...
  ]
  ```
  ## model
  ### create new model and start training
  #### url 
  ```
  /model
  ```
  #### method
  POST
  #### body
  ```
  {
    "scheme_id":schema_id
    "dataset":"dataset_name",
    "epochs":"epochs_number",
    "batch_size":"batch_size_number",
  }
  ```
  #### returns
  ```
  {
    "id":model_id
    "dataset":"dataset_name",
    "epochs_learnt":"epochs_number",
    "epochs_to_learn":"epochs_number",
  }
  ```
  ### get model info
  #### url
  ```
  /model/<model_id>
  ```
  #### method
  GET
  #### returns
  ```
  {
    "id":model_id
    "dataset":"dataset_name",
    "epochs_learnt":"epochs_number",
    "epochs_to_learn":"epochs_number",
  }
  ```
  ### get model list
  #### url
  ```
  /model
  ```
  #### method
  GET
  #### returns
  ```
  [
    {
      "id":model_id
      "dataset":"dataset_name",
      "epochs_learnt":"epochs_number",
      "epochs_to_learn":"epochs_number",
    },
    ...
  ]
  ```
  ### get model list
  #### url
  ```
  /model/<model_id>/file/<filename>
  ```
  #### method 
  GET
  #### returns
  file with given filename from model files
  
  ## datasets
  
  ### create new scheme
  #### url
  ```
  /data/<dataset_id>
  ```
  #### method
  GET
  #### returns
  ```
  {
    "id": id
    "name":name,
    "train_images_count": files_numer,
    "img_width": pixel_number,
    "img_height": pixel_number,
    "img_depth": channels_number,
    "labels":[
      label_1,
      label_2,
      label_3,
      ...
    ]
  }
  ```
  
  ### get dataset list
  #### url
  ```
  /data
  ```
  #### method 
  GET
  #### returns
  ```
  [
    {
      "id": id,
      "name":name,
      "train_images_count": files_numer,
      "img_width": pixel_number,
      "img_height": pixel_number,
      "img_depth": channels_number,
      "labels":[
        label_1,
        label_2,
        label_3,
        ...
      ]
    },
    ...
  ]
  ```
  ### get file as jpg
  #### url
  ```
  /data/<dataset_id>/<image_id>/bitmaps
  ```
  #### method
  GET
  #### returns
  image as jpg file
