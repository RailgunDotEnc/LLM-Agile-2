import sys
from setuptools import setup, find_packages
import subprocess
import json

required_packages = [
    'firebase-admin', 'ipython', 'google-generativeai', 'torch', 'anthropic', 'transformers',
    'uvicorn', 'fastapi', 'openai', 'jsons', 'pgpt_python'
]

# automatically installs the required packages
subprocess.call([sys.executable, '-m', 'pip', 'install'] + required_packages)

# sample.json with a template
def create_sample_json():
    config_data = {
        "api_keys": "YOUR_API_KEY_HERE",
        "firebase_url": "YOUR_FIREBASE_URL_HERE",
        "other_config": {}
    }
    with open('sample.json', 'w') as f:
        json.dump(config_data, f, indent=4)
    print("Created sample.json. Please fill it with your specific details and upload it to Firebase.")

create_sample_json()

# prompting user to manually enter sensitive information
print("Please enter your API keys and other sensitive information in the created sample.json file.")

setup(
    name='MultiLLM-Agile-Assistant',
    version='1.0.0',
    packages=find_packages(),
    description='A collaborative tool integrating multiple large language models for agile project management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Asa McDaniel, Daniel Morandi, Faizul Anis, Guaidi Morado, Rishi Meka, and Ubadah Saleh',
    author_email='',
    url='https://github.com/RailgunDotEnc/LLM-Agile-2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=required_packages,
    python_requires='>=3.11',
    
)