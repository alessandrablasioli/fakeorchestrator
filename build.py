import json
import os
import subprocess
import xml_utils
import sys
import yaml
from jinja2 import Template
from collections import defaultdict

def count_objects_per_class(file_path):
    class_labels = ["Client", "Database", "Firewall", "Router", "Server", "WebServer"]
    class_counts = defaultdict(int)

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            data = line.split()
            class_id = int(data[0])

            if class_id < len(class_labels):
                class_label = class_labels[class_id]
                class_counts[class_label] += 1

    # Creazione della lista di dizionari
    result_list = [{'Type': label} for label, count in class_counts.items() for _ in range(count)]
    return result_list

'''
ANALYZE THE INPUT: IMAGE OR XML
'''
def analyze_file(file_path):
    # Verifica se il file è un XML
    if file_path.lower().endswith('.xml'):
        # Chiama la funzione per il parsing XML
        result = xml_utils.parse_xml_file(file_path)
        print(result)
    elif any(file_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
        # Verifica se il file è un'immagine
        # Chiama il comando per la classificazione delle immagini
        command = f'''
        python C:/Users/Acer/Dropbox/PC/Desktop/yolov5/detect.py --source C:/Users/Acer/Dropbox/PC/Desktop/cybersecurity/Progetto/diag3.jpg --weights C:/Users/Acer/Dropbox/PC/Desktop/yolov5/runs/train/yolov5s_results20/weights/best.pt --conf 0.0019 --save-txt --save-conf --img-size 256 --augment --iou-thres=0
        '''
        os.system(command=command)
        result= count_objects_per_class('C:/Users/Acer/Dropbox/PC/Desktop/yolov5/runs/detect/exp230/labels/diag3.txt')
        print(result)

    else:
        print("Tipo di file non supportato")

    return result


# Funzione per associare le immagini Docker ai servizi
import json

def associate_images_to_services(services_list):
    # Leggi il file JSON che associa i servizi alle immagini Docker
    with open('conf.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Associa le immagini Docker ai servizi
    images_for_services = {}
    for service_dict in services_list:
        service_type = service_dict.get('Type').lower()
        if service_type and service_type in config_data['services']:
            configs = images_for_services.get(service_type)
            if configs is None:
                images_for_services[service_type] = [config_data['services'][service_type]]
            else:
                configs.append(config_data['services'][service_type])
    print(images_for_services)
    return images_for_services



def generate_docker_compose(services_to_images):
    docker_compose_content = ["version: '3'", "services:"]

    # Verifica se services_to_images contiene dati
    if services_to_images:
        # Aggiungi ogni servizio con l'immagine corrispondente al docker-compose
        for service, images in services_to_images.items():
            i = 1
            for image in images:
                if i > 1:
                    service = service + f"-{i}"
                service_content = f"  {service}:\n    image: {image}"
                # Verifica se il servizio è il webserver e aggiungi la porta se è lui
                if service == 'webserver':
                    service_content += "\n    ports:\n      - '8080:80'"  # Cambia la porta come necessario
                docker_compose_content.append(service_content)
                # Puoi aggiungere altre configurazioni o parametri per ciascun servizio qui se necessario
                i += 1
        
    # Scrivi il contenuto nel file docker-compose.yml
    with open('docker-compose.yml', 'w') as docker_compose_file:
        docker_compose_file.write('\n'.join(docker_compose_content))

    return os.path.abspath('docker-compose.yml')



def start_docker_compose(docker_compose_path):
    if os.path.exists(docker_compose_path):
        # Start Docker Compose using subprocess command
        subprocess.run(["docker-compose", "-f", docker_compose_path, "up", "-d"], check=True)
        print("Docker Compose started successfully.")
    else:
        print("The specified Docker Compose file does not exist.")



def generate_terraform_config_from_docker_compose(docker_compose_file):
    with open(docker_compose_file, 'r') as file:
        docker_compose_data = yaml.safe_load(file)

        # Caricamento del template Terraform utilizzando Jinja2
        with open('terraform_template.tf.j2', 'r') as template_file:
            template_content = template_file.read()
        
        # Inizializzazione del template Jinja2
        template = Template(template_content)

        # Creazione del contesto per il template
        context = {'services': docker_compose_data['services']}

        # Rendering del template con il contesto
        terraform_config = template.render(context)

        # Definizione del percorso del file Terraform da creare
        terraform_file_path = "main.tf"

        # Scrittura del contenuto nel file Terraform
        with open(terraform_file_path, 'w') as terraform_file:
            terraform_file.write(terraform_config)

        return terraform_file_path


def terraform_apply_from_config_file():
    try:
        # Esegui il comando per inizializzare Terraform
        subprocess.run(["C:/Program Files/Terraform/terraform", "init"], check=True)
        
        subprocess.run(["C:/Program Files/Terraform/terraform", "refresh"], check=True)
        # Esegui il piano Terraform
        subprocess.run(["C:/Program Files/Terraform/terraform", "plan", "-out=tfplan"], check=True)
        subprocess.run(["C:/Program Files/Terraform/terraform", "show"], check=True)
        # Applica il piano Terraform
        subprocess.run(["C:/Program Files/Terraform/terraform", "apply"], check=True)
        print("Success: Terraform plan applied.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to apply Terraform plan - {e}")


'''
------
 MAIN
------
'''

def main():
    if len(sys.argv) < 2:
        print("Please provide the file name as an argument")
        return

    file_name = sys.argv[1]
    file_path = os.path.abspath(file_name)

    # Check if the file exists
    weights_path = 'C:/Users/Acer/Dropbox/PC/Desktop/yolov5/runs/train/yolov5s_results20/weights/best.pt'
    if not os.path.exists(weights_path):
        print("Training has not been executed. Please wait before proceeding...")
        # Execute yolo.py script if weights fil1e does not exist
        subprocess.run("python yolo.py", shell=True)
        print(file_path)
        services_detected = analyze_file(file_path)
        print(services_detected)
    else:
        # Run the analyze_file function if the weights file exists
        services_detected = analyze_file(file_path)
        print(services_detected)
    print("Please wait for image association...")
    
    images_associated = associate_images_to_services(services_detected)

    # Print the association between services and Docker images
    for service, images in images_associated.items():
        for image in images:
            print(f"Service: {service} - Docker Image: {image}")
    docker_compose_path = generate_docker_compose(images_associated) 

    start_docker_compose(docker_compose_path)  
    terraform_file_path = generate_terraform_config_from_docker_compose(docker_compose_path)
    print(f"Generated Terraform configuration file created: {terraform_file_path}")
    terraform_apply_from_config_file()

    

if __name__ == "__main__":
    main()

