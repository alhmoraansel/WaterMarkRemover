import fitz  # PyMuPDF
import customtkinter as ctk
from tkinter import filedialog, messagebox

def remove_watermarks_and_links(input_path, output_path, watermark_text="watermark"):
    try:
        document = fitz.open(input_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open the PDF file: {e}")
        return

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        # Remove text watermarks
        text_instances = page.search_for(watermark_text,flags=fitz.TEXT_PRESERVE_WHITESPACE) #added flags
        for inst in text_instances:
            try:
                page.add_redact_annot(inst, text=" ", fill=(1, 1, 1))  # Add a redaction annotation
                page.apply_redactions()
            except Exception as e:
                print(f"Error redacting watermark: {e}")

        # Remove links - Improved Approach
        while True:
            links = page.get_links()
            if not links:
                break  # Exit loop if no more links

            link_to_delete = links[0]  # Get the first link
            try:
                page.delete_link(link_to_delete)
            except IndexError:
                print(f"IndexError encountered while deleting link: {link_to_delete}")
                break # Exit the loop if there is an index error

    try:
        document.save(output_path)
        messagebox.showinfo("Success", f"PDF saved successfully as {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the PDF file: {e}")
    finally:
        document.close()

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        input_entry.delete(0, ctk.END)
        input_entry.insert(0, file_path)

def save_file():
    input_path = input_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    watermark_text = watermark_entry.get()  # Get watermark text from entry
    if output_path:
        if input_path:
            remove_watermarks_and_links(input_path, output_path, watermark_text)  # Pass watermark text
        else:
            messagebox.showwarning("Warning", "Please select an input file.")

app = ctk.CTk()
app.title("PDF Watermark and Link Remover")
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 400
window_height = 350  # Increased height to accommodate the new entry field
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.minsize(height=350, width=400)  # increased minimum height
input_label = ctk.CTkLabel(app, text="Select Input PDF:")
input_label.pack(pady=5)
input_entry = ctk.CTkEntry(app, width=300)
input_entry.pack(pady=5)
open_button = ctk.CTkButton(app, text="Open File", command=open_file)
open_button.pack(pady=5)
output_label = ctk.CTkLabel(app, text="Output Filename:")
output_label.pack(pady=5)
output_entry = ctk.CTkEntry(app, width=300)
output_entry.insert(0, "output.pdf")
output_entry.pack(pady=5)
watermark_label = ctk.CTkLabel(app, text="Watermark Text:")
watermark_label.pack(pady=5)
watermark_entry = ctk.CTkEntry(app, width=300)
watermark_entry.insert(0, "watermark")  # Default watermark text
watermark_entry.pack(pady=5)
save_button = ctk.CTkButton(app, text="Save File", command=save_file)
save_button.pack(pady=5)
app.mainloop()
