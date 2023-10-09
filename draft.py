import re

cont = 16
padrao = r'(\d+)'
padrao2 = r'@[a-zA-Z]+'
padrao3 = r'@[0-9]+'

def DEST(code):
    ans = ""
    ans += "1" if "A" in code else "0"
    ans += "1" if "D" in code else "0"
    ans += "1" if "M" in code else "0"
    return ans

JUMP = {
    "" : "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111",
}

COMP = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "A" : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "D+1" : "011111",
    "A+1" : "110111",
    "D-1" : "001110",
    "A-1" : "110010",
    "D+A" : "000010",
    "D-A" : "010011",
    "A-D" : "000111",
    "D&A" : "000000",
    "D|A" : "010101",
    "M" : "110000",
    "!M" : "110001",
    "-M" : "110011",
    "M+1" : "110111",
    "M-1" : "110010",
    "D+M" : "000010",
    "D-M" : "010011",
    "M-D" : "000111",
    "D&M" : "000000",
    "D|M" : "010101",
}

with open("prog.asm", "r") as f:
    linha_atual = f.readline()
    lines = list(l.split("//")[0].strip() for l in f.readlines() if l.strip() and not l.strip().startswith("//"))

linha_iniciada_com_parenteses = False
linha_iniciada_com_arroba = False
inteiro_apos_arroba = None
inteiro_apos_arroba_cont = None
linha_atual = None

instrucoes_pular = {}

endereco_a_ser_usado = None

for i, line in enumerate(lines):
    line = line.strip()
    
    correspondencia = re.search(padrao, line)
    correspondencia2 = re.search(padrao2, line)
    correspondencia3 = re.search(padrao3, line)
    
    if line.startswith("("):
        linha_iniciada_com_parenteses = True
        instrucao_pular = line[1:-1]
        if i + 1 < len(lines):
            proxima_linha = lines[i + 1].strip()
            if re.match(r'^@[0-9]+$', proxima_linha):
                instrucoes_pular[instrucao_pular] = int(proxima_linha[1:])
    elif correspondencia3:
        inteiro_apos_arroba = int(correspondencia3.group(0)[1:])
        linha_iniciada_com_parenteses = False
    else:
        inteiro_apos_arroba = cont

    if correspondencia:
        inteiro_apos_arroba_cont = int(correspondencia.group(1))
    elif correspondencia2:
        inteiro_apos_arroba_cont = cont
    else:
        inteiro_apos_arroba_cont = None

for i, line in enumerate(lines): 
    line = line.strip()
    
    if line.startswith("("):
        instrucao_pular = line[1:-1]
        if instrucao_pular in instrucoes_pular:
            endereco_a_ser_usado = instrucoes_pular[instrucao_pular]
        else:
            endereco_a_ser_usado = cont
    
    if line.startswith("@"):
        if line[1:].isdigit():
            a_command = "0" + f"{int(line[1:]):015b}"
            print(a_command)
        elif line == f"@{instrucao_pular}":
            if endereco_a_ser_usado is not None:
                endereco_binario = f"{endereco_a_ser_usado:016b}"
                print(endereco_binario)
            else:
                endereco_contador = f"{cont:016b}"
                print(endereco_contador)
        #else:
            #print(f"Instrução A inválida: {line}")
    else:
        if "=" in line:
            dest = line[:line.index("=")]
            line = line[line.index("=")+1:]
        else:
            dest = ""
        if ";" in line:
            jump = line[line.index(";")+1:]
            line = line[:line.index(";")]
        else:
            jump = ""
        
        comp = line
        if comp in COMP:
            if endereco_a_ser_usado is not None:
                inteiro_apos_arroba = endereco_a_ser_usado
                # endereco_a_ser_usado = None
            c_command = "111" + ("1" if "M" in comp else "0") + COMP[comp] + DEST(dest) + JUMP[jump]
            print(c_command)
        elif line == f"@{instrucao_pular}":
            if endereco_a_ser_usado is not None:
                endereco_binario = f"{endereco_a_ser_usado:016b}"
                print(endereco_binario)