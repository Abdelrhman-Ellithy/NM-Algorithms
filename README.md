# Four New Hybrid Root Bracketing Algorithms: Optimization-Based Approaches for Numerical Root Finding

## Project Overview
This project presents four novel hybrid root bracketing algorithms that combine the reliability of traditional bracketing methods with the speed of optimization-based techniques. The algorithms are implemented in Python, evaluated on a diverse set of test functions, and analyzed for convergence and computational efficiency. The results are compiled and discussed in an academic LaTeX paper.

**Authors:** Abdelrahman Ellithy, Dr. Ahmed Shalaby, Elsayed Badr

## Repository Structure
- **Python Scripts**: Each algorithm is implemented in its own script (e.g., `06-Optimized-Bisection-FalsePosition.py`, `07-Optimized-Bisection-FalsePosition-Modified-Secant.py`, etc.).
- **Results Files**: 
  - `Results.db`: SQLite database containing raw results from algorithm runs.
  - `Results.xlsx`, `CPU_Times_Per_Algorithm.xlsx`, `Results_tableII.csv`: Processed results and summary tables.
  - Plots: PNG files visualizing CPU time and performance (e.g., `avg_cpu_time_per_algorithm.png`, `cpu_time_lineplot_per_problem.png`, etc.).
- **Paper**: 
  - `hybrid_root_bracketing_paper.tex`: Main LaTeX source for the research paper.
  - `Sample Latex Paper Format file.tex`: Example format for reference.
- **Reference Papers**: PDF files in the `Refrence Papers/` directory.
- **Analysis Script**: `analyze_results.py` for processing results and generating plots.
- **References**: `refrences.txt` contains a comprehensive list of related works.
- **CI/CD**: `.github/workflows/benchmark.yml` automates benchmarking on push to `main`.

## How to Run the Algorithms
1. Ensure you have Python 3.11+ and the required packages:
   ```bash
   pip install sympy numpy pandas matplotlib seaborn
   ```
2. Run each algorithm script (e.g., `python 06-Optimized-Bisection-FalsePosition.py`). Results will be stored in `Results.db`.
3. To run all algorithms and regenerate results, you can use the provided scripts in sequence or adapt the CI workflow steps.

## Analyzing Results and Generating Plots
- Run `python analyze_results.py` to:
  - Summarize CPU time and iteration statistics
  - Generate plots (saved as PNG files)
  - Output summary tables for inclusion in the paper

## Compiling the LaTeX Paper
1. Make sure you have a LaTeX distribution (e.g., TeX Live, MiKTeX).
2. Compile `hybrid_root_bracketing_paper.tex` using your preferred LaTeX editor or:
   ```bash
   pdflatex hybrid_root_bracketing_paper.tex
   bibtex hybrid_root_bracketing_paper
   pdflatex hybrid_root_bracketing_paper.tex
   pdflatex hybrid_root_bracketing_paper.tex
   ```
3. The resulting PDF will include all tables, plots, and references.

## Continuous Integration (CI)
- The `.github/workflows/benchmark.yml` workflow automatically runs all algorithm scripts and verifies the results database on every push to `main`. It uploads the results as an artifact for reproducibility.

## Reference Materials
- See the `Refrence Papers/` directory for foundational and recent papers on hybrid and bracketing algorithms.
- `refrences.txt` contains a comprehensive bibliography, and the LaTeX paper's references are kept in sync with this file.

## Contributing
- Contributions are welcome! Please ensure any new algorithms or results are well-documented and integrated into the analysis and paper.

## License
- See `LICENSE` for details.