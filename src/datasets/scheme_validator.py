import json

from src.exceptions.invalid_usage import InvalidUsage


class ModelValidator:
    ACTIVATIONS = ["linear", "softmax", "relu", "elu", "tanh"]

    @staticmethod
    def check_activation_field(value, errors):
        if value not in ModelValidator.ACTIVATIONS:
            errors.append(f'Unknown activation type: {value}')

    @staticmethod
    def check_kernel_field(value, errors):
        if value[0] <= 0 or value[1] <= 0:
            errors.append(f'Kernel dimensions must be positive')

    @staticmethod
    def check_strides_field(value, errors):
        if value[0] <= 0 or value[1] <= 0:
            errors.append(f'Strides dimensions must be positive')

    @staticmethod
    def check_filters_field(value, errors):
        if value <= 0:
            errors.append(f'Filters value must be positive')

    @staticmethod
    def check_units_field(value, errors):
        if value <= 0:
            errors.append(f'Units value must be positive')

    @staticmethod
    def check_rate_field(value, errors):
        if value <= 0 or value > 1:
            errors.append(f'Rate value must be positive and less than 1')

    @staticmethod
    def check_pool_size_field(value, errors):
        if value[0] <= 0 or value[1] <= 0:
            errors.append(f'Pool size dimensions must be positive')

    @staticmethod
    def check_momentum_field(value, errors):
        if value <= 0 or value > 1:
            errors.append(f'Momentum value must be positive and less than 1')

    @staticmethod
    def check_epsilon_field(value, errors):
        if value <= 0 or value > 1:
            errors.append(f'Epsilon value must be positive and less than 1')

    @staticmethod
    def check_axis_field(value, errors):
        if type(value) != int:
            errors.append(f'Axis must be an int')

    @staticmethod
    def validate_conv_layer(args, conds):
        errors = []
        if conds['was_flatten']:
            errors.append('Conv layers can only be before flatten')
        if not set(args.keys()).issuperset(['kernel_size', 'filters']):
            errors.append('Conv layers must have kernel_size and filters')
        for arg in args:
            value = args[arg]
            switcher = {
                'kernel_size': lambda: ModelValidator.check_kernel_field(value, errors),
                'strides': lambda: ModelValidator.check_strides_field(value, errors),
                'filters': lambda: ModelValidator.check_filters_field(value, errors),
                'activation': lambda: ModelValidator.check_activation_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for conv layer'))()
        conds['was_conv'] = True
        conds['was_activation'] = False
        conds['was_pooling'] = False
        conds['was_dropout'] = False
        conds['was_batch_normalization'] = False
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_flatten_layer(args, conds):
        errors = []
        if conds['was_flatten']:
            errors.append('There can be only one flatten in scheme')
        for arg in args:
            errors.append(f'Unknown property: {arg} for flatten layer')
        conds['was_flatten'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_activation_layer(args, conds):
        errors = []
        if conds['was_activation']:
            errors.append('There can be only one activation between active layers')
        if 'activation' not in args:
            errors.append('Activation property is mandatory in activation layer')
        for arg in args:
            value = args[arg]
            switcher = {
                'activation': lambda: ModelValidator.check_activation_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for activation layer'))()
        conds['was_activation'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_dense_layer(args, conds):
        errors = []
        if not conds['was_flatten']:
            errors.append('Dense layers can only be after flatten')
        if not set(args.keys()).issuperset(['units']):
            errors.append('Dense layers must have units')
        for arg in args:
            value = args[arg]
            switcher = {
                'units': lambda: ModelValidator.check_units_field(value, errors),
                'activation': lambda: ModelValidator.check_activation_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for dense layer'))()
        conds['was_dense'] = True
        conds['was_activation'] = False
        conds['was_pooling'] = False
        conds['was_dropout'] = False
        conds['was_batch_normalization'] = False
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_batch_normalization_layer(args, conds):
        errors = []
        if conds['was_batch_normalization']:
            errors.append('There can be only one batch normalization between active layers')
        for arg in args:
            value = args[arg]
            switcher = {
                'axis': lambda: ModelValidator.check_axis_field(value, errors),
                'momentum': lambda: ModelValidator.check_momentum_field(value, errors),
                'epsilon': lambda: ModelValidator.check_epsilon_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for batch normalization layer'))()
        conds['was_batch_normalization'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_max_pooling_layer(args, conds):
        errors = []
        if conds['was_pooling']:
            errors.append('There can be only one pooling between active layers')
        for arg in args:
            value = args[arg]
            switcher = {
                'pool_size': lambda: ModelValidator.check_pool_size_field(value, errors),
                'strides': lambda: ModelValidator.check_strides_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for max pooling layer'))()
        conds['was_pooling'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_average_pooling_layer(args, conds):
        errors = []
        if conds['was_pooling']:
            errors.append('There can be only one pooling between active layers')
        for arg in args:
            value = args[arg]
            switcher = {
                'pool_size': lambda: ModelValidator.check_pool_size_field(value, errors),
                'strides': lambda: ModelValidator.check_strides_field(value, errors),
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for average pooling layer'))()
        conds['was_pooling'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_dropout_layer(args, conds):
        errors = []
        if conds['was_dropout']:
            errors.append('There can be only one dropout between active layers')
        for arg in args:
            value = args[arg]
            switcher = {
                'rate': lambda: ModelValidator.check_rate_field(value, errors)
            }
            switcher.get(arg, lambda: errors.append(f'Unknown property: {arg} for dropout layer'))()
        conds['was_dropout'] = True
        if len(errors) != 0:
            return errors
        return None

    @staticmethod
    def validate_layer(layer, conds):
        name = layer.get('layer_name')
        args = layer.get('args')
        switcher = {
            'Conv2D': lambda: ModelValidator.validate_conv_layer(args, conds),
            'Dense': lambda: ModelValidator.validate_dense_layer(args, conds),
            'Activation': lambda: ModelValidator.validate_activation_layer(args, conds),
            'Dropout': lambda: ModelValidator.validate_dropout_layer(args, conds),
            'Flatten': lambda: ModelValidator.validate_flatten_layer(args, conds),
            'MaxPooling2D': lambda: ModelValidator.validate_max_pooling_layer(args, conds),
            'AveragePooling2D': lambda: ModelValidator.validate_average_pooling_layer(args, conds),
            'BatchNormalization': lambda: ModelValidator.validate_batch_normalization_layer(args, conds),
        }
        return switcher.get(name, lambda: [f'Unknown layer type: {layer}'])()

    @staticmethod
    def add_error(errors, index, msg):
        if index not in errors:
            errors[index] = []
        errors[index].append(msg)

    @staticmethod
    def validate_model(model):
        model_json = json.loads(model.model_json)
        layers = model_json.get('layers')
        layers_size = len(layers)
        if layers is None or len(layers) == 0:
            raise InvalidUsage("Scheme do not have layers config", status_code=400)

        errors = {}
        conds = {
            'was_flatten': False,
            'was_dense': False,
            'was_conv': False,
            'was_activation': False,
            'was_pooling': False,
            'was_dropout': False,
            'was_batch_normalization': False,
        }

        for i in range(layers_size):
            layer = layers[i]
            layer_errors = ModelValidator.validate_layer(layer, conds)
            if layer_errors:
                errors[i] = layer_errors

        last_index = layers_size - 1
        if not conds['was_dense']:
            ModelValidator.add_error(errors, last_index, "There must be dense layer in scheme")
        if not conds['was_flatten']:
            ModelValidator.add_error(errors, last_index, "There must be flatten layer in scheme")

        if len(errors):
            raise InvalidUsage("Scheme not valid", status_code=400, payload={'errors': errors})
