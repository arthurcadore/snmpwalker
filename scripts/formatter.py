import csv
import re
import os
import time

def wait_for_stable_file(input_file, timeout=5):
    last_size = -1
    while True:
        current_size = os.path.getsize(input_file)
        if current_size == last_size:
            break
        last_size = current_size
        print(f"Monitorando '{input_file}'...")
        time.sleep(timeout)

def convert_txt_to_csv():
    input_file = os.getenv('INPUT_FILE')
    if not input_file:
        print("Erro: Variável de ambiente INPUT_FILE não definida.")
        return
    
    print(f"Iniciando monitoramento do arquivo...")
    wait_for_stable_file(input_file)
    
    output_file = f"{os.path.splitext(input_file)[0]}.csv"
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)
        csv_writer.writerow(["OID", "MIB", "TYPE", "VALUE"])
        
        pattern = re.compile(r'^(\S+)\s+(\S+)\s+=\s+(\S+):\s*(.*)$')
        
        for line in infile:
            match = pattern.match(line.strip())
            if match:
                oid, mib, var_type, value = match.groups()
                csv_writer.writerow([oid, mib, var_type, value])
    
    print(f"Conversão concluída. Arquivo salvo como {output_file}")

# Executa o processo
convert_txt_to_csv()
