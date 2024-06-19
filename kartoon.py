import json

from generate_panels import generate_panels, generate_characters
from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

SCENARIO = """
Miki-san and Kabata-san are two employees of an investment bank. Miki-san is explaining the importance of NISA account to Kabata-san.
"""

CHARACTERS = """
Miki-san is a tall and slim Japanese guy. Kabata-san is a average heighted japanese man. Both are in formal attire.
"""

negative_prompt = """Worst quality, Normal quality, Low quality, Low res, Blurry, Jpeg artifacts, Grainy, Cropped, Out of frame, Out of focus, Bad anatomy, Bad proportions, Deformed, Disconnected limbs, Disfigured, Extra arms, Extra limbs, Extra hands, Fused fingers, Gross proportions, Long neck, Malformed limbs, Mutated, Mutated hands, Mutated limbs, Missing arms, Missing fingers, Poorly drawn hands, Poorly drawn face, NSFW, nudity, mature content"""

STYLE = "manga, colored"

# ==========================================================================================

print(f"Generate panels with style '{STYLE}' for this scenario: \n {SCENARIO}")

characters = generate_characters(CHARACTERS)

panels = generate_panels(SCENARIO, characters)

with open('output/panels.json', 'w') as outfile:
  json.dump(panels, outfile)

with open('output/panels.json') as json_file:
  panels = json.load(json_file)

panel_images = []

for panel in panels:
  panel_prompt = panel["description"] + ", cartoon box, " + STYLE + ". Use the following as negative prompts: "+negative_prompt
  print(f"Generate panel {panel['number']} with prompt: {panel_prompt}")
  panel_image = text_to_image(panel_prompt)
  panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
  panel_image_with_text.save(f"output/panel-{panel['number']}.png")
  panel_images.append(panel_image_with_text)

create_strip(panel_images).save("output/strip.png")
