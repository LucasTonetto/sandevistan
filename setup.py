from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='sandevistan',
    version='0.0.16',
    url='https://github.com/LucasTonetto/sandevistan',
    license='MIT License',
    author='Lucas Tonetto Firmo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lucasfirmo@hotmail.com',
    keywords=[
        'CDK',
        'CDK for Terraform',
        'Terraform',
        'sandevistan',
        'IaC',
        'IaaC',
        'infraestrutura',
    ],
    description=u'Pacote sandevistan baseado no CDK for Terraform para abstração da complexidade de deploys de arquiteturas e serviços em cloud',
    packages=find_packages()
)