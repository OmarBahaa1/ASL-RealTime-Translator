import cv2
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import os
from ultralytics import YOLO 

# 1. Load the YOLO model
model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

# --- TRANSLATOR STATE VARIABLES ---
sentence = ""
current_letter = ""
consecutive_frames = 0
cooldown = 0
NO_HAND_FRAMES = 0

# --- SNAPSHOT CAMERA SETTINGS ---
CONF_THRESHOLD = 0.65      # Strict confidence (no blurry hands)
REQUIRED_FRAMES = 15       # Must hold perfectly still for ~0.5 seconds
COOLDOWN_FRAMES = 30       # "Camera Flash" delay (waits 1 sec before next letter)
AUTO_SPACE_THRESHOLD = 45  # Drop hand for 1.5s to add a space

# --- GUI FUNCTIONS ---
def clear_text():
    global sentence
    sentence = ""
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)
    text_display.config(state=tk.DISABLED)

def save_text():
    global sentence
    if sentence.strip():
        filename = datetime.datetime.now().strftime("Translation_%Y%m%d_%H%M%S.txt")
        with open(filename, "w") as file:
            file.write(sentence)
        print(f"Saved to {filename}!")

def quit_app():
    cap.release()
    root.destroy()

def update_frame():
    global sentence, current_letter, consecutive_frames, cooldown, NO_HAND_FRAMES
    
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)

        results = model(frame, conf=CONF_THRESHOLD, verbose=False)

        best_detection = None
        highest_conf = 0.0

        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf > highest_conf:
                    highest_conf = conf
                    best_detection = box

        if best_detection is not None:
            NO_HAND_FRAMES = 0
            x1, y1, x2, y2 = map(int, best_detection.xyxy[0])
            cls = int(best_detection.cls[0])
            detected_char = model.names[cls]
            
            # Draw the basic box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{detected_char}", (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # --- THE SNAPSHOT LOGIC ---
            if cooldown > 0:
                # The camera is "recharging", show a blue cool-down message
                cv2.putText(frame, "Waiting...", (x1, y2 + 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                cooldown -= 1
            else:
                if detected_char == current_letter:
                    consecutive_frames += 1
                    
                    # Calculate and draw the "Loading Bar" percentage!
                    progress = int((consecutive_frames / REQUIRED_FRAMES) * 100)
                    cv2.putText(frame, f"Locking in: {progress}%", (x1, y2 + 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    current_letter = detected_char
                    consecutive_frames = 1

                # When it hits 100% (Takes the photo!)
                if consecutive_frames >= REQUIRED_FRAMES:
                    if detected_char == "space":
                        if not sentence.endswith(" "): sentence += " "
                    elif detected_char == "del":
                        sentence = sentence[:-1]
                    else:
                        sentence += detected_char
                    
                    # Reset for the next photo
                    consecutive_frames = 0
                    cooldown = COOLDOWN_FRAMES
                    current_letter = ""
                    
                    # Flash the screen green slightly to simulate a photo!
                    cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), (0, 255, 0), 10)
        else:
            # Auto-space logic
            NO_HAND_FRAMES += 1
            if NO_HAND_FRAMES == AUTO_SPACE_THRESHOLD:
                if len(sentence) > 0 and not sentence.endswith(" "):
                    sentence += " "
            if cooldown > 0:
                cooldown -= 1

        # --- UPDATE GUI ---
        text_display.config(state=tk.NORMAL)
        text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, sentence)
        text_display.config(state=tk.DISABLED)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    root.after(10, update_frame)

# ==========================================
# --- BUILD THE GUI ---
# ==========================================
root = tk.Tk()
root.title("ASL to Text Translator - Pro Vision")
root.geometry("1200x750")
root.configure(bg="#e0e0e0")

top_frame = tk.Frame(root, bg="#e0e0e0")
top_frame.pack(pady=10)

video_label = tk.Label(top_frame, bg="black")
video_label.pack(side=tk.LEFT, padx=10)

alphabet_label = tk.Label(top_frame, bg="white", text="Looking for alphabet.png...", font=("Helvetica", 14))
alphabet_label.pack(side=tk.RIGHT, padx=10)

image_path = "alphabet.jpeg" 
if os.path.exists(image_path):
    alpha_img = Image.open(image_path)
    alpha_img = alpha_img.resize((450, 450))
    alpha_tk = ImageTk.PhotoImage(alpha_img)
    alphabet_label.configure(image=alpha_tk, text="")
    alphabet_label.image = alpha_tk 

text_display = tk.Text(root, height=3, width=50, font=("Helvetica", 24, "bold"), bg="white", fg="black")
text_display.pack(pady=10)
text_display.insert(tk.END, "Waiting for translation...")
text_display.config(state=tk.DISABLED)

button_frame = tk.Frame(root, bg="#e0e0e0")
button_frame.pack(pady=10)

btn_clear = tk.Button(button_frame, text="Clear All", font=("Helvetica", 14, "bold"), bg="#f2e394", width=12, command=clear_text)
btn_clear.grid(row=0, column=0, padx=10)

btn_save = tk.Button(button_frame, text="Save to Text File", font=("Helvetica", 14, "bold"), bg="#85c48b", width=16, command=save_text)
btn_save.grid(row=0, column=1, padx=10)

btn_quit = tk.Button(button_frame, text="Quit", font=("Helvetica", 14, "bold"), bg="#f2635f", fg="white", width=12, command=quit_app)
btn_quit.grid(row=0, column=2, padx=10)

update_frame()
root.mainloop()