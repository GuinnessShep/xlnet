from flask import Flask, request, jsonify
from sagemaker.huggingface import HuggingFaceModel
import boto3

app = Flask(name)

iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='{IAM_ROLE_WITH_SAGEMAKER_PERMISSIONS}')['Role']['Arn']

hub = {
'HF_MODEL_ID':'xlnet-base-cased',
'HF_TASK':'conversational'
}

huggingface_model = HuggingFaceModel(
transformers_version='4.17.0',
pytorch_version='1.10.2',
py_version='py38',
env=hub,
role=role,
)

predictor = huggingface_model.deploy(
initial_instance_count=1,
instance_type='ml.m5.xlarge'
)

@app.route('/')
def home():
return "Welcome to the XLNet Chatbot!"

@app.route('/predict', methods=['POST'])
def predict():
data = request.get_json()
inputs = data['inputs']
response = predictor.predict({'inputs': inputs})
return jsonify(response)

if name == 'main':
app.run(debug=True)
