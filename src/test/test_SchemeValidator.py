from src.models.db_models import *
from src.datasets.scheme_validator import *
import unittest


class TestModelValidator(unittest.TestCase):
    def setUp(self):
        MODELS = [NNModel, NNTrainedModel, Dataset]
        # use an in-memory SQLite for tests.
        self.conds = {
            'was_flatten': False,
            'was_dense': False,
            'was_conv': False,
            'was_activation': False,
            'was_pooling': False,
            'was_dropout': False,
            'was_batch_normalization': False}
        self.expected_conds = {
            'was_flatten': False,
            'was_dense': False,
            'was_conv': False,
            'was_activation': False,
            'was_pooling': False,
            'was_dropout': False,
            'was_batch_normalization': False}
        self.valid_conv_layer = {"kernel_size": [3, 3], "filters": 30}
        self.valid_flatten_layer = {}
        self.valid_activation_layer = {'activation': 'softmax'}
        self.valid_dense_layer = {'units': 10}
        self.valid_normalization_layer = {}
        self.valid_max_pooling_layer = {}
        self.valid_avg_pooling_layer = {}
        self.valid_dropout_layer = {"rate": 0.1}

    def test_conv_valid(self):
        self.expected_conds['was_conv'] = True
        errors = ModelValidator.validate_conv_layer(self.valid_conv_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_flatten_before_conv(self):
        self.expected_conds['was_conv'] = True
        self.expected_conds['was_flatten'] = True
        self.conds['was_flatten'] = True
        errors = ModelValidator.validate_conv_layer(self.valid_conv_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_conv_no_kernel_size(self):
        self.expected_conds['was_conv'] = True
        conv_layer = {"kernel_size": [3, 3]}
        errors = ModelValidator.validate_conv_layer(conv_layer, self.conds)
        self.assertEqual(len(errors), 1)
        conv_layer = {"kernel_size": [3, 3], "filters": 0}
        errors = ModelValidator.validate_conv_layer(conv_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_conv_no_filters(self):
        self.expected_conds['was_conv'] = True
        conv_layer = {}
        errors = ModelValidator.validate_conv_layer(conv_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_conv_invalid_kernel_size(self):
        def validate(layer, errors_amount):
            self.expected_conds['was_conv'] = True
            errors = ModelValidator.validate_conv_layer(layer, self.conds)
            self.assertDictEqual(self.conds, self.expected_conds)
            if errors_amount > 0:
                self.assertEqual(len(errors), errors_amount)
            else:
                self.assertIs(errors, None)
            self.conds['was_conv'] = False
        self.valid_conv_layer['kernel_size'] = [3, 0]
        validate(self.valid_conv_layer, 1)
        self.valid_conv_layer['kernel_size'] = [3, -1]
        validate(self.valid_conv_layer, 1)
        self.valid_conv_layer['kernel_size'] = [-1, 3]
        validate(self.valid_conv_layer, 1)
        self.valid_conv_layer['kernel_size'] = [1, 1]
        validate(self.valid_conv_layer, 0)

    def test_flatten_layer(self):
        self.expected_conds['was_flatten'] = True
        errors = ModelValidator.validate_flatten_layer(self.valid_flatten_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_flatten_with_args(self):
        self.expected_conds['was_flatten'] = True
        flatten_layer = {'data_format': 'channels_last'}
        errors = ModelValidator.validate_flatten_layer(flatten_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_flatten_after_flatten(self):
        self.expected_conds['was_flatten'] = True
        ModelValidator.validate_flatten_layer(self.valid_flatten_layer, self.conds)
        errors = ModelValidator.validate_flatten_layer(self.valid_flatten_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_activation_layer(self):
        self.expected_conds['was_activation'] = True
        errors = ModelValidator.validate_activation_layer(self.valid_activation_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_activation_layer_with_no_args(self):
        self.expected_conds['was_activation'] = True
        errors = ModelValidator.validate_activation_layer({}, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_activation_after_activation(self):
        self.expected_conds['was_activation'] = True
        ModelValidator.validate_activation_layer(self.valid_activation_layer, self.conds)
        errors = ModelValidator.validate_activation_layer(self.valid_activation_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_dense_layer_without_flatten_first(self):
        self.expected_conds['was_dense'] = True
        errors = ModelValidator.validate_dense_layer(self.valid_dense_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_dense_layer(self):
        self.expected_conds['was_dense'] = True
        self.conds = {
            'was_flatten': True,
            'was_dense': True,
            'was_conv': False,
            'was_activation': True,
            'was_pooling': True,
            'was_dropout': True,
            'was_batch_normalization': True}
        self.expected_conds['was_flatten'] = True
        errors = ModelValidator.validate_dense_layer(self.valid_dense_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_validate_batch_normalization_layer(self):
        self.expected_conds['was_batch_normalization'] = True
        errors = ModelValidator.validate_batch_normalization_layer(self.valid_normalization_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_batch_norm_after_batch_norm(self):
        self.expected_conds['was_batch_normalization'] = True
        ModelValidator.validate_batch_normalization_layer(self.valid_normalization_layer, self.conds)
        errors = ModelValidator.validate_batch_normalization_layer(self.valid_normalization_layer, self.conds)
        self.assertDictEqual(self.conds, self.expected_conds)
        self.assertEqual(len(errors), 1)

    def test_max_pooling_layer(self):
        self.expected_conds['was_pooling'] = True
        errors = ModelValidator.validate_max_pooling_layer(self.valid_max_pooling_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_max_pooling_layer_after_max_pooling_layer(self):
        self.expected_conds['was_pooling'] = True
        ModelValidator.validate_max_pooling_layer(self.valid_max_pooling_layer, self.conds)
        errors = ModelValidator.validate_max_pooling_layer(self.valid_max_pooling_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_avg_pooling_layer(self):
        self.expected_conds['was_pooling'] = True
        errors = ModelValidator.validate_average_pooling_layer(self.valid_avg_pooling_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_avg_pooling_layer_after_max_pooling_layer(self):
        self.expected_conds['was_pooling'] = True
        ModelValidator.validate_max_pooling_layer(self.valid_max_pooling_layer, self.conds)
        errors = ModelValidator.validate_average_pooling_layer(self.valid_avg_pooling_layer, self.conds)
        self.assertEqual(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_validate_dropout_layer(self):
        self.expected_conds['was_dropout'] = True
        errors = ModelValidator.validate_dropout_layer(self.valid_dropout_layer, self.conds)
        self.assertIs(errors, None)
        self.assertDictEqual(self.conds, self.expected_conds)

    def test_validate_dropout_layer_after_dropout_layer(self):
        self.expected_conds['was_dropout'] = True
        ModelValidator.validate_dropout_layer(self.valid_dropout_layer, self.conds)
        errors = ModelValidator.validate_dropout_layer(self.valid_dropout_layer, self.conds)
        self.assertIs(len(errors), 1)
        self.assertDictEqual(self.conds, self.expected_conds)
