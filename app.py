import streamlit as st
import json
import requests
import base64
from PIL import Image
import io


#these are main classes your image is trained on
#you can define the classes in alphabectical order
PREDICTED_LABELS = ["Balloon Vine", "Black Honey Shrub","Cape Gooseberry","Coriander Leaves", "Curry Leaves", "Indian Copper Leaf", "Indian Stinging Nettle", "Mexican Mint"]
#'Balloon vine', 'Black Honey Shrub', 'Cape Gooseberry', 'Coriander Leaves', 'Curry Leaves', 'Indian Copper Leaf', 'Indian Stinging Nettle', 'Mexican Mint'

def get_prediction(image_data):
  #replace your image classification ai service URL
  url = 'https://askai.aiclub.world/b8c8a182-f728-4cdc-bdd5-c475cb17264a'
  r = requests.post(url, data=image_data)
  response = r.json()['predicted_label']
  score = r.json()['score']
  #print("Predicted_label: {} and confidence_score: {}".format(response,score))
  return response, score


#creating the web app

#setting up the title
st.title("Leaf Librarian")#change according to your project
#setting up the subheader
st.subheader("Upload a picture of a leaf you want to identify!")#change according to your project


#file uploader
image = st.file_uploader(label="Upload an image",accept_multiple_files=False, help="Upload an image to classify them")
if image:
    #converting the image to bytes
    img = Image.open(image)
    buf = io.BytesIO()
    img.save(buf,format = 'JPEG')
    byte_im = buf.getvalue()

    #converting bytes to b64encoding
    payload = base64.b64encode(byte_im)

    #file details
    file_details = {
      "file name": image.name,
      "file type": image.type,
      "file size": image.size
    }

    #write file details
    st.write(file_details)

    #setting up the image
    st.image(img)

    #predictions
    response, scores = get_prediction(payload)

    #if you are using the model deployment in navigator
    #you need to define the labels
    response_label = PREDICTED_LABELS[response]

    col1, col2 = st.columns(2)
    with col1:
      st.metric("Prediction Label",response_label)
    with col2:
      st.metric("Confidence Score", round(max(scores)*100,2))
    # Adding blocks of nice-looking text based on predictions
    if response_label == "Balloon Vine":
        st.info("Balloon Vine can be used to treat cough, skin diseases, earache, constipation, dandruff, and headache")
        st.link_button("Click here for some uses", "https://herbpathy.com/Uses-and-Benefits-of-Balloon-Vine-Cid490")
    elif response_label == "Black Honey Shrub":
        st.info("Black Honey Shrub can be used to treat sore throat, burns, headaches, and asthma")
        st.link_button("Click here for some uses", "https://www.healthbenefitstimes.com/black-honey-shrub/")
    elif response_label == "Cape Gooseberry":
        st.info("Cape Gooseberry can be used to treat inflammation, infections, and sore throats")
        st.link_button("Click here for some uses", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8523295/")
    elif response_label == "Coriander Leaves":
        st.info("Coriander Leaves can be used to treat blood pressure, stomach problems, infections and boost your immune system")
        st.link_button("Click here for some uses", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8747064/")
    elif response_label == "Curry Leaves":
        st.info("Curry Leaves can be used to treat nausea, inflammation, high cholesterol, and high blood sugar")
        st.link_button("Click here for some uses", "https://pharmeasy.in/blog/ayurveda-uses-benefits-side-effects-of-curry-leaves/")
    elif response_label == "Indian Copper Leaf":
        st.info("Indian Copper Leaves can be used to treat headaches, swelling, stomach aches, and skin diseases")
        st.link_button("Click here for some uses", "https://www.bimbima.com/ayurveda/medicinal-use-of-indian-acalypha/974/")
    elif response_label == "Indian Stinging Nettle":
        st.info("Indian Stinging Nettle can be used to treat muscle pain, anemia, and inflammation")
        st.link_button("Click here for some uses", "https://www.mountsinai.org/health-library/herb/stinging-nettle#:~:text=Stinging%20nettle%20has%20been%20used,benign%20prostatic%20hyperplasia%20or%20BPH")
    elif response_label == "Mexican Mint":
        st.info("Mexican Mint can be used to treat cold, stress, anxiety and detoxify the body")
        st.link_button("Click here for some uses", "https://www.organicfacts.net/health-benefits/herbs-and-spices/indian-borage-mexican-mint.html")
    else:
        st.write("This is a category I do not understand.")
