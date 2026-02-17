# AI Agents for Fraud Investigation Demo

## Overview

The landscape of financial fraud has been changing rapid in recent years. AI tools have given criminals access to sophisticated tools. They can spin up websites, generate videos or fake documents leaving customers vunerable to new forms of abuse. Banks already operate strong fraud detection systems using classical ML techniques (gradient-boosted trees, network analysis etc) to flag risky transactions. 

However, decection is only part of the story. Investigation, explanation, escalation and documentation remain heavily human-driven processes. For customers, experiencing fraud can be a terrifying experience. Every year, 300 UK residents are at risk of suicide from the stress and fear induced by fraud. Therefore, every moment saved in resolving a fraud case is precious, translating directly into an improved customer experience, strengthing the reputation of financiual institurions in these moments of great personal distress. 

This repo simulates how AI agents could assist fraud investigators by:
1. Sythesising all relevant data for a flagged financial transaction
2. Generating regulatory and legal documentaiton to be passed to a human for review
3. Suipporting human decion-making with recomendations grounded in relevant context, linked to direct citattions to the source data
4. Streamlines investigfations to improve response times and customer outcomes

The AI agent effectively acts as a fraud analyst support-worker, augmenting humans to achieve faster and more accurate resolutions whilst remaining fully grounded in real transactional and regulatory data. 

## Install instructions

Clone the repository:

```sh
git clone <git@github.com:oliverkiranbrown/fraud-investigation-agent-demo.git>
cd fraud-investigation-agent-demo
```

Create a Python virtual environment (Python 3.10+ required):

```sh
python3.11 -m venv .venv
source .venv/bin/activate
```

Upgrade pip:

```sh
pip install --upgrade pip
```

Install dependencies:

```sh
pip install -r requirements.txt
```

### Configuration

Then, create an `.env` file in the project root

```sh
OPENAI_API_KEY=your_api_key_here
```

### Usage

Run `python main.py` in the terminal from the project root. 