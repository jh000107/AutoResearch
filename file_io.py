from datetime import datetime

def save_markdown(task_output):
    today_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today_date}.md"

    with open(filename, 'w') as file:
        file.write(task_output.result)
    print(f"Survey papers saved as {filename}")

def save_json(task_output):
    filename = "paper_details.json"
    
    with open(filename, 'w') as file:
        file.write(task_output.result)

    print(f"Survey papers saved as {filename}")

