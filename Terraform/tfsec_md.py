import json

with open("tfsec-report.json", "r") as f:
    report = json.load(f)

with open("tfsec-report.md", "w") as md:
    md.write("# Relatório de Segurança - tfsec\n\n")
    if len(report['results']) != 0:
        for issue in report['results']:
            md.write(f"## {issue['resource']}\n")
            md.write(f"**Id:** {issue['rule_id']}\n")
            md.write(f"**Descrição:** {issue['description']}\n\n")
            md.write(f"**Severidade:** {issue['severity']}\n\n")
            md.write(f"**Arquivo:** {issue['location']['filename']}:{issue['location']['start_line']}\n\n")
            md.write("---\n")
    else:
        md.write("**Sem erros reportados**")
print("✅ Relatório tfsec-report.md gerado com sucesso!")
