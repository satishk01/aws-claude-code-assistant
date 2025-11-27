# AWS Bedrock Setup Guide

This guide explains how to configure and use AWS Bedrock as the LLM provider for the Claude Code Assistant.

## 🚀 Quick Start

### 1. Set Provider to Bedrock (Default)

Create or edit your `.env` file:

```bash
# Use Bedrock as the LLM provider (default)
LLM_PROVIDER=bedrock

# AWS Bedrock Configuration
AWS_REGION=us-east-1
BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0

# Optional: Customize LLM settings
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4096
```

### 2. Configure AWS Credentials

The assistant supports multiple AWS credential methods:

#### Option A: IAM Role (Recommended for EC2)
If running on EC2, attach an IAM role with Bedrock permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
            ]
        }
    ]
}
```

#### Option B: AWS Profile
```bash
# Set AWS profile
export AWS_PROFILE=your-profile-name

# Or add to .env
AWS_PROFILE=your-profile-name
```

#### Option C: Environment Variables
```bash
# Add to .env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
```

### 3. Run the Assistant

```bash
# Install dependencies
uv sync

# Run the assistant
uv run main.py
```

## 🔧 Configuration Options

### Available Bedrock Models

| Model ID | Description | Use Case |
|----------|-------------|----------|
| `anthropic.claude-3-5-sonnet-20241022-v2:0` | Latest Sonnet (Default) | Complex reasoning, coding |
| `anthropic.claude-3-haiku-20240307-v1:0` | Fast Haiku | Quick responses, simple tasks |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `bedrock` | Provider: `bedrock` or `anthropic` |
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |
| `BEDROCK_MODEL` | `anthropic.claude-3-5-sonnet-20241022-v2:0` | Model ID |
| `LLM_TEMPERATURE` | `0.0` | Response randomness (0.0-1.0) |
| `LLM_MAX_TOKENS` | `4096` | Maximum response length |

## 🔄 Switching Between Providers

### Switch to Bedrock (Default)
```bash
# Edit .env
LLM_PROVIDER=bedrock
```

### Switch to Anthropic
```bash
# Edit .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

The assistant will automatically detect and use the configured provider on startup.

## 🛠️ Troubleshooting

### "Unable to locate credentials"
- Ensure AWS credentials are configured (IAM role, profile, or env vars)
- Check AWS CLI: `aws sts get-caller-identity`
- Verify region is supported for Bedrock

### "Access Denied" Errors
- Check IAM permissions for `bedrock:InvokeModel`
- Ensure the model is available in your region
- Request model access in AWS Bedrock console if needed

### "Model not found"
- Verify the model ID is correct
- Check if the model is available in your AWS region
- Some models require explicit access requests

### Region Availability
Bedrock is available in these regions:
- `us-east-1` (N. Virginia) - Recommended
- `us-west-2` (Oregon)
- `eu-west-1` (Ireland)
- `ap-southeast-1` (Singapore)

## 📊 Cost Optimization

### Model Pricing (Approximate)
- **Claude 3.5 Sonnet**: $3.00 per 1M input tokens, $15.00 per 1M output tokens
- **Claude 3 Haiku**: $0.25 per 1M input tokens, $1.25 per 1M output tokens

### Tips to Reduce Costs
1. Use Haiku for simple tasks: `BEDROCK_MODEL=anthropic.claude-3-haiku-20240307-v1:0`
2. Lower max tokens: `LLM_MAX_TOKENS=2048`
3. Monitor usage in AWS Cost Explorer

## 🔐 Security Best Practices

1. **Use IAM Roles**: Prefer IAM roles over access keys
2. **Least Privilege**: Grant minimal required permissions
3. **Rotate Keys**: Regularly rotate access keys if used
4. **Monitor Usage**: Set up CloudWatch alarms for unusual activity
5. **VPC Endpoints**: Use VPC endpoints for private connectivity

## 🚀 EC2 Deployment

### 1. Create IAM Role
```bash
# Create role with Bedrock permissions
aws iam create-role --role-name BedrockCodeAssistant --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name BedrockCodeAssistant --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### 2. Launch EC2 Instance
```bash
# Launch with IAM role
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.medium \
    --iam-instance-profile Name=BedrockCodeAssistant \
    --key-name your-key-pair \
    --security-group-ids sg-12345678
```

### 3. Setup on EC2
```bash
# Install Python and uv
sudo apt update
sudo apt install -y python3 python3-pip
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone <your-repo>
cd claude-code-assistant
cp .env.example .env
# Edit .env to set LLM_PROVIDER=bedrock

# Install and run
uv sync
uv run main.py
```

## 📈 Monitoring

### CloudWatch Metrics
Monitor these metrics in CloudWatch:
- `AWS/Bedrock/InvocationsCount`
- `AWS/Bedrock/InputTokenCount`
- `AWS/Bedrock/OutputTokenCount`

### Cost Alerts
Set up billing alerts for Bedrock usage:
```bash
aws budgets create-budget --account-id 123456789012 --budget file://bedrock-budget.json
```

## 🔗 Additional Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude Models](https://docs.anthropic.com/claude/docs/models-overview)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)