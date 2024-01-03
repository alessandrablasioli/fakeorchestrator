import subprocess
import os
import docker


'''
def create_dockerfiles(components, dockerfile_dir):
    dockerfile_dir = dockerfile_dir

    for component in components:
        component_name = component["Type"]
        if component_name == "Database":
            dockerfile_content = """
            FROM mysql:latest

            # Imposta la password per l'utente root
            ENV MYSQL_ROOT_PASSWORD=your_password

            # Copia gli script SQL all'interno del container
            COPY ./initialization_script.sql /docker-entrypoint-initdb.d/

            # Avvia il server MySQL
            CMD ["mysqld"]
            """
            dockerfile_path = os.path.join(dockerfile_dir, "Dockerfile_Database")
            with open(dockerfile_path, "w") as dockerfile:
              dockerfile.write(dockerfile_content)

            
            image_name = f"my-{component_name.lower()}-image:latest"
            subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])

            container_name = f"my-{component_name.lower()}-container"
            subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])

        if component_name == "Server":
            dockerfile_content = f"""
            FROM ubuntu:latest

            # Esempio di comandi per installare e configurare un server (es. Apache)
            RUN apt-get update && apt-get install -y apache2
            """
            dockerfile_path = os.path.join(dockerfile_dir, f"Dockerfile_{component_name}")

            with open(dockerfile_path, "w") as dockerfile:
              dockerfile.write(dockerfile_content)

            image_name = f"my-{component_name.lower()}-image:latest"
            subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])

            container_name = f"my-{component_name.lower()}-container"
            subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])

        elif component_name == "WebServer":
            dockerfile_content = f"""
            FROM nginx:latest

            # Esempio di comandi per configurare un server web (es. Nginx)
            # Sostituisci 'index.html' con il tuo file HTML principale
            COPY dockerfiles/index.html /usr/share/nginx/html/index.html
            EXPOSE 8080
            CMD ["nginx", "-g", "daemon off;"]
            """
            dockerfile_path = os.path.join(dockerfile_dir, f"Dockerfile_{component_name}")

            with open(dockerfile_path, "w") as dockerfile:
              dockerfile.write(dockerfile_content)

            image_name = f"my-{component_name.lower()}-image:latest"
            print( subprocess.getstatusoutput(["docker", "build", "-t", image_name, "-f", dockerfile_path, ".", "--no-cache"]))

            container_name = f"my-{component_name.lower()}-container"
            subprocess.run(["docker", "run", "-d", "-p", "8080:80", "--name", container_name, image_name])
            
        elif component_name == "Client":
            dockerfile_content = f"""
            FROM ubuntu:latest

            # Esempio di comandi per installare software client (es. SSH client)
            RUN apt-get update && apt-get install -y openssh-client

            """
            dockerfile_path = os.path.join(dockerfile_dir, f"Dockerfile_{component_name}")

            with open(dockerfile_path, "w") as dockerfile:
              dockerfile.write(dockerfile_content)

            image_name = f"my-{component_name.lower()}-image:latest"
            subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])

            container_name = f"my-{component_name.lower()}-container"
            subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])
        elif component_name == "Firewall":
            dockerfile_content = f"""
            FROM ubuntu:latest

            # Esempio di comandi per installare e configurare un firewall (es. iptables)
            RUN apt-get update && apt-get install -y iptables


            """
            dockerfile_path = os.path.join(dockerfile_dir, f"Dockerfile_{component_name}")

            with open(dockerfile_path, "w") as dockerfile:
              dockerfile.write(dockerfile_content)

            image_name = f"my-{component_name.lower()}-image:latest"
            subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])

            container_name = f"my-{component_name.lower()}-container"
            subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])

'''


def create_dockerfiles(components, dockerfile_dir):
    docker_compose_content = "version: '3'\n\nservices:\n"
    good = ['Database', 'Server', 'WebServer', 'Client', 'Firewall']
    filtered = []
    for c in components:
        if c['Type'] in good:
            filtered.append(c)
    components = filtered
    for component in components:

        component_name = component["Type"]
        image_name = f"my-{component_name.lower()}-image:latest"
        container_name = f"{component_name.lower()}--2"

        dockerfile_content = ""

        if component_name == "Database":
            dockerfile_content = """
            FROM mysql:latest

            # Set root user password
            ENV MYSQL_ROOT_PASSWORD=your_password

            # Copy SQL scripts into the container
            COPY ./initialization_script.sql /docker-entrypoint-initdb.d/

            # Start MySQL server
            CMD ["mysqld"]
            """
        elif component_name == "Server":
            dockerfile_content = """
            FROM ubuntu:latest

            # Example commands to install and configure a server (e.g., Apache)
            RUN apt-get update && apt-get install -y apache2
            CMD ["tail", "-f", "/dev/null"]

            """
        elif component_name == "WebServer":
            dockerfile_content = """
            FROM nginx:latest

            # Example commands to configure a web server (e.g., Nginx)
            # Replace 'index.html' with your main HTML file
            COPY dockerfiles/index.html /usr/share/nginx/html/index.html
            EXPOSE 8080
            CMD ["nginx", "-g", "daemon off;"]
            """
        elif component_name == "Client":
            dockerfile_content = """
            FROM ubuntu:latest

            # Installa il software del client (esempio: SSH client)
            RUN apt-get update && apt-get install -y openssh-client


            # Esempio di comando che mantiene il container in esecuzione
            CMD ["tail", "-f", "/dev/null"]

            """
        elif component_name == "Firewall":
            dockerfile_content = """
            FROM ubuntu:latest

            # Example commands to install and configure a firewall (e.g., iptables)
            RUN apt-get update && apt-get install -y iptables
            CMD ["tail", "-f", "/dev/null"]

            """

        # Write Dockerfile
        dockerfile_path = os.path.join(dockerfile_dir, f"Dockerfile_{component_name}")
        with open(dockerfile_path, "w") as dockerfile:
            dockerfile.write(dockerfile_content)

        # Build Docker image
        subprocess.run(["docker", "build", "-t", image_name, "-f", dockerfile_path, "."])

        # Run Docker container
        subprocess.run(["docker", "run", "-d", "--name", container_name, image_name])

        # Append container to docker-compose content
        docker_compose_content += f"  {container_name}:\n"
        docker_compose_content += f"    image: {image_name}\n"
        docker_compose_content += "    # Add any other necessary configurations\n\n"
        if container_name == 'webserver':
                docker_compose_content += "\n    ports:\n      - '8080:80'"

    # Write docker-compose.yml file
    docker_compose_path = os.path.join(dockerfile_dir, "dockercompose.yml")
    with open(docker_compose_path, "w") as docker_compose_file:
        docker_compose_file.write(docker_compose_content)

    # Run docker-compose up command
    subprocess.run(["docker-compose", "-f", docker_compose_path, "up", "-d"], cwd=dockerfile_dir)

    return docker_compose_path







