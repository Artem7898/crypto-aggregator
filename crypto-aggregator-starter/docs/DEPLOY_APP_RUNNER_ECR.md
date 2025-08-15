# AWS ECR + App Runner (Checklist)

## 0) Prereqs
- AWS account, region chosen
- Install & configure AWS CLI: `aws configure`
- Create ECR repo: `aws ecr create-repository --repository-name crypto-aggregator`

## 1) Build & Push Image
```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/crypto-aggregator"

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

docker build -t crypto-aggregator:latest .
docker tag crypto-aggregator:latest "$REPO:latest"
docker push "$REPO:latest"
```

## 2) Create App Runner Service
- Console → **App Runner** → Create service → **From ECR** → pick repo & image
- Runtime: port **8000**
- Health check: `/healthz`
- Env vars: `ENV=prod`, `REDIS_URL` (if using Redis), `ALLOWED_ORIGINS=*`
- Logs: enable **CloudWatch**

## 3) Secrets
- Use **AWS Secrets Manager** for sensitive values
- Reference them as env vars

## 4) Verify
- Open service URL → `GET /healthz`
- Run connector locally or as a sidecar to populate cache

## 5) CI/CD (outline)
- GitHub Actions: lint/tests → build → push to ECR on tags
- (Optional) trigger App Runner deployment

