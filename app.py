import streamlit as st

import tempfile

import os

import fitz

# Function to compress the PDF

def compress_pdf(input_pdf, output_pdf, compression_level):

    # Open the input PDF

    doc = fitz.open(input_pdf)

    # Calculate the compression quality

    compression_quality = 1 - (compression_level / 100)

    # Compress each page of the PDF

    for page in doc:

        # Convert the page to an image

        pix = page.get_pixmap()

        img_data = pix.get_png_data(compression=9 - int(compression_quality * 9))

        # Recreate the PDF page with the compressed image

        new_page = doc.new_page(width=pix.width, height=pix.height)

        new_page.set_pixmap(fitz.Pixmap(img_data))

        # Replace the original page with the compressed page

        doc.delete_page(page.number)

        doc.insert_page(page.number, new_page)

    # Save the compressed PDF

    doc.save(output_pdf)

    doc.close()

# Streamlit app

def main():

    st.title("PDF Compressor")

    # File uploader

    st.subheader("Upload the PDF file")

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:

        # Create a temporary directory to save the uploaded file

        temp_dir = tempfile.TemporaryDirectory()

        input_path = os.path.join(temp_dir.name, uploaded_file.name)

        output_path = os.path.join(temp_dir.name, "compressed.pdf")

        # Save the uploaded file to the temporary directory

        with open(input_path, "wb") as file:

            file.write(uploaded_file.getvalue())

        # Compression level selection

        st.subheader("Compression Level")

        compression_level = st.select_slider("Select the compression level", options=list(range(101)), value=50)

        # Compress the PDF when the user clicks the button

        if st.button("Compress"):

            compress_pdf(input_path, output_path, compression_level)

            st.success("PDF compression complete!")

            # Download link for the compressed file

            compressed_file = open(output_path, "rb").read()

            st.download_button("Download Compressed PDF", compressed_file, file_name="compressed.pdf")

        # Cleanup the temporary directory

        temp_dir.cleanup()

if __name__ == "__main__":

    main()



     
        
