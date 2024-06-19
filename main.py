from flask import Flask, request, jsonify
import json
from generate_panels import generate_panels
from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

app = Flask(__name__)

@app.route('/api/generate_panels', methods=['POST'])
def generate_panels_api():
    data = request.get_json()
    scenario = data.get('scenario')
    if not scenario:
        return jsonify({'error': 'Please provide a scenario'}), 400
    
    panels = generate_panels(scenario)
    with open('output/panels.json', 'w') as outfile:
        json.dump(panels, outfile)
    
    return jsonify({'message': 'Panels generated successfully'}), 200

@app.route('/api/generate_strip', methods=['POST'])
def generate_strip_api():
    # Assuming panels are already generated and saved in panels.json
    with open('output/panels.json') as json_file:
        panels = json.load(json_file)

    panel_images = []
    for panel in panels:
        panel_prompt = panel["description"] + ", cartoon box, manga, colored. Use the following as negative prompts: Worst quality, Normal quality, Low quality, Low res, Blurry, Jpeg artifacts, Grainy, Cropped, Out of frame, Out of focus, Bad anatomy, Bad proportions, Deformed, Disconnected limbs, Disfigured, Extra arms, Extra limbs, Extra hands, Fused fingers, Gross proportions, Long neck, Malformed limbs, Mutated, Mutated hands, Mutated limbs, Missing arms, Missing fingers, Poorly drawn hands, Poorly drawn face, NSFW, nudity, mature content"
        panel_image = text_to_image(panel_prompt)
        panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
        panel_images.append(panel_image_with_text)
    
    create_strip(panel_images).save("output/strip.png")
    
    return jsonify({'message': 'Strip generated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
