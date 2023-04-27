import requests as r
import base64

#! Pegar headers da requisição
def getHeaders():
   tokenPersonal = input('Coloque o seu personal Token: ')
   authorization = str(base64.b64encode(bytes(':'+tokenPersonal, 'ascii')), 'ascii')
   headers = {
   'Accept': 'application/json',
   'Authorization': 'Basic '+authorization
   }
   return headers 


organization = input('Coloque a organização: ')
project = input('Coloque o projeto: ')
#! Pegar ID do repositório
def getIdRepo():
   headers = getHeaders()
   wikiUrl = f"https://dev.azure.com/{organization}/{project}/_apis/wiki/wikis"
   requestID = r.get(url=wikiUrl,headers=headers)
   IDjson = requestID.json()
   if(IDjson['count'] == 1):
      valueJson = IDjson['value']
      valueJson = valueJson[0]
      repositoryID = valueJson['repositoryId']
      repositoryName = valueJson['name']
      print(f'{repositoryName} tem o id: {repositoryID}')
      return repositoryID
   else:
      print('Existe mais de uma wiki')


def deleteWiki():
   headers = getHeaders()
   repositoryId = getIdRepo()
   confirmDelete = input('Confirma a exclusão desse repositório? (Y) Sim/(N) Não: ')
   if(confirmDelete == 'Y'):
      repourl = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repositoryId}?api-version=7.0"
      print(repourl)
      requestDelete = r.delete(url=repourl,headers=headers)
      if(str(requestDelete.status_code)=='204'):
         print("Seu repositório da Wiki foi apagado")
deleteWiki()