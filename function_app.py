import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# code AI-generated - just for learning purpose
def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0

    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0

    # Verifica se os dígitos verificadores são iguais aos informados
    return cpf[-2:] == f"{digito1}{digito2}"

# Main function
@app.route(route="funcappCPFValidator")
def funcappCPFValidator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting CPF Validation')

    data = req.params.get('cpf')
    if data is None:
        return func.HttpResponse(f'Please inform a CPF to validate.', status_code=400)

    if validar_cpf(data):
        return func.HttpResponse(f"CPF {data} is valid", status_code=200)
    else:
        return func.HttpResponse(f"CPF {data} is NOT valid", status_code=200)