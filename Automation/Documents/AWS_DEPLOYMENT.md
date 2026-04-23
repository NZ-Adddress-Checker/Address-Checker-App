# AWS Deployment Guide - ECR and ECS Fargate

## Overview

This guide covers the AWS deployment path for the Address Checker app using:

- Amazon ECR for container images
- Amazon ECS on Fargate for running the backend and frontend
- An Application Load Balancer for public access
- GitHub Actions for build, push, and deploy automation

## Repository Layout

- Backend image source: [app/backend](../../app/backend)
- Frontend image source: [app/frontend](../../app/frontend)
- Image build and push workflow: [\.github/workflows/build-push-ecr.yml](../../.github/workflows/build-push-ecr.yml)
- Infrastructure bootstrap workflow: [\.github/workflows/infra-bootstrap.yml](../../.github/workflows/infra-bootstrap.yml)

## AWS Resources

The deployment flow creates or uses these resources:

- ECR repositories
  - `address-checker-backend`
  - `address-checker-frontend`
- ECS cluster
  - `address-checker`
- ECS services
  - `address-checker-backend`
  - `address-checker-frontend`
- ECS task execution role
  - `ecsTaskExecutionRole`
- CloudWatch log groups
  - `/ecs/address-checker-backend`
  - `/ecs/address-checker-frontend`
- Application Load Balancer
  - `address-checker-alb`
- Target groups
  - `address-checker-backend-tg`
  - `address-checker-frontend-tg`

## Port Mapping

The deployed containers use these internal ports:

- Backend container port: `5000`
- Frontend container port: `50`

The ALB exposes:

- Frontend via listener port `80`
- Backend via listener port `8000`

## Required GitHub Secrets

Set these in GitHub Actions before running the workflows:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `SONAR_TOKEN`
- `REACT_APP_API_URL`
- `REACT_APP_COGNITO_AUTHORITY`
- `REACT_APP_COGNITO_DOMAIN`
- `REACT_APP_COGNITO_CLIENT_ID`
- `REACT_APP_REDIRECT_URI`
- `REACT_APP_LOGOUT_URI`
- `COGNITO_REGION`
- `USER_POOL_ID`
- `CLIENT_ID`

## Required GitHub Variables

Set these repository variables for the deploy workflow:

- `ECS_CLUSTER` = `address-checker`
- `ECS_BACKEND_SERVICE` = `address-checker-backend`
- `ECS_FRONTEND_SERVICE` = `address-checker-frontend`

## Bootstrap Workflow

Run [infra-bootstrap.yml](../../.github/workflows/infra-bootstrap.yml) first if the AWS resources do not already exist.

It will:

1. Resolve the default VPC and subnets.
2. Create security groups for the ALB and ECS tasks.
3. Create the ECS cluster.
4. Create CloudWatch log groups.
5. Create the ALB, target groups, and listeners.
6. Register task definitions for backend and frontend.
7. Create or update the ECS services.

## Build and Deploy Workflow

Run [build-push-ecr.yml](../../.github/workflows/build-push-ecr.yml) on `mainline` to:

1. Build the backend image.
2. Scan it with Trivy.
3. Push it to ECR.
4. Build the frontend image with the AWS and Cognito build args.
5. Scan it with Trivy.
6. Push it to ECR.
7. Register updated ECS task definitions.
8. Deploy both ECS services.
9. Wait for the services to stabilize.

## Backend Runtime Configuration

The backend container expects these environment variables in Fargate:

- `COGNITO_REGION`
- `USER_POOL_ID`
- `CLIENT_ID`
- `CORS_ORIGIN`

The workflow sets `CORS_ORIGIN` to the ALB DNS name.

## Frontend Runtime Configuration

The frontend build receives these build arguments:

- `REACT_APP_API_URL`
- `REACT_APP_COGNITO_AUTHORITY`
- `REACT_APP_COGNITO_DOMAIN`
- `REACT_APP_COGNITO_CLIENT_ID`
- `REACT_APP_REDIRECT_URI`
- `REACT_APP_LOGOUT_URI`

The build uses these values to point the React app at the deployed backend and Cognito endpoints.

## Verification

After deployment, verify:

1. The ECS services are running.
2. The backend health endpoint responds at `/api/health`.
3. The frontend responds from the ALB DNS name.
4. The frontend can reach the backend through the configured API URL.

Example checks:

```bash
aws ecs describe-services --cluster address-checker --services address-checker-backend address-checker-frontend
curl http://<alb-dns-name>:8000/api/health
curl http://<alb-dns-name>
```

## Troubleshooting

- If the backend task fails health checks, confirm the task definition uses container port `5000`.
- If the frontend does not load, confirm the task definition uses container port `50` and the target group is healthy.
- If GitHub Actions cannot push to ECR, confirm the OIDC role and ECR repository names exist.
- If Cognito login fails, confirm the build arguments and backend environment variables match the Cognito user pool.
