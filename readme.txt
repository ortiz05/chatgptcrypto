git clone git@github.com:ortiz05/crypto.git

# Stop all containers
docker-compose down

# Rebuild
docker-compose build

# Start again
docker-compose up


# Stop all containers
docker-compose down

# Remove orphaned containers
docker-compose down --remove-orphans

# Clean up volumes (be careful with this if you have important data)
docker-compose down -v

docker-compose build --no-cache
docker-compose up

# Stop all containers
docker-compose down

# Remove all containers and volumes
docker-compose rm -f
docker volume prune -f

# Clean up any dangling images
docker system prune -f

# Remove the .env file and create it again
rm .env
nano .env

sudo rm -rf crypto



# Clean everything
docker-compose down -v
docker system prune -f

# Make sure all files are readable
sudo chmod -R 755 .

# Build images
docker-compose build --no-cache

# Start services
docker-compose up -d db redis
sleep 10  # Wait for database to be ready

# Start web and scanners
docker-compose up -d

# Check logs
docker-compose logs -f