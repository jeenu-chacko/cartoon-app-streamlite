import streamlit as st
import os
import cv2 
from PIL import Image
import numpy as np
from io import BytesIO
import base64


@st.cache
def load_image(image_file):
	img = Image.open(image_file)
	return img 

def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">Download</a>'
    return href

def main():
	st.title('Cartoon app')
	
	image_file = st.file_uploader("Upload Image", type=["png","jpeg","jpg"])
	if image_file is not None:	
		img = load_image(image_file)
		

		st.image(img, caption='Original Image',use_column_width=True,width=250)

		new_img = np.array(img.convert('RGB'))
		new_img = cv2.cvtColor(new_img,1)
		gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
		gray = cv2.medianBlur(gray, 5)
		edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
		color = cv2.bilateralFilter(new_img, 15, 70, 70)
		cartoon = cv2.bitwise_and(color, color, mask=edges)
		
		st.image(cartoon, caption='Catoonised Image',use_column_width=True,width=250)

		result = Image.fromarray(cartoon)		
		st.markdown(get_image_download_link(result,image_file.name,'Download '+image_file.name), unsafe_allow_html=True)
	else:
		st.write("Make sure you image is in JPEG/JPG/PNG Format.")
	






if __name__ == '__main__':
	main()
