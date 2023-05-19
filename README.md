# sandevistan
Pacote sandevistan baseado no CDK for Terraform para abstração da complexidade de deploys de arquiteturas e serviços em cloud
## Getting Started
#### Dependencies
You need Python 3.7 or later to use **sandevistan**. You can find it at [python.org](https://www.python.org/).
You also need CDKTF, which is available from [Install CDK for Terraform](https://developer.hashicorp.com/terraform/tutorials/cdktf/cdktf-install). 
#### Installation
Create virtual env.
```
python3 -m venv venv
source venv/bin/activate
```
Init CDK for Terraform and select **aws**, **google** and **null** providers: 
```
cdktf init --local --template=python --providers=aws google null
```
Install sandevistan.
```
pip install -i https://test.pypi.org/simple/ sandevistan
```
Clone this repo to your local machine using:
```
git clone https://github.com/LucasTonetto/sandevistan.git
```
## Features
- GCP
    - Presets
    - Components
- AWS
    - Presets
    - Components