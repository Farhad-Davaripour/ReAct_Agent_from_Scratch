# ReAct Agentic Workflow

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://react-agent-from-scratch.streamlit.app/).

<a href="https://colab.research.google.com/github/Farhad-Davaripour/ReAct_Agent_from_Scratch/blob/main/demo.ipynb" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"/>
</a>

This repository provides an introductory implementation of the ReAct (Reasoning and Acting) Agentic workflow. The example has been deployed and could be accessed through this [link](https://react-agent-from-scratch.streamlit.app/). Accordingly, a simple example is designed and implemented which includes the following tasks:

1. Retrieve a list of tasks.
2. Retrieve available resources.
3. Allocate resources to high-priority tasks.
4. Estimate the budget based on allocated hours.

### Components

#### app.py

The main script for the Streamlit application. It sets up the UI, handles user inputs, and interacts with backend functions.

#### tools.py

Contains utility functions and the `Agent` class, which manages the Thought, Action, PAUSE, and Observation loop and executes predefined actions. Key functions include:
- **calculate**: Performs arithmetic calculations.
- **retrieve_tasks**: Retrieves a list of tasks with their priorities and effort estimates.
- **retrieve_resources**: Retrieves a list of resources with their available hours and skills.
- **allocate_resources**: Allocates resources to tasks based on provided input.
- **estimate_budget**: Estimates the budget based on hours and hourly rate.

#### config.py

Defines the system prompt guiding the agent's actions and responses, detailing how the agent should handle the Thought, Action, PAUSE, and Observation loop.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/react-agentic-workflow.git
   cd react-agentic-workflow
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Interact with the application**:
   - Select the model type from the sidebar.
   - Enter your query in the text input.
   - Click the "Run" button to execute the query.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Reference
This project draws inspiration from the short course offered by [deeplearning.ai](https://www.deeplearning.ai/): [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/). The Agent class and query function in `src/tools.py` are largely based on the source code provided in this course.