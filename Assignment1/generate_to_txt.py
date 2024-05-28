import nbformat

def extract_code_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    code_cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
    code = '\n'.join(cell.source for cell in code_cells)
    return code

notebook_paths = ['Task1.ipynb', 'Task2.ipynb', 'Task3.ipynb']
code = '\n'.join(extract_code_from_notebook(path) for path in notebook_paths)

with open('code.txt', 'w', encoding='utf-8') as f:
    f.write(code)