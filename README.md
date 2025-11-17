# RAMIC - Remote Actuation of Motors with Industrial Control

O **RAMIC** é um sistema de controle e monitoramento de motores industriais desenvolvido em Django. A plataforma permite o acionamento remoto, o acompanhamento do estado em tempo real e o registro de todo o histórico de operações de cada motor.

## 🛠️ Tecnologias Utilizadas
<table> <tr> <td align="center"><strong>Backend</strong></td> <td align="center"><strong>Frontend</strong></td> <td align="center"><strong>Base de Dados</strong></td> </tr> <tr> <td align="center"> <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python Badge"/> <br> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" alt="Django Badge"/> </td> <td align="center"> <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 Badge"/> <br> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3 Badge"/> <br> <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap Badge"/> </td> <td align="center"> <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite Badge"/> </td> </tr> </table>

## ✨ Funcionalidades

-   **Autenticação de Utilizadores:** Sistema seguro de login e registo de contas.
    
-   **Dashboard Intuitivo:** Visualização rápida do estado de todos os motores (Ligado, Desligado, Em Manutenção).
    
-   **Controle Remoto:** Ligue e desligue os motores com um único clique.
    
-   **Gestão de Motores (CRUD):** Adicione, edite e apague motores com informações detalhadas.
    
-   **Modo de Manutenção:** Coloque os motores em modo de manutenção para desativar os controlos.
    
-   **Histórico Detalhado:** Registo de todas as ações realizadas em cada motor.
    
-   **Pesquisa e Filtragem:** Encontre motores rapidamente por nome, número de série ou localização.
    
-   **Exportação de Dados:** Exporte o histórico completo de acionamentos para um arquivo CSV.
    


## ⚙️ Setup e Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento. Clique no seu sistema operacional:

<details> <summary><strong> 💻 Raspberry </strong></summary>

1.  **Instale os pacotes:**

    Bash
    
    ```
    sudo apt install net-tools
    sudo apt install openssh-server
    sudo apt install mosquitto mosquitto_clients
    sudo apt intall mariadb-server
    sudo apt install guncorn nginx -y 

    sudo nano /etc/netplan/*.yaml
    sudo tail -f /log/var/mosquitto/mosquitto.conf
    ```
    
2.  **Identifique falhas:**
    
    Bash
    
    ```
    sudo systemctl status ssh
    sudo systemctl start ssh
    sudo systemctl status mosquitto 
    sudo ss -tulnp | grep 1883
    sudo chown mosquitto:mosquitto /etc/mosquitto/passwd
    sudo chmod 600 /etc/mosquitto/passwd

    sudo cd /etc/ssh
    sudo ssh-keygen -A
    sudo sshd -t
    
    ```
    
3.  **Verifique bloqueios no firewall do linux e autorize portas:**
    
    Bash
    
    ```
    sudo ufw status verbose  
    sudo ufw allow 1883 
    sudo ufw allow ssh
    sudo ufw enable
    
    ```
    
4.  **Inscreva-se e publique tópicos:**
    
    Bash
    
    ```
    mosquitto_sub -u <usuario> -P <senha> -v -t 'motor/a110'   
    mosquitto_pub -h <ip> -u <usuario> -P <senha> -t "motor/a110" -m "ligar" 
    mosquitto_pub -h <ip> -u <usuario> -P <senha> -t "motor/a110" -m "desligar"
    
    ```
    

</details>


<details> <summary><strong> 💻 Windows </strong></summary>

1.  **Crie e ative um ambiente virtual:**
    
    Bash
    
    ```
    # É recomendado usar Python 3.9 ou superior
    python -m venv ramic_env
    .\ramic_env\Scripts\activate
    
    ```
    
2.  **Instale as dependências:**
    
    Bash
    
    ```
    pip install -r requirements.txt
    
    ```
    
3.  **Execute as migrações da base de dados:**
    
    Bash
    
    ```
    python manage.py makemigrations
    python manage.py migrate
    
    ```
    
4.  **Crie um superusuário (administrador):**
    
    Bash
    
    ```
    python manage.py createsuperuser
    
    ```
    

</details>

<details> <summary><strong> 🍏 Macbook </strong></summary>

1.  **Crie e ative um ambiente virtual:**
    
    Bash
    
    ```
    # É recomendado usar Python 3.9 ou superior
    python3 -m venv ramic_env
    source ramic_env/bin/activate
    
    ```
    
2.  **Instale as dependências:**
    
    Bash
    
    ```
    pip install -r requirements.txt
    
    ```
    
3.  **Execute as migrações da base de dados:**
    
    Bash
    
    ```
    python manage.py makemigrations
    python manage.py migrate
    
    ```
    
4.  **Crie um superusuário (administrador):**
    
    Bash
    
    ```
    python manage.py createsuperuser
    
    ```
    

</details>

----------

## ▶️ Como Executar o Projeto

Após a instalação, com o ambiente virtual ativado, inicie o servidor de desenvolvimento:

Bash

```
python manage.py runserver

```

Abra o seu navegador e acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/).



## 👥 Criadores e Orientador
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/mauricioroos">
        <img src="https://github.com/mauricioroos.png" width="115"><br>
        <sub><b>Mauricio Roos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/KauanFruhauf">
        <img src="https://github.com/KauanFruhauf.png" width="115"><br>
        <sub><b>Kauan</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/dbernardos">
        <img src="https://github.com/dbernardos.png" width="115"><br>
        <sub><b>Davi Bernardos</b></sub><br>
        <sub>(Orientador)</sub>
      </a>
    </td>
  </tr>
</table>
