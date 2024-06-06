import time
import logging


# Configuração do logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Exemplo de execução do script com logs
logging.info('Início da execução do script')

try:
    # Simulando alguma lógica de script
    for i in range(10):
        logging.info(f'Iteração {i + 1}')
        time.sleep(1)

        # Simulando uma exceção em uma iteração específica
        if i == 7:
            raise ValueError('Erro simulado')

    logging.info('Script concluído com sucesso')

except Exception as e:
    logging.error(f'Erro durante a execução do script: {e}')

