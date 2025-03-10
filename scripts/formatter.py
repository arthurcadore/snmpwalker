import csv
import re
import os

def format_value(value):
    return '\n'.join([value[i:i+32] for i in range(0, len(value), 32)]) if len(value) > 32 else value

def convert_txt_to_csv(input_file):
    output_file = f"{os.path.splitext(input_file)[0]}.csv"
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["OID", "MIB", "TYPE", "VALUE"])
        
        pattern = re.compile(r'^(\S+)\s+(\S+)\s+=\s+(\S+):\s*(.*)$')
        
        for line in infile:
            match = pattern.match(line.strip())
            if match:
                oid, mib, var_type, value = match.groups()
                oid = format_value(oid)
                mib = format_value(mib)
                var_type = format_value(var_type)
                value = format_value(value)
                csv_writer.writerow([oid, mib, var_type, value])
    
    print(f"Conversão concluída. Arquivo salvo como {output_file}")

def process_folder():
    input_folder = os.getenv('INPUT_FOLDER')
    if not input_folder:
        print("Erro: Variável de ambiente INPUT_FOLDER não definida.")
        return
    
    if not os.path.isdir(input_folder):
        print(f"Erro: O diretório {input_folder} não existe.")
        return
    
    txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    
    if not txt_files:
        print("Nenhum arquivo .txt encontrado no diretório.")
        return
    
    for txt_file in txt_files:
        convert_txt_to_csv(os.path.join(input_folder, txt_file))

# Executa o processo
process_folder()
