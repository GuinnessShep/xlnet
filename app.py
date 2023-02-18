from flask import Flask, render_template, request
from sagemaker.huggingface import HuggingFaceModel
import boto3

app = Flask(__name__)

iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='{IAM_ROLE_WITH_SAGEMAKER_PERMISSIONS}')['Role']['Arn']

hub = {
	'HF_MODEL_ID': 'xlnet-base-cased',
	'HF_TASK': 'conversational'
}

huggingface_model = HuggingFaceModel(
	transformers_version='4.17.0',
	pytorch_version='1.10.2',
	py_version='py38',
	env=hub,
	role=role
)

predictor = huggingface_model.deploy(
	initial_instance_count=1,
	instance_type='ml.m5.xlarge'
)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	message = request.form['message']
	response = predictor.predict({'inputs': message})
	return render_template('index.html', response=response)

if __name__ == '__main__':
	app.run(debug=True)
