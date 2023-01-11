from pathlib import Path
import os



root = Path(__file__).parent
if __name__ == "__main__":
    hetpy_dir = "hetpy"
    output_dir = "./docs"
    os.system(f"pdoc {hetpy_dir} -o {output_dir}")
    