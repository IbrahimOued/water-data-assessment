# Makefile pour l'évaluation Uduma

.PHONY: start stop check-docker

check-docker:
	@echo "Vérification de l'installation de docker compose..."
	@if ! (command -v docker-compose >/dev/null 2>&1 || command -v docker compose >/dev/null 2>&1); then \
		echo "ERREUR : docker compose n'est pas installé. Veuillez l'installer d'abord." >&2; \
		exit 1; \
	fi
	@echo "docker compose est installé."

start: check-docker
	@echo "Vérification des fichiers docker-compose..."
	@if [ ! -f docker-compose.yml ] && [ ! -f docker-compose.yaml ]; then \
		echo "ERREUR : Le fichier docker-compose.yml ou docker-compose.yaml est introuvable dans le répertoire courant." >&2; \
		exit 1; \
	fi
	@echo "Démarrage des conteneurs Docker..."
	@docker compose up -d
	@if [ $$? -ne 0 ]; then \
		echo "ERREUR : Échec du démarrage des conteneurs Docker. Veuillez vérifier le fichier docker compose et réessayer." >&2; \
		exit 1; \
	fi
	@sleep 10
	@echo "Vérification de l'état du conteneur Airflow..."
	@docker inspect -f '{{.State.Health.Status}}' airflow
	@echo "Trigger du DAG..."
	@docker exec airflow airflow dags trigger upload_water_metering_to_postgres
	@echo "Vérification de l'état du DAG..."
	@docker exec airflow airflow dags list-runs upload_water_metering_to_postgres
	@echo "Les conteneurs Docker ont démarré avec succès."


stop: check-docker
	@echo "Vérification des fichiers docker-compose..."
	@if [ ! -f docker-compose.yml ] && [ ! -f docker-compose.yaml ]; then \
		echo "ERREUR : Le fichier docker-compose.yml ou docker-compose.yaml est introuvable dans le répertoire courant." >&2; \
		exit 1; \
	fi
	@echo "Arrêt des conteneurs Docker..."
	@docker compose down
	@if [ $$? -ne 0 ]; then \
		echo "ERREUR : Échec de l'arrêt des conteneurs Docker. Veuillez vérifier le fichier docker-compose.yml et réessayer." >&2; \
		exit 1; \
	fi
	@echo "Les conteneurs Docker ont été arrêtés avec succès."

credentials: check-docker
	@echo "Récupération des credentials Airflow..."
	@sleep 10
	@docker exec airflow bash -c "cat simple_auth_manager_passwords.json.generated" > airflow_credentials.txt
	@echo "Les credentials ont été récupérés et copiés dans airflow_credentials.txt."