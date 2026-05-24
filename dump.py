import os

# Папка с вашим проектом (текущая)
project_dir = os.getcwd()
output_file = "dump.txt"

with open(output_file, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(project_dir):
        # Пропускаем системные папки, если они есть
        if '.git' in root or '__pycache__' in root or '.venv' in root:
            continue
            
        for file in files:
            if file.endswith('.py') and file != os.path.basename(__file__):
                rel_path = os.path.relpath(os.path.join(root, file), project_dir)
                out.write(f"--- FILE: {rel_path} ---\n```python\n")
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    out.write(f.read())
                out.write("\n```\n\n")

print(f"Готово! Все файлы собраны в {output_file}")
