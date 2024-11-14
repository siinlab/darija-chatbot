# Contributing to darija-tts

Thank you for your interest in contributing to the **darija-tts** project! This project aims to develop resources and models for synthesizing Moroccan Darija speech. Your contributions, whether it's code, data, documentation, or ideas, are greatly valued.

## How to Contribute

### 1. Reporting Issues
If you encounter bugs, have questions, or want to suggest improvements:
- Check if an issue already exists.
- If not, create a new issue with a clear description, including relevant details like steps to reproduce (if applicable) and suggestions.

### 2. Suggesting New Features
We welcome suggestions for new features and enhancements! Please:
- Open an issue to discuss your proposed feature.
- Provide as much context and detail as possible.

### 3. Contributing Code
We appreciate code contributions, whether they are bug fixes, new features, or optimizations. To contribute code:
1. **Review the getting started section below**.
2. **Fork the repository**.
3. **Create a new branch**:  
   ```bash
   git checkout -b your-branch-name
   ```
   Make sure your branch name is descriptive and relates to the issue you're addressing.
4. **Make your changes**:
   - Ensure code follows project guidelines mentioned below.
   - Add or update tests if applicable.
5. **Commit your changes**:
   - Write clear and descriptive commit messages.
6. **Push your branch** to your fork:
   ```bash
   git push origin your-branch-name
   ```
7. **Create a pull request**:
   - Provide a detailed description of the changes.
   - Mention related issues, if applicable.

### 5. Documentation Contributions
Clear, concise, and thorough documentation is vital to this project's success. You can help by:
- Correcting typos or inaccuracies.
- Adding examples or clarifications.
- Contributing to tutorials or guides.

### 6. Testing and Reviewing
- Help by testing existing code and providing feedback.
- Review pull requests and offer constructive feedback.

## Project Guidelines

1. Ensure that your branch names are descriptive and use lowercase letters with hyphens for separation.
2. Ensure your commit messages are clear and concise.
3. Ensure that your changes pass all tests and do not introduce new issues. In particular, check for linting errors by setting the the pre-commit hooks using the scripts in [.git-hooks](.git-hooks).
4. Ensure that your code is modular and funcional as much as possible. Avoid writing monolithic functions or classes. Avoid hardcoding values that can be parameterized. Avoid using global variables. Avoid writing tests in the same file as the code.
5. Ensure that all modules, classes, and functions are documented according to Google-style docstrings.
6. Ensure that build and runtime files are not included in the repository. Add them to the `.gitignore` file.

## Code of Conduct
All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive environment.

## Getting Started
For instructions on setting up the project locally and other relevant details, please refer to the [README](README.md#setup-environment).

## Contact
If you have questions or need support, you can reach out by opening an issue or contacting the maintainers.

Thank you for contributing to the **darija-tts** project!