# 🐳 Docker Deployment Guide

This guide covers Docker deployment for the Tech News Aggregator platform with both development and production configurations.

## 🚀 Quick Start

### Prerequisites
- Docker 20.0+ and Docker Compose 2.0+
- At least 4GB RAM available for Docker
- OpenAI API key

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
# Set your OPENAI_API_KEY and other configurations
```

### 2. Development Environment
```bash
# Start development environment
./build.sh dev up

# Or using Docker Compose directly
docker-compose up --build -d
```

### 3. Production Environment
```bash
# Start production environment
./build.sh prod up

# Or using Docker Compose directly
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📁 Docker Files Overview

### Core Docker Files
- **`backend/Dockerfile`** - Production backend image
- **`backend/Dockerfile.dev`** - Development backend with hot reload
- **`backend/.dockerignore`** - Optimized build context

### Orchestration Files
- **`docker-compose.yml`** - Development environment
- **`docker-compose.prod.yml`** - Production environment with scaling
- **`build.sh`** - Automated build and deployment script

### Configuration Files
- **`nginx.conf`** - Load balancer and reverse proxy
- **`redis.conf`** - Redis configuration with persistence
- **`crontab`** - Automated news fetching schedule

## 🏗️ Architecture

### Development Environment
```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Frontend      │    │   Backend    │    │   Redis     │
│   (Optional)    │    │   FastAPI    │    │   Cache     │
│   Port: 3000    │───▶│   Port: 8000 │───▶│   Port: 6379│
└─────────────────┘    └──────────────┘    └─────────────┘
                              │
                              ▼
                       ┌──────────────┐
                       │ PostgreSQL   │
                       │ Port: 5432   │
                       └──────────────┘
```

### Production Environment
```
┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Nginx     │    │  Backend    │    │   Redis      │    │ PostgreSQL  │
│ Load Balancer│───▶│  (2+ replicas)│───▶│   Cache      │    │  Database   │
│ Port: 80/443│    │  Port: 8000 │    │  Port: 6379  │    │ Port: 5432  │
└─────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │ News Fetcher │
                   │  Cron Job    │
                   └──────────────┘
```

## 🔧 Build Script Usage

The `build.sh` script provides a convenient interface for managing Docker deployments:

### Development Commands
```bash
# Start development environment
./build.sh dev up

# View logs
./build.sh dev logs

# Stop environment
./build.sh dev down

# Restart services
./build.sh dev restart
```

### Production Commands
```bash
# Start production environment
./build.sh prod up

# Scale API to 4 replicas
./build.sh prod scale 4

# View production logs
./build.sh prod logs

# Stop production environment
./build.sh prod down
```

### Utility Commands
```bash
# Run health checks
./build.sh test

# Clean up Docker resources
./build.sh clean

# Show help
./build.sh help
```

## 🌐 Service Access

### Development Environment
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Redis**: localhost:6379
- **PostgreSQL**: localhost:5432

### Production Environment
- **Load Balancer**: http://localhost:80
- **API (Direct)**: http://localhost:8000
- **Redis**: localhost:6379
- **PostgreSQL**: localhost:5432

## 📊 Monitoring and Health Checks

### Health Endpoints
```bash
# API Health Check
curl http://localhost:8000/health

# Redis Health Check
docker exec tech_news_redis redis-cli ping

# PostgreSQL Health Check
docker exec tech_news_postgres pg_isready -U technews_user
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# Production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Resource Monitoring
```bash
# Container stats
docker stats

# Service status
docker-compose ps

# Disk usage
docker system df
```

## ⚙️ Configuration

### Environment Variables
Key configuration options in `.env`:

```bash
# Required
OPENAI_API_KEY=your_api_key_here
POSTGRES_PASSWORD=secure_password

# Optional
MAX_ARTICLES_PER_BATCH=50
RSS_TIMEOUT=30
REDIS_PASSWORD=redis_password
```

### Resource Limits
Production services have configured resource limits:

- **API**: 1GB RAM limit, 512MB reserved
- **Redis**: 512MB RAM limit, 256MB reserved  
- **PostgreSQL**: 1GB RAM limit, 512MB reserved
- **Nginx**: 128MB RAM limit, 64MB reserved

### Scaling Configuration
```bash
# Scale API service
docker-compose -f docker-compose.prod.yml up --scale api=3 -d

# Using build script
./build.sh prod scale 3
```

## 🔒 Security Considerations

### Production Security
- **Non-root user**: Backend runs as non-root user in container
- **Resource limits**: All services have memory limits
- **Network isolation**: Services communicate via Docker network
- **Health checks**: All services have health monitoring

### SSL Configuration
Uncomment HTTPS section in `nginx.conf` for SSL:

1. Place SSL certificates in `./ssl/` directory
2. Update `nginx.conf` with your domain
3. Uncomment HTTPS server block

### Redis Security
For production, uncomment password in `redis.conf`:
```conf
requirepass your_secure_redis_password
```

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check if ports are in use
netstat -tulpn | grep :8000
netstat -tulpn | grep :6379
netstat -tulpn | grep :5432

# Stop conflicting services
sudo systemctl stop redis
sudo systemctl stop postgresql
```

#### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Connect to database manually
docker exec -it tech_news_postgres psql -U technews_user -d technews
```

#### Redis Connection Issues
```bash
# Check Redis logs
docker-compose logs redis

# Test Redis connection
docker exec -it tech_news_redis redis-cli ping
```

#### UV Cache Permission Issues
```bash
# If you see "Permission denied" for UV cache directory:

# Option 1: Use the simple Dockerfile
cd backend
cp Dockerfile.simple Dockerfile
docker-compose build --no-cache api

# Option 2: Clean and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Option 3: Check UV cache volume permissions
docker volume inspect <project>_uv_cache
```

#### API Not Responding
```bash
# Check API logs
docker-compose logs api

# Restart API service
docker-compose restart api

# Check health endpoint
curl -v http://localhost:8000/health
```

### Performance Issues
```bash
# Check container resource usage
docker stats

# Clean up unused resources
./build.sh clean

# Restart with fresh containers
docker-compose down && docker-compose up --build -d
```

### Log Management
```bash
# Clean old logs
docker system prune -f

# Limit log size in docker-compose.yml
services:
  api:
    logging:
      options:
        max-size: "10m"
        max-file: "3"
```

## 🔄 Updates and Maintenance

### Updating Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
./build.sh prod down
./build.sh prod up
```

### Database Migrations
```bash
# Access database container
docker exec -it tech_news_postgres psql -U technews_user -d technews

# Run manual migrations if needed
# (Add migration commands here)
```

### Backup and Restore
```bash
# Backup PostgreSQL
docker exec tech_news_postgres pg_dump -U technews_user technews > backup.sql

# Restore PostgreSQL
docker exec -i tech_news_postgres psql -U technews_user -d technews < backup.sql

# Backup Redis
docker exec tech_news_redis redis-cli --rdb /data/backup.rdb
```

## 📈 Performance Optimization

### Production Optimizations
- **Multi-stage builds**: Optimized Docker images
- **Resource limits**: Prevent resource exhaustion
- **Health checks**: Automatic service recovery
- **Load balancing**: Nginx with upstream servers
- **Caching**: Redis with persistence
- **Connection pooling**: PostgreSQL optimization

### Scaling Strategies
```bash
# Horizontal scaling
./build.sh prod scale 4

# Vertical scaling (adjust in docker-compose.prod.yml)
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 🎯 Next Steps

1. **SSL Setup**: Configure HTTPS with Let's Encrypt
2. **Monitoring**: Add Prometheus and Grafana
3. **CI/CD**: Set up automated deployment
4. **Backups**: Implement automated backup strategy
5. **Alerting**: Configure health check alerts

For more information, see the main [README.md](README.md) file.