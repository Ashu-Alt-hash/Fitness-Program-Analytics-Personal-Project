import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Excel data
file_path = "C:\\Users\\91877\\Downloads\\client_fitness_data.xlsx"
df = pd.read_excel("C:\\Users\\91877\\Downloads\\client_fitness_data.xlsx")


# Ensure correct data types
df['Dropout'] = df['Dropout'].astype(int)
df['Goal_Completed'] = df['Goal_Completed'].astype(int)

# =========================
# 1. Improvement Over Time
# =========================
progress_over_time = df.groupby('Week')['Progress_Score'].mean()

# =========================
# 2. Retention vs Dropout
# =========================
dropout_summary = df.groupby('Client')['Dropout'].max().value_counts()
dropout_labels = ['Retained', 'Dropped Out']

# =========================
# 3. Dropout Reasons by Goal
# =========================
last_weeks = df.sort_values('Week').groupby('Client').last().reset_index()
dropout_by_goal = last_weeks[last_weeks['Dropout'] == 1]['Goal'].value_counts()

# =========================
# 4. Recommendations
# =========================
incomplete_goals = last_weeks[(last_weeks['Goal_Completed'] == 0) & (last_weeks['Dropout'] == 0)]

# =========================
# Visualization
# =========================
sns.set(style="whitegrid")
fig, axs = plt.subplots(3, 1, figsize=(12, 18))

# 1. Progress Chart
axs[0].plot(progress_over_time.index, progress_over_time.values, marker='o', color='green')
axs[0].set_title("Average Progress Score Over Weeks", fontsize=14)
axs[0].set_xlabel("Week")
axs[0].set_ylabel("Average Progress Score")

# 2. Retention Pie Chart
axs[1].pie(dropout_summary, labels=dropout_labels, autopct='%1.1f%%', startangle=90,
           colors=['skyblue', 'salmon'], textprops={'fontsize': 12})
axs[1].set_title("Client Retention vs Dropout", fontsize=14)

# 3. Dropout by Goal
sns.barplot(x=dropout_by_goal.index,y=dropout_by_goal.values,ax=axs[2],hue=dropout_by_goal.index,palette='muted',legend=False)
axs[2].set_title("Dropout Count by Fitness Goal", fontsize=14)
axs[2].set_ylabel("Number of Dropouts")
axs[2].set_xlabel("Fitness Goal")

plt.tight_layout()
plt.show()

# =========================
# Show Personalized Recommendations
# =========================
print("\n📌 Clients who need personalized improvements (incomplete goals but retained):")
print(incomplete_goals[['Client', 'Goal']].drop_duplicates().to_string(index=False))