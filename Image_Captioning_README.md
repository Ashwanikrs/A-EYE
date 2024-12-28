
# Image Captioning with Text and Audio Output

## Overview
This project is a deep learning-based system that generates captions for images and provides the captions as both text and audio. The model uses a combination of computer vision and natural language processing techniques to create descriptive captions for input images.

## Features
- **Image Upload**: Users can upload images or provide a URL for prediction.
- **Caption Generation**: Generates descriptive captions for images using a trained neural network.
- **Audio Output**: Converts the generated caption to audio for accessibility.
- **Deployment**: Deployed on a platform for easy accessibility via a web interface.

## Workflow
1. **Data Preparation**:
   - Dataset: [Flickr8k Dataset](https://www.kaggle.com/adityajn105/flickr8k) is used for training the model.
   - Preprocessing: Extract image features using a pre-trained CNN (e.g., InceptionV3) and tokenize captions.

2. **Model Training**:
   - Encoder: A CNN extracts image features and encodes them into a dense representation.
   - Decoder: An LSTM-based decoder generates captions based on the encoded image features and word embeddings.
   - Loss Function: Cross-entropy loss is used to train the model.

3. **Evaluation**:
   - Test the model on unseen images to evaluate the quality of generated captions.
   - Metrics: Use BLEU scores to assess caption quality.

4. **Deployment**:
   - Flask-based application with a user-friendly interface.
   - Allows users to upload images and receive captions in text and audio formats.

## Model Architecture
- **Feature Extractor**: Pre-trained InceptionV3 (CNN) extracts image features.
- **Sequence Model**: LSTM processes image features and generates captions.
- **Embedding Layer**: Converts words into dense vectors for input to the LSTM.

## Screenshots
![alt text](chrome_D3gkuZWhoR.jpg)
![alt text](chrome_QPJFia8IFq.png)
## Requirements
- Python 3.8+
- TensorFlow 2.5+
- Flask
- Numpy
- Matplotlib
- Tqdm
- gTTS (for audio output)

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/image-captioning.git
cd image-captioning
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Dataset
- Place the Flickr8k dataset in the `data` directory.

### 4. Train the Model
Run the Jupyter Notebook to train the model:
```bash
jupyter notebook train_model.ipynb
```

### 5. Start the Application
Run the Flask application:
```bash
python app.py
```

Access the app at `http://localhost:5000`.

## Usage
1. Upload an image or paste a URL.
2. Click "Generate Caption" to see the predicted caption as text and hear voice concurrently.

## Results
- **BLEU score**: ~0.74
- Sample Captions:
  - Input: Image of a dog playing with a ball
  - Output: "A dog playing with a ball on the grass."

## Challenges
- Handling overfitting: Applied dropout and early stopping.
- Improving generalization: Used data augmentation and pre-trained models.

## Future Work
- Extend support for multiple languages in audio output.
- Experiment with different architectures like Transformer-based models.
- Enhance the web app with advanced features like batch processing and caption editing.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please create an issue or pull request for any enhancements or bug fixes.

## Acknowledgements
- Flickr8k Dataset
- TensorFlow Documentation
