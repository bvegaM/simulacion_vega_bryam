import ast
import coloredlogs
import logging
import math
import multiprocessing
import numpy as np
import operator
import pandas as pd
import seaborn as sns
import time

import os
os.environ['NUMEXPR_MAX_THREADS'] = '12'
os.environ['NUMEXPR_NUM_THREADS'] = '10'


from sklearn.decomposition import TruncatedSVD


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install()

class EjeSemantico():
    
    def leer_dataset(self,filename):
        df=pd.read_csv(filename)
        return df
    
    def obtener_codigo_valor(self,df):
        lista=[]
        for i,j in df[['uuid','tokens_abstract']].values:
            lista.append((i,ast.literal_eval(j)))
        return lista
    
    def frecuenciaPalabras(self,diccionarioTexto):
        palabrasXdocumento = {}
        for x in diccionarioTexto.values():
            for z in x:
                if z not in palabrasXdocumento.keys():
                    palabrasXdocumento[z] = 1
                else:
                    palabrasXdocumento[z] = palabrasXdocumento[z] + 1
        return palabrasXdocumento
    
    def obtenerVocabulario(self,frecuenciaTermino):
        return [(i,frecuenciaTermino[i]) for i in frecuenciaTermino if frecuenciaTermino[i]>10]

class TerminoDocumento:
    
    def __init__(self,listaT):
        self.diccionarioTexto=listaT
        self.diccionarioContador={}
        self.ejeSemantico = EjeSemantico()
    
    def obtenerTerminoDocumento(self,frecuenciaTermino):
        aux={}
        diccionarioTermDoc={}
        for j in self.diccionarioContador:
            if frecuenciaTermino[0] not in self.diccionarioContador[j].keys(): 
                aux[j]=0
            else:
                aux[j]=self.diccionarioContador[j][frecuenciaTermino[0]]
        diccionarioTermDoc[frecuenciaTermino[0]]=aux
        return diccionarioTermDoc
    
    def obtenerpalabrasDocumento(self):
        for i in self.diccionarioTexto:
            aux={}
            aux[i]=self.diccionarioTexto[i]
            self.diccionarioContador[i]=self.ejeSemantico.frecuenciaPalabras(aux)

    def unirDiccionario(self,texto):
        union={}
        for i in texto:
            for j in i:
                union[j]=i[j]
        return union
    
    def matrizTerminoDocumento(self,terminoDocumento):
        documentos=terminoDocumento[list(terminoDocumento.keys())[0]].keys()
        dframe = pd.DataFrame([key for key in documentos], columns=['Palabras'])
        for i in terminoDocumento:
            dframe[i]=[terminoDocumento[i][j] for j in terminoDocumento[i]]
        
        dframe=dframe.transpose()
        indices=list(dframe.loc['Palabras'])
        dframe.columns=indices
        dframe=dframe.drop(['Palabras'],axis=0)
        return dframe


class TfIdf:
    
    def __init__(self,len,term):
        self.lenArchivos=len
        self.terminoDocumento=term
        
    def obtenerIdf(self,palabra):
        count=0
        valorIdf=0
        for j in self.terminoDocumento[palabra]:
            if(self.terminoDocumento[palabra][j]!=0):
                count+=1
        if (count!=0):
            valorIdf=math.log10(self.lenArchivos/count)
        else:
            valorIdf=0
        return valorIdf
    
    def obtenerTfIdf(self,terminoDocumentoM,idf):
        for i in terminoDocumentoM:
            terminoDocumentoM[i]=terminoDocumentoM[i]*idf
        return terminoDocumentoM
    

class SimilaridadCoseno:
    
    def __init__(self,tfIdfMatriz,tfIdfHtmlMatriz):
        self.html = tfIdfHtmlMatriz
        self.json = tfIdfMatriz
    
    def obtenerSimilaridadCoseno(self,valor):
        respaldoDos=pd.DataFrame(self.html.values,columns=self.html.columns)
        lista=[]
        for i in respaldoDos:
            dot_product = np.dot(np.array(respaldoDos[i]),np.array(self.json[valor]))
            norm_a = np.linalg.norm(np.array(respaldoDos[i]))
            norm_b = np.linalg.norm(np.array(self.json[valor])) 
            coseno=dot_product/(norm_a*norm_b)
            lista.append(coseno)
        return lista
    
    def armarMatrizCoseno(self,lista):
        respaldo=pd.DataFrame(self.html.values,columns=self.html.columns)
        cosenoFrame=pd.DataFrame(columns=respaldo.columns)
        for i in lista:
            cosenoFrame.loc[len(cosenoFrame)]=i
        cosenoFrame=cosenoFrame.set_index(self.json.columns)
        return cosenoFrame

if __name__ == '__main__':
    

    logger.info('Proceso del eje semantico')

    ejeSemantico            = EjeSemantico()
    df                      = ejeSemantico.leer_dataset('./data_articles.csv')
    listaTexto              = dict(ejeSemantico.obtener_codigo_valor(df))
    logger.warning('Obteniendo frecuencia de palabras')
    frecuenciaTermino       = ejeSemantico.frecuenciaPalabras(listaTexto)
    logger.warning('Obteniendo vocabulario')
    vocabulario             = ejeSemantico.obtenerVocabulario(frecuenciaTermino)

    logger.info('Proceso de reducción de dimensionalidad')

    logger.warning('Obteniendo matriz termino-documento')
    termDoc                 = TerminoDocumento(listaTexto)
    pool                    = multiprocessing.Pool(processes=8)
    termDoc.obtenerpalabrasDocumento()
    terminoDocumento        = pool.map(termDoc.obtenerTerminoDocumento,vocabulario)
    pool.close() 
    pool.join()
    terminoDocumento        = termDoc.unirDiccionario(terminoDocumento) 
    matTerminoDocumento     = termDoc.matrizTerminoDocumento(terminoDocumento)
    
    logger.warning('Obteniendo matriz tf-idf')
    tfidf                   = TfIdf(df.shape[0],terminoDocumento)
    pool                    = multiprocessing.Pool(processes=8)
    idf                     = pool.map(tfidf.obtenerIdf,terminoDocumento)
    pool.close() 
    pool.join()
    tfIdfMatriz             = tfidf.obtenerTfIdf(matTerminoDocumento,idf)
    

    logger.info('Proceso de recuperación e información')
    
    df                      = ejeSemantico.leer_dataset('./clean_tweets.csv')
    listaTexto              = dict(ejeSemantico.obtener_codigo_valor(df))
    termDoc                 = TerminoDocumento(listaTexto)
    pool                    = multiprocessing.Pool(processes=8)
    
    logger.warning('Obteniendo matriz termino-documento')
    termDoc                 = TerminoDocumento(listaTexto)
    pool                    = multiprocessing.Pool(processes=8)
    termDoc.obtenerpalabrasDocumento()
    terminoDocumento        = pool.map(termDoc.obtenerTerminoDocumento,vocabulario)
    pool.close() 
    pool.join()
    terminoDocumento        = termDoc.unirDiccionario(terminoDocumento) 
    matTerminoDocumento     = termDoc.matrizTerminoDocumento(terminoDocumento)
    
    logger.warning('Obteniendo matriz tf-idf')
    tfidf                   = TfIdf(df.shape[0],terminoDocumento)
    pool                    = multiprocessing.Pool(processes=8)
    idf                     = pool.map(tfidf.obtenerIdf,terminoDocumento)
    pool.close() 
    pool.join()
    tfIdfMatriz_r             = tfidf.obtenerTfIdf(matTerminoDocumento,idf)
    
    
    logger.warning('Proceso de similitud de coseno')
    df_svd          = df_svd.T
    df_svd.columns  = df_svd.iloc[0]
    df_svd          = df_svd.drop('documents',axis=0)
    
    df_svd_r         = df_svd_r.T
    df_svd_r.columns = df_svd_r.iloc[0]
    df_svd_r         = df_svd_r.drop('documents',axis=0)

    cosenoS                       = SimilaridadCoseno(tfIdfMatriz,tfIdfMatriz_r)
    poolU                         = multiprocessing.Pool(processes=8)
    cosenoSimilaridadMatriz       = poolU.map(cosenoS.obtenerSimilaridadCoseno,df_svd.to_dict())
    poolU.close() 
    poolU.join()
    cosenoSimilaridadMatriz       = cosenoS.armarMatrizCoseno(cosenoSimilaridadMatriz)
    descripcionMatrizCoseno       = cosenoSimilaridadMatriz.transpose().describe()
    cosenoSimilaridadMatriz.to_csv('similitud.csv')
    


