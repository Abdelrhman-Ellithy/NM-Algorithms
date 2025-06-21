import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Connect to the database
conn = sqlite3.connect('Results.db')

# Query: Average, min, max CPU time per algorithm
df_alg = pd.read_sql_query('''
    SELECT method_name, 
           AVG(CPU_Time) as avg_cpu, 
           MIN(CPU_Time) as min_cpu, 
           MAX(CPU_Time) as max_cpu, 
           COUNT(*) as runs
    FROM results
    GROUP BY method_name
    ORDER BY avg_cpu
''', conn)

print('Average CPU time per algorithm:')
print(df_alg)

# Query: Average CPU time per problem per algorithm
df_prob = pd.read_sql_query('''
    SELECT problemId, method_name, AVG(CPU_Time) as avg_cpu
    FROM results
    GROUP BY problemId, method_name
    ORDER BY method_name, problemId
''', conn)

# Plot: Barplot of average CPU time per algorithm
plt.figure(figsize=(10, 5))
sns.barplot(data=df_alg, x='method_name', y='avg_cpu')
plt.xticks(rotation=45, ha='right')
plt.title('Average CPU Time per Algorithm')
plt.ylabel('Avg CPU Time (s)')
plt.xlabel('Algorithm')
plt.tight_layout()
plt.savefig('avg_cpu_time_per_algorithm.png')
plt.show()

# Additional summary statistics for CPU time per algorithm
cpu_stats = df_alg.copy()
cpu_stats['std_cpu'] = df_prob.groupby('method_name')['avg_cpu'].std().values
cpu_stats['median_cpu'] = df_prob.groupby('method_name')['avg_cpu'].median().values
print('\nCPU time statistics per algorithm:')
print(cpu_stats)

# Line plot: CPU time per problem for each algorithm
plt.figure(figsize=(12, 6))
for alg in df_prob['method_name'].unique():
    subset = df_prob[df_prob['method_name'] == alg]
    plt.plot(subset['problemId'], subset['avg_cpu'], marker='o', label=alg)
plt.title('CPU Time per Problem for Each Algorithm')
plt.xlabel('Problem ID')
plt.ylabel('Avg CPU Time (s)')
plt.xlim(0, 14)
plt.ylim(bottom=0)
plt.yticks([round(x,6) for x in plt.yticks()[0] if x <= max(df_prob['avg_cpu'].max(), 0.015)])
plt.legend()
plt.tight_layout()
plt.savefig('cpu_time_lineplot_per_problem.png')
plt.show()

# Query: Average iterations per algorithm (if available)
try:
    df_iter = pd.read_sql_query('''
        SELECT method_name, AVG(iterations) as avg_iter
        FROM results
        GROUP BY method_name
        ORDER BY avg_iter
    ''', conn)
    print('Average iterations per algorithm:')
    print(df_iter)
except Exception as e:
    print('No iterations data found in the database.')

# 1. Line plot: Average CPU time per algorithm across all problems (already present, but clearer)
avg_cpu_per_alg = df_prob.groupby('method_name')['avg_cpu'].mean().sort_values()
plt.figure(figsize=(10, 5))
avg_cpu_per_alg.plot(marker='o')
plt.title('Average CPU Time per Algorithm (Overall)')
plt.ylabel('Avg CPU Time (s)')
plt.xlabel('Algorithm')
plt.xticks(rotation=45, ha='right')
plt.ylim(bottom=0)
plt.yticks([round(x,6) for x in plt.yticks()[0] if x <= max(avg_cpu_per_alg.max(), 0.015)])
plt.tight_layout()
plt.savefig('avg_cpu_time_lineplot_overall.png')
plt.show()

# 2. Line plot: Fastest algorithm for each problem (min CPU time per problem), with legend for clarity
fastest = df_prob.loc[df_prob.groupby('problemId')['avg_cpu'].idxmin()]
plt.figure(figsize=(12, 6))
for alg in fastest['method_name'].unique():
    subset = fastest[fastest['method_name'] == alg]
    plt.plot(subset['problemId'], subset['avg_cpu'], marker='o', label=alg)
plt.title('Fastest Algorithm per Problem (CPU Time)')
plt.xlabel('Problem ID')
plt.ylabel('Fastest CPU Time (s)')
plt.xlim(0, 14)
plt.ylim(bottom=0)
plt.yticks([round(x,6) for x in plt.yticks()[0] if x <= max(fastest['avg_cpu'].max(), 0.015)])
plt.legend(title='Algorithm')
plt.tight_layout()
plt.savefig('fastest_algorithm_per_problem_lineplot.png')
plt.show()

# 3. Line plot: Top 3 fastest algorithms (by overall average CPU time) across all problems
top3_algs = avg_cpu_per_alg.head(3).index.tolist()
plt.figure(figsize=(12, 6))
for alg in top3_algs:
    subset = df_prob[df_prob['method_name'] == alg]
    plt.plot(subset['problemId'], subset['avg_cpu'], marker='o', label=alg)
plt.title('Top 3 Fastest Algorithms: CPU Time per Problem')
plt.xlabel('Problem ID')
plt.ylabel('Avg CPU Time (s)')
plt.xlim(0, 14)
plt.ylim(bottom=0)
plt.yticks([round(x,6) for x in plt.yticks()[0] if x <= max(df_prob[df_prob['method_name'].isin(top3_algs)]['avg_cpu'].max(), 0.015)])
plt.legend()
plt.tight_layout()
plt.savefig('top3_fastest_algorithms_lineplot.png')
plt.show()
conn.close()