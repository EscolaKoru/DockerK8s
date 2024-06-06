# Docker & K8s

### Aula Prática: Orquestração de Containers para uma Aplicação Web com Kubernetes

**Objetivo:** 
Demonstrar como orquestrar containers usando Kubernetes para implantar uma aplicação web simples, garantindo alta disponibilidade e escalabilidade.

**Pré-requisitos:**

1. Docker instalado.
2. Kubernetes instalado (Minikube).
3. kubectl instalado (Minikube).

**Descrição da Aplicação:**
Vamos usar uma aplicação web simples em Python com Flask, que exibe uma mensagem "Hello, World!".

### Passo 1: Criar a Aplicação Web

1. **Crie o diretório do projeto:**
   ```sh
   mkdir flask-app
   cd flask-app
   ```

2. **Crie o arquivo `app.py`:**
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def hello():
       return "Hello, World!"

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. **Crie o arquivo `requirements.txt`:**
   ```plaintext
   Flask==2.0.1
   Werkzeug==2.0.1
   ```

### Passo 2: Dockerizar a Aplicação

1. **Crie o arquivo `Dockerfile`:**
   ```dockerfile
   # Use uma imagem base do Python
   FROM python:3.9-slim

   # Defina o diretório de trabalho
   WORKDIR /app

   # Copie os arquivos de requisitos e instale as dependências
   COPY requirements.txt requirements.txt
   RUN pip install -r requirements.txt

   # Copie o código da aplicação
   COPY app.py app.py

   # Defina o comando padrão a ser executado quando o container iniciar
   CMD ["python", "app.py"]
   ```

2. **Autentique com o Docker:**
   ```sh
   docker login
   ```

3. **Construa a imagem Docker:**
   ```sh
   docker build -t flask-app:1.0 .
   ```

4. **Teste a aplicação localmente:**
   ```sh
   docker run -p 5001:5000 flask-app:1.0
   ```
   Acesse `http://localhost:5001` para verificar se a aplicação está funcionando.

### Passo 3: Preparar os Arquivos de Configuração do Kubernetes

1. **Crie o arquivo `deployment.yaml`:**
   ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: flask-app-deployment
    spec:
    selector:
        matchLabels:
        app: flask-app
    replicas: 3
    template:
        metadata:
        labels:
            app: flask-app
        spec:
        containers:
            - name: flask-app
            image: flask-app:1.0
            ports:
            - containerPort: 5000
   ```

2. **Crie o arquivo `service.yaml`:**
   ```yaml
    apiVersion: v1
    kind: Service
    metadata:
    name: flask-app-service
    labels:
        name: flask-app-service
    spec:
    ports:
        - protocol: TCP
        port: 5051
        targetPort: 5000
    selector:
        app: flask-app
    type: NodePort
   ```

### Passo 4: Implantar no Kubernetes

1. **Inicie o Minikube:**
   ```sh
   minikube start
   ```

2. **Carregue a imagem Docker para o Minikube:**
   ```sh
   eval $(minikube docker-env)
   docker build -t flask-app:1.0 .
   ```

3. **Aplique as configurações do Kubernetes:**
   ```sh
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

4. **Verifique o status do deployment:**
   ```sh
   kubectl get deployments
   kubectl get pods
   ```

5. **Acesse a aplicação:**
   - Obtenha a URL:
     ```sh
     minikube service flask-app-service --url
     ```
   - Acesse a URL fornecido.

### Conclusão

Nesta aula prática, você aprendeu a:
1. Criar uma aplicação web simples com Flask.
2. Dockerizar a aplicação.
3. Criar arquivos de configuração do Kubernetes para deployment e serviço.
4. Implantar a aplicação no Kubernetes usando Minikube.

**Desafios adicionais:**
1. Configure um Ingress para gerenciar o tráfego.
2. Adicione uma configuração de volume persistente para armazenar dados.
3. Explore a escalabilidade alterando o número de réplicas.