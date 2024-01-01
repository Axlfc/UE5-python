def remove_all_duplicate_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    unique_lines = set()
    cleaned_lines = []

    for line in lines:
        if line not in unique_lines:
            unique_lines.add(line)
            cleaned_lines.append(line)

    cleaned_text = ''.join(cleaned_lines)

    with open('cleaned_file.txt', 'w') as file:
        file.write(cleaned_text)

# Usage
remove_all_duplicate_lines('mia.txt')
