from manim_animations import style1  # your existing manual style

class VisualGenerator:
    def __init__(self):
        self.styles = {
            "style1": style1.SceneRenderer(),
            # add more styles when ready
        }

    def render(self, scene_plan: dict):
        style_name = scene_plan.get("style", "style1")
        renderer = self.styles.get(style_name)
        if not renderer:
            raise ValueError(f"Unknown style: {style_name}")
        return renderer.render(scene_plan.get("scenes", []))

_visual_generator = VisualGenerator()

def generate_animation(scene_text: str, style: str = "style1") -> str:
    scene_plan = {
        "style": style,
        "scenes": [{"text": scene_text}]
    }
    return _visual_generator.render(scene_plan)