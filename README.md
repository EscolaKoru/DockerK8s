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

### Para entender melhor

No contexto do Kubernetes, o Docker desempenha um papel crucial na criação e na execução dos containers que compõem os Pods, que são a menor unidade de implantação no Kubernetes.



### Docker:

1. **Empacotamento de Aplicativos em Containers:**
   O Docker é uma tecnologia de contêinerização que permite empacotar aplicativos e suas dependências em contêineres, garantindo que eles sejam executados de maneira consistente em qualquer ambiente. No contexto do Kubernetes, os aplicativos são empacotados em imagens Docker, que são usadas para criar e executar containers.

2. **Implantação de Contêineres no Kubernetes:**
   O Kubernetes utiliza containers Docker como a unidade básica de implantação. O Kubernetes é capaz de implantar, gerenciar e escalar esses containers de forma eficiente e automatizada.

3. **Criação de Pods:**
   No Kubernetes, um Pod é um grupo de um ou mais containers, com armazenamento e configurações de rede compartilhados. Os containers dentro de um Pod compartilham o mesmo ambiente de rede e podem se comunicar entre si usando o loopback do Pod.

4. **Kubelet e Docker:**
   O Kubelet é um componente do Kubernetes que executa em cada nó do cluster e é responsável por iniciar e monitorar os containers dentro dos Pods. O Kubelet interage diretamente com o Docker (ou outro runtime de contêiner, como containerd) para criar e gerenciar os containers conforme necessário.

5. **Portabilidade e Consistência:**
   O Docker fornece uma camada de abstração que torna os aplicativos portáteis e independentes do ambiente de execução. Isso permite que os aplicativos sejam desenvolvidos e testados localmente usando Docker e, em seguida, implantados em qualquer ambiente Kubernetes sem modificações.

O Docker desempenha um papel fundamental no processo de implantação de aplicativos no Kubernetes, fornecendo uma maneira padronizada e eficiente de empacotar, distribuir e executar aplicativos em contêineres.

## Kubernetes:

O Deployment e o Service são dois recursos fundamentais no Kubernetes que desempenham papéis diferentes, mas complementares, na implantação e na exposição de aplicativos.

### Deployment:
Um Deployment no Kubernetes é uma descrição declarativa de um conjunto de Pods, juntamente com a configuração de como eles devem ser implantados e atualizados. Ele fornece uma maneira de declarar, gerenciar e atualizar o estado desejado de uma aplicação distribuída. Aqui estão alguns pontos-chave sobre Deployments:

- **Gestão de Replicas:** O Deployment gerencia automaticamente um conjunto de réplicas de Pods, garantindo que o número especificado de Pods esteja sempre em execução.
  
- **Atualizações e Rollbacks:** Os Deployments permitem atualizações de forma controlada e rollback para versões anteriores, garantindo que a aplicação permaneça disponível durante o processo de atualização.

- **Autoreparo:** Se um Pod falhar, o Deployment irá automaticamente substituí-lo por um novo Pod saudável.

- **Rótulos e Seletores:** Os Deployments usam rótulos e seletores para definir conjuntos de Pods que compõem a aplicação. Isso permite a fácil gestão de conjuntos de Pods relacionados.

### Service:
Um Service no Kubernetes é um recurso que define uma política de acesso de rede para um conjunto de Pods. Ele fornece uma maneira estável e uniforme de acessar os Pods, independentemente de onde eles estejam implantados na infraestrutura subjacente. Aqui estão alguns pontos-chave sobre Services:

- **Descoberta de Serviços:** Um Service fornece um ponto de acesso único para um conjunto de Pods, permitindo que outros componentes do sistema os encontrem dinamicamente sem precisar conhecer os detalhes de implementação.

- **Balanceamento de Carga:** Os Services podem fornecer balanceamento de carga entre vários Pods, distribuindo o tráfego de entrada de forma equilibrada entre eles.

- **Exposição de Aplicativos:** Os Services permitem que os Pods sejam expostos para dentro ou fora do cluster Kubernetes, facilitando a exposição de aplicativos para o tráfego externo.

- **Integração de DNS:** Cada Service obtém um registro DNS automático no cluster Kubernetes, permitindo que outros serviços usem seu nome DNS para acessá-lo.

Em resumo, enquanto o Deployment gerencia a implantação e a escalabilidade dos Pods que compõem a aplicação, o Service gerencia a exposição de rede dos Pods, garantindo que eles possam ser acessados de forma confiável por outros componentes do sistema. Juntos, esses recursos fornecem uma base sólida para implantar e executar aplicativos distribuídos no Kubernetes.

## APM

Para adicionar um serviço de APM de código aberto ano projeto Flask sem usar Docker Compose, uma boa opção é usar o **Prometheus** para monitoramento e o **Grafana** para visualização. Vamos configurar essas ferramentas manualmente.

### Passo 1: Configurar o Prometheus

1. **Instalar o Prometheus:**

   Baixe e instale o Prometheus  seguindo as instruções no [site oficial](https://prometheus.io/download/).


2. **Configurar o Prometheus:**

   Crie um arquivo de configuração para o Prometheus (`prometheus.yml`):

   ```yaml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'flask-app'
       static_configs:
         - targets: ['localhost:8000']
   ```

3. **Iniciar o Prometheus:**

   Execute o Prometheus com a configuração criada:

   ```sh
   prometheus --config.file=prometheus.yml
   ```

### Passo 2: Configurar o Flask para Exportar Métricas

1. **Atualizar o Código do Flask:**

   Modifique o `app.py` para expor as métricas do Prometheus:

   ```python
   from flask import Flask, render_template, request
   from prometheus_client import start_http_server, Summary, Counter, Gauge, generate_latest
   import random
   import time

   app = Flask(__name__)

   # Create metrics
   REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
   REQUEST_COUNT = Counter('request_count', 'Number of requests processed')
   IN_PROGRESS = Gauge('inprogress_requests', 'Number of requests in progress')

   @REQUEST_TIME.time()
   def process_request(t):
       time.sleep(t)

   @app.route('/')
   def home():
       IN_PROGRESS.inc()
       process_request(random.random())
       REQUEST_COUNT.inc()
       IN_PROGRESS.dec()
       return render_template('index.html')

   @app.route('/metrics')
   def metrics():
       return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

   if __name__ == '__main__':
       start_http_server(8000)
       app.run(host='0.0.0.0', port=5001)
   ```

2. **Reconstruir e Executar o Container:**

   Reconstrua e execute a imagem Docker:

   ```sh
   docker build -t flask-app:1.0 .
   docker run -p 5001:5000 -p 8000:8000 flask-app:1.0
   ```

### Passo 3: Configurar o Grafana

1. **Instalar o Grafana:**

   Baixe e instale o Grafana seguindo as instruções no [site oficial](https://grafana.com/grafana/download).


2. **Iniciar o Grafana:**

   Execute o Grafana:

   ```sh
   services start grafana
   ```

3. **Configurar o Grafana:**

   - Acesse o Grafana no navegador em `http://localhost:3000`.
   - Faça login com as credenciais padrão (usuário: `admin`, senha: `admin`).
   - Adicione um novo Data Source:
     - Vá para `Configuration > Data Sources > Add data source`.
     - Selecione `Prometheus`.
     - Configure a URL do Prometheus como `http://localhost:9090`.
     - Clique em `Save & Test`.

4. **Criar um Dashboard:**

   - Vá para `Create > Dashboard`.
   - Adicione um novo painel (Panel):
     - Selecione a métrica que deseja visualizar (`request_count`, `request_processing_seconds`, etc.).
     - Configure o gráfico de acordo com suas necessidades.
   - Salve o dashboard.

### Passo 4: Verificar a Configuração

1. **Verificar se o Prometheus está Coletando Métricas:**

   Acesse o Prometheus em `http://localhost:9090` e verifique se as métricas estão sendo coletadas.

2. **Visualizar Métricas no Grafana:**

   Acesse o Grafana em `http://localhost:3000` e veja se o dashboard está exibindo as métricas corretamente.
