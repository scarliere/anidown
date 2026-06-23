import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import processor
from .paths import EPISODE_LIST_PATH, TORRENT_DIR

COLORS = {
	"background": "#f5f7fb",
	"surface": "#ffffff",
	"surface_alt": "#eef2f8",
	"primary": "#1565c0",
	"primary_hover": "#0d47a1",
	"text": "#17212b",
	"muted": "#5f6b7a",
	"border": "#d7dee8",
	"success": "#1b7f45",
	"warning": "#9a6700",
	"error": "#b3261e",
}


def load_episode_data():
	if not EPISODE_LIST_PATH.exists():
		return {}
	with EPISODE_LIST_PATH.open("r", encoding="utf-8") as read_file:
		return json.load(read_file)


def save_episode_data(epidump):
	EPISODE_LIST_PATH.parent.mkdir(parents=True, exist_ok=True)
	with EPISODE_LIST_PATH.open("w", encoding="utf-8") as outfile:
		json.dump(epidump, outfile, indent=4)


def configure_styles(root):
	style = ttk.Style(root)
	style.theme_use("clam")

	root.configure(bg=COLORS["background"])

	style.configure("App.TFrame", background=COLORS["background"])
	style.configure("Surface.TFrame", background=COLORS["surface"], relief="flat")
	style.configure("Header.TLabel", background=COLORS["background"], foreground=COLORS["text"], font=("Segoe UI", 22, "bold"))
	style.configure("Subhead.TLabel", background=COLORS["background"], foreground=COLORS["muted"], font=("Segoe UI", 10))
	style.configure("Section.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("Segoe UI", 12, "bold"))
	style.configure("Field.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=("Segoe UI", 9))
	style.configure("Status.TLabel", background=COLORS["background"], foreground=COLORS["muted"], font=("Segoe UI", 9))

	style.configure(
		"TEntry",
		fieldbackground=COLORS["surface"],
		background=COLORS["surface"],
		foreground=COLORS["text"],
		bordercolor=COLORS["border"],
		lightcolor=COLORS["border"],
		darkcolor=COLORS["border"],
		padding=(10, 8),
	)
	style.map("TEntry", bordercolor=[("focus", COLORS["primary"])])

	style.configure(
		"TSpinbox",
		fieldbackground=COLORS["surface"],
		background=COLORS["surface"],
		foreground=COLORS["text"],
		bordercolor=COLORS["border"],
		lightcolor=COLORS["border"],
		darkcolor=COLORS["border"],
		padding=(10, 8),
		arrowsize=14,
	)
	style.map("TSpinbox", bordercolor=[("focus", COLORS["primary"])])

	style.configure(
		"Primary.TButton",
		background=COLORS["primary"],
		foreground="#ffffff",
		borderwidth=0,
		focusthickness=0,
		font=("Segoe UI", 10, "bold"),
		padding=(16, 10),
	)
	style.map(
		"Primary.TButton",
		background=[("active", COLORS["primary_hover"]), ("disabled", COLORS["border"])],
		foreground=[("disabled", COLORS["muted"])],
	)

	style.configure(
		"Secondary.TButton",
		background=COLORS["surface_alt"],
		foreground=COLORS["primary"],
		borderwidth=0,
		focusthickness=0,
		font=("Segoe UI", 10, "bold"),
		padding=(14, 9),
	)
	style.map("Secondary.TButton", background=[("active", "#e1e8f2"), ("disabled", COLORS["border"])])


def make_surface(parent, row, title):
	frame = ttk.Frame(parent, style="Surface.TFrame", padding=18)
	frame.grid(row=row, column=0, sticky="nsew", pady=(0, 16))
	frame.columnconfigure(1, weight=1)
	ttk.Label(frame, text=title, style="Section.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 14))
	return frame


def run_gui():
	epidump = load_episode_data()

	root = tk.Tk()
	root.geometry("760x620")
	root.minsize(520, 360)
	root.title("Anidown")
	configure_styles(root)

	title_var = tk.StringVar()
	subber_var = tk.StringVar(value="[SubsPlease]")
	episode_var = tk.StringVar(value="1")
	destination_var = tk.StringVar(value=str(TORRENT_DIR))
	status_var = tk.StringVar(value="Ready")

	shell = tk.Frame(root, bg=COLORS["background"])
	shell.pack(fill="both", expand=True)
	shell.rowconfigure(0, weight=1)
	shell.columnconfigure(0, weight=1)

	canvas = tk.Canvas(shell, bg=COLORS["background"], highlightthickness=0)
	page_scrollbar = ttk.Scrollbar(shell, orient="vertical", command=canvas.yview)
	canvas.configure(yscrollcommand=page_scrollbar.set)
	canvas.grid(row=0, column=0, sticky="nsew")
	page_scrollbar.grid(row=0, column=1, sticky="ns")

	container = ttk.Frame(canvas, style="App.TFrame", padding=24)
	container_window = canvas.create_window((0, 0), window=container, anchor="nw")
	container.columnconfigure(0, weight=1)

	def sync_scroll_region(event=None):
		canvas.configure(scrollregion=canvas.bbox("all"))

	def sync_content_width(event):
		canvas.itemconfigure(container_window, width=event.width)

	def scroll_page(event):
		canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	container.bind("<Configure>", sync_scroll_region)
	canvas.bind("<Configure>", sync_content_width)
	root.bind_all("<MouseWheel>", scroll_page)

	ttk.Label(container, text="Anidown", style="Header.TLabel").grid(row=0, column=0, sticky="w")
	ttk.Label(container, text="Add an anime and download the next matching Nyaa torrent.", style="Subhead.TLabel").grid(
		row=1,
		column=0,
		sticky="w",
		pady=(2, 18),
	)

	form = make_surface(container, 2, "New anime")
	form.rowconfigure(7, weight=1)

	ttk.Label(form, text="Anime", style="Field.TLabel").grid(row=1, column=0, sticky="w", pady=(0, 6))
	title_entry = ttk.Entry(form, textvariable=title_var)
	title_entry.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(0, 14))

	ttk.Label(form, text="Subber", style="Field.TLabel").grid(row=3, column=0, sticky="w", pady=(0, 6))
	ttk.Label(form, text="Next episode", style="Field.TLabel").grid(row=3, column=2, sticky="w", pady=(0, 6), padx=(16, 0))
	subber_entry = ttk.Entry(form, textvariable=subber_var)
	subber_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 14))
	episode_spinbox = ttk.Spinbox(form, from_=1, to=9999, textvariable=episode_var, width=10)
	episode_spinbox.grid(row=4, column=2, sticky="ew", pady=(0, 14), padx=(16, 0))

	ttk.Label(form, text="Download folder", style="Field.TLabel").grid(row=5, column=0, sticky="w", pady=(0, 6))
	destination_entry = ttk.Entry(form, textvariable=destination_var)
	destination_entry.grid(row=6, column=0, columnspan=2, sticky="ew")

	def choose_destination():
		selected = filedialog.askdirectory(initialdir=destination_var.get() or str(TORRENT_DIR))
		if selected:
			destination_var.set(selected)

	browse_button = ttk.Button(form, text="Browse", style="Secondary.TButton", command=choose_destination)
	browse_button.grid(row=6, column=2, sticky="ew", padx=(16, 0))

	actions = ttk.Frame(form, style="Surface.TFrame")
	actions.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(18, 0))
	actions.columnconfigure(0, weight=1)

	download_button = ttk.Button(actions, text="Add and Download", style="Primary.TButton")
	download_button.grid(row=0, column=1, sticky="e")

	list_surface = make_surface(container, 3, "Saved anime")
	list_surface.rowconfigure(1, weight=1)
	list_surface.columnconfigure(0, weight=1)

	list_frame = tk.Frame(list_surface, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
	list_frame.grid(row=1, column=0, sticky="nsew")
	list_frame.rowconfigure(0, weight=1)
	list_frame.columnconfigure(0, weight=1)

	anime_list = tk.Listbox(
		list_frame,
		height=8,
		activestyle="none",
		bg=COLORS["surface"],
		fg=COLORS["text"],
		selectbackground="#d6e7ff",
		selectforeground=COLORS["text"],
		borderwidth=0,
		highlightthickness=0,
		font=("Segoe UI", 10),
	)
	anime_list.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
	scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=anime_list.yview)
	scrollbar.grid(row=0, column=1, sticky="ns")
	anime_list.configure(yscrollcommand=scrollbar.set)

	status_label = ttk.Label(container, textvariable=status_var, style="Status.TLabel")
	status_label.grid(row=4, column=0, sticky="w", pady=(0, 2))

	def refresh_list():
		anime_list.delete(0, tk.END)
		for anime_name, anime_data in sorted(epidump.items()):
			anime_list.insert(tk.END, "{}    {}    latest {}".format(anime_name, anime_data[0], anime_data[1]))

	refresh_list()

	def set_status(message, color_key="muted"):
		status_var.set(message)
		status_label.configure(foreground=COLORS[color_key])

	def set_form_state(state):
		for widget in (title_entry, subber_entry, episode_spinbox, destination_entry, browse_button, download_button):
			widget.configure(state=state)

	def add_and_download():
		name = title_var.get().strip()
		subber = subber_var.get().strip() or "[SubsPlease]"
		destination = destination_var.get().strip()

		try:
			next_episode = int(episode_var.get())
		except ValueError:
			messagebox.showerror("Invalid episode", "Episode must be a number.")
			return

		if not name:
			messagebox.showerror("Missing anime", "Enter an anime title.")
			return
		if not destination:
			messagebox.showerror("Missing folder", "Choose a download folder.")
			return

		set_form_state("disabled")
		set_status("Searching Nyaa RSS...", "primary")

		def worker():
			try:
				resolution, download_path = processor.processpage_with_resolution_fallback(
					subber,
					next_episode,
					name,
					destination_dir=destination,
				)
				if download_path:
					epidump[name] = [subber, next_episode]
					save_episode_data(epidump)
					root.after(0, refresh_list)
					root.after(0, lambda: set_status("Downloaded {}p: {}".format(resolution, download_path), "success"))
					root.after(0, lambda: messagebox.showinfo("Downloaded", "Saved torrent to:\n{}".format(download_path)))
				else:
					root.after(0, lambda: set_status("No matching torrent found.", "warning"))
					root.after(0, lambda: messagebox.showwarning("Not found", "No matching torrent was found."))
			except Exception as error:
				error_message = str(error)
				root.after(0, lambda message=error_message: set_status("Error: {}".format(message), "error"))
				root.after(0, lambda message=error_message: messagebox.showerror("Download failed", message))
			finally:
				root.after(0, lambda: set_form_state("normal"))

		threading.Thread(target=worker, daemon=True).start()

	download_button.configure(command=add_and_download)
	title_entry.focus()
	root.mainloop()
