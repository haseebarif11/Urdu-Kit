# Contributing to UrduKit

Thank you for your interest in improving UrduKit! We welcome contributions of all kinds — bug fixes, new features, documentation improvements, and tests.

## Getting Started

1. **Fork the repository** and clone your fork locally.
   ```bash
   git clone https://github.com/<your-username>/Urdu-Kit.git
   cd Urdu-Kit
   ```
2. **Create a virtual environment** and install development dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   pip install -e ".[dev]"
   ```
3. **Run the test suite** to ensure everything works:
   ```bash
   pytest
   ```
4. **Make your changes**. Please keep the code style consistent with PEP 8 and run the formatter (`black .`) before committing.
5. **Write tests** for any new functionality or bugfixes.
6. **Submit a Pull Request** with a clear description of what you changed and why.

## Code Style & Quality

- Use **black** for formatting and **ruff** for linting. The CI workflow will check these automatically.
- Include docstrings for public functions and classes.
- Update the documentation (README, docstrings, examples) when you add new features.

## Issues

If you encounter a bug or have a feature request, please open an issue first. Provide a minimal reproducible example and, if possible, add a test that demonstrates the problem.

---

Happy coding! 🎉
