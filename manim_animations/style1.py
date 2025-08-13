import subprocess
import time
import os
import glob
import traceback  # <-- import here

class SceneRenderer:
    def __init__(self):
        pass

    def render(self, scenes):
        output_dir = "manim_animations/output"
        os.makedirs(output_dir, exist_ok=True)

        scene_file = "manim_animations/scene1.py"
        scene_name = "SimpleScene"

        cmd = [
            "manim",
            "-ql",
            scene_file,
            scene_name,
            "-o",
            output_dir
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(f"[style1.SceneRenderer] Manim stdout:\n{result.stdout}")
            print(f"[style1.SceneRenderer] Manim stderr:\n{result.stderr}")

            if result.returncode != 0:
                print(f"[style1.SceneRenderer] Manim CLI error output:\n{result.stderr}")
                raise RuntimeError(f"Manim rendering failed:\n{result.stderr}")

            pattern = os.path.join(output_dir, f"{scene_name}_*.mp4")
            list_of_files = glob.glob(pattern)
            if not list_of_files:
                raise FileNotFoundError(f"No output video found matching {pattern}")

            latest_file = max(list_of_files, key=os.path.getctime)
            return os.path.basename(latest_file)

        except Exception as e:
            print(f"[style1.SceneRenderer] Error during rendering: {e}")
            print(traceback.format_exc())
            raise e