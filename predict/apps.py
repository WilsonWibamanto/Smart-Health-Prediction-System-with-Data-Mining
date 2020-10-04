from django.apps import AppConfig


class PredictConfig(AppConfig):
    name = 'predict'

    def ready(self):
        import predict.signals
