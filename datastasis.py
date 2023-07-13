import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from resources.metadata import MetadataManager
from resources.extractor import AudioFileExtractor

__version__ = 1.0
__author__ = 'RafaelHorta'
__github__ = 'https://github.com/RafaelHorta?tab=repositories'
__doc__ = 'Datastasis'

class Application(tk.Tk):

    DIR_APP = os.path.dirname(__file__)
    DIR_HOME = os.path.expanduser('~')
    TMP_FILE = "tmp_cover.png"


    def __init__(self):
        super().__init__()

        # Initial Settings
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        self.title("Datastasis")
        self.geometry(f"{width}x{height}")
        self.minsize(1260, 685)

        # Styles settings
        self.tk.call('source', 'awthemes/awdark.tcl')
        styles = ttk.Style()
        styles.theme_use('awdark')
        styles.configure('TEntry', padding=5)
        styles.configure('meta.TButton', background='#33393b')
        styles.configure('dark.TLabel', foreground='#B5B5B5')

        # Variables
        self._tmp_path = ""
        self._cover_filepath = ""
        self._filename = ""

        # Control variables
        self._current_rute = tk.StringVar()
        self._new_filename = tk.StringVar()
        self._title = tk.StringVar()
        self._artist = tk.StringVar()
        self._album_artist = tk.StringVar()
        self._album = tk.StringVar()
        self._track = tk.StringVar()
        self._genre = tk.StringVar()
        self._date = tk.StringVar()
        self._compositor = tk.StringVar()
        self._encodedby = tk.StringVar()

        # - - - - - - - - - - - MAIN FRAME - - - - - - - - - - - - - -
        frame_main = ttk.Frame(self)
        frame_main.pack(fill='both', expand=True)

        for index in range(6):
            frame_main.columnconfigure(index=index, weight=1)
            frame_main.rowconfigure(index=index, weight=1)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - - DATA FRAME - - - - - - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        frame_data = ttk.Frame(frame_main)
        frame_data.grid(row=0, column=0, rowspan=6, columnspan=2, padx=10, pady=10, sticky="nsew")
        frame_data.grid_columnconfigure(index=0, weight=1)
        frame_data.grid_rowconfigure(index=0, weight=1)
        frame_data.grid_rowconfigure(index=1, weight=1)
        frame_data.grid_rowconfigure(index=2, weight=1)

        # - - - - - - - - - - - HEAD FRAME - - - - - - - - - - - - - -
        frame_head = ttk.LabelFrame(frame_data, text="Directory")
        frame_head.grid(row=0, column=0, sticky="nsew")
        frame_head.columnconfigure(index=0, weight=1)
        frame_head.columnconfigure(index=1, weight=3)
        frame_head.rowconfigure(index=0, weight=1)

        ttk.Label(frame_head, text="", style="dark.TLabel", textvariable=self._current_rute).grid(row=0, column=0, padx=10, sticky="we")
        ttk.Button(frame_head, text="Change directory", cursor='hand2', command=self._change_directory).grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # - - - - - - - - - - - EXPORT FRAME - - - - - - - - - - - - - -
        frame_export = ttk.LabelFrame(frame_data, text="Export songs list")
        frame_export.grid(row=1, column=0, sticky="nsew")
        frame_export.columnconfigure(index=0, weight=1)
        frame_export.rowconfigure(index=0, weight=1)

        ttk.Button(frame_export, text="Export", cursor="hand2", command=self._export_list).grid(row=0, column=0, padx=10, pady=5, sticky="e")

        # - - - - - - - - - - - TABLE FRAME - - - - - - - - - - - - - -
        frame_table = ttk.Labelframe(frame_data, text="Songs list")
        frame_table.grid(row=2, column=0, sticky="nsew")

        # Treeview
        scrollbar = ttk.Scrollbar(frame_table)
        scrollbar.pack(side="right", fill="y")

        columns = ('filename',)
        self._table = ttk.Treeview(frame_table, selectmode="browse", columns=columns, yscrollcommand=scrollbar.set, height=25)
        self._table.pack(fill="both", expand=True)
        scrollbar.config(command=self._table.yview)

        # Treeview - Headings
        self._table.heading("#0", text="ID")
        self._table.heading("filename", text="File Name")

        # Treeview - Columns
        self._table.column("#0", width=40, minwidth=40, anchor="center")
        self._table.column("filename", width=350, minwidth=300)

        self._table.bind('<Double-1>', self._fill_form)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - - FORM FRAME - - - - - - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        frame_form = ttk.Frame(frame_main)
        frame_form.grid(row=0, column=2, rowspan=6, columnspan=4, padx=10, pady=10, sticky="nsew")
        frame_form.grid_columnconfigure(index=0, weight=1)
        frame_form.grid_columnconfigure(index=1, weight=1)
        frame_form.grid_rowconfigure(index=0, weight=1)

        # - - - - - - - - - - - META FRAME - - - - - - - - - - - - - -
        frame_meta = ttk.Labelframe(frame_form, text="Metadata")
        frame_meta.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame_meta, style="dark.TLabel", text="File name").grid(row=0, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Title").grid(row=1, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Artist").grid(row=2, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Album artist").grid(row=3, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Album").grid(row=4, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Track number").grid(row=5, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Genre").grid(row=6, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Year").grid(row=7, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Composer").grid(row=8, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Encoded by").grid(row=9, column=0, padx=10, sticky="we")
        ttk.Label(frame_meta, style="dark.TLabel", text="Lyrics").grid(row=10, column=0, padx=10, sticky="we")

        ttk.Entry(frame_meta, textvariable=self._new_filename).grid(row=0, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._title).grid(row=1, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._artist).grid(row=2, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._album_artist).grid(row=3, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._album).grid(row=4, column=1, padx=10, pady=5, sticky="we")
        ttk.Spinbox(frame_meta, from_=0, to=100, increment=1, textvariable=self._track).grid(row=5, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._genre).grid(row=6, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._date).grid(row=7, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._compositor).grid(row=8, column=1, padx=10, pady=5, sticky="we")
        ttk.Entry(frame_meta, textvariable=self._encodedby).grid(row=9, column=1, padx=10, pady=5, sticky="we")

        # - Lyrics Entry
        self._lyrics = tk.Text(frame_meta, height=10, width=60)
        scrollbar_lyrics = ttk.Scrollbar(frame_meta, command=self._lyrics.yview)

        self._lyrics.grid(row=10, column=1, padx=10, pady=5, sticky="we")
        scrollbar_lyrics.grid(row=10, column=1, padx=10, pady=5, sticky="nse")
        self._lyrics.configure(yscrollcommand=scrollbar_lyrics.set)

        # - - - - - - - - - - - ACTIONS FRAME - - - - - - - - - - - - - -
        frame_actions = ttk.Frame(frame_form)
        frame_actions.grid(row=0, column=1, pady=10, sticky="nse")

        ttk.Button(frame_actions, text="Clean fields", cursor="hand2", command=self._clean_form).grid(row=0, column=0, padx=5, pady=5, sticky="we")
        self._btn_save = ttk.Button(frame_actions, text="Save metadata", cursor="hand2", style="meta.TButton", command=self._extract_save_metadata, state="disabled")
        self._btn_change = ttk.Button(frame_actions, text="Change image cover", cursor="hand2", style="meta.TButton", command=self._change_cover_image, state="disabled")
        self._btn_save.grid(row=1, column=0, padx=5, pady=5, sticky="we")
        self._btn_change.grid(row=2, column=0, padx=5, pady=5, sticky="we")

        # - - - - - - - - - - - COVER FRAME - - - - - - - - - - - - - -
        frame_cover = ttk.Frame(frame_actions)
        frame_cover.grid(row=4, column=0, sticky="nsew")

        self._cover = ttk.Label(frame_cover)
        self._cover.grid(row=0, column=0, pady=10)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - - RUN INTIALIZE - - - - - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        self._objExtractor = AudioFileExtractor()
        self._objMetadata = MetadataManager()

        self._current_rute.set(self._objExtractor.get_rute)
        self._insert_into_table()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - - - FUNCITONS - - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # Insert songs list into table
    def _insert_into_table(self):
        self._table.delete(*self._table.get_children())

        audiofiles = self._objExtractor.list_audio_files()

        if audiofiles:
            for i, data in enumerate(sorted(audiofiles)):
                i += 1

                self._table.insert('', 'end', text=i, values=(data,))
        else:
            messagebox.showinfo("(˘︹˘)", "Not audio files found")

    # Fill form with metadata
    def _fill_form(self, event):
        global image

        try:
            current_item = self._table.focus() # Get selected item from Treeview

            if not current_item:
                raise ValueError("Item has not been selected")

            self._clean_form()
            self._filename = self._table.item(current_item, 'values')[0]

            filepath = os.path.join(self._objExtractor.get_rute, self._filename)
            metadata = self._objMetadata.get_metadata(filepath, False)

            if 'APIC:' in metadata:
                apic_metadata = metadata.tags.getall('APIC')[0].data
                self._tmp_path = os.path.join(self.DIR_APP, 'tmp', self.TMP_FILE)

                with open(self._tmp_path, 'wb') as tmp:
                    tmp.write(apic_metadata)

                image = self._proccess_cover_image(self._tmp_path)
                self._cover.config(image=image)

            else:
                self._cover.config(text="Not image", image="")

            lyrics = metadata.tags.getall('USLT')

            self._new_filename.set(os.path.splitext(self._filename)[0])
            self._title.set(metadata['TIT2'][0] if 'TIT2' in metadata else "")
            self._artist.set(metadata['TPE1'][0] if 'TPE1' in metadata else "")
            self._album_artist.set(metadata['TPE2'][0] if 'TPE2' in metadata else "")
            self._album.set(metadata['TALB'][0] if 'TALB' in metadata else "")
            self._track.set(metadata['TRCK'][0] if 'TRCK' in metadata else "")
            self._date.set(metadata['TDRC'][0] if 'TDRC' in metadata else "")
            self._genre.set(metadata['TCON'][0] if 'TCON' in metadata else "")
            self._compositor.set(metadata['TCOM'][0] if 'TCOM' in metadata else "")
            self._encodedby.set(metadata['TENC'][0] if 'TENC' in metadata else "")
            self._lyrics.insert("end", lyrics[0].text if lyrics else "")

            self._btn_change.config(state="normal")
            self._btn_save.config(state="normal")

        except Exception as ex:
            messagebox.showerror('(ಠ ͜ʖಠ)', ex)

    # Extract metadata from form and save it
    def _extract_save_metadata(self):
        try:
            self._objMetadata.save_metadata(self._objExtractor.get_rute, {
                'filename': self._filename,
                'new_filename': self._new_filename.get(),
                'title': self._title.get(),
                'artist': self._artist.get(),
                'album_artist': self._album_artist.get(),
                'album': self._album.get(),
                'track': self._track.get(),
                'date': self._date.get(),
                'genre': self._genre.get(),
                'compositor': self._compositor.get(),
                'encodedby': self._encodedby.get(),
                'lyrics': self._lyrics.get("0.1", "end"),
                'cover': self._cover_filepath
            })

            self._clean_form()
            self._insert_into_table()

        except Exception as ex:
            messagebox.showerror("( ͡° ͜ʖ ͡°)", ex)

    # Clean metadata form
    def _clean_form(self):
        if os.path.exists(self._tmp_path):
            os.remove(self._tmp_path)

        self._tmp_path = ""
        self._cover_filepath = ""

        self._new_filename.set("")
        self._title.set("")
        self._artist.set("")
        self._album_artist.set("")
        self._album.set("")
        self._track.set("")
        self._date.set("")
        self._genre.set("")
        self._compositor.set("")
        self._encodedby.set("")
        self._lyrics.delete("1.0", "end")

        self._cover.config(text="Not image", image="")
        self._btn_change.config(state="disabled")
        self._btn_save.config(state="disabled")

    # Select directory
    def _change_directory(self):
        rute = self._get_directory_path(self._current_rute.get())

        self._current_rute.set(rute)
        self._objExtractor.set_rute(rute)
        self._insert_into_table()

    # Select a new image file to cover
    def _change_cover_image(self):
        global image

        self._cover_filepath = filedialog.askopenfilename(
            initialdir=os.path.expanduser('~'),
            filetypes=(
                ("Image files", "*.jpg;*.jpeg;*.png"), ("JPEG files", "*.jpeg"),
                ("JPG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")
            )
        )

        if self._cover_filepath:
            image = self._proccess_cover_image(self._cover_filepath)
            self._cover.config(image=image)

    # Open temporal file (cover image)
    def _proccess_cover_image(self, filepath):
        cover_image = ""

        if os.path.exists(filepath):
            with Image.open(filepath) as img:
                width = 200
                height = int(width * img.height / img.width) # Calculate height size based on set width size

                cover_resize = img.resize((width, height), Image.LANCZOS)
                cover_image = ImageTk.PhotoImage(cover_resize)

        return cover_image

    # Export songs metadata
    def _export_list(self):
        try:
            filename = filedialog.asksaveasfilename(
                initialdir=self.DIR_HOME,
                filetypes=(
                    ("Excel Files", "*.xlsx"),
                )
            )

            if not filename:
                raise ValueError("Must select a directory")

            # Import
            from resources.export import ExportList

            heading = [
                'Filename', 'Title', 'Artist', 'Album', 'Album Artist',
                'Genre', 'Composer', 'Track', 'Organization', 'Date', 'Encoded By'
            ]
            content = self._objExtractor.list_metadata_audio_files()

            export = ExportList(filename)
            export.add_worksheet(heading, content, "Songs List")

            messagebox.showinfo("( ͡° ͜ʖ ͡°)", "The song list has been exported")

        except Exception as ex:
            messagebox.showerror("", ex)

    # Get directory path
    def _get_directory_path(self, initial = None):
        dirpath = filedialog.askdirectory(initialdir=self.DIR_HOME if initial is None else initial)

        return dirpath if dirpath else self._current_rute.get()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
