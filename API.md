# API
  ## model
  ### create new model
  #### url
  ```
  /model
  ```
  #### method
  POST
  #### body
  ```
  {
    "name": "model name"
    "model_json":
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
  }
  ```
  #### returns
  ```
  {
      "id":schema_id
      "model_json":input.json (as it was sent)
      "name": "model name"
  },
  ```
  ### get all schema
  #### url
  ```
  /model/<schema_id>
  ```
  #### method
  GET

  #### returns
  ```
  {
      "id":schema_id
      "model_json":input.json (as it was sent)
      "name": "model name"
  },
  ```
  ### get all schema
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
      "id":schema_id
      "model_json":input.json (as it was sent)
      "name": "model name"
    },
    ...
  ]
  ```
  ## trained_model
  ### create new trained_model and start training
  #### url 
  ```
  /trained_model
  ```
  #### method
  POST
  #### body
  ```
  {
    "model_id":schema_id,
    "dataset":"dataset_name",
    "name":"trained_model name",
    "params":
    {
      "epochs":epochs_number,
      "batch_size":batch_size_number
    }
  }
  ```
  #### returns
  ```
  {
    "dataset": {
        "id": datasset_id,
        "img_depth": number_of_colors,
        "img_height": img_height,
        "img_width": img_width,
        "labels": [
            "list",
            "of",
            "possible",
            "labels"
        ],
        "name": "dataset name",
        "test_images_count": test_images_count,
        "train_images_count": train_images_count
    },
    "epochs_learnt": epochs_learnt,
    "epochs_to_learn": epochs_to_learn,
    "id": id,
    "name": "trained_model name"
}
  ```
  ### get trained_model info
  #### url
  ```
  /trained_model/<trained_model_id>
  ```
  #### method
  GET
  #### returns
  ```
  {
    "id":trained_model_id,
    "name":"trained_model name",
    "dataset": {
        "id": id,
        "name":name,
        "train_images_count": train_images_count,
        "test_images_count": files_number,
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
    "epochs_learnt":epochs_number,
    "epochs_to_learn":epochs_number,
  }
  ```
  ### get trained_model list
  #### url
  ```
  /trained_model
  ```
  #### method
  GET
  #### returns
  ```
  [
    {
      "id":trained_model_id,
      "name":"trained_model name"
      "dataset": {
        "id": id,
        "name":name,
        "train_images_count": files_numer,
        "test_images_count": files_numer,
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
      "epochs_learnt":"epochs_number",
      "epochs_to_learn":"epochs_number",
    },
    ...
  ]
  ```
  ### get trained_model file
  #### url
  ```
  /trained_model/<trained_model_id>/file/<filename>
  ```
  #### method 
  GET
  #### returns
  file with given filename from trained_model files
  
  ## datasets
  
  ### create new model
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
    "test_images_count": files_numer,
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
      "test_images_count": files_numer,
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
  ### get file as bmp
  #### url
  ```
  /data/<dataset_id>/bitmaps/<image_id>
  ```
  #### method
  GET
  #### params:
  imageset=[train|test]
  #### returns
  image as bmp file
  
  /data/<dataset_id>/label/<image_id>
  ```
  #### method
  GET
  #### params:
  imageset=[train|test]
  #### returns
  ```
  {
     "label":label
  }
  ```
