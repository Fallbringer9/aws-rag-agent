from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    Duration,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigateway,
    aws_apigatewayv2_integrations as integrations,
    aws_iam as iam,
    aws_s3_notifications as s3n,
)
from constructs import Construct

class RagStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.rag_bucket = s3.Bucket(
            self,
            "RagBucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
        )

        CfnOutput(
            self,
            "RagBucketName",
            value=self.rag_bucket.bucket_name,
        )

        self.faiss_layer = _lambda.LayerVersion(
            self,
            "FaissLayer",
            code=_lambda.Code.from_asset("../layers/faiss"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_13],
            compatible_architectures=[_lambda.Architecture.X86_64],
            description="FAISS and numpy dependencies for RAG Lambdas",
        )

        self.strands_layer = _lambda.LayerVersion(
            self,
            "StrandsLayer",
            code=_lambda.Code.from_asset("../layers/strands"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_13],
            compatible_architectures=[_lambda.Architecture.X86_64],
            description="Strands agent dependencies",
        )

        self.ingestion_lambda = _lambda.Function(
            self,
            "IngestionLambda",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="interfaces.api.handler_ingestion.handler",
            code=_lambda.Code.from_asset(
                "../",
                exclude=[
                    ".venv",
                    ".git",
                    ".idea",
                    "infra",
                    "tests",
                    "layers",
                    "data",
                    "README.md",
                    "**/__pycache__",
                    "**/*.pyc",
                ],
            ),
            architecture=_lambda.Architecture.X86_64,
            layers=[self.faiss_layer],
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": self.rag_bucket.bucket_name,
                "BEDROCK_REGION": "us-east-1",
            },
        )

        # Permissions: allow Lambda to read/write in the bucket
        self.rag_bucket.grant_read_write(self.ingestion_lambda)

        self.rag_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.ingestion_lambda),
            s3.NotificationKeyFilter(prefix="documents/")
        )

        self.query_lambda = _lambda.Function(
            self,
            "QueryLambda",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="interfaces.api.handler_query.handler",
            code=_lambda.Code.from_asset(
                "../",
                exclude=[
                    ".venv",
                    ".git",
                    ".idea",
                    "infra",
                    "tests",
                    "layers",
                    "data",
                    "README.md",
                    "**/__pycache__",
                    "**/*.pyc",
                ],
            ),
            architecture=_lambda.Architecture.X86_64,
            layers=[self.faiss_layer, self.strands_layer],
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": self.rag_bucket.bucket_name,
                "BEDROCK_REGION": "us-east-1",
            },
        )

        self.rag_bucket.grant_read(self.query_lambda)

        bedrock_policy = iam.PolicyStatement(
            actions=[
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream",
                "bedrock:Converse",
                "bedrock:ConverseStream",
            ],
            resources=["*"],
        )

        self.ingestion_lambda.add_to_role_policy(bedrock_policy)
        self.query_lambda.add_to_role_policy(bedrock_policy)

        self.http_api = apigateway.HttpApi(
            self,
            "RagHttpApi",
            api_name="aws-rag-agent-api",
        )

        query_integration = integrations.HttpLambdaIntegration(
            "QueryIntegration",
            self.query_lambda,
        )

        self.http_api.add_routes(
            path="/ask",
            methods=[apigateway.HttpMethod.POST],
            integration=query_integration,
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=self.http_api.url,
        )
