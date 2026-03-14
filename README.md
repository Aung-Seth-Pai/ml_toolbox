
# ML Toolbox

A hands-on reference repository for learning and experimenting with machine learning and related tooling. The project is organized by topic so you can quickly find code, notebooks, and demo projects that illustrate key concepts.

---

## What’s Included

### Computer Vision
- **CNN** (Keras): experiments with convolutional neural networks and transfer learning
  - `Computer_Vision/CNN/cnn_keras.ipynb`
  - `Computer_Vision/CNN/vgg16.ipynb`
- **Image Processing**: basic image manipulation pipelines and creative effects
  - `Computer_Vision/img_processing/Image Processing Test.ipynb`
  - `Computer_Vision/img_processing/Photo to Sketch.ipynb`

### General
- **Chatbot**: a simple chatbot server and client demo
  - `General/chatbot_test/botwork.py`
  - `General/chatbot_test/server.py`
  - `General/chatbot_test/test_server.py`
  - `General/chatbot_test/requirements.txt`
- **Prompt Engineering**: LangChain-based prompt workflows and utilities
  - `General/prompt_engineering/main.py`
  - `General/prompt_engineering/LangChain_utils.ipynb`
  - `General/prompt_engineering/chains/` (LLM chain implementations)
  - `General/prompt_engineering/config/settings.py` (config patterns)
  - `General/prompt_engineering/llm_providers/` (Groq + Ollama client examples)
  - `General/prompt_engineering/output_parsers/` (custom output parsing logic)
  - `General/prompt_engineering/tests/` (unit tests for chain logic)
- **TFRecord**: TensorFlow record creation and consumption for tabular datasets
  - `General/TFrecord/tabular_tfrecord.ipynb`

### MLOps & Infrastructure
- **Airflow**: DAG examples, local config, and airflow environment setup
  - `MLOps/Airflow/dags/` (example DAGs)
  - `MLOps/Airflow/airflow.cfg`, `webserver_config.py`
  - `MLOps/Airflow/.venv_airflow/` (self-contained dev environment)
- **NGINX Primer**: simple NGINX + Node.js demo for reverse proxy & static hosting
  - `MLOps/NGINX_primer/docker-compose.yaml`
  - `MLOps/NGINX_primer/Dockerfile`
  - `MLOps/NGINX_primer/nginx.conf`
  - `MLOps/NGINX_primer/src/server.js`

### TensorFlow
- **Basics**: TensorFlow fundamentals and examples
  - `Tensorflow/tf_basics.ipynb`

---

## Getting Started

1. **Pick a topic** (Computer Vision, Prompt Engineering, MLOps, etc.)
2. **Open the relevant notebook or script** and run it in a Python environment with the required dependencies.
3. **Refer to in-folder README files** for project-specific setup and requirements.

> If you want to run something end-to-end, start with the `General/prompt_engineering` or `General/chatbot_test` folders and follow their `requirements.txt` and code comments.

---

## Notes

- This repo is intended as a learning playground — expect experiments, prototypes, and “notes-to-self” style code.
- Feel free to add your own demos and link them here as you build out more learning paths.
