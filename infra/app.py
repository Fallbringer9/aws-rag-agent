#!/usr/bin/env python3
import os

import aws_cdk as cdk


from stacks.rag_stack import RagStack


app = cdk.App()

env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION")
)

RagStack(app, "RagStack", env=env,)

app.synth()
