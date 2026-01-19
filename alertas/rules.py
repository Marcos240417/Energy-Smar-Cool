from alertas.models import Alerta

def verificar_limites_temperatura(sensor, temperatura):

    if temperatura > sensor.max_temperature:
        return Alerta.objects.create(
            titulo=f"Temperatura Alta: {sensor.name}",
            mensagem=f"Detectado {temperatura}°C (Limite: {sensor.max_temperature}°C)",
            nivel='critical'
        )
    elif temperatura < sensor.min_temperature:
        return Alerta.objects.create(
            titulo=f"Temperatura Baixa: {sensor.name}",
            mensagem=f"Detectado {temperatura}°C (Mínimo: {sensor.min_temperature}°C)",
            nivel='warning'
        )
    return None