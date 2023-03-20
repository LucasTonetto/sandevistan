from constructs import Construct
from cdktf import App
from sandevistan.stacks.SandevistanStack import SandevistanStack
from sandevistan.google.presets.CloudRunScheduled import CloudRunScheduled

class MyStack(SandevistanStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        CloudRunScheduled(
            self,
            'projeto', # ID do projeto no GCP
            'regiao', # Região do deploy, exemplo: southamerica-east1
            'nome_do_deploy',
            'nome_da_imagem_do_docker', # Se quiser utilizar tags, passe aqui a especificação, exemplo nome:tag
            'email_da_conta@de_servico', # email da service account, é possível encontrá-lo dentro do arquivo service_account.json na chave "client_email"
            'con_scheduler', # periodo de rodagem do job no cloud run em cron > https://crontab.guru/
            create_repository=True, # True se for necessário criar um novo repositório no Artifact Registry
            service_account_path='service_account.json', # path do arquivo service_account.json, caso esteja na raiz do projeto, passar apenas service_account
            build_docker_image = True, # True se for necessário realizar o build da imagem do docker
            docker_image_to_build_folder_path = './cloud_run_job_code' # Caminho da pasta onde se encontra os códigos a serem colcoados no cloud run (não alterar para este template)
        )

app = App()
MyStack(app, "sandevistan-docker")

app.synth()