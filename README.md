# sandevistan

## Requisitos

- [Node.js](https://nodejs.org/) and npm v16+.
- [Python](https://www.python.org/downloads/) v3.7 and [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv/) v2021.5.29.
- The [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) (1.2+).

### Instalação dos requisitos

Crie uma service account com permissões necessárias, de acordo com a arquitetura que deseja subir e baixe o json referente a ela:

1. Acessar o GCP;
2. Buscar pelo serviço IAM;
3. Acessar a opção "Contas de serviço" no menu lateral esquerdo;
4. Clicar na opção "+ Criar conta de serviço";
5. Preencher com as informações e permissões necessárias;
6. Buscar pela conta no filtro e clicar no nome da conta de serviço criada;
7. Clicar na aba "Chaves"; 
8. Clica rna opção "Adicionar Chave" > "Criar nova chave";
9. Selecionar a opção "JSON" e Criar.
10. O Download do arquivo será iniciado, salve-o pois será necessário utilizá-lo posteriormente;

#### Instalação do Terraform

Alterne para o usuário root

```
sudo su
```

Instale os pacotes necessário para as etapas seguintes: 

```
apt-get update && sudo apt-get install -y gnupg software-properties-common curl
```

Adicione a chave GPG da Hashicorp necessária ao repositório:

```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
```

Adicione o repositório oficial do HashiCorp para Linux: 

```
apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

Atualize o repositório: 

```
apt-get update
```

Instale o terraform

```
apt-get install terraform
```

Valide a versão do terraform: 

```
terraform -version
```

#### Instalação do Node

```
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
```

```
apt-get install -y nodejs
```

Checar a versão do node instalada

```
node --v
```

#### Instalação npm

```
apt install npm
```

#### Instalação CDK for Terraform

Instale a biblioteca com o npm

```
npm install --global cdktf-cli@latest
```

#### Instalação pip

```
apt-get install python3-pip -y
```

#### Instalação Docker

Seguir os passos em: https://dev.to/klo2k/run-docker-in-wsl2-in-5-minutes-via-systemd-without-docker-desktop-28gi

Instalação das credenciais independentes do Docker: 

```
VERSION=2.1.6
OS=linux  # or "darwin" for OSX, "windows" for Windows.
ARCH=amd64  # or "386" for 32-bit OSs

curl -fsSL "https://github.com/GoogleCloudPlatform/docker-credential-gcr/releases/download/v${VERSION}/docker-credential-gcr_${OS}_${ARCH}-${VERSION}.tar.gz" \
| tar xz docker-credential-gcr \
&& chmod +x docker-credential-gcr && sudo mv docker-credential-gcr /usr/bin/
```

Configure a região do Docker no GCP:

```
docker-credential-gcr configure-docker --registries=REGION
```

Por exemplo, se quer subir um container na região southametica-east1:

```
docker-credential-gcr configure-docker --registries=southamerica-east1
```

#### Instalação dependências libCDK e CDK for Terraform

Instalação do pipenv

```
pip install pipenv
```

```
apt-get install python3-venv -y
```

Altere para a pasta onde você deseja armazenar o projeto:

```
cd /mnt/c/Users/<seu_usuario>/Desktop/...
```

Realize o clone do repositório:

```
git clone <repo>
```

Vá para a pasta do repositório

```
cd sandevistan
```

Inicialize o ambiente virtual:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Instale as dependências dos provedores cloud:

```
pipenv install cdktf-cdktf-provider-aws
```

```
pipenv install cdktf-cdktf-provider-null
```

```
pipenv install cdktf-cdktf-provider-google
```

Cole o JSON da conta de serviço baixado no início do tutorial para a dentro da pasta raiz do sandevistan e renomeie para "service_account.json".

Referencia a chave na variável de ambiente do Google Application Credentials:

```
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/service_account.json
```

## Utilizando o libCDK para o CloudRunScheduled

- O arquivo main.py na raiz do projeto diz respeito à sua infraestrutura, é nele onde as classes de subida de infraestrutura serão declaradas;
- A pasta cloud_run_job_code contém os arquivos que serão buildados na imagem Docker, obrigatoriamente, ela deverá ter os seguintes arquivos:
  - **Dockerfile**: Dockerfile referente à imagem que será construída;
  - **main.py**: Arquivo principal que iniciará a execução do modelo;
  - **requirements.txt**: Listagem dos pacotes e dependências do seu código python;
  - Quaisquer outros arquivos necessários para a execução do seu código também devem ficar dentro desta pasta.
- **service_account.json**: JSON da conta de serviço do Google.



