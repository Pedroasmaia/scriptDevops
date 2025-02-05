import requests as r
import csv

def get_qtdLines(sonarcloud_token,organization,n_projects):
    '''Gera arquivo csv com a contagem das linhas dos projetos
    parameters:
        sonarcloud_token(string): Token gerado a partir da sua conta do SonarCloud
        organization(string): Nome da sua organização do SonarCloud (https://sonarcloud.io/organizations/organization_name/projects)
        n_projects(int): Número de Projetos por página
    '''
    url = f"https://sonarcloud.io/api/projects/search"
    params = {
        'p': 1,
        'ps': n_projects,
        'organization': organization
    }
    headers = {
    'Authorization': f'Bearer {sonarcloud_token}'
    }
    response = r.get(url, headers=headers, params=params)
    with open('resultado.csv', mode='w', newline='') as arquivo_csv:
        for i,project in enumerate(response.json()['components']):
            key = project['key']
            name = project['name']
            url = f"https://sonarcloud.io/api/measures/component"
            params = {'componentKey': project['key'],'metricKeys': 'ncloc'}
            headers = {'Authorization': f'Bearer {sonarcloud_token}'}
            metrics = r.get(url, headers=headers, params=params)
            metrics_data = metrics.json()
            escritor_csv = csv.writer(arquivo_csv)
            try:
                if len(metrics_data["component"]["measures"]) == 0: 
                    qtd_linhas = 0
                    dados = [name,"0"]
                    escritor_csv.writerow(dados)
                    print(f"Escrevendo: {i+1} {name}:0")
                    continue
            except KeyError as key_error:
                print(f"{i+1} {metrics_data} : {key}")
                continue
            qtd_linhas = metrics_data["component"]["measures"][0]['value']

            
            dados = [name,qtd_linhas]
            escritor_csv.writerow(dados)
            print(f"Escrevendo: {i+1} {name}:{qtd_linhas}")
            # Escrevendo os dados no arquivo CSV
