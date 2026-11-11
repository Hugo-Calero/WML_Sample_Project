import io
import os

import ibm_boto3
import pandas as pd
from botocore.client import Config
from ibm_watsonx_ai import APIClient
from sklearn.tree import DecisionTreeClassifier

# All secrets are read from environment variables. Never commit them to Git.
# Required: COS_API_KEY, COS_INSTANCE_CRN, WML_API_KEY, PROJECT_ID
# Optional: COS_ENDPOINT, COS_BUCKET, COS_OBJECT_KEY, WML_URL
cos_client = ibm_boto3.client(
    service_name="s3",
    ibm_api_key_id=os.environ["COS_API_KEY"],
    ibm_service_instance_id=os.environ["COS_INSTANCE_CRN"],
    ibm_auth_endpoint="https://iam.cloud.ibm.com/identity/token",
    config=Config(signature_version="oauth"),
    endpoint_url=os.environ.get(
        "COS_ENDPOINT", "https://s3.us-south.cloud-object-storage.appdomain.cloud"
    ),
)
bucket = os.environ.get("COS_BUCKET", "cicd-bucket-test")
object_key = os.environ.get("COS_OBJECT_KEY", "pre.xlsx")

body = cos_client.get_object(Bucket=bucket, Key=object_key)["Body"]
df_0 = pd.read_excel(io.BytesIO(body.read()))
print(df_0.head(10))

X = df_0.drop(columns=["target"])
y = df_0["target"]

# Train a decision tree classifier model
model = DecisionTreeClassifier()
model.fit(X, y)
print(f"Training accuracy: {model.score(X, y):.2f}")

# Configure Watson Machine Learning credentials
credentials = {
    "url": os.environ.get("WML_URL", "https://eu-de.ml.cloud.ibm.com"),
    "apikey": os.environ["WML_API_KEY"],
}

client = APIClient(credentials)

# Associate with the current Watson Studio project
project_id = os.environ["PROJECT_ID"]
client.set.default_project(project_id)

# Select a software specification compatible with your
# Python and Scikit-learn versions
software_spec_uid = client.software_specifications.get_id_by_name(
    "runtime-25.1-py3.12"
)
print("Software specification UID:", software_spec_uid)

metadata = {
    client.repository.ModelMetaNames.NAME: "Decision Tree Classifier Model",
    client.repository.ModelMetaNames.TYPE: "scikit-learn_1.6",
    client.repository.ModelMetaNames.SOFTWARE_SPEC_ID: software_spec_uid,
}

# Register the trained model as a Model asset
model_details = client.repository.store_model(model=model, meta_props=metadata)

# Get the registered model ID
model_id = client.repository.get_model_id(model_details)
print("Model asset created:", model_id)
