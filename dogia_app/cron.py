from django.utils import timezone
from django_cron import CronJobBase, Schedule
from dogia_app.models import Cachorro

class UpdateDogStatusCronJob(CronJobBase):

    schedule = Schedule(run_at_times=['00:00'])
    code = 'dogia_app.atualizar_status_cachorros_cron_job'  # Nome único para a tarefa

    def do(self):

        # Calcular a data limite (30 dias atrás)
        data_limite = timezone.now() - timezone.timedelta(days=30)
        cachorros_a_atualizar = Cachorro.objects.filter(data_criacao__date__lte=data_limite.date(), status=True)
        cachorros_a_atualizar.update(status=False)

        for cachorro in cachorros_a_atualizar:
            cachorro.status = False
            cachorro.save()

        # Log ou mensagem de confirmação
        print('Status dos cachorros atualizado com sucesso.')