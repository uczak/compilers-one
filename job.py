from fileinput import filename
import io
from xml.dom.minidom import TypeInfo
import enum
import os

system_files = [ 'token.txt','simbolos.txt','erros.txt']
'''[ 'saida.txt','saida.txt','saida.txt']'''


tokens_id = []
palavras_reservadas_vet = ["int","double","float","real","break","case","char","const","continue"]


letras_minusculas_min = 97 # a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q,
letras_minusculas_max = 122 # z

letras_maiusculas_min = 65 # A
letras_maiusculas_max = 90 # Z

numeros_min = 48 # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
numeros_max = 57

simbolos_1_min = 32# space, !, ", #, $, %, &, ', (, ), *, +, ,, -, ., /, 
simbolos_1_max = 47

simbolos_2_min = 58# :, ;, <, =, >, ?, @,
simbolos_2_max = 64

simbolos_3_min = 91# [, \, ], ^, _, `,
simbolos_3_max = 96

simbolos_4_min = 123# {, |, }, ~,
simbolos_4_max = 126

token_counter = 0# conta as linhas para a tebela/arquivo de tokens
symbols_counter = 0# conta as linhas para a tebela/arquivo de simbolos
error_counter = 0# conta as linhas para a tebela/arquivo de errors
 
line_counter= 0# contador de linhas do arquivo de entrada

file = None


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def read_file():
    with open('teste.txt', 'r', encoding='utf-8') as f:
        file = f.readlines()
    return file


def write_file_token(text):
    with open(system_files[0], 'a', encoding='utf-8') as file:
        file.writelines(f'[{line_counter}] {text} \n')


def write_file_simbolos(text, type):
    if text in tokens_id:
        write_file_token(f'{type} {tokens_id.index(text) + 1}')
    else:# se o texto não existe na lista o token é novo e vamos adicionar na lista gravar o simbolo e gravar o token
        tokens_id.append(text)
        with open(system_files[1], 'a', encoding='utf-8') as file:
            file.writelines(f'{tokens_id.index(text) + 1} - {text} \n')
        write_file_token(f'{type} {tokens_id.index(text) + 1}')


def write_file_erros(text):
    with open(system_files[2], 'a', encoding='utf-8') as file:
        file.writelines(f'{line_counter} ({text}) \n')


def comentario(vet_line):
    if vet_line:
        if ord(vet_line[0][0]) == 47 and ord(vet_line[0][1]) == 47: # //
            write_file_token('COMENTARIO')
            return True
    return False


def palavras_reservadas(vet_line):
    if vet_line and len(vet_line)<=1:
        if vet_line[0] in palavras_reservadas_vet: # palavras reservadas && se tem apenas a apalvra reservada na linha
            write_file_token(str(vet_line[0]).upper())
            return True  
    else:
        write_file_erros(' '.join(map(str, vet_line))) # converte a lista para uma string separando por espaço cada uma das posicoes, para voltar ao conteudo original da linha.
    return False


def valida_identificador_iniciado_por_numerico(word):
    value = 0
    real_number = True
    if '.' in word: # se possui ponto, indicando possivel numero decimal
        splite = word.split('.')
        if len(splite[1]) < 2:
            write_file_erros(str(vet_line[0]))
            return False
        try: # tenta converter uma palavra que não tem '.' e começa com um caractere numerico
            value = float(word)
        except ValueError:
            write_file_erros(str(vet_line[0]))
            return False
    else:
        real_number = False # identifica que o numero não é um numero real.
        try: # tenta converter uma palavra que não tem '.' e começa com um caractere numerico
            value = int(word)
        except ValueError:
            write_file_erros(str(vet_line[0]))
            return False
    
    if value > 99.99: # numero maior do que a gramatica permite
        write_file_erros(str(vet_line[0]))
        return False

    write_file_simbolos(str(vet_line[0]), 'NÚMERO REAL') if real_number else write_file_simbolos(str(vet_line[0]), 'NÚMERO INTEIRO')
    return True


def validar_identificador_iniciado_por_letra(word):
    for w in word:
        value = ord(w)
        #verifica se os caracteres são letras minusculas, maiusculas ou numeros
        if (value >= letras_minusculas_min and value <= letras_minusculas_max) or (value >= letras_maiusculas_min and value <= letras_maiusculas_max) or (value >= numeros_min and value <= numeros_max):
            #print(w)
            pass
        else:
            write_file_erros(str(vet_line[0]))
            return False

    write_file_simbolos(str(vet_line[0]), 'IDENTIFICADOR')
    return True


def identificador(vet_line):
    word = vet_line[0]
    first_character = word[0]

    if ord(first_character) >= numeros_min and ord(first_character) <= numeros_max: # primeiro caractere é numérico.
       return valida_identificador_iniciado_por_numerico(word)
    elif ord(first_character) >= letras_minusculas_min and ord(first_character) <= letras_minusculas_max: # primeiro caractere é letra minuscula.
        return validar_identificador_iniciado_por_letra(word)
    elif ord(first_character) >= letras_maiusculas_min and ord(first_character) <= letras_maiusculas_max: # primeiro caractere é letra MAIUSCULA.
        return validar_identificador_iniciado_por_letra(word)
    else: # palavras que comecao por qualquer outro caractere
        write_file_erros(word)
    return True


file = read_file()
#print(file)
# Apaga os arquvis de saida caso eles existam.
for file_name in system_files: remove_file(file_name) 


# Percorre as linhas do arquivo de entrada.
for linha in file:
    line_counter += 1
    vet_line = linha.split()

    if comentario(vet_line):
        continue
    if palavras_reservadas(vet_line):
        continue
    if len(vet_line)<=1 and identificador(vet_line):
        continue
