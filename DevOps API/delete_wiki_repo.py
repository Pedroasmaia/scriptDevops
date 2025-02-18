import requests as r
import base64


def delete_wiki_repo(token_personal,organization,project):
    '''Deleta o repositório que a Wiki Utiliza
    parameters:
        token_personal(string): Token Pessoal para autenticar a requisição, pode ser obtida através  do portal do Azure DevOps
        project(string): Nome do Projeto
        organization(string): Nome da Organização
    '''
    authorization = str(base64.b64encode(bytes(':'+token_personal, 'ascii')), 'ascii')
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic '+authorization
    }
    wiki_url = f"https://dev.azure.com/{organization}/{project}/_apis/wiki/wikis"
    request_response = r.get(url=wiki_url,headers=headers)
    request_response = request_response.json()
    if request_response['count'] == 1:
        value_response = request_response['value']
        value_response = value_response[0]
        repository_id = value_response['repositoryId']
        repo_url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository_id}?api-version=7.2-preview.1"
        repository_name = value_response['name']
        confirm = input(f'Deseja apagar o {repository_name}? (y) Sim (n) Não: ')
        if confirm.lower() == 'y':
            request_delete = r.delete(url=repo_url,headers=headers)
            if(str(request_delete.status_code)=='204'):
                print('-------Apagado--------')
                print(f'Nome: {repository_name}')
                print(f'ID: {repository_id}')
                print('----------------------')
    else:
        for repository in request_response['value']:
            repository_name = repository['name']
            repository_id = repository['repositoryId']
            repo_url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository_id}?api-version=7.2-preview.1"
            print('---------------')
            print(f'Nome: {repository_name}')
            print(f'ID: {repository_id}')
            print('---------------')
            confirm = input(f'Deseja apagar o {repository_name}? (y) Sim (n) Não: ')
            if confirm.lower() == 'y':
                request_delete = r.delete(url=repo_url,headers=headers)
                if(str(request_delete.status_code)=='204'):
                    print('-------Apagado--------')
                    print(f'Nome: {repository_name}')
                    print(f'ID: {repository_id}')
                    print('----------------------')
                else:
                    print(str(request_delete.status_code))