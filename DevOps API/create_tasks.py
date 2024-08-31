import requests as r
import base64
import json

def create_tasks(tokenPersonal,organization,project,parent_id,list_task):
  '''Cria tarefas no Azure DevOps de acordo com a lista com os nomes indicados como parâmetro
  parameters:
      tokenPersonal(string): Token Pessoal para autenticar a requisição, pode ser obtida através  do portal do Azure DevOps
      project(string): Nome do Projeto
      organization(string): Nome da Organização
      parent_id(string or int): Id do Backlog que ira receber a tarefa
      list_task(list): Lista de strings que serão utilizados como o nome de cada tarefa.
  '''
  authorization = str(base64.b64encode(bytes(':'+tokenPersonal, 'ascii')), 'ascii')
  headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic '+authorization,
  'Content-Type': 'application/json-patch+json'
  }
  for name_task in list_task:
    data =  [{
    "op": "add",
    "path": "/fields/System.Title",
    "from": None,
    "value": f"{name_task}"
  },{
      "op": "add",
      "path": "/relations/-",
      "from": None,
      "value": {
          "rel": "System.LinkTypes.Hierarchy-Reverse",
          "url": f"https://dev.azure.com/{organization}/{project}/_apis/wit/workItems/{parent_id}",
          "attributes": {
              "comment": "Making a new child task"
            }}}
            ]
    data = json.dumps(data)
    url_api = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$task?api-version=7.1-preview.3'
    response = r.post(url_api,data=data,headers=headers)
    print(f"Response: {response.status_code}")  