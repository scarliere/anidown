import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from anidown.gui import run_gui


if __name__ == "__main__":
	run_gui()
