import os
import numpy as np
import torch
from PIL import Image

class ChessPiecePrompt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "piece": (["King", "Queen", "Bishop", "Knight", "Rook", "Pawn"],),
                "color": (["white", "black"],)
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("prompt", "image")

    FUNCTION = "generate_prompt"

    CATEGORY = "Chess"

    def load_image(self, image_path):
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            image_array = np.array(img).astype(np.float32) / 255.0
            # Convert the numpy array to a PyTorch tensor and adjust dimensions
            image_tensor = torch.tensor(image_array).permute(2, 0, 1).unsqueeze(0)
            # Convert the numpy array to an image
            image_output = Image.fromarray((image_array * 255).astype(np.uint8))
            return image_tensor, image_output

    def generate_prompt(self, piece, color):
        color_variable = "red" if color == "black" else "blue"

        prompt_map = {
            "King": f"Figurine of a king standing. wearing a {color_variable} cape, holding a sword in the air, burly, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image",
            "Queen": f"Figurine of a queen standing. wearing a {color_variable} cape, holding a rapier in the air, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image",
            "Rook": f"Figurine of a rook standing. wearing {color_variable} armour, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image",
            "Bishop": f"Figurine of a bishop standing. wearing a {color_variable} cloak, holding a staff, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image",
            "Knight": f"Figurine of a knight riding a horse. wearing a {color_variable} helmet, holding a lance, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image",
            "Pawn": f"Figurine of a pawn standing. wearing {color_variable} armour, metallic sheen, chiselled marble-like texture, high quality, detailed, chess piece, pose matching reference image"
}

        image_folder = "whiteImages" if color == "white" else "blackImages"
        image_path = os.path.join(os.path.dirname(__file__), image_folder, f"{piece.lower()}_720.png")
        image_tensor, image_output = self.load_image(image_path)
        return (prompt_map[piece], image_output)

NODE_CLASS_MAPPINGS = {
    "ChessPiecePrompt": ChessPiecePrompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChessPiecePrompt": "Chess Piece Prompt"
}