from ultralytics import YOLO
from flask import Flask, request, jsonify, render_template_string
from PIL import Image
import io
import os

# ==========================================================
# LOCAL MODEL PATH
# Put your .pt model file in the same folder as this app.py
# Example: skin-disease-app/model.pt
# ==========================================================
MODEL_PATH = "model.pt"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. "
        "Please place your .pt model file in the same folder as app.py "
        "or update MODEL_PATH." 
    )

model = YOLO(MODEL_PATH)
print(f"✅ Model loaded: {MODEL_PATH}")

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skin Disease Classifier</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 900px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f8f9ff;
        }
        .upload-area:hover {
            border-color: #764ba2;
            background: #f0f2ff;
        }
        .upload-icon { font-size: 48px; margin-bottom: 15px; }
        #fileInput { display: none; }

        .preview-container {
            display: none;
            margin-top: 20px;
            text-align: center;
        }
        .preview-container.show { display: block; }
        #preview {
            max-width: 100%;
            max-height: 300px;
            border-radius: 10px;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            border-radius: 30px;
            cursor: pointer;
            margin-top: 20px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102,126,234,0.4);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .results {
            margin-top: 30px;
            display: none;
        }
        .results.show { display: block; }

        .top-result {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .top-result h2 {
            color: #764ba2;
            font-size: 1.6rem;
        }
        .confidence {
            color: #667eea;
            font-size: 1.2rem;
            margin-top: 5px;
        }

        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
            line-height: 1.6;
        }
        .treatment-box { border-left-color: #28a745; }

        .result-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }
        .result-label {
            width: 160px;
            font-weight: 500;
            color: #444;
            font-size: 0.9rem;
        }
        .result-bar {
            flex: 1;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 0 10px;
        }
        .result-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        .result-value {
            width: 50px;
            text-align: right;
            font-weight: 600;
            color: #667eea;
            font-size: 0.9rem;
        }

        .disclaimer {
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-radius: 10px;
            color: #856404;
            font-size: 0.9rem;
        }

        .loading {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        .loading.show { display: block; }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        h3 { color: #333; margin: 20px 0 15px; }

        @media (max-width: 600px) {
            .header h1 { font-size: 2rem; }
            .card { padding: 20px; }
            .result-label { width: 120px; font-size: 0.8rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🩺 Skin Disease Classifier</h1>
            <p>Upload a skin condition image for AI-based classification</p>
        </div>

        <div class="card">
            <div class="upload-area" id="uploadArea" onclick="document.getElementById('fileInput').click()">
                <div class="upload-icon">📷</div>
                <p><strong>Drop an image here</strong></p>
                <p style="color: #888; margin-top: 10px;">or click to choose a file</p>
                <input type="file" id="fileInput" accept="image/*">
            </div>

            <div class="preview-container" id="previewContainer">
                <img id="preview" alt="Image preview">
                <br>
                <button class="btn" id="classifyBtn" onclick="classify()">🔬 Analyze Image</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 15px;">Analyzing image...</p>
            </div>

            <div class="results" id="results">
                <div class="top-result" id="topResult"></div>
                <div class="info-box" id="diseaseDesc"></div>
                <div class="info-box treatment-box" id="diseaseTreatment"></div>

                <h3>Top 5 Predictions</h3>
                <div id="resultsList"></div>
            </div>

            <div class="disclaimer">
                ⚠️ <strong>Disclaimer:</strong>
                This tool is for educational and informational purposes only.
                It is not a medical diagnosis. Always consult a qualified healthcare professional
                or dermatologist for proper medical evaluation and treatment.
            </div>
        </div>
    </div>

    <script>
        const diseaseInfo = {
            "Acne": {
                name: "Acne",
                desc: "Inflammation of hair follicles and oil glands caused by clogged pores, dead skin cells, excess oil, and bacteria.",
                treatment: "Wash your face twice daily with a gentle cleanser. Avoid squeezing pimples. Consider over-the-counter acne products such as salicylic acid or benzoyl peroxide."
            },
            "Actinic_Keratosis": {
                name: "Actinic Keratosis",
                desc: "A rough, dry, scaly patch of skin caused by years of sun exposure. It is considered a precancerous skin condition.",
                treatment: "Avoid direct sun exposure, use sunscreen daily, and consult a dermatologist for proper evaluation."
            },
            "Benign_tumors": {
                name: "Benign Tumors",
                desc: "Non-cancerous skin growths that do not invade nearby tissue or spread to other parts of the body.",
                treatment: "Do not cut, puncture, or remove the lesion yourself. Monitor for changes and consult a doctor if it becomes painful, inflamed, or grows quickly."
            },
            "Bullous": {
                name: "Bullous Skin Condition",
                desc: "A skin condition characterized by large fluid-filled blisters on the skin surface.",
                treatment: "Do not burst the blisters. Keep the area clean and dry, cover it with sterile gauze, and seek medical attention."
            },
            "DrugEruption": {
                name: "Drug Eruption",
                desc: "A skin reaction that may occur after taking certain medications, often appearing as a widespread red or itchy rash.",
                treatment: "Contact a healthcare professional immediately. Do not stop prescribed medication without medical advice unless severe symptoms occur."
            },
            "Eczema": {
                name: "Eczema",
                desc: "A chronic inflammatory skin condition that can cause dry, red, cracked, itchy, or irritated skin.",
                treatment: "Use fragrance-free moisturizer regularly, avoid harsh soaps, take lukewarm showers, and avoid scratching the affected area."
            },
            "Infestations_Bites": {
                name: "Infestations and Bites",
                desc: "Skin irritation caused by insect bites, mites, or parasitic infestation such as scabies.",
                treatment: "Wash the area with soap and water. Apply a cold compress. Avoid scratching. If scabies is suspected, medical treatment may be needed for close contacts as well."
            },
            "Lichen": {
                name: "Lichen Planus",
                desc: "An inflammatory skin condition that may cause purplish, itchy, flat-topped bumps or thickened skin patches.",
                treatment: "Avoid scratching. Use moisturizers and cold compresses. Consult a dermatologist if symptoms persist or spread."
            },
            "Psoriasis": {
                name: "Psoriasis",
                desc: "An autoimmune-related skin condition that causes thick, red, inflamed patches covered with silvery-white scales.",
                treatment: "Do not forcibly remove scales. Moisturize regularly, manage stress, and consult a doctor for appropriate treatment options."
            },
            "Rosacea": {
                name: "Rosacea",
                desc: "A chronic facial skin condition that causes redness, visible blood vessels, and sometimes acne-like bumps.",
                treatment: "Avoid common triggers such as extreme temperatures, spicy foods, alcohol, and harsh skincare products. Use sunscreen suitable for sensitive skin."
            },
            "Seborrh_Keratoses": {
                name: "Seborrheic Keratoses",
                desc: "A common non-cancerous skin growth that may look waxy, brown, black, or slightly raised.",
                treatment: "Usually harmless and does not require treatment. Avoid scratching. A doctor can remove it if it becomes irritated or cosmetically concerning."
            },
            "SkinCancer": {
                name: "⚠️ Skin Cancer",
                desc: "An abnormal and potentially malignant growth of skin cells. Warning signs may include changing moles, irregular borders, unusual colors, or non-healing wounds.",
                treatment: "⚠️ Seek immediate medical evaluation from a dermatologist. Early detection and proper diagnosis are very important."
            },
            "Tinea": {
                name: "Tinea / Ringworm",
                desc: "A fungal skin infection that often appears as a red, itchy, ring-shaped rash.",
                treatment: "Keep the area clean and dry. Change sweaty clothes promptly. Antifungal creams may help, but consult a healthcare professional if symptoms persist."
            },
            "Unknown_Normal": {
                name: "Unknown / Normal",
                desc: "No identifiable skin disease pattern was detected by the model.",
                treatment: "No specific treatment is suggested. Maintain good hygiene, moisturize the skin, and use sunscreen regularly."
            },
            "Vascular_Tumors": {
                name: "Vascular Tumors",
                desc: "Skin growths related to blood vessels, often appearing as red or purple marks or bumps.",
                treatment: "Often harmless, but medical evaluation is recommended if it bleeds, grows rapidly, becomes painful, or changes appearance."
            },
            "Vasculitis": {
                name: "Vasculitis",
                desc: "Inflammation of blood vessels that may cause reddish or purplish spots, swelling, pain, or skin changes.",
                treatment: "Seek medical evaluation because vasculitis can be associated with internal health conditions. Rest and elevate affected limbs if swelling is present."
            },
            "Vitiligo": {
                name: "Vitiligo",
                desc: "A condition where pigment-producing cells are lost, causing well-defined white patches on the skin.",
                treatment: "Protect depigmented areas from sunburn by using high-SPF sunscreen. Consult a dermatologist for treatment options."
            },
            "Warts": {
                name: "Warts",
                desc: "Rough skin growths caused by human papillomavirus (HPV). They can be contagious through direct contact.",
                treatment: "Do not pick or cut warts. Keep the area clean and dry. Over-the-counter salicylic acid products may help, or consult a doctor for removal."
            }
        };

        const uploadArea = document.getElementById("uploadArea");
        const fileInput = document.getElementById("fileInput");
        const preview = document.getElementById("preview");
        const previewContainer = document.getElementById("previewContainer");
        let currentFile = null;

        uploadArea.ondragover = (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = "#764ba2";
        };

        uploadArea.ondragleave = () => {
            uploadArea.style.borderColor = "#667eea";
        };

        uploadArea.ondrop = (e) => {
            e.preventDefault();
            uploadArea.style.borderColor = "#667eea";
            handleFile(e.dataTransfer.files[0]);
        };

        fileInput.onchange = (e) => handleFile(e.target.files[0]);

        function handleFile(file) {
            if (!file || !file.type.startsWith("image/")) {
                alert("Please select a valid image file.");
                return;
            }

            currentFile = file;
            const reader = new FileReader();

            reader.onload = (e) => {
                preview.src = e.target.result;
                previewContainer.classList.add("show");
                document.getElementById("results").classList.remove("show");
            };

            reader.readAsDataURL(file);
        }

        async function classify() {
            if (!currentFile) return;

            document.getElementById("classifyBtn").disabled = true;
            document.getElementById("loading").classList.add("show");
            document.getElementById("results").classList.remove("show");

            const formData = new FormData();
            formData.append("image", currentFile);

            try {
                const response = await fetch("/predict", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                if (!response.ok || data.error) {
                    throw new Error(data.error || "Prediction failed.");
                }

                displayResults(data.predictions);
            } catch (error) {
                alert("Error: " + error.message);
            }

            document.getElementById("classifyBtn").disabled = false;
            document.getElementById("loading").classList.remove("show");
        }

        function displayResults(predictions) {
            const sorted = Object.entries(predictions).sort((a, b) => b[1] - a[1]);
            const top = sorted[0];

            const info = diseaseInfo[top[0]] || {
                name: top[0],
                desc: "Description is not available for this class.",
                treatment: "Please consult a qualified healthcare professional for further guidance."
            };

            document.getElementById("topResult").innerHTML =
                "<h2>" + info.name + "</h2>" +
                "<div class='confidence'>" + (top[1] * 100).toFixed(1) + "% confidence</div>";

            document.getElementById("diseaseDesc").innerHTML =
                "<strong>📋 Description:</strong> " + info.desc;

            document.getElementById("diseaseTreatment").innerHTML =
                "<strong>💊 Initial Care:</strong> " + info.treatment;

            let html = "";

            sorted.slice(0, 5).forEach(([name, prob]) => {
                html +=
                    "<div class='result-item'>" +
                        "<div class='result-label'>" + name.replace(/_/g, " ") + "</div>" +
                        "<div class='result-bar'>" +
                            "<div class='result-fill' style='width:" + (prob * 100) + "%'></div>" +
                        "</div>" +
                        "<div class='result-value'>" + (prob * 100).toFixed(1) + "%</div>" +
                    "</div>";
            });

            document.getElementById("resultsList").innerHTML = html;
            document.getElementById("results").classList.add("show");
        }
    </script>
</body>
</html>
'''


@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file was uploaded."}), 400

    try:
        file = request.files["image"]
        image = Image.open(io.BytesIO(file.read())).convert("RGB")

        results = model(image, imgsz=416, verbose=False)
        probs = results[0].probs

        if probs is not None:
            prob_values = probs.data.cpu().numpy()
            names = results[0].names

            predictions = {
                names.get(idx, f"Class_{idx}"): float(prob)
                for idx, prob in enumerate(prob_values)
            }

            return jsonify({"predictions": predictions})

        return jsonify({"error": "Prediction failed. This model may not be a classification model."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Localhost only:
    # Access from the same computer using http://127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)