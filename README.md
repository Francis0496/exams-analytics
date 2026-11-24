# Exams Analytics

Class exam results for one cohort: a Jupyter analysis and a browser dashboard you can put on a projector.

The dashboard is `class_dashboard.html`. Double-click it, or open it in a browser, then press F11 for full screen. The same page is published with GitHub Pages. Search by name or ID, filter by grade or exam status, and click a student to open their marks. Opening the file on your computer needs no server and no internet connection.

## What is in this folder

| File | Purpose |
| --- | --- |
| `class_dashboard.html` | Interactive class board. Student records are embedded in the page. |
| `Exams_Analytics_Notebook.ipynb` | The full analysis: grades, score spreads, outliers, correlations, and the summary charts. |
| `create_notebook.py` | Rebuilds `Exams_Analytics_Notebook.ipynb` from the same analysis. |
| `Student_Data_Analytics_Analysis.xlsx` | Source spreadsheet. |
| `*.png` | Charts saved from the notebook. |
| `test.ipynb` | Scratch notebook. |

The notebook expects Python with pandas, openpyxl, matplotlib, and seaborn. Run `create_notebook.py` with that environment if you want to regenerate the notebook after editing the analysis script.

If the spreadsheet changes, the HTML dashboard does not update by itself. Rebuild `class_dashboard.html` from the new workbook before presenting again.

## Author

Francis Sesay  
GitHub: [Francis0496](https://github.com/Francis0496)  
Email: ffsesay04@gmail.com

## Licence

The code in this repository is released under the MIT Licence. See [LICENSE](LICENSE).

Copyright (c) 2026 Francis Sesay.

`Student_Data_Analytics_Analysis.xlsx` and the student names, ID numbers, and marks embedded in `class_dashboard.html` are not covered by that licence. Do not publish or share those records outside the class.
