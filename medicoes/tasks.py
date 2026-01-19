from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.models import Aparelho
from alertas.models import Alerta
from alertas.rules import verificar_limites_temperatura
from sensors.models import Sensor
from .models import Medicao


@shared_task
def task_verificar_alerta_temperatura(sensor_id, temperatura):

    try:
        sensor = Sensor.objects.get(id=sensor_id)
        verificar_limites_temperatura(sensor, temperatura)
        return f"Sucesso: Sensor {sensor.code} verificado."
    except Exception as e:
        return f"Erro na automação: {str(e)}"


@shared_task
def verificar_aparelhos_offline():

    limite = timezone.now() - timedelta(minutes=15)
    aparelhos = Aparelho.objects.filter(ativo=True)
    alertas_gerados = 0

    for aparelho in aparelhos:

        ultima_medicao = Medicao.objects.filter(aparelho=aparelho).order_by('-registrada_em').first()


        if not ultima_medicao or ultima_medicao.registrada_em < limite:

            titulo_alerta = f"Offline: {aparelho.nome}"


            alerta_existente = Alerta.objects.filter(
                titulo=titulo_alerta,
                ativo=True
            ).exists()

            if not alerta_existente:
                Alerta.objects.create(
                    titulo=titulo_alerta,
                    mensagem=f"O aparelho {aparelho.nome} (ID: {aparelho.id}) está sem comunicação há mais de 15 minutos.",
                    nivel="CRITICO",
                    ativo=True
                )
                alertas_gerados += 1

    return f"Monitoramento finalizado. {alertas_gerados} novos alertas gerados."


    destinatario = aparelho.loja.usuario_set.filter(role='CLIENTE').first().email or 'seu-email-pessoal@gmail.com'

    send_mail(
        subject=f"🚨 ALERTA: {aparelho.nome} Offline",
        message=f"O aparelho {aparelho.nome} parou de enviar dados.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[destinatario],
        fail_silently=False,
    )
