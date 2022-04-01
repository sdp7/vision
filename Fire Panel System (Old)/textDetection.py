import cv2
import pytesseract
 
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

vid = cv2.VideoCapture(0)

while True:
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
 
    # Specify structure shape and kernel size.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
 
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)
 
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
 
# Creating a copy of image
    im2 = frame.copy()
 
# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.drawContours(frame, cnt, -1, (0, 255, 0), 2)
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        print(text)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(100)

    if key == 27:
        break

vid.release()
cv2.destroyAllWindows()