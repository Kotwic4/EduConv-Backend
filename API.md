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
    "name": model_name
    "model_json":
    {
      "layers": [
        {
          "layer_name": layer_name,
          "args":{
            arg_name: arg_value,
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
      "id": model_id
      "model_json": input_json (as it was sent)
      "name": model_name
  },
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
      "id": model_id
      "model_json": input_json (as it was sent)
      "name": model_name
  },
  ```
  ### get all models info
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
      "id": model_id
      "model_json": input_json (as it was sent)
      "name": model name
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
    "model_id": model_id,
    "dataset": dataset_name,
    "name": trained_model_name,
    "params":
    {
      "epochs": epochs_number,
      "batch_size": batch_size_number
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
            label1,
            label2,
            ...
        ],
        "name": dataset_name,
        "test_images_count": test_images_count,
        "train_images_count": train_images_count
    },
    "epochs_learnt": epochs_learnt,
    "epochs_to_learn": epochs_to_learn,
    "batch_size": batch_size_number,
    "id": trained_model_id,
    "name": trained_model_name,
    "model_id": model_id,
    "epochs_data": {
      epoch_number: {
        "acc": acc_value,
        "loss": loss_value,
      }
      ...
    }
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
    "dataset": {
        "id": datasset_id,
        "img_depth": number_of_colors,
        "img_height": img_height,
        "img_width": img_width,
        "labels": [
            label1,
            label2,
            ...
        ],
        "name": dataset_name,
        "test_images_count": test_images_count,
        "train_images_count": train_images_count
    },
    "epochs_learnt": epochs_learnt,
    "epochs_to_learn": epochs_to_learn,
    "batch_size": batch_size_number,
    "id": trained_model_id,
    "name": trained_model_name,
    "model_id": model_id,
    "epochs_data": {
      epoch_number: {
        "acc": acc_value,
        "loss": loss_value,
      }
      ...
    }
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
        "dataset": {
            "id": datasset_id,
            "img_depth": number_of_colors,
            "img_height": img_height,
            "img_width": img_width,
            "labels": [
                label1,
                label2,
                ...
            ],
            "name": dataset_name,
            "test_images_count": test_images_count,
            "train_images_count": train_images_count
        },
        "epochs_learnt": epochs_learnt,
        "epochs_to_learn": epochs_to_learn,
        "batch_size": batch_size_number,
        "id": trained_model_id,
        "name": trained_model_name,
        "model_id": model_id,
        "epochs_data": {
          epoch_number: {
            "acc": acc_value,
            "loss": loss_value,
          }
          ...
        }
      }
    ...
  ]
  ```
  ### get trained_model list
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
  ```
  /data/<dataset_id>/label/<image_id>
  ```
  #### method
  GET
  #### params:
  imageset=[train|test]
  #### returns
  ```
  {
     "label": label
  }
  ```
