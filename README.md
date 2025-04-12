<div align="center">

# ICHIBOSS-

*Empower your trading strategies with data-driven insights.*

![last-commit](https://img.shields.io/github/last-commit/adamarbain/ichiboss-?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/adamarbain/ichiboss-?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/adamarbain/ichiboss-?style=flat&color=0080ff)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=Jupyter&style=flat)

*Built with the tools and technologies:*

![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environtment Variables](#environtment-variables)
  - [Usage](#usage)
    - [Data Fetching](#data-fetching)
    - [Backtesting](#backtesting)
    - [Model - (Developing)](#model---developing)
- [License](#license)

---

## Overview

**ichiboss** is a powerful developer tool designed for cryptocurrency trading strategy evaluation and backtesting. It empowers developers to analyze and refine their trading algorithms using historical market data.

**Why ichiboss?**

This project aims to streamline the process of testing and optimizing trading strategies. The core features include:

- 📊 **Backtesting Framework:** Evaluate trading strategies against historical data for informed decision-making.
- 🧪 **Interactive Notebooks:** Experiment with data analysis and model training in a user-friendly environment.
- 📈 **Performance Metrics Evaluation:** Assess the effectiveness of strategies with comprehensive performance reports.
- 🔗 **Integration with Data Processing Libraries:** Leverage Pandas and NumPy for efficient data manipulation and analysis.
- 📉 **Specialized Strategies:** Utilize network metrics to identify optimal trading signals tailored for cryptocurrency markets.

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip

### Installation

Build **ichiboss-** from the source and install dependencies:

```bash
# Clone the repository
git clone https://github.com/adamarbain/ichiboss-

# Navigate to the project directory
cd ichiboss-

# Install dependencies
pip install -r requirements.txt model/requirements.txt backtesting_framework/requirements.txt

```

---

## Environtment Variables

To use the Cybotrade APIs, you need to set up environment variables for your API keys. Create a `.env` file in the root directory of the project and add the following lines:

```bash
# Cybotrade API Key
X-API-KEY=your_cybotrade_api_key
```

---

## Usage

### Data Fetching

The data fetching module is designed to retrieve historical cryptocurrency data from various sources. It supports multiple exchanges and allows users to specify the desired time frame and granularity of the data.

Run the notebook to fetch and preprocess data using CryptoQuant and Glassnode APIs:

```bash
jupyter notebook data/fetch/main.ipynb 
```
File path to `data/fetch/main.ipynb` : [Open Data Fetch Notebook](data/fetch/main.ipynb)


#### API Sources :
- "data/fetch/api/cryptoquant" 
- "data/fetch/api/glassnode"


### Backtesting
Backtesting is a crucial step in evaluating the performance of trading strategies. The backtesting framework allows users to simulate trades based on historical data and assess the effectiveness of their strategies.

To run the backtesting framework, execute the following command:

```bash
jupyter notebook backtesting_framework/main.ipynb 
```
File path to `backtesting_framework/main.ipynb` : [Open Backtesting Notebook](backtesting_framework/main.ipynb)

This will evaluate strategies using historical data inside the backtesting_framework/ module.

### Model - (Developing)
**The model module is currently under development.** It will provide advanced machine learning and deep learning capabilities for predicting cryptocurrency price movements and optimizing trading strategies.
To run the model module, execute the following command:

```bash
jupyter notebook model/first_model.ipynb 
```
File path to `model/first_model.ipynb` : [Open Model Notebook](model/first_model.ipynb)

---

## License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this software.  
See the [LICENSE](LICENSE) file for full license text.

---

[⬆ Return to top](#ICHIBOSS-)
