import json

nb = {
 'nbformat': 4,
 'nbformat_minor': 5,
 'metadata': {
  'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
  'language_info': {'name': 'python', 'version': '3.11.0'}
 },
 'cells': []
}

def md(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': src, 'id': 'md' + str(abs(hash(src)))[:6]}

def code(src):
    return {'cell_type': 'code', 'metadata': {}, 'source': src, 'outputs': [], 'execution_count': None, 'id': 'c' + str(abs(hash(src)))[:6]}

grade_order_str = '["A", "B+", "B", "B-", "C+", "C", "C-", "F"]'

cells = [

md("""# 📊 Student Exams Analytics
**Comprehensive Data Analysis Report**  
Dataset: `Student_Data_Analytics_Analysis.xlsx`  
Objective: Extract actionable insights about student academic performance.

---"""),

md("## 📦 Phase 1 — Setup & Data Loading"),

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Plot style
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.family"] = "sans-serif"
sns.set_theme(style="whitegrid", palette="Set2")

print("Libraries loaded ✅")"""),

code("""# Load dataset
df = pd.read_excel("Student_Data_Analytics_Analysis.xlsx")

print(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
df.head()"""),

md("## 🔍 Phase 2 — Data Understanding & Quality Check"),

code("""# Data types & structure
df.info()"""),

code("""# Descriptive statistics
df.describe(include="all").T"""),

code("""# Missing values analysis
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
missing_df[missing_df["Missing Count"] > 0]"""),

code("""# Investigate absent students (cause of NaN)
print("Students marked Absent:")
df[df["Exam status"] == "Absent"][["No", "Name", "ID Number", "Exam status", "EXAMS", "FINAL_SCORE", "GRADE"]]"""),

code("""# Grade & Exam status distribution
print("Grade Distribution:")
print(df["GRADE"].value_counts())
print("\\nExam Status:")
print(df["Exam status"].value_counts())"""),

md("## 📈 Phase 3 — Exploratory Data Analysis (EDA)"),

md("### 3.1 — Grade Distribution"),

code("""grade_order = ["A", "B+", "B", "B-", "C+", "C", "C-", "F"]
grade_counts = df["GRADE"].value_counts().reindex(grade_order, fill_value=0)
colors = ["#2ecc71" if g in ["A","B+","B","B-"] else "#f39c12" if g in ["C+","C","C-"] else "#e74c3c" for g in grade_order]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Grade bar chart
axes[0].bar(grade_order, grade_counts.values, color=colors, edgecolor="black", linewidth=0.7)
axes[0].set_title("Grade Distribution", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Grade")
axes[0].set_ylabel("Number of Students")
for i, v in enumerate(grade_counts.values):
    axes[0].text(i, v + 0.2, str(v), ha="center", va="bottom", fontsize=10)

# Pie chart: Pass vs Fail
pass_fail = df["GRADE"].apply(
    lambda x: "Fail" if x == "F" else ("Pass" if pd.notna(x) else "Absent")
).value_counts()
axes[1].pie(pass_fail, labels=pass_fail.index, autopct="%1.1f%%",
            colors=["#2ecc71", "#e74c3c", "#95a5a6"], startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":1.5})
axes[1].set_title("Pass / Fail / Absent Rate", fontsize=13, fontweight="bold")

plt.suptitle("Student Grade Overview", fontsize=15, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("grade_distribution.png", bbox_inches="tight")
plt.show()

total_graded = grade_counts.sum()
fail_rate = grade_counts.get("F", 0) / total_graded * 100
a_rate = grade_counts.get("A", 0) / total_graded * 100
print(f"Fail rate: {fail_rate:.1f}%  |  A grade: {a_rate:.1f}%")"""),

md("### 3.2 — Score Distributions"),

code("""score_cols = ["Test 1 (100)", "Test 2 (100)", "AVERAGE", "EXAMS", "Final CA (30%)", "FINAL_SCORE"]
titles = ["Test 1 Score", "Test 2 Score", "CA Average (Tests)", "Exam Score", "Final CA (30%)", "Final Score"]

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()
palette = sns.color_palette("Set2")

for i, (col, title) in enumerate(zip(score_cols, titles)):
    data = df[col].dropna()
    axes[i].hist(data, bins=15, edgecolor="black", color=palette[i % 6], linewidth=0.6)
    axes[i].axvline(data.mean(), color="red", linestyle="--", linewidth=1.5,
                    label=f"Mean: {data.mean():.1f}")
    axes[i].axvline(data.median(), color="blue", linestyle="--", linewidth=1.5,
                    label=f"Median: {data.median():.1f}")
    axes[i].set_title(title, fontsize=11, fontweight="bold")
    axes[i].set_xlabel("Score")
    axes[i].set_ylabel("Frequency")
    axes[i].legend(fontsize=8)

plt.suptitle("Score Distributions Across All Assessment Components", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("score_distributions.png", bbox_inches="tight")
plt.show()"""),

md("### 3.3 — Box Plots (Outlier Detection)"),

code("""fig, ax = plt.subplots(figsize=(14, 6))

cols_bp = ["Test 1 (100)", "Test 2 (100)", "EXAMS", "FINAL_SCORE"]
labels_bp = ["Test 1", "Test 2", "Exam", "Final Score"]
data_bp = [df[c].dropna().values for c in cols_bp]

bp = ax.boxplot(data_bp, patch_artist=True, notch=False)
ax.set_xticks(range(1, len(labels_bp) + 1))
ax.set_xticklabels(labels_bp)
colors_bp = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
for patch, color in zip(bp["boxes"], colors_bp):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_title("Score Distributions — Box Plot (Outlier View)", fontsize=13, fontweight="bold")
ax.set_ylabel("Score")
ax.set_xlabel("Assessment Component")
plt.tight_layout()
plt.savefig("boxplots.png", bbox_inches="tight")
plt.show()"""),

md("### 3.4 — Correlation Analysis"),

code("""num_cols = ["Test 1 (100)", "Test 2 (100)", "AVERAGE", "EXAMS", "Final CA (30%)", "FINAL_SCORE"]
corr_matrix = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="RdYlGn",
            mask=mask, square=True, ax=ax, linewidths=0.5,
            cbar_kws={"shrink": 0.8}, vmin=-1, vmax=1)
ax.set_title("Correlation Matrix — Score Components", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("correlation_heatmap.png", bbox_inches="tight")
plt.show()

print("Key Correlations with FINAL_SCORE:")
print(corr_matrix["FINAL_SCORE"].sort_values(ascending=False).to_string())"""),

md("### 3.5 — Test 1 vs Test 2 Comparison"),

code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Scatter plot
axes[0].scatter(df["Test 1 (100)"], df["Test 2 (100)"],
                alpha=0.7, color="#3498db", edgecolor="black", linewidth=0.5, s=60)
axes[0].plot([0, 100], [0, 100], "r--", linewidth=1.5, label="Equal performance line")
axes[0].set_xlabel("Test 1 Score")
axes[0].set_ylabel("Test 2 Score")
axes[0].set_title("Test 1 vs Test 2 Scores", fontsize=12, fontweight="bold")
axes[0].legend()

# Improvement distribution
improvement = df["Test 2 minus Test 1"]
axes[1].hist(improvement, bins=20, edgecolor="black", color="#9b59b6", alpha=0.8)
axes[1].axvline(0, color="red", linestyle="--", linewidth=1.5, label="No change")
axes[1].axvline(improvement.mean(), color="blue", linestyle="--", linewidth=1.5,
                label=f"Mean change: +{improvement.mean():.1f}")
axes[1].set_xlabel("Test 2 - Test 1 Score")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Improvement from Test 1 to Test 2", fontsize=12, fontweight="bold")
axes[1].legend()

improved = (improvement > 0).sum()
declined = (improvement < 0).sum()
no_change = (improvement == 0).sum()
print(f"Improved: {improved} ({improved/len(df)*100:.1f}%)  |  "
      f"Declined: {declined} ({declined/len(df)*100:.1f}%)  |  No change: {no_change}")

plt.tight_layout()
plt.savefig("test_comparison.png", bbox_inches="tight")
plt.show()"""),

md("## 👤 Phase 4 — Student-Level Insights"),

md("### 4.1 — Top 10 Performers"),

code("""top10 = df[df["GRADE"].notna()].nlargest(10, "FINAL_SCORE")[
    ["No", "Name", "Test 1 (100)", "Test 2 (100)", "EXAMS", "FINAL_SCORE", "GRADE"]
].reset_index(drop=True)
top10.index += 1

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(top10["Name"][::-1], top10["FINAL_SCORE"][::-1],
               color="#2ecc71", edgecolor="black", linewidth=0.7)
ax.set_xlabel("Final Score")
ax.set_title("Top 10 Students by Final Score", fontsize=13, fontweight="bold")
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.1f}", va="center", fontsize=9)
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig("top10_performers.png", bbox_inches="tight")
plt.show()

print(top10.to_string())"""),

md("### 4.2 — Bottom 10 Performers (At-Risk Students)"),

code("""bottom10 = df[df["GRADE"].notna()].nsmallest(10, "FINAL_SCORE")[
    ["No", "Name", "Test 1 (100)", "Test 2 (100)", "EXAMS", "FINAL_SCORE", "GRADE"]
].reset_index(drop=True)
bottom10.index += 1

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.barh(bottom10["Name"][::-1], bottom10["FINAL_SCORE"][::-1],
               color="#e74c3c", edgecolor="black", linewidth=0.7)
ax.set_xlabel("Final Score")
ax.set_title("Bottom 10 Students (At-Risk)", fontsize=13, fontweight="bold")
ax.axvline(50, color="orange", linestyle="--", linewidth=1.5, label="Pass threshold (~50)")
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():.1f}", va="center", fontsize=9)
ax.set_xlim(0, 80)
ax.legend()
plt.tight_layout()
plt.savefig("bottom10_atrisk.png", bbox_inches="tight")
plt.show()

print(bottom10.to_string())"""),

md("### 4.3 — CA Average vs Exam Score (by Grade)"),

code("""grade_order = ["A", "B+", "B", "B-", "C+", "C", "C-", "F"]
grade_colors = {
    "A": "#1abc9c", "B+": "#2ecc71", "B": "#3498db", "B-": "#9b59b6",
    "C+": "#f39c12", "C": "#e67e22", "C-": "#d35400", "F": "#e74c3c"
}

fig, ax = plt.subplots(figsize=(10, 7))
for grade in grade_order:
    subset = df[df["GRADE"] == grade]
    ax.scatter(subset["AVERAGE"], subset["EXAMS"],
               label=grade, color=grade_colors.get(grade, "grey"),
               s=80, alpha=0.85, edgecolor="black", linewidth=0.5)

ax.set_xlabel("CA Average (Tests 1 & 2)", fontsize=11)
ax.set_ylabel("Exam Score", fontsize=11)
ax.set_title("CA Average vs Exam Score (coloured by Grade)", fontsize=13, fontweight="bold")
ax.legend(title="Grade", loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig("ca_vs_exam.png", bbox_inches="tight")
plt.show()"""),

md("### 4.4 — Performance Consistency: CA vs Exam Gap"),

code("""gap = df["Test average minus exam"].dropna()
colors_gap = ["#e74c3c" if v < 0 else "#2ecc71" if v > 10 else "#f39c12" for v in gap]

fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(range(len(gap)), gap.values, color=colors_gap, edgecolor="black", linewidth=0.5)
ax.axhline(0, color="black", linewidth=1)
ax.set_title("CA Average vs Exam Score Gap (per student)", fontsize=13, fontweight="bold")
ax.set_xlabel("Student Index")
ax.set_ylabel("CA Average - Exam Score")
ax.text(0.02, 0.95, "Green = Performed much better in CA",
        transform=ax.transAxes, color="#2ecc71", fontsize=9)
ax.text(0.02, 0.90, "Orange = Small gap",
        transform=ax.transAxes, color="#f39c12", fontsize=9)
ax.text(0.02, 0.85, "Red = Performed better in Exam",
        transform=ax.transAxes, color="#e74c3c", fontsize=9)
plt.tight_layout()
plt.savefig("ca_exam_gap.png", bbox_inches="tight")
plt.show()

print(f"Students who scored higher in exam than CA : {(gap < 0).sum()}")
print(f"Students who scored higher in CA than exam : {(gap > 0).sum()}")
print(f"Mean CA-Exam gap                           : {gap.mean():.1f} points")"""),

md("## 📊 Phase 5 — Summary Dashboard"),

code("""grade_order = ["A", "B+", "B", "B-", "C+", "C", "C-", "F"]
grade_counts = df["GRADE"].value_counts().reindex(grade_order, fill_value=0)

fig = plt.figure(figsize=(18, 12))
fig.suptitle("Student Performance Analytics — Summary Dashboard",
             fontsize=16, fontweight="bold", y=1.01)

# 1. Grade distribution
ax1 = fig.add_subplot(2, 3, 1)
colors_g = ["#2ecc71","#27ae60","#3498db","#9b59b6","#f39c12","#e67e22","#d35400","#e74c3c"]
ax1.bar(grade_order, grade_counts, color=colors_g, edgecolor="black", linewidth=0.6)
ax1.set_title("Grade Distribution", fontsize=11, fontweight="bold")
ax1.set_xlabel("Grade"); ax1.set_ylabel("Count")

# 2. Final score histogram
ax2 = fig.add_subplot(2, 3, 2)
final_data = df["FINAL_SCORE"].dropna()
ax2.hist(final_data, bins=15, color="#3498db", edgecolor="black", linewidth=0.6)
ax2.axvline(final_data.mean(), color="red", linestyle="--", linewidth=2,
            label=f"Mean: {final_data.mean():.1f}")
ax2.set_title("Final Score Distribution", fontsize=11, fontweight="bold")
ax2.set_xlabel("Final Score"); ax2.set_ylabel("Students"); ax2.legend(fontsize=8)

# 3. Mean scores comparison
ax3 = fig.add_subplot(2, 3, 3)
means = [df["Test 1 (100)"].mean(), df["Test 2 (100)"].mean(), df["EXAMS"].mean()]
bars3 = ax3.bar(["Test 1", "Test 2", "Exam"], means,
                color=["#e74c3c","#2ecc71","#3498db"], edgecolor="black", linewidth=0.6)
for bar in bars3:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}", ha="center", fontsize=10, fontweight="bold")
ax3.set_title("Mean Scores: T1 vs T2 vs Exam", fontsize=11, fontweight="bold")
ax3.set_ylabel("Mean Score"); ax3.set_ylim(0, 100)

# 4. Scatter: CA Average vs Final Score
ax4 = fig.add_subplot(2, 3, 4)
valid = df[["AVERAGE","FINAL_SCORE"]].dropna()
ax4.scatter(valid["AVERAGE"], valid["FINAL_SCORE"],
            alpha=0.7, color="#9b59b6", edgecolor="black", linewidth=0.5, s=50)
z = np.polyfit(valid["AVERAGE"], valid["FINAL_SCORE"], 1)
p = np.poly1d(z)
x_line = np.linspace(valid["AVERAGE"].min(), valid["AVERAGE"].max(), 100)
ax4.plot(x_line, p(x_line), "r--", linewidth=1.5, label="Trend")
ax4.set_title("CA Average vs Final Score", fontsize=11, fontweight="bold")
ax4.set_xlabel("CA Average"); ax4.set_ylabel("Final Score"); ax4.legend(fontsize=8)

# 5. Exam attendance pie
ax5 = fig.add_subplot(2, 3, 5)
attendance = df["Exam status"].value_counts()
ax5.pie(attendance, labels=attendance.index, autopct="%1.1f%%",
        colors=["#2ecc71","#e74c3c"], startangle=90,
        wedgeprops={"edgecolor":"white","linewidth":2})
ax5.set_title("Exam Attendance", fontsize=11, fontweight="bold")

# 6. Test 1 -> Test 2 improvement
ax6 = fig.add_subplot(2, 3, 6)
improved = (df["Test 2 minus Test 1"] > 0).sum()
declined = (df["Test 2 minus Test 1"] < 0).sum()
no_change = (df["Test 2 minus Test 1"] == 0).sum()
bars6 = ax6.bar(["Improved", "Declined", "No Change"],
                [improved, declined, no_change],
                color=["#2ecc71","#e74c3c","#95a5a6"],
                edgecolor="black", linewidth=0.6)
for bar in bars6:
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             str(int(bar.get_height())), ha="center", fontsize=11, fontweight="bold")
ax6.set_title("Test 1 to Test 2 Improvement", fontsize=11, fontweight="bold")
ax6.set_ylabel("Number of Students")

plt.tight_layout()
plt.savefig("summary_dashboard.png", bbox_inches="tight", dpi=150)
plt.show()"""),

md("## 📝 Phase 6 — Key Findings & Recommendations"),

code("""grade_order = ["A", "B+", "B", "B-", "C+", "C", "C-", "F"]
grade_counts = df["GRADE"].value_counts().reindex(grade_order, fill_value=0)

total = len(df)
taken = (df["Exam status"] == "Taken").sum()
absent = (df["Exam status"] == "Absent").sum()
passed = df["GRADE"].isin(["A","B+","B","B-","C+","C","C-"]).sum()
failed = (df["GRADE"] == "F").sum()
mean_t1 = df["Test 1 (100)"].mean()
mean_t2 = df["Test 2 (100)"].mean()
mean_exam = df["EXAMS"].mean()
mean_final = df["FINAL_SCORE"].mean()
improved = (df["Test 2 minus Test 1"] > 0).sum()

SEP = "=" * 60

print(SEP)
print("       STUDENT ANALYTICS — KEY FINDINGS SUMMARY")
print(SEP)
print(f"  Total Students           : {total}")
print(f"  Exam Takers              : {taken} ({taken/total*100:.1f}%)")
print(f"  Exam Absentees           : {absent}")
print(f"  Students Passed          : {passed} ({passed/total*100:.1f}%)")
print(f"  Students Failed (Grade F): {failed} ({failed/total*100:.1f}%)")
print()
print(f"  Mean Test 1 Score        : {mean_t1:.1f} / 100")
print(f"  Mean Test 2 Score        : {mean_t2:.1f} / 100  (+{mean_t2-mean_t1:.1f} from Test 1)")
print(f"  Mean Exam Score          : {mean_exam:.1f} / 100")
print(f"  Mean Final Score         : {mean_final:.1f} / 100")
print()
print(f"  Students Improved T1->T2 : {improved} ({improved/total*100:.1f}%)")
print()
print("  Grade Distribution:")
for g in grade_order:
    count = grade_counts.get(g, 0)
    bar = chr(9608) * count
    print(f"    {g:3s}: {bar} ({count})")
print()
print("RECOMMENDATIONS:")
print("-" * 60)
print(f"1. EXAM PERFORMANCE GAP: Mean exam ({mean_exam:.1f}) vs Test 2 ({mean_t2:.1f})")
print(f"   — a {mean_t2-mean_exam:.1f}-pt drop. Students need better exam preparation.")
print(f"2. HIGH FAIL RATE: {failed/total*100:.1f}% of students scored grade F.")
print("   Targeted remediation & early intervention is needed.")
print(f"3. IMPROVEMENT TREND: {improved/total*100:.1f}% improved Test1->Test2.")
print("   Continue the teaching approach used between tests.")
print(f"4. TEST 1 WEAKNESS: Mean only {mean_t1:.1f}/100 vs Test 2 mean {mean_t2:.1f}.")
print("   Initial teaching delivery/pace should be reviewed.")
print("5. CA vs EXAM GAP: Most students perform significantly better")
print("   in CA than in the final exam — exam anxiety or poor")
print("   revision strategy may be contributing factors.")
print("6. AT-RISK STUDENTS: Bottom 10 students (see chart) need")
print("   individual mentoring and academic support plans.")
print(SEP)"""),

md("""---
**Analysis complete!** 🎉  
All charts saved as PNG files in the working directory.  

### Charts Generated:
- `grade_distribution.png` — Grade bar chart + Pass/Fail pie
- `score_distributions.png` — Histograms for all 6 score columns
- `boxplots.png` — Box plots for outlier detection
- `correlation_heatmap.png` — Pearson correlation matrix
- `test_comparison.png` — T1 vs T2 scatter + improvement histogram
- `top10_performers.png` — Top 10 students
- `bottom10_atrisk.png` — Bottom 10 / at-risk students
- `ca_vs_exam.png` — CA vs Exam by grade
- `ca_exam_gap.png` — Per-student CA-Exam gap
- `summary_dashboard.png` — Full summary dashboard
""")
]

nb["cells"] = cells

output_path = r"c:\Users\User1\Desktop\EXAMS_ANALYTICS\Exams_Analytics_Notebook.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"✅ Notebook created: {output_path}")

