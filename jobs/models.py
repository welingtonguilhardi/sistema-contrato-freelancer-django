from django.db import models
from django.contrib.auth.models import User





class Jobs(models.Model):
    categoria_choices = (('D', 'Design'), #opções de trabalho 
                         ('EV', 'Edição de Vídeo'))
    status_choices = (('C', 'Em criação'), #opções de status do trabalho  
                      ('AA', 'Aguardando aprovação'),
                      ('F', 'Finalizado'))

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=2, choices=categoria_choices, default="D")
    prazo_entrega = models.DateTimeField()
    preco = models.FloatField()
    arquivo = models.FileField(upload_to=None,null=True)
    profissional = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)# um para muitos oq siginifica que um trabalho só pode ter um profissional, o termo on_delete é para quando um profissional for apagado não acontecer nada nos jobs. 
    reservado = models.BooleanField(default=False)
    status = models.CharField(max_length=2,choices=status_choices, default='C')
    arquivo_final = models.FileField(null=True)

    def __str__(self) -> str:
         return self.titulo
