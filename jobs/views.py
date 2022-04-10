from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Jobs
from django.contrib import messages #importa as mensagens de verificação
from django.contrib.messages import constants #importa o modulo constants das mensagens de verificação
from django.contrib.auth.models import User #importa a class de usuario do django 
from django.contrib.auth.decorators import login_required # se usuario não estiver logado ele nega a requisição e envia o usuario para a parte de login  
from django.views import generic


class JobsNovo(generic.CreateView):
    model = Jobs
    fields = 'titulo','descricao','categoria','prazo_entrega','preco','arquivo','profissional','reservado','status'
    success_url = reverse_lazy('perfil')
    
class JobsAll(generic.ListView):

    
    def get_queryset(self):
     model = Jobs
     queryset = Jobs.objects.all()
      
     try:  
      categoria = self.request.GET.get('categoria')
      status = self.request.GET.get('status')
      #verifica a categoria e transforma-o em uma lista pois o filtro __in pede uma lista, enquanto minha categoria retorna uma string    
      if categoria == 'D':
         categoria = ['D']
      elif categoria == 'EV':
         categoria = ['EV']
         
      if status == 'C':
         status = ['C']
      elif status == 'AA':
          status = ['AA']
      elif status == 'F':
          status = ['F']            
          
      if categoria:
      
         queryset = Jobs.objects.filter(categoria__in=categoria,status__in=status,)
         
         
         
     except:
               queryset =  Jobs.objects.all()

              
              
      
     return queryset
    
    
    
    
    
    
class JobsUpdate(generic.UpdateView):
    model = Jobs
    fields = '__all__' 
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('perfil')
    
         
    
  
    
    
    



@login_required(login_url='/auth/logar')# se usuario não estiver logado ele nega a requisição e envia o usuario para a parte de login  
def encontrar_jobs(request):
    
    if request.method == 'GET':
     
     
    #sistema de filter form
        preco_minimo = request.GET.get('preco_minimo')
        preco_maximo = request.GET.get('preco_maximo')

        prazo_minimo = request.GET.get('prazo_minimo')
        prazo_maximo = request.GET.get('prazo_maximo')

        categoria = request.GET.get('categoria')
        
        if prazo_minimo or prazo_maximo or preco_minimo or preco_maximo or categoria:
            
            #sistema de if para verificar caso o campo esteja vazio ele define um valor padrão para cada campo 
            if not preco_minimo:
                preco_minimo = 0

            if not preco_maximo:
                preco_maximo = 999999

            if not prazo_minimo:
                prazo_minimo = datetime(year=1900, month=1, day=1)

            if not prazo_maximo:
                prazo_maximo = datetime(year=3000, month=1, day=1)
                
            #verifica a categoria e transforma-o em uma lista pois o filtro __in pede uma lista, enquanto minha categoria retorna uma string    
            if categoria == 'D':
                categoria = ['D']
            elif categoria == 'EV':
                categoria = ['EV']  
                  
            #gte = maior que, lte = menor que, in = esteja dentro
            jobs = Jobs.objects.filter(preco__gte=preco_minimo)\
                .filter(preco__lte=preco_maximo)\
                .filter(prazo_entrega__gte=prazo_minimo)\
                .filter(prazo_entrega__lte=prazo_maximo)\
                .filter(reservado=False)\
                .filter(categoria__in=categoria)
            

                
                          
            
        else:
            jobs = Jobs.objects.filter(reservado=False)   #busca só jobs em que ainda não foram aceitos 
            
            
        return render(request,'encontrar_jobs.html',{'jobs':jobs}) #terceiro parametro me permite acessar os valores do banco de dados pelo meu HTML como por exemplo {{jobs.titulo}}, para mais informação acessar meu html de encontrar_jobs
@login_required(login_url='/auth/logar')# se usuario não estiver logado ele nega a requisição e envia o usuario para a parte de login  
def aceitar_job(request, id): #tem como parametro id pois será a forma de acessar o id dos jobs 
    job = Jobs.objects.get(id=id) #verifica atravez do id se existe um job com o id solicitado na url
    job.profissional = request.user #acessa a linha do banco de dados profissional e altera o valor para o usuario que clicou no botão para aceitar o job
    job.reservado = True # muda o valor de reservado para não aparecer para mais ninguem
    job.save() #salva as informações
    return redirect('/jobs/encontrar_jobs')  
@login_required(login_url='/auth/logar')# se usuario não estiver logado ele nega a requisição e envia o usuario para a parte de login  
def perfil(request):
    if request.method == "GET":
        jobs = Jobs.objects.filter(profissional=request.user) # busca no banco de dados os jobs onde existe o profissional que está logado e fazendo a requisição
        return render(request, 'perfil.html', {'jobs': jobs})
    
    
    elif request.method == "POST": #faz a verificação se está sendo enviado uma requisição do tipo POST, que seria quando eu mudasse meus dados 
        username = request.POST.get('username') # busca o campo username do form no perfil.html
        email = request.POST.get('email') # busca o campo email do form no perfil.html
        primeiro_nome = request.POST.get('primeiro_nome') # busca o campo primeiro_nome do form no perfil.html
        ultimo_nome = request.POST.get('ultimo_nome') # busca o campo ultimo_nome do form no perfil.html

        usuario = User.objects.filter(username=username).exclude(id=request.user.id) # busca no banco de dados usuarios com nome igual ao digitado no input para não ter usuarios com nomes iguais, o .exclude está excluido dessa busca o nome do propio usuario que está fazendo a requisição para não ter conflito 

        if usuario.exists(): # se o usuario já existe
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse Username')
            return redirect('/jobs/perfil')

        usuario = User.objects.filter(email=email).exclude(id=request.user.id) # busca no banco de dados usuarios com email igual ao digitado no input para não ter usuarios com nomes iguais, o .exclude está excluido dessa busca o nome do propio usuario que está fazendo a requisição para não ter conflito 

        if usuario.exists(): #se o email existe
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse E-mail')
            return redirect('/jobs/perfil')

        
        request.user.username = username #modificar nosso username conforme foi digitado no input 
        request.user.email = email #modificar nosso email conforme foi digitado no input 
        request.user.first_name = primeiro_nome #modificar nosso primeiro_nome conforme foi digitado no input 
        request.user.last_name = ultimo_nome #modificar nosso ultimo_nome conforme foi digitado no input 
        request.user.save() #salva minhas informações 
        messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
        return redirect('/jobs/perfil')
@login_required(login_url='/auth/logar') # se usuario não estiver logado ele nega a requisição e envia o usuario para a parte de login    
def enviar_projeto(request):
    arquivo = request.FILES.get('file')
    id_job = request.POST.get('id')

    job = Jobs.objects.get(id=id_job)

    job.arquivo_final = arquivo
    job.status = 'AA'
    job.save()
    return redirect('/jobs/perfil')    
        