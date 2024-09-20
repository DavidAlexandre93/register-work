# verificar_feriados.py
from datetime import datetime, timedelta

# Feriados Nacionais no Brasil
feriados_nacionais = [
    "01-01",  # Confraternização Universal
    "04-21",  # Tiradentes
    "05-01",  # Dia do Trabalhador
    "09-07",  # Independência do Brasil
    "10-12",  # Nossa Senhora Aparecida
    "11-02",  # Finados
    "11-15",  # Proclamação da República
    "12-25"   # Natal
]

# Feriados Estaduais de São Paulo
feriados_sp = [
    "07-09"   # Revolução Constitucionalista de 1932
]

# Feriados Municipais de São Paulo (Capital)
feriados_municipais_sp = [
    "01-25"  # Aniversário da cidade de São Paulo
]

# Verifica feriados móveis
def verificar_feriados_moveis():
    ano = datetime.now().year
    # Cálculo de Páscoa baseado no algoritmo de computus
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1

    pascoa = datetime(ano, mes, dia)
    carnaval = (pascoa - timedelta(days=47)).strftime("%m-%d")
    quarta_cinzas = (pascoa - timedelta(days=46)).strftime("%m-%d")
    sexta_santa = (pascoa - timedelta(days=2)).strftime("%m-%d")
    corpus_christi = (pascoa + timedelta(days=60)).strftime("%m-%d")
    pascoa = pascoa.strftime("%m-%d")

    return [carnaval, quarta_cinzas, sexta_santa, pascoa, corpus_christi]

def eh_feriado():
    hoje = datetime.now().strftime("%m-%d")
    agora = datetime.now().strftime("%H:%M")

    # Verificar feriados fixos nacionais, estaduais e municipais
    if hoje in feriados_nacionais or hoje in feriados_sp or hoje in feriados_municipais_sp:
        return True
    
    # Verificar feriados móveis
    feriados_moveis = verificar_feriados_moveis()
    
    # Tratamento especial para Quarta-feira de Cinzas até meio-dia
    if hoje in feriados_moveis:
        if hoje == feriados_moveis[1]:  # Quarta-feira de Cinzas
            if agora < "12:00":
                return True
        else:
            return True

    return False

# Verificar e retornar o resultado
if eh_feriado():
    print("Hoje é feriado ou ponto facultativo! O job não deve ser executado.")
    exit(1)
else:
    print("Hoje não é feriado. O job pode ser executado.")
    exit(0)
