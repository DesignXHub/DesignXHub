import bpy
import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BLENDER_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "blender_scripts"))
WATCH_FILE = os.path.join(BLENDER_SCRIPTS_DIR, "auto_script.py")
OUTPUT_DIR = os.path.join(BLENDER_SCRIPTS_DIR, "output")
CHECK_INTERVAL = 1

class ScriptWatcher:
    def __init__(self):
        self.last_modified = 0
        self._ensure_directories()

    def _ensure_directories(self):
        os.makedirs(BLENDER_SCRIPTS_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def safe_execute(self, code):
        try:
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()
            exec(code)
            bpy.context.scene.render.filepath = os.path.join(OUTPUT_DIR, "render.png")
            bpy.ops.render.render(write_still=True)
            logger.info("Code executed and render exported!")
            return True
        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            return False

    def check_file(self):
        try:
            current_modified = os.path.getmtime(WATCH_FILE)
            if current_modified > self.last_modified:
                with open(WATCH_FILE, 'r', encoding='utf-8') as f:
                    code = f.read()
                if self.safe_execute(code):
                    self.last_modified = current_modified
        except FileNotFoundError:
            logger.warning("Script file not found!")
        except Exception as e:
            logger.error(f"Error: {str(e)}")
        return CHECK_INTERVAL

watcher = ScriptWatcher()
bpy.app.timers.register(watcher.check_file, persistent=True)
