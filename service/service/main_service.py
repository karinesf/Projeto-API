import time
import json
from loguru import logger
from service.constants import mensagens
import pandas as pd
import requests as rq


class ConsultaCep():

    def __init__(self):
        logger.debug(mensagens.INICIO_LOAD_SERVICO)
        self.load_servico()

    def load_servico(self):
        """"
        Carrega o servico de consulta de CEP
        """

        logger.debug(mensagens.FIM_LOAD_SERVICO)

    def executar_rest(self, texts):
        response = {}

        logger.debug(mensagens.INICIO_CONSULTA)
        start_time = time.time()

        response_consulta = self.consulta_cep(texts['textoMensagem'])

        logger.debug(mensagens.FIM_CONSULTA)
        logger.debug(f"Fim de todas as consultas em {time.time()-start_time}")

        df_response = pd.DataFrame(texts, columns=['textoMensagem'])
        df_response['consulta'] = response_consulta

        df_response = df_response.drop(columns=['textoMensagem'])

        response = {
                     "listaConsultas": json.loads(df_response.to_json(
                                                                            orient='records', force_ascii=False))}

        return response

    def consulta_cep(self, texts):
        """
        Faz a consulta do CEP e retona as informaçõs dele
        """
        logger.debug('Iniciando a consulta...')

        response = []

        for text in texts:
            req = 'https://viacep.com.br/ws/{}/json/'.format(text)
            resp = rq.get(req)
            if resp.status_code == 200:
                response.append(resp.json())

        return response