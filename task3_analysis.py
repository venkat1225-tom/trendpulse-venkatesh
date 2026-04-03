Q: 3
Task 3 — Analysis with Pandas & NumPy
TrendPulse: What's Actually Trending Right Now
Marks: 20 | File: task3_analysis.py

Submission: Push your file to the same public GitHub repo and share the direct link: https://github.com/<username>/trendpulse-<name>/blob/main/task3_analysis.py

⚠️ Anti-AI Policy: Write your own code. Comments explaining your logic count in your favour.

Needs: data/trends_clean.csv from Task 2

What to Build
Load the clean CSV from Task 2 and explore the data using Pandas and NumPy. Find patterns, compute statistics, and add a couple of new columns. Save the result as a new CSV for Task 4.

Tasks
1 — Load and Explore (4 marks)
Load data/trends_clean.csv into a Pandas DataFrame
Print the first 5 rows
Print the shape of the DataFrame (rows and columns)
Print the average score and average num_comments across all stories
2 — Basic Analysis with NumPy (8 marks)
Use NumPy to answer these questions and print the results:

What is the mean, median, and standard deviation of score?
What is the highest score and lowest score?
Which category has the most stories?
Which story has the most comments? Print its title and comment count.
3 — Add New Columns (5 marks)
Add these two new columns to your DataFrame:

Column	Formula
engagement	num_comments / (score + 1) — how much discussion a story gets per upvote
is_popular	True if score > average score, else False
4 — Save the Result (3 marks)
Save the updated DataFrame (with the 2 new columns) to data/trends_analysed.csv
Print a confirmation message
Expected Output
Loaded data: (114, 7)

First 5 rows:
   post_id   title             category   score  num_comments ...

Average score   : 12,450
Average comments: 342

--- NumPy Stats ---
Mean score   : 12,450
Median score : 8,200
Std deviation: 9,870
Max score    : 87,432
Min score    : 5

Most stories in: technology (22 stories)

Most commented story: "AI model beats humans at coding"  — 4,891 comments

Saved to data/trends_analysed.csv
Submission Checklist
 Script runs without errors
 NumPy used for at least mean, median, std
 engagement and is_popular columns added
 data/trends_analysed.csv saved
 Code is commented
Marks Breakdown
Description	Marks
1	Load and explore the data	4
2	NumPy statistics	8
3	Add new columns	5
4	Save to CSV	3
Total	20
Next: Task 4 will load this CSV and turn the numbers into charts.
