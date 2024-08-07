# Lens Label 🍏🔎

Welcome to **Lens Label**, a Streamlit app designed to help you make healthier food choices by providing detailed health scores for scanned food labels. Powered by the Gemini-PRO LLM API from Google, Lens Label is your personal health assistant in the grocery aisle!

## Introduction

Lens Label is your go-to tool for analyzing nutritional information on food labels. With its advanced Gen AI features using Gemini and intuitive interface, it helps you understand the health value of the products you choose, ensuring you pick the best options for a healthier lifestyle.

## Features

- **📲 Scan Food Labels**: Simply scan the food labels of products to get instant analysis.
- **🏷️ Health Scores**: Receive a health score that summarizes the nutritional value of the product.
- **🚀 Detailed Analysis**: Get a thorough breakdown of ingredients and nutritional information.
- **💼 Track Scanned Items**: Keep a record of your scanned items to monitor your dietary choices over time.
- **🌟 Compare Products**: Compare different products to make the healthiest choices.

## Installation

To run Lens Label locally, follow these steps:

1. **Clone the Repository**

   ```bash
   
   git clone https://github.com/AmarnathSiliveri/gencam-health.git
   ```


2. **Navigate to the Project Directory**

   ```bash
   
   cd lens-label
   ```

3. **Create a Virtual Environment (optional but recommended)**

   ```bash
   
   python -m venv venv
   ```
4. **Activate the Virtual Environment**

   ```bash
   
   #on windows
   
   venv\Scripts\activate

   #on Macos
   source venv/bin/activate
   ```
5. **Install the Required Packages**

   ```bash
   
   pip install -r requirements.txt
   ```
6. **Run the Streamlit App**

   ```bash
   
   streamlit run app.py
   ```

## Configuration

To use the Gemini-PRO LLM API, you'll need to set up your API key. Create a `.env` file in the project root and add your API key like this:

```text
GEMINI_API_KEY=your_api_key_here
```
## Usage

1. Open the app in your browser (usually at `http://localhost:8501`).
2. Navigate to the LensLabel tab.
3. Use the scanning feature to analyze food labels.
4. Review the health scores and detailed ingredient analysis to make informed decisions.

## Contributing

We welcome contributions to Lens Label! If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes with descriptive messages.
4. Push the branch to your forked repository.
5. Open a pull request with a clear explanation of your changes.


## Contact

For any questions or support, please contact us at amarnathsiliveri@gmail.com.
